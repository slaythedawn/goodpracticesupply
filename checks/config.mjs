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

console.log(bad ? `\n${bad} problem${bad === 1 ? '' : 's'} in vercel.json`
                : 'vercel.json: ok');
process.exit(bad ? 1 : 0);
