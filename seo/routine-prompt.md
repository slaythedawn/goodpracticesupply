# The prompt for the daily refresh Routine

Create this at [claude.ai/settings/routines](https://claude.ai/settings/routines),
not from a session. A Routine created programmatically cannot be given connector
access, so the session it fires comes up with no Ahrefs tools and the run fails.
Created from the Routines page, the connectors can be attached.

Settings: run every day at 18:40 UTC, start a new session each time, and attach the
**Ahrefs** and **Google Search Console** connectors. 18:40 is half an hour before
the Daily SEO loop workflow fires, so the workflow ranks against today's figures.

Paste everything below the line as the prompt.

---

Refresh the SEO data for Good Practice Supply. This runs every day about half an hour before the Daily SEO loop workflow fires, so the workflow ranks against today's figures rather than last week's.

Repository: slaythedawn/goodpracticesupply, branch claude/live-link-publishing-7zujix. Read seo/README.md first; it explains the whole loop and why each step exists.

You need the Ahrefs and Google Search Console connectors for this. If either is not available to you, stop and say so plainly in your reply rather than guessing at figures or writing anything to the repository.

Do these in order. Do not skip the verification at the end.

1. Ahrefs keyword refresh, through the Ahrefs MCP connector. Read the list of tracked terms out of seo/keywords-au.json. Call keywords-explorer-overview for them in batches of about 50, country au, selecting keyword,volume,difficulty,cpc,traffic_potential,intents. Save each response verbatim to a file and run:

       python3 seo/refresh.py --apply <that file>

   Do not hand-edit seo/keywords-au.json. The merge, the what-moved report and the sorting live in refresh.py so that the file cannot quietly acquire a term with a difficulty somebody remembered.

   Compare a figure only against the endpoint that produced it. Keywords Explorer and Site Explorer report different volumes for the same term, and treating one as a change in the other is a mistake already made once on this project.

2. Look for new terms. Call keywords-explorer-matching-terms on the seeds listed in seo/keywords-au.json, match_mode terms, country au, filtered to volume at least 100 and difficulty at most 35, ordered by volume descending, limit 100. Apply it the same way. New terms arrive unjudged, which is deliberate: it keeps them out of the publishing queue until the TypeSafe triage in CI has cleared them.

3. Search Console, through the Google Search Console connector. Property sc-domain:goodpracticesupply.com.au. Query the last 28 complete days, ending three days before today because Search Console finalises late, with dimensions query and page, dataState all, rowLimit 25000. Write it to seo/gsc-snapshot.json in the shape that file already uses: property, start, end, pulled, note, rows. Then run:

       python3 seo/performance.py --from-file seo/gsc-snapshot.json

   Read what it prints. If it reports a page to optimise or expand, that is the most useful output of the whole run.

4. On Sundays only, also refresh the competitor positions. For the twelve highest volume tracked terms, call serp-overview with country au, top_positions 10, type organic, selecting position,url,domain_rating,traffic,title. Update the matching entries in seo/competitors.json carefully, keeping each rival's existing lane and why text unchanged. A lane is a judgement about how to treat a rival and is not something a position change should overwrite.

5. Write today's page. This is the step that has never run: the loop produced
   thirty-six briefs in five weeks and not one became a page, because the writing
   was left to a CI step that needs ANTHROPIC_API_KEY and the key was never set.
   A session can do it, so do it here.

   Run `python3 seo/opportunities.py --write`, read the brief it names, and carry
   it out. Read `.claude/skills/gps-guide/SKILL.md` and
   `.claude/skills/gps-compliance/SKILL.md` first. Copy goes in
   `gen/guidecontent.py` for a guide or the `CATEGORY_SEO` table in `gen/seo.py`
   for a shop category, never into `docs/*.html`, which is generated and thrown
   away on the next build.

   The brief leads with a table of what Google already shows that page for and
   does not answer. Those are real searches. Answer them plainly, in the page, and
   do not pad to hit a word count.

   Three things every page carries, and the build fails without the second:
   an image, one featured product or tool in `FEATURED` in `gen/feature.py`, and
   the email sign-up, which `gen/guides.py` adds for you.

   For a brand new page, generate the image rather than reusing a catalogue
   photograph: use Higgsfield, upload it, add the key to `I` in
   `gen/catalogue.py` and to `PHOTO` in `gen/guides.py`. It has to pass the OCR
   gate in `brand/PHOTOGRAPHY.md`, which rejects generated lettering, so no text
   in the image.

   Link out to the product pages. They are indexable now, so a link from a guide
   passes authority to something that can be pre-ordered, which is the point of
   writing the guide.

6. Verify before committing. Run:

       python3 seo/refresh.py --age
       python3 seo/opportunities.py

   The queue should read sensibly: real page expansions near the top, not somebody else's brand name. If it does not, say so in your reply and do not commit.

   Then rebuild and check, which is what the gps-preflight skill does:

       python3 gen/build.py && python3 gen/tools.py && python3 gen/guides.py
       # then learnindex, headmeta, launchstate, footer, autolink,
       # optimise_images, searchindex, llms, sitemap, in that order
       node checks/config.mjs && node checks/linkcheck.mjs
       node checks/seocheck.mjs && node checks/depth.mjs

   `gen/autolink.py` applies the internal links the suggester was confident
   about, so a page written today is linked to today rather than left an orphan.

   The TGA language gate needs TYPESAFE_API_KEY, which is not reachable from this
   sandbox. Push, then trigger the workflow: it runs
   `checks/compliance.py` and a finding fails the run. Do not call the page done
   until that has passed.

7. Commit and push to claude/live-link-publishing-7zujix. The commit message says what moved and what was added, in plain words. End it with:

       Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>

   Then trigger the workflow so it runs against the fresh data, using the GitHub MCP: actions_run_trigger, method run_workflow, workflow_id daily-seo.yml, ref claude/live-link-publishing-7zujix.

House rules, which apply to anything you write: consumables only, never imply this business supplies a peptide, a hormone or any prescription medicine. Australian spelling. No em dashes. No emoji.

If `opportunities.py` says every cluster is held back, do not invent work. Read
why. "Still outstanding" means a brief was written and never carried out, and the
right response is to write that one rather than to produce another brief.

If nothing moved, nothing new turned up and there is no page to write, commit
nothing, trigger nothing, and say so in one line. A quiet day is a real result and
does not need a commit to prove it happened.
