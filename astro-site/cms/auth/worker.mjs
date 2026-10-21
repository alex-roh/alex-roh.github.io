const headers = {
  'Cache-Control': 'no-store', 'Referrer-Policy': 'no-referrer',
  'X-Content-Type-Options': 'nosniff', 'X-Frame-Options': 'DENY',
};
const cookieName = '__Host-cave-oauth';
const cookie = (value, age) => `${cookieName}=${value}; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=${age}`;
const clearCookie = cookie('', 0);
const error = (message, status = 400) => new Response(message, { status, headers: { ...headers, 'Set-Cookie': clearCookie } });

export function isRestrictedInstallation(installations) {
  if (installations.length !== 1) return false;
  const installation = installations[0];
  return installation.account?.login === 'alex-roh'
    && installation.repository_selection === 'selected'
    && installation.permissions?.contents === 'write'
    && Object.entries(installation.permissions).every(([permission, level]) =>
      permission === 'contents' ? level === 'write' : permission === 'metadata' && level === 'read');
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === '/health') return new Response('Cave CMS auth', { headers });
    if (!env.GITHUB_CLIENT_ID || !env.GITHUB_CLIENT_SECRET) return error('GitHub login is not configured.', 503);
    if (request.method !== 'GET') return error('Method not allowed', 405);
    if (url.pathname === '/auth') {
      if (url.searchParams.get('provider') !== 'github' || url.searchParams.get('site_id') !== 'alex-roh.github.io') return error('Invalid site');
      const state = crypto.randomUUID();
      const destination = new URL('https://github.com/login/oauth/authorize');
      destination.search = new URLSearchParams({ client_id: env.GITHUB_CLIENT_ID,
        redirect_uri: `${url.origin}/callback`, state });
      return new Response(null, { status: 302, headers: { ...headers, Location: destination.href, 'Set-Cookie': cookie(state, 600) } });
    }
    if (url.pathname !== '/callback') return error('Not found', 404);
    const state = url.searchParams.get('state');
    const stored = (request.headers.get('Cookie') || '').split('; ').find(part => part.startsWith(`${cookieName}=`))?.slice(cookieName.length + 1);
    const code = url.searchParams.get('code');
    if (!state || state !== stored || !code) return error('Login expired or invalid. Please sign in again.');
    try {
      const tokenResponse = await fetch('https://github.com/login/oauth/access_token', {
        method: 'POST', headers: { Accept: 'application/json', 'Content-Type': 'application/json' },
        body: JSON.stringify({ client_id: env.GITHUB_CLIENT_ID, client_secret: env.GITHUB_CLIENT_SECRET,
          code, redirect_uri: `${url.origin}/callback` }),
      });
      const token = (await tokenResponse.json()).access_token;
      // A GitHub App user token is repository-scoped; reject broad OAuth tokens.
      if (!token?.startsWith('ghu_')) return error('A repository-restricted GitHub App login is required.', 401);
      const githubHeaders = { Authorization: `Bearer ${token}`, Accept: 'application/vnd.github+json', 'User-Agent': 'Cave-Decap-Auth' };
      const profile = await fetch('https://api.github.com/user', { headers: githubHeaders });
      if (!profile.ok || (await profile.json()).login !== 'alex-roh') return error('This editor is restricted to its owner.', 403);
      const installationsResponse = await fetch('https://api.github.com/user/installations', { headers: githubHeaders });
      if (!installationsResponse.ok) return error('Cannot verify the GitHub App installation.', 403);
      const installations = (await installationsResponse.json()).installations || [];
      if (!isRestrictedInstallation(installations)) return error('Install this app only on the blog repository, with Contents read/write and Metadata read permissions.', 403);
      const repositoriesResponse = await fetch(`https://api.github.com/user/installations/${installations[0].id}/repositories`, { headers: githubHeaders });
      const repositories = repositoriesResponse.ok ? await repositoriesResponse.json() : {};
      if (repositories.total_count !== 1 || repositories.repositories?.[0]?.full_name !== 'alex-roh/alex-roh.github.io') {
        return error('Only alex-roh/alex-roh.github.io may be selected for this app.', 403);
      }
      const repo = await fetch('https://api.github.com/repos/alex-roh/alex-roh.github.io', { headers: githubHeaders });
      if (!repo.ok || !(await repo.json()).permissions?.push) return error('Repository write access required.', 403);
      const nonce = crypto.randomUUID();
      const message = JSON.stringify(`authorization:github:success:${JSON.stringify({ token, provider: 'github' })}`).replaceAll('<', '\\u003c');
      const body = `<!doctype html><html lang="ko"><meta charset="utf-8"><title>Cave · 로그인</title><p>로그인되었습니다. 편집기로 돌아가는 중입니다.</p><script nonce="${nonce}">const origin='https://alex-roh.github.io';window.addEventListener('message',function receive(event){if(event.origin!==origin||event.source!==window.opener)return;window.removeEventListener('message',receive);window.opener.postMessage(${message},origin);window.close()});if(window.opener)window.opener.postMessage('authorizing:github',origin);</script></html>`;
      return new Response(body, { headers: { ...headers, 'Set-Cookie': clearCookie, 'Content-Type': 'text/html; charset=utf-8',
        'Content-Security-Policy': `default-src 'none'; script-src 'nonce-${nonce}'; base-uri 'none'; frame-ancestors 'none'` } });
    } catch {
      return error('Login service temporarily unavailable. Please try again.', 502);
    }
  },
};
