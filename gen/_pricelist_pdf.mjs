// Render export/supply-list.html to A4 portrait PDF.
// Called by gen/pricelist.py. Not part of the site build.
// Chromium comes from checks/browser.mjs, which resolves a local, global or
// sandbox Playwright in turn. Importing 'playwright' directly is the exact bug
// that file was written to kill, and it failed here the same way the first time.
import { chromium as loadChromium } from '../checks/browser.mjs';
import { pathToFileURL } from 'node:url';

const [src, out] = process.argv.slice(2);
if (!src || !out) {
  console.error('usage: node gen/_pricelist_pdf.mjs <in.html> <out.pdf>');
  process.exit(2);
}

const chromium = await loadChromium();
const browser = await chromium.launch();
const page = await browser.newPage();

// Google Fonts is outside this environment's allowlist, so the request hangs
// rather than failing fast. Serve an empty stylesheet instead of aborting: an
// abort logs "Failed to load resource" to the console, and the console is what
// decides whether this render passed, so aborting made the script fail on a
// condition it had caused itself. The stack falls through to Inter, which is
// installed, and the brand lockup is outlined vector so the mark is exact.
let blocked = 0;
await page.route('**/*', (route) => {
  const u = route.request().url();
  if (u.includes('fonts.googleapis.com') || u.includes('fonts.gstatic.com')) {
    blocked += 1;
    return route.fulfill({ status: 200, contentType: 'text/css', body: '' });
  }
  return route.continue();
});

const errors = [];
page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
page.on('pageerror', (e) => errors.push(String(e)));

await page.goto(pathToFileURL(src).href, { waitUntil: 'load' });

const foot =
  '<div style="width:100%;padding:0 12mm;font:7pt -apple-system,Inter,Arial,' +
  'sans-serif;color:#59595A;display:flex;justify-content:space-between">' +
  '<span>Good Practice Supply &middot; Wholesale pricing available on request</span>' +
  '<span>Page <span class="pageNumber"></span> of <span class="totalPages"></span></span>' +
  '</div>';

await page.pdf({
  path: out,
  format: 'A4',
  printBackground: true,
  displayHeaderFooter: true,
  headerTemplate: '<span></span>',
  footerTemplate: foot,
  margin: { top: '11mm', bottom: '14mm', left: '11mm', right: '11mm' },
});

await browser.close();

if (errors.length) {
  console.error('pricelist: %d console error(s) during render:', errors.length);
  for (const e of errors.slice(0, 5)) console.error('  ' + e);
  process.exit(1);
}
console.log(`pricelist: ${out} rendered (${blocked} font request(s) aborted, 0 console errors)`);
