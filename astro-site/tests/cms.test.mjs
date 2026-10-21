import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile, readdir } from 'node:fs/promises';
import { renderPreview } from '../cms/preview.mjs';
import { config } from '../cms/config.mjs';
import auth, { isRestrictedInstallation } from '../cms/auth/worker.mjs';

test('all current articles preview math without losing subscripts or executing HTML', async () => {
  let count = 0;
  for (const category of ['enai601', 'python']) {
    for (const slug of await readdir(`contents/posts/${category}`)) {
      const text = await readFile(`contents/posts/${category}/${slug}/index.md`, 'utf8');
      const body = text.replace(/^---\r?\n[\s\S]*?\r?\n---\r?\n/, '');
      const html = renderPreview(body, slug);
      assert.ok(!html.includes('class="katex-error"'), slug);
      if (category === 'enai601') assert.match(html, /class="katex"/, slug);
      count++;
    }
  }
  assert.ok(count >= 14);
  const html = renderPreview('$\\lVert x\\rVert_2^2$\n\n$$\nx^2\n$$\n\n<script>alert(1)</script><img src=x onerror=alert(1)>', 'test');
  assert.match(html, /katex-display/);
  assert.match(html, /sizing reset-size6 size3/);
  assert.ok(!html.includes('<script') && !html.includes('onerror'));
});

test('CMS writes only to canonical production repo and preserves raw math source', () => {
  assert.equal(config.backend.repo, 'alex-roh/alex-roh.github.io');
  assert.equal(config.backend.branch, 'main');
  for (const collection of config.collections) {
    assert.equal(collection.delete, false);
    assert.ok(collection.folder.startsWith('astro-site/contents/posts/'));
    assert.deepEqual(collection.fields.find(field => field.name === 'body').modes, ['raw']);
  }
});

test('OAuth refuses other sites and missing/forged state before token exchange', async () => {
  const env = { GITHUB_CLIENT_ID: 'test', GITHUB_CLIENT_SECRET: 'test' };
  const request = path => new Request(`https://auth.example${path}`);
  assert.equal((await auth.fetch(request('/auth?provider=github&site_id=evil.example'), env)).status, 400);
  assert.equal((await auth.fetch(request('/callback?code=test&state=forged'), env)).status, 400);
  const response = await auth.fetch(request('/auth?provider=github&site_id=alex-roh.github.io'), env);
  assert.equal(response.status, 302);
  const location = new URL(response.headers.get('Location'));
  assert.equal(location.searchParams.has('scope'), false);
  assert.match(response.headers.get('Set-Cookie'), /HttpOnly; Secure; SameSite=Lax/);
});

test('GitHub App installation must be selected-repository only with minimal permissions', () => {
  const installation = { account: { login: 'alex-roh' }, repository_selection: 'selected', permissions: { contents: 'write', metadata: 'read' } };
  assert.equal(isRestrictedInstallation([installation]), true);
  assert.equal(isRestrictedInstallation([{ ...installation, repository_selection: 'all' }]), false);
  assert.equal(isRestrictedInstallation([{ ...installation, permissions: { ...installation.permissions, administration: 'write' } }]), false);
  assert.equal(isRestrictedInstallation([installation, installation]), false);
  assert.equal(isRestrictedInstallation([]), false);
});
