import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { createRequire } from 'node:module';
import config from '../astro.config.mjs';
import { formatPublicationTime } from '../src/lib/publication.mjs';

test('the production Markdown pipeline renders inline and display math but preserves code', async () => {
  const renderer = await config.markdown.processor.createRenderer({});
  const opts = { fileURL: new URL('../contents/posts/enai601/enai601-convex-functions/index.md', import.meta.url) };
  const inline = (await renderer.render('본문 $f(x)=x^2$ 입니다.', opts)).code;
  assert.match(inline, /class="katex"/);
  assert.doesNotMatch(inline, /katex-display|katex-error/);
  const display = (await renderer.render('$$\nf(x)=x^2\n$$', opts)).code;
  assert.match(display, /katex-display/);
  const code = (await renderer.render('`$5` and `$f(x)$`', opts)).code;
  assert.doesNotMatch(code, /class="katex"/);
  assert.match(code, /<code>\$5<\/code>/);
});
test('publication times use the correct Eastern daylight and standard times across date boundaries', () => {
  assert.match(formatPublicationTime('2026-10-21T06:52:02Z'), /02:52.*EDT/);
  assert.match(formatPublicationTime('2026-12-01T04:30:00Z'), /11월 30일.*23:30.*EST/);
});

test('the stylesheet matches the renderer and reduces norm subscripts and square superscripts', async () => {
  const require = createRequire(import.meta.url);
  const rendererRequire = createRequire(require.resolve('rehype-katex'));
  const katex = require('katex');
  const rendererKatex = rendererRequire('katex');
  assert.equal(katex.version, rendererKatex.version, 'KaTeX HTML and CSS must use the same version');
  const css = readFileSync(require.resolve('katex/dist/katex.min.css'), 'utf8');
  const renderer = await config.markdown.processor.createRenderer({});
  const opts = { fileURL: new URL('../contents/posts/enai601/enai601-convex-functions/index.md', import.meta.url) };
  const html = (await renderer.render('$\\lVert x\\rVert_2^2 + x^{2^2}$', opts)).code;
  assert.doesNotMatch(html, /katex-error/);
  for (const classes of ['reset-size6 size3', 'reset-size3 size1']) {
    const sizing = html.match(new RegExp(`class="([^" ]*sizing) ${classes}[^\"]*"`))?.[1];
    assert.ok(sizing, `Rendered scripts must include ${classes}`);
    const selector = `.${sizing}.${classes.replaceAll(' ', '.')}`;
    const at = css.indexOf(selector + '{');
    assert.ok(at >= 0, `Missing CSS sizing rule for ${selector}`);
    const declaration = css.slice(at, css.indexOf('}', at));
    const ratio = Number(declaration.match(/font-size:([.\d]+)em/)?.[1]);
    assert.ok(ratio > 0 && ratio < 1, `${selector} must be smaller than its parent`);
  }
});

test('CMS YAML dates and quoted ISO timestamps preserve the same instant', async () => {
  const { normalizeTimestampInput } = await import('../src/lib/publication.mjs');
  const { z } = await import('astro/zod');
  const schema = z.preprocess(normalizeTimestampInput, z.iso.datetime({ offset: true }));
  const original = '2026-10-21T02:52:02-04:00';
  assert.equal(schema.parse(original), original);
  assert.equal(Date.parse(schema.parse(new Date(original))), Date.parse(original));
  assert.match(formatPublicationTime(schema.parse(new Date(original))), /02:52.*EDT/);
  assert.equal(schema.safeParse('not-a-timestamp').success, false);
  assert.equal(schema.safeParse(new Date('invalid')).success, false);
});
