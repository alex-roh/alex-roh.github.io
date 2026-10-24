import { mkdir, cp, writeFile, readFile } from 'node:fs/promises';
import { build } from 'esbuild';
import { createHash } from 'node:crypto';
import { config } from '../cms/config.mjs';
import { patchDecap } from '../cms/vendor-patches.mjs';

await mkdir('public/admin/vendor', { recursive: true });
await cp('node_modules/decap-cms/dist', 'public/admin/vendor', {
  recursive: true, filter: source => !source.endsWith('.map') && !/[/\\](?:\d+\.)?cms\.js/.test(source),
});
await writeFile('public/admin/vendor/decap-cms.js', patchDecap(await readFile('public/admin/vendor/decap-cms.js', 'utf8')));
await cp('node_modules/katex/dist', 'public/admin/katex', { recursive: true });
await build({ entryPoints: ['cms/admin.mjs'], bundle: true, format: 'esm', external: ['/fonts/*'], outfile: 'public/admin/admin.js', minify: true });
// JSON is a YAML subset accepted by Decap. Keep one typed config for tests and build.
await writeFile('public/admin/config.yml', JSON.stringify(config, null, 2));
const styles = await readFile('src/styles/global.css', 'utf8');
// Both surfaces consume the exact same light/dark tokens; admin.css adds layout only.
const themeRules = [...styles.matchAll(/:root(?:\[data-theme="dark"\])?\s*\{[^}]*\}/g)].map(match => match[0]);
if (themeRules.length !== 2) throw new Error('Expected the blog light and dark theme token rules');
const adminStyles = await readFile('public/admin/admin.css', 'utf8');
await writeFile('public/admin/admin.css', themeRules.join('\n') + '\n' + adminStyles);

await writeFile('public/admin/preview.css', styles + '\n.cms-preview{max-width:800px;margin:auto;padding:36px 32px}.cms-preview header{border-bottom:1px solid var(--line);margin-bottom:36px}.cms-preview h1{font-size:clamp(22px,4vw,34px);overflow-wrap:anywhere;word-break:keep-all}html{scroll-behavior:auto!important;scroll-padding-top:0}.cms-preview pre{white-space:pre-wrap;overflow-wrap:anywhere}.cms-preview .katex-display{overflow-x:auto;overflow-y:hidden}\n');

// Each release must refresh the editor even when GitHub Pages caches static files.
const assetHash = async path => createHash('sha256').update(await readFile(path)).digest('hex').slice(0, 12);
const html = (await readFile('cms/index.html', 'utf8'))
  .replace('/admin/vendor/decap-cms.js', '/admin/vendor/decap-cms.js?v=' + await assetHash('public/admin/vendor/decap-cms.js'))
  .replace('/admin/admin.css', '/admin/admin.css?v=' + await assetHash('public/admin/admin.css'))
  .replace('/admin/admin.js', '/admin/admin.js?v=' + await assetHash('public/admin/admin.js'));
await writeFile('public/admin/index.html', html);
