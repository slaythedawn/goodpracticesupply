// vercel.json against Vercel's schema for the fields this project uses.
//
// This exists because an unknown "comment" key inside a headers rule took
// production down for two deploys. Vercel validates the config before it starts
// building, so the deployment fails with no build log to read, which is a
// confusing way to find out. Nothing else in checks/ touches this file: the
// other three run against a local static server and never see it.

import { readFileSync } from 'fs';

const ALLOWED_TOP = new Set(['$schema', 'buildCommand', 'cleanUrls', 'devCommand',
  'framework', 'functions', 'git', 'headers', 'ignoreCommand', 'images',
  'installCommand', 'outputDirectory', 'public', 'redirects', 'regions',
  'rewrites', 'trailingSlash', 'crons', 'routes']);
const ALLOWED_RULE = { headers: ['source', 'headers', 'has', 'missing'],
                       redirects: ['source', 'destination', 'permanent', 'statusCode', 'has', 'missing'],
                       rewrites: ['source', 'destination', 'has', 'missing'] };

let bad = 0;
const fail = m => { bad++; console.log('FAIL', m); };

let cfg;
try { cfg = JSON.parse(readFileSync('vercel.json', 'utf8')); }
catch (e) { console.log('FAIL vercel.json is not valid JSON:', e.message); process.exit(1); }

for (const k of Object.keys(cfg))
  if (!ALLOWED_TOP.has(k)) fail(`unknown top-level key "${k}"`);

for (const [section, allowed] of Object.entries(ALLOWED_RULE)) {
  for (const [i, rule] of (cfg[section] || []).entries()) {
    for (const k of Object.keys(rule))
      if (!allowed.includes(k)) fail(`${section}[${i}] has unknown key "${k}"`);
    if (!rule.source) fail(`${section}[${i}] has no source`);
  }
}
for (const [i, rule] of (cfg.headers || []).entries())
  for (const [j, h] of (rule.headers || []).entries())
    if (!h.key || typeof h.value !== 'string')
      fail(`headers[${i}].headers[${j}] needs a key and a string value`);

// The header rules decide what search engines are told, so what they match is
// worth testing rather than reading. A pattern that quietly stopped matching a
// product page would publish fifty-seven invented prices to the index, and a
// pattern that started matching a category would hide eight pages that are
// meant to rank. Neither is visible in a browser.
function toRegex(source) {
  // path-to-regexp, restricted to the two forms this config uses: :name and
  // :name* . The source is validated before conversion, not after: checking the
  // converted body for a leftover star finds the star this function just wrote.
  if (!/^(\/(?:[A-Za-z0-9_.-]+|:[A-Za-z_]+\*?))+$/.test(source))
    throw new Error('unsupported pattern, extend toRegex: ' + source);
  const body = source
    .replace(/\/:[A-Za-z_]+\*/g, '(?:\\/[^/]+)*')
    .replace(/\/:[A-Za-z_]+/g, '\\/[^/]+')
    .replace(/\//g, (m, i, str) => str[i - 1] === '\\' ? m : '\\/');
  return new RegExp('^' + body.replace(/\\\\\//g, '\\/') + '$');
}

const EXPECT = [
  ['/shop', false, 'the shop index is indexed'],
  ['/shop/syringes-needles', false, 'a category is indexed'],
  ['/shop/syringes-needles/u-100-insulin-syringes', true, 'a product is noindex'],
  ['/internal/photo-review', true, 'internal pages stay noindex'],
  ['/learn/sharps-disposal-australia', false, 'a guide is indexed'],
  ['/', false, 'the home page is indexed'],
];

{
  const rules = (cfg.headers || []).filter(r =>
    (r.headers || []).some(h => /x-robots-tag/i.test(h.key) && /noindex/i.test(h.value)));
  let wrong = 0;
  for (const [path, shouldMatch, why] of EXPECT) {
    const hit = rules.some(r => toRegex(r.source).test(path));
    if (hit !== shouldMatch) {
      wrong++;
      fail(why + ': ' + path + ' ' + (hit ? 'is' : 'is not') +
           ' covered by a noindex header rule');
    }
  }
  if (!wrong) console.log('header rules: ' + EXPECT.length + ' paths checked, all as intended');
}

console.log(bad ? `\n${bad} problem${bad === 1 ? '' : 's'} in vercel.json`
                : 'vercel.json: ok');
process.exit(bad ? 1 : 0);
