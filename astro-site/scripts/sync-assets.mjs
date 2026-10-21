import { readdir, mkdir, copyFile, rm } from 'node:fs/promises';
import path from 'node:path';
async function walk(dir) {
 for (const e of await readdir(dir,{withFileTypes:true})) {
  const source=path.join(dir,e.name);
  if (e.isDirectory()) await walk(source);
  else if (!source.endsWith('.md')) {
   const dest=path.join('public','media',path.basename(dir),e.name);
   await mkdir(path.dirname(dest),{recursive:true}); await copyFile(source,dest);
  }
 }
}
// Recreate only this generated directory so archived post assets are not published.
const root = process.cwd();
const media = path.resolve(root, 'public', 'media');
if (path.dirname(media) !== path.resolve(root, 'public')) throw new Error('Unexpected generated asset path');
await rm(media, { recursive: true, force: true });
await walk('contents/posts');
