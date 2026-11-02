# Setup checklist

Eight things only you can do. Ordered by time to value rather than by
importance, so the five minute jobs that unblock something today come before
the one that takes weeks.

Never paste a key into the Claude chat. Every step below is done in a provider
dashboard or a local file.

| # | Step | Time | What it unblocks |
| --- | --- | --- | --- |
| 1 | Resend key on Vercel | 5 min | 89 pages start capturing sign-ups |
| 2 | `ANTHROPIC_API_KEY` repo secret | 5 min | the loop writes pages instead of issues |
| 3 | Rotate Higgsfield and TypeSafe | 10 min | closes two leaked keys |
| 4 | Network access | 2 min | lets me verify prices and settle the ARTG question |
| 5 | Six legal documents to Drive | 5 min | the six legal pages |
| 6 | Four DNS records | 10 min, then propagation | mail can send from your own domain |
| 7 | Request indexing | 10 min | the eight category pages get crawled |
| 8 | Supplier data sheet | days | 31 real prices, every ARTG row, the backlinks |

---

## 1. Resend key on Vercel

This is the highest value for the least work. Right now the endpoint returns
503 and the form prints "Sign-ups are not connected just yet". Every day it
stays that way is sign-ups lost from pages that are live and indexed.

1. Go to the Resend dashboard, API Keys, and create a key. Name it
   **Good Practice Supply site** so it can be revoked on its own later. Five
   keys already exist and none of them is for this site, including two old
   "Vercel Integration" keys, so make a new one rather than reusing those.
2. Give it **full access, not sending only**. The endpoint creates a contact,
   which is a write to the audience, not just an email send.
3. Copy the key once. Resend shows it a single time.
4. Vercel dashboard, the `goodpracticesupply` project, Settings, Environment
   Variables. Add:
   - Name `RESEND_API_KEY`
   - Value: the key
   - Environments: tick **Production**, and Preview if you want the preview
     deployments to capture too
5. **Redeploy.** A Vercel environment variable only reaches new deployments, so
   nothing changes until you redeploy. Deployments, the most recent one, the
   menu on the right, Redeploy.

### Add `ENQUIRIES_TO` in the same visit, or enquiries vanish

This one matters and it is easy to miss. `api/_lib.js` sends every contact
enquiry and clinic application to `ENQUIRIES_TO`, and that variable defaults to
`hello@gpsupply.com.au`. There is no mailbox on that address yet. So setting
`RESEND_API_KEY` alone turns the forms on and posts every enquiry to an address
that cannot receive, where it bounces and is lost. The form would tell the
customer their message was received, and it would not be.

So add a second variable in the same visit:

    ENQUIRIES_TO = an inbox you actually read

Your own address is fine for now. Swap it for `hello@gpsupply.com.au` once the
forwarding in step 6 exists. Leave `ENQUIRIES_FROM` alone: it defaults to
`hello@gpsupply.com.au`, which needs the domain verified, and until then Resend
will reject the send rather than deliver it from an unverified sender.

You do not need `RESEND_SEGMENT_ID`. The code now defaults to the segment
"Good Practice Supply, website sign-ups", which I created because the account
is shared with Online Model Academy and the old default filed everything into
the shared "General" list.

Note that the sign-up box and the enquiry forms fail differently. A sign-up
writes a contact, which needs no verified domain and works the moment the key
is set. An enquiry sends an email, which needs both a verified sending domain
and a destination that receives. That is why step 6 is not optional if you want
the contact form to function.

**To check it worked:** submit the sign-up box on any page of the live site with
your own address, then tell me. I can read the Resend contacts and confirm it
landed in the right segment with the right source and interest tags.

Worth knowing: creating a contact does not need the domain verified, so this
works immediately. Step 6 is only needed to *send* to those addresses.

### Two plan limits you are sitting on

The account is on a tier that allows three domains and three segments, and it is
at both caps.

**Domains 3 of 3:** gpsupply.com.au, forwardmatter.com.au and sevenam.com.au.
gpsupply.com.au already holds its slot, so step 6 is verifying it rather than
adding it. A fourth domain would need one removed or the plan upgraded.

**Segments 3 of 3:** the Online Model Academy promo list, "General", and the
Good Practice Supply one. I used the last slot creating that third segment, so
you should know that was the cost of separating this site's sign-ups from the
shared list. It was the right trade, because the sign-up box promises the
address is not shared, but it does mean another segment needs a deletion or an
upgrade.

Sending volume is not a constraint. Nothing has been sent at all: 0 of 100 today
and 0 of 3000 this month, against 162 contacts.

---

## 2. `ANTHROPIC_API_KEY` as a repository secret

