import { readFileSync, writeFileSync } from 'node:fs';
import { globSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

const [slug, kind, timestamp] = process.argv.slice(2);
const field = { published: 'publishedAt', updated: 'updatedAt' }[kind];
if (!/^[a-z0-9-]+$/.test(slug || '') || !field || !/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$/.test(timestamp || '') || !Number.isFinite(Date.parse(timestamp))) {
  throw new Error('Usage: node scripts/set-publication-time.mjs <slug> published|updated <ISO timestamp with offset>');
}
const root = fileURLToPath(new URL('../', import.meta.url));
const paths = [...globSync(`contents/posts/**/${slug}/index.md`, { cwd: root })];
if (paths.length !== 1) throw new Error(`Expected exactly one post for ${slug}, found ${paths.length}`);
const file = `${root}/${paths[0]}`;
const source = readFileSync(file, 'utf8');
const end = source.indexOf('\n---', 4);
if (!source.startsWith('---') || end < 0) throw new Error('Missing frontmatter');
let front = source.slice(0, end);
const existing = front.match(new RegExp(`^${field}:.*$`, 'm'));
if (kind === 'published' && existing) throw new Error('The first publication time is already recorded; keep it unchanged.');
const other = front.match(/^publishedAt:\s*["']?([^"'\r\n]+)["']?\s*$/m)?.[1];
if (kind === 'updated' && other && Date.parse(timestamp) < Date.parse(other)) throw new Error('An update cannot precede first publication.');
const line = `${field}: "${timestamp}"`;
front = existing ? front.replace(existing[0], line) : `${front}\n${line}`;
writeFileSync(file, front + source.slice(end));
console.log(`${slug}: ${field} = ${timestamp}`);
