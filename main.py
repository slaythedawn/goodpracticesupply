"""Generate one video with Higgsfield Seedance 2.5 and print its URL.

Run it with the project virtualenv so the SDK is on the path:

    ./.venv/bin/python main.py

Credentials come from HF_KEY in .env.local, in key-id:key-secret format. That
file is gitignored and is never read, printed or logged by this script beyond
checking that it is set. The SDK reads it out of the environment itself.

A successful run costs money. Seedance 2.5 bills per generation, so treat every
invocation as a real charge rather than a test.
"""

import json
import os
import sys

import httpx
from dotenv import load_dotenv

# Load before importing the SDK. The client reads the key lazily, on the first
# request rather than at import, so the order is not strictly required, but
# loading first means a missing key fails here with a readable message instead
# of somewhere inside the transport.
load_dotenv('.env.local')

import higgsfield_client as hf
from higgsfield_client.types_ import Cancelled, Completed, Failed, NSFW

APPLICATION = 'bytedance/seedance-2.5/text-to-video'

ARGUMENTS = {
    'prompt': 'A cinematic scene at sunset',
    'duration': 5,
    'resolution': '720p',
    'aspect_ratio': '16:9',
}

# What each terminal state means, for a message that says something useful
# rather than just naming the class.
TERMINAL = {
    Failed: 'the generation failed',
    Cancelled: 'the request was cancelled',
    NSFW: 'the request was flagged by content moderation',
}


def find_video_url(payload):
    """Pull the output URL out of the response.

    The response schema is not something this script can assume, so it looks in
    the obvious places first and then walks the whole structure. Returning None
    is a real answer: a completed request with no retrievable URL is a failure
    to report, not a success to paper over.
    """
    if not isinstance(payload, dict):
        return None

    for key in ('video_url', 'url', 'output_url'):
        value = payload.get(key)
        if isinstance(value, str) and value.startswith('http'):
            return value

    found = []

    def walk(node):
        if isinstance(node, dict):
            for k, v in node.items():
                if (isinstance(v, str) and v.startswith('http')
                        and ('video' in k.lower() or 'url' in k.lower())):
                    found.append(v)
                else:
                    walk(v)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(payload)
    return found[0] if found else None


def main():
    if not (os.getenv('HF_KEY') or (os.getenv('HF_API_KEY') and os.getenv('HF_API_SECRET'))):
        print('HF_KEY is not set. Put it in .env.local as HF_KEY=key-id:key-secret.',
              file=sys.stderr)
        return 2

    # subscribe() returns the response body for whatever terminal state the
    # request reached. It does not raise on failure, moderation or
    # cancellation, so the status has to be captured as it polls and checked
    # afterwards. Without this, a moderated request looks exactly like a
    # successful one to the caller.
    last_status = []

    print('submitting %s' % APPLICATION)
    print('  %s' % json.dumps(ARGUMENTS))

    try:
        result = hf.subscribe(
            APPLICATION,
            ARGUMENTS,
            on_enqueue=lambda request_id: print('queued as %s' % request_id),
            on_queue_update=lambda status: (
                last_status.append(status),
                print('  status: %s' % type(status).__name__),
            ),
        )
    except hf.CredentialsMissedError:
        print('The SDK could not find credentials. Check HF_KEY in .env.local.',
              file=sys.stderr)
        return 2
    except hf.HiggsfieldClientError as exc:
        print('The API rejected the request: %s' % exc, file=sys.stderr)
        return 1
    except httpx.HTTPError as exc:
        # Never reached the API at all: proxy refusal, DNS, TLS, timeout. Worth
        # separating from an API error, because the fix is somewhere else
        # entirely and nothing was submitted or billed.
        print('Could not reach %s: %s: %s'
              % (hf.sync_client.base_url, type(exc).__name__, exc), file=sys.stderr)
        return 3

    final = type(last_status[-1]) if last_status else None

    if final in TERMINAL:
        print('No video was produced: %s.' % TERMINAL[final], file=sys.stderr)
        print(json.dumps(result, indent=2)[:2000], file=sys.stderr)
        return 1

    if final is not Completed:
        print('Finished in an unrecognised state (%s), so this is not a success.'
              % (final.__name__ if final else 'no status observed'), file=sys.stderr)
        return 1

    url = find_video_url(result)

    if not url:
        print('The request completed but no video URL was found in the response.',
              file=sys.stderr)
        print(json.dumps(result, indent=2)[:2000], file=sys.stderr)
        return 1

    print('\nvideo: %s' % url)
    return 0


if __name__ == '__main__':
    sys.exit(main())