This is why the loop produces briefs as GitHub issues instead of published
pages. The "Write the page" step is skipped every run because the key is
absent.

1. console.anthropic.com, API keys, create a key.
2. GitHub, the `slaythedawn/goodpracticesupply` repository, Settings, Secrets
   and variables, Actions, New repository secret.
3. Name `ANTHROPIC_API_KEY`, paste the value, add.

**To check it worked:** the next run of `daily-seo.yml` shows "Write the page:
success" instead of "skipped", and commits a page rather than opening an issue.

---

## 3. Rotate Higgsfield and TypeSafe

Both keys were pasted into a chat window earlier, so treat them as leaked.
Rotating means revoking the old one, not just issuing a new one. Replacing the
value without revoking leaves the leaked key working.

**Higgsfield.** In the Higgsfield dashboard, revoke the existing key, then
create a new one. Put it in `.env.local` in the repository root on your own
machine, on one line:

    HF_KEY=key-id:key-secret

`.env.local` is gitignored. Nothing in CI reads this, only `main.py`.
`HF_API_KEY` plus `HF_API_SECRET` works as an alternative pair if the dashboard
gives you the halves separately.

**TypeSafe.** Revoke the existing key in the TypeSafe dashboard, create a new
one, then add it as a GitHub repository secret the same way as step 2, named
`TYPESAFE_API_KEY`. Add it to `.env.local` as well if you want to run
`checks/compliance.py` by hand.

**To check TypeSafe worked:** the next loop run reaches "The language gate" and
reports a page count rather than failing with "TYPESAFE_API_KEY is not set".
That key is load bearing: without it nothing is judged and nothing publishes,
by design.

---

## 4. Network access

Three hosts failed to resolve from this session, so every price in
`seo/pricing-research.json` is a search snapshot rather than a live page, and
the bacteriostatic water question could not be settled at all.

1. The cloud environment menu in this session's title bar, then Edit.
2. Network access. Under Allowed domains add:
   - `tga.gov.au`
   - `www.livingstone.com.au`
   - `www.medshop.com.au`
3. Leave **Allow package managers** ticked.

A new session picks this up. The one already running does not, so start a fresh
session afterwards.

What it gets you: the 26 researched prices verified against live pages, and the
ARTG and Poisons Standard searchable so the bacteriostatic water status can be
established from the source rather than from conflicting vendor claims.

---

## 5. The six legal documents to Google Drive

I cannot pull attachments out of Gmail from a cloud session. There is no
attachment download tool, and the only other route is transcribing the raw MIME
by hand, which is not a safe way to move a zip archive. Adam's email is also
marked as possibly privileged, so it should not be routed through a third party
service to extract it.

1. Open the Gmail thread **"Goodpractice Documents"** from Adam Mazzaferro,
   27 October.
2. Download all six attachments.
3. Upload them to Google Drive. Any folder, no particular name needed.
4. Tell me they are there.

Then I read them, build the six pages, and give you a list of every highlighted
section with a proposed answer drawn from how the site actually works. That
list is what you send back to Adam to settle the documents. Once he signs off,
going live is one line: `LEGAL_LIVE = True` in `gen/seo.py`.

---

## 6. Four DNS records for gpsupply.com.au

The domain is already registered in Resend and its status is **failed**, which
means the records were never added. Here they are exactly as Resend wants them.
The domain is not on Vercel, so these go in at whichever registrar holds
gpsupply.com.au.

**1. DKIM, type TXT**

    Name:  resend._domainkey
    Value: p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCfA4/X/JrzYh+3duAkEWW/0SPT/3ql2s88xaAPCbbBvNchjtNjx4N9nR9LbrNMw/vJknVJKQKgdUqJjRcKke8zV8S5TZHbxfYr6Vdz7YQtf6KGoF1Zei93+XyxlOuw9flXMuaRbHDpx2iv8W4faFgPCeG4GS3Rb1hk12tuPvK7awIDAQAB
    TTL:   Auto

**2. SPF, type MX**

    Name:     send
    Value:    feedback-smtp.ap-northeast-1.amazonses.com
    Priority: 10
    TTL:      Auto

**3. SPF, type TXT**

    Name:  send
    Value: v=spf1 include:amazonses.com ~all
    TTL:   Auto

**4. Type CNAME**

    Name:  rsend
    Value: send.forge.rmta.net
    TTL:   Auto

### How to enter them in GoDaddy without breaking them

Domain portfolio, gpsupply.com.au, DNS, DNS Records, Add New Record.

