import { renderPreview } from './preview.mjs';

const CMS = window.CMS;
const h = window.h;
let pendingPublication;
let deploymentTimer;
const Preview = ({ entry }) => {
  const data = entry.get('data');
  return h('article', { className: 'cms-preview' },
    h('header', {}, h('p', { className: 'eyebrow' }, 'CAVE · ARTICLE PREVIEW'),
      h('h1', {}, data.get('title'))),
    h('div', { className: 'prose', dangerouslySetInnerHTML: {
      __html: renderPreview(data.get('body') || '', entry.get('slug').replace(/\/index$/, '')),
    } }));
};
CMS.registerPreviewTemplate('enai601', Preview);
CMS.registerPreviewTemplate('python', Preview);
CMS.registerPreviewStyle('/admin/preview.css');
CMS.registerPreviewStyle('/admin/katex/katex.min.css');
CMS.registerEventListener({
  name: 'preSave',
  handler: ({ entry }) => {
    const data = entry.get('data');
    const now = new Date().toISOString();
    pendingPublication = { slug: entry.get('slug').replace(/\/index$/, ''), timestamp: now,
      field: entry.get('newRecord') ? 'publishedAt' : 'updatedAt' };
    // Unknown historical publication times stay unknown.
    return entry.get('newRecord')
      ? data.set('publishedAt', data.get('publishedAt') || now)
      : data.set('updatedAt', now);
  },
});
CMS.registerEventListener({
  name: 'postSave',
  handler: () => {
    const status = document.getElementById('publish-status');
    status.hidden = false;
    status.innerHTML = 'GitHub에 저장했습니다. 자동 배포가 진행됩니다. <a href="https://github.com/alex-roh/alex-roh.github.io/actions/workflows/deploy-astro.yml" target="_blank" rel="noopener noreferrer">배포 상태 확인 ↗</a>';
    clearInterval(deploymentTimer);
    const expected = pendingPublication;
    if (!expected) return;
    const started = Date.now();
    deploymentTimer = setInterval(async () => {
      if (Date.now() - started > 180000) { clearInterval(deploymentTimer); return; }
      try {
        const result = await fetch(`/deployment.json?v=${Date.now()}`, { cache: 'no-store' });
        if (!result.ok) return;
        const deployment = await result.json();
        const post = deployment.posts[expected.slug];
        if (post && Date.parse(post[expected.field]) === Date.parse(expected.timestamp)) {
          clearInterval(deploymentTimer);
          status.innerHTML = `블로그 반영이 완료되었습니다. <a href="/${encodeURIComponent(expected.slug)}/" target="_blank" rel="noopener noreferrer">수정한 글 열기 ↗</a>`;
        }
      } catch { /* Keep the saved change and expose the Actions link on timeout. */ }
    }, 5000);
  },
});
CMS.init();
