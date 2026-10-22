import enai601 from '../editorial/enai601.md';
import { renderPreview } from './preview.mjs';

const guides = {
  enai601: { title: 'ENAI601 Numerical Methods', markdown: enai601 },
  python: { title: 'ENAI607 Python Programming', markdown: '이 시리즈에는 아직 별도 편집 지침이 등록되지 않았습니다.' },
};

export function installEditorialGuides() {
  const button = document.createElement('button');
  button.type = 'button';
  button.className = 'cave-guide-button';
  button.textContent = '편집 지침';
  button.setAttribute('aria-haspopup', 'dialog');
  const dialog = document.createElement('dialog');
  dialog.id = 'cave-editorial-guide';
  dialog.setAttribute('aria-labelledby', 'cave-guide-title');
  const header = document.createElement('header');
  const title = document.createElement('h2');
  title.id = 'cave-guide-title';
  const close = document.createElement('button');
  close.type = 'button';
  close.textContent = '닫기';
  header.append(title, close);
  const content = document.createElement('div');
  content.className = 'cave-guide-content';
  dialog.append(header, content);
  document.body.append(dialog);
  close.addEventListener('click', () => dialog.close());
  button.addEventListener('click', () => {
    const key = location.hash.match(/^#\/collections\/([^/]+)/)?.[1];
    const guide = guides[key];
    if (!guide) return;
    title.textContent = guide.title + ' · 편집 지침';
    content.innerHTML = renderPreview(guide.markdown, 'editorial-guide');
    if (key === 'enai601') {
      const link = document.createElement('a');
      link.href = 'https://github.com/alex-roh/alex-roh.github.io/blob/main/astro-site/editorial/enai601.md';
      link.target = '_blank';
      link.rel = 'noopener noreferrer';
      link.textContent = '지침 Markdown 파일 보기 ↗';
      content.append(link);
    }
    dialog.showModal();
  });
  let scheduled = false;
  function place() {
    scheduled = false;
    const key = location.hash.match(/^#\/collections\/([^/]+)/)?.[1];
    const target = guides[key] && (document.querySelector('[class*="CollectionTopContainer"]')
      || document.querySelector('[class*="PreviewPaneContainer-ControlPaneContainer"]'));
    if (target) {
      if (button.parentElement !== target) target.prepend(button);
    } else button.remove();
  }
  function schedule() {
    if (!scheduled) { scheduled = true; requestAnimationFrame(place); }
  }
  const root = document.getElementById('nc-root');
  new MutationObserver(schedule).observe(root || document.body, { childList: true, subtree: true });
  addEventListener('hashchange', () => { if (dialog.open) dialog.close(); schedule(); });
  place();
}