**GoDaddy appends the domain to the Name field for you.** Enter
`resend._domainkey`, not `resend._domainkey.gpsupply.com.au`. Typing the full
name produces `resend._domainkey.gpsupply.com.au.gpsupply.com.au`, and that is
the single most common reason DKIM verification fails. Same for `send` and
`rsend`.

Two of the four records are both named `send`, one MX and one TXT. That is
correct and not a conflict, because they are different record types. Add both.

Paste the DKIM value as one unbroken line. Do not add quotes around it and do
not let an editor insert a line break. It is about 216 characters, which fits
inside a single TXT string, so it does not need splitting.

None of these touch the root of the domain, so they cannot clash with an
existing SPF record at the root if there is one. They also have nothing to do
with goodpracticesupply.com.au, which is the website domain and is served by
Vercel. If both domains are in the same GoDaddy account, leave that one alone.

TTL can stay at GoDaddy's default. A shorter TTL only helps while you are
iterating.

Then in Resend, Domains, gpsupply.com.au, press Verify. The status should move
from failed to pending to verified. Propagation is usually minutes but can be
hours.

### Receiving at hello@gpsupply.com.au is a separate job

The four records above let mail go **out** from that address. They do not give
you an inbox. The MX on `send` is for bounce feedback to Resend, not for
receiving mail at the root of the domain.

That matters because hello@gpsupply.com.au is the only address printed on the
site, and the design is that replies come back to it. Right now a customer who
replies to a contact-form email gets a bounce.

Two ways to fix it, both in GoDaddy or via its DNS:

- **Forwarding**, if your GoDaddy plan includes email forwarding: point
  hello@gpsupply.com.au at an inbox you already read. This adds root MX records
  pointing at GoDaddy's forwarding servers, which does not conflict with the
  `send` records above.
- **A real mailbox**, via Google Workspace or Microsoft 365, which replaces the
  root MX records with that provider's. More to set up, and the better answer
  once the business is trading.

Until either exists, keep `ENQUIRIES_TO` pointed at your own inbox.

What it gets you: mail can go out from hello@gpsupply.com.au. The contact form
and the apply form both send from that address, and so would any restock notice
to the list step 1 starts collecting. Collecting works without this; sending
does not.

---

## 7. Request indexing for the eight category pages

There is no API for this, it is a button in Search Console, and the quota is
roughly ten URLs a day.

1. Search Console, property `sc-domain:goodpracticesupply.com.au`.
2. Paste each URL into the inspection bar at the top, wait for the result, then
   press **Request indexing**.

    https://goodpracticesupply.com.au/shop/syringes-needles
    https://goodpracticesupply.com.au/shop/gloves-ppe
    https://goodpracticesupply.com.au/shop/diluents-swabs
    https://goodpracticesupply.com.au/shop/wound-care
    https://goodpracticesupply.com.au/shop/diagnostics
    https://goodpracticesupply.com.au/shop/clinic-disposal
    https://goodpracticesupply.com.au/shop/hygiene-cleaning
    https://goodpracticesupply.com.au/shop/taping-supports

Be realistic about this one. `/shop/syringes-needles` has not been refetched
since 22 September, so Google still holds the noindex verdict that came off the
page afterwards. Requesting indexing clears that specific problem. It does not
fix the underlying one, which is zero referring domains, and that is step 8.

While you are in there, the Ahrefs site audit project is a two minute job at
app.ahrefs.com, Site Audit, add project for goodpracticesupply.com.au. It gives
the loop crawl data it currently does not have.

---

## 8. The supplier data sheet

The long pole, and the one everything else eventually waits on.
`supplier-data-request.csv` is one row per product, 57 of them.

1. Send it to each supplier you are getting quotes from.
2. Ask them to fill in: included medical device yes, no or not applicable, ARTG
   number, sponsor name exactly as it appears on the Register, country of
   manufacture, their cost per pack ex GST, minimum order quantity, lead time,
   and the brand and manufacturer part number.
3. Send the completed sheet back to me.

Then I set the 31 placeholder prices from real cost plus a margin, fill the
ARTG and country of origin rows per product, rebuild, and the language gate
judges the new copy before any of it publishes.

Two things to tell the supplier. Write **N/A** in the device column for lines
that are plainly not therapeutic goods, such as facial tissues, hand towels,
couch roll and hand soap. And the ARTG number has to be theirs for those exact
goods, not a number from a similar product, because an ARTG entry identifies one
sponsor's specific goods and printing somebody else's against ours would be a
false regulatory claim. This site has already made that mistake once in the
other direction, printing "ARTG: Listed, see carton" on all 57 products
including cotton wool.

Worth sanity checking the 26 already researched prices against the real cost
when it comes back. A few of the placeholders they replaced were out by a factor
of two in both directions.
