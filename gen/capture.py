"""The email sign-up block, and the promise printed next to it.

Every page the daily loop publishes carries one of these. The point is a list of
people who might buy something, built while the catalogue is still being put
together, so that the day it opens there is somebody to tell.

Two design decisions worth defending.

It is one field. Asking what somebody does, or which practice they are at, costs
conversions and buys data we would not use. The address is the whole ask.

The promise beside it is a promise. The site already says, on the Gauge Finder,
that answers stay in the browser and never feed advertising, and that is a
commitment rather than copy. This is the same: what arrives, roughly how often,
one click to stop, and the address is not sold or handed on. Nothing here says
the emails will contain health advice, because they will not.

Self contained on purpose. Guides are static pages rather than streaming
components, so this is plain HTML with one small script rather than another hole
for renderVals to fill. Two blocks on one page share the one script.
"""

import html

E = html.escape

MONO = "font-family:'IBM Plex Mono',monospace;font-weight:500"
WRAP = 'max-width:1440px;margin:0 auto;padding:clamp(48px,7vw,96px) clamp(20px,5vw,72px)'

# What the block says it will send. Kept here rather than per page so there is
# one sentence to change if the answer ever changes.
PROMISE = ('Restock notices and new guides. Two or three emails a month at most, '
           'one click to stop, and we do not sell or share the address.')

FIELD = ('width:100%;padding:13px 15px;border:1px solid #C4C4C2;border-radius:12px;'
         "font-family:'Archivo',sans-serif;font-size:16px;background:#FFF;color:#0E0E0E")

BUTTON = ('padding:13px 26px;border:0;border-radius:12px;background:#1C4034;color:#FAFAFA;'
          "font-family:'Archivo',sans-serif;font-weight:600;font-size:16px;cursor:pointer;"
          'white-space:nowrap')

SCRIPT = """
    <script>
    (function () {
      if (window.__gpSubscribe) return;
      window.__gpSubscribe = true;
      function wire(form) {
        var status = form.querySelector('[data-gp-status]');
        var button = form.querySelector('button');
        function say(msg, ok) {
          status.textContent = msg;
          status.style.color = ok ? '#1C4034' : '#8A2B22';
        }
        form.addEventListener('submit', function (ev) {
          ev.preventDefault();
          var email = form.querySelector('[name=email]').value.trim();
          if (!/^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$/.test(email)) {
            say('That does not look like an email address.', false);
            return;
          }
          button.disabled = true;
          say('Just a moment.', true);
          fetch('/api/subscribe', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              email: email,
              source: form.getAttribute('data-gp-source') || location.pathname,
              interest: form.getAttribute('data-gp-interest') || 'general',
              website: form.querySelector('[name=website]').value
            })
          }).then(function (r) {
            return r.json().catch(function () { return { ok: r.ok }; });
          }).then(function (d) {
            if (d && d.ok) {
              form.querySelector('[name=email]').value = '';
              say('You are on the list. Thanks.', true);
            } else {
              say((d && d.message) || 'Something went wrong. Try again in a minute.', false);
            }
            button.disabled = false;
          }).catch(function () {
            say('We could not reach the server. Check your connection and try again.', false);
            button.disabled = false;
          });
        });
      }
      function boot() {
        var forms = document.querySelectorAll('[data-gp-subscribe]');
        for (var i = 0; i < forms.length; i++) wire(forms[i]);
      }
      if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', boot);
      } else {
        boot();
      }
    })();
    </script>
"""


def block(source, interest='general', heading='Know when it lands',
          lead='We are still building the range. Leave an address and we will tell you '
               'what has come in, without making a project of it.',
          bg='background:#EDEDEB;'):
    """One sign-up section.

    `source` records which page the address came from and `interest` what that
    page was about. Both are written to the contact, so a list built over months
    can still be told apart later.
    """
    o = []
    a = o.append
    a('    <section style="%sborder-bottom:1px solid #E3E3E1">\n      <div style="%s">\n'
      % (bg, WRAP))
    a('        <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(320px,100%),1fr));'
      'gap:clamp(24px,4vw,56px);align-items:start">\n')
    a('          <div>\n')
    a('            <div style="%s;font-size:11px;letter-spacing:.16em;text-transform:uppercase;'
      'color:#1C4034;margin-bottom:12px">Stay in the loop</div>\n' % MONO)
    a("            <h2 style=\"font-family:'Archivo',sans-serif;font-weight:600;"
      'font-size:clamp(22px,2.4vw,30px);letter-spacing:-.025em;line-height:1.1;'
      'margin:0 0 12px">%s</h2>\n' % E(heading))
    a('            <p style="margin:0;font-size:16px;line-height:1.55;color:#3A3A38;'
      'max-width:46ch">%s</p>\n' % E(lead))
    a('          </div>\n')
    a('          <div>\n')
    a('            <form data-gp-subscribe data-gp-source="%s" data-gp-interest="%s" novalidate '
      'style="display:flex;flex-wrap:wrap;gap:10px">\n' % (E(source), E(interest)))
    a('              <label for="gp-sub-email" style="position:absolute;width:1px;height:1px;'
      'overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap">Email address</label>\n')
    a('              <input id="gp-sub-email" name="email" type="email" inputmode="email" '
      'autocomplete="email" placeholder="you@example.com.au" '
      'style="%s;flex:1 1 240px">\n' % FIELD)
    a('              <input name="website" type="text" tabindex="-1" autocomplete="off" '
      'aria-hidden="true" style="position:absolute;left:-9999px;width:1px;height:1px">\n')
    a('              <button type="submit" style="%s">Keep me posted</button>\n' % BUTTON)
    a('              <p data-gp-status role="status" aria-live="polite" '
      'style="flex:1 1 100%;margin:2px 0 0;font-size:14.5px;line-height:1.5;'
      'min-height:1.4em;color:#1C4034"></p>\n')
    a('            </form>\n')
    a('            <p style="margin:14px 0 0;font-size:13.5px;line-height:1.55;color:#59595A;'
      'max-width:44ch">%s</p>\n' % E(PROMISE))
    a('          </div>\n')
    a('        </div>\n      </div>\n    </section>\n')
    a(SCRIPT)
    a('\n')
    return ''.join(o)
