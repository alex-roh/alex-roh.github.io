import { mkdir, cp, writeFile, readFile } from 'node:fs/promises';
import { build } from 'esbuild';
import { config } from '../cms/config.mjs';

await mkdir('public/admin/vendor', { recursive: true });
await cp('node_modules/decap-cms/dist', 'public/admin/vendor', {
  recursive: true, filter: source => !source.endsWith('.map') && !/[/\\](?:\d+\.)?cms\.js/.test(source),
});
await cp('node_modules/katex/dist', 'public/admin/katex', { recursive: true });
await build({ entryPoints: ['cms/admin.mjs'], bundle: true, format: 'esm', outfile: 'public/admin/admin.js', minify: true });
// JSON is a YAML subset accepted by Decap. Keep one typed config for tests and build.
await writeFile('public/admin/config.yml', JSON.stringify(config, null, 2));
const styles = await readFile('src/styles/global.css', 'utf8');
await writeFile('public/admin/preview.css', styles + '\n.cms-preview{max-width:800px;margin:auto;padding:36px 32px}.cms-preview header{border-bottom:1px solid var(--line);margin-bottom:36px}.cms-preview h1{font-size:34px}.cms-preview pre{white-space:pre-wrap}.cms-preview .katex-display{overflow-x:auto;overflow-y:hidden}\n');
