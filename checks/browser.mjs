// Where Chromium comes from.
//
// The three browser checks each hardcoded an absolute path into one machine's
// global node_modules. They ran there and nowhere else, which nothing noticed
// because there was nowhere else, until CI ran them on a GitHub runner and all
// three failed instantly on the import. That is the same bug gen/footer.py had,
// found the same way, an hour apart.
//
// Resolved rather than assumed: a local install if the project has one, then a
// global one, then the sandbox path. Whichever answers first wins.
const CANDIDATES = [
  'playwright',
  'playwright-core',
  '/opt/node22/lib/node_modules/playwright/index.mjs',
];

export async function chromium() {
  const tried = [];
  for (const spec of CANDIDATES) {
    try {
      const mod = await import(spec);
      if (mod.chromium) return mod.chromium;
      tried.push(spec + ' (no chromium export)');
    } catch (e) {
      tried.push(spec + ' (' + String(e.message).split('\n')[0].slice(0, 60) + ')');
    }
  }
  throw new Error('no Playwright available. Tried:\n  ' + tried.join('\n  '));
}
