import { renderPreview } from './preview.mjs';
import ko from 'decap-cms-locales/dist/esm/ko/index.js';
import { attachPreview, initializeEditor } from './editor-ui.mjs';
import { registerWritingTools } from './writing-tools.mjs';
import { createPublicationMonitor } from './publication.mjs';
import './admin.css';
import '../src/styles/header-controls.css';

const CMS = window.CMS;
const h = window.h;
// Keep Decap's translations, changing only the vocabulary for this blog.
const phrases = JSON.parse(JSON.stringify(ko).replace(/컬렉션|컬랙션/g, '시리즈'));
phrases.app.header.content = 'POSTS';
phrases.app.header.media = '미디어';
phrases.app.header.quickAdd = 'NEW POST';
phrases.collection.collectionTop.newButton = '새 글 쓰기';
phrases.editor.editorToolbar.backCollection = '글 목록';
phrases.editor.editorToolbar.unsavedChanges = '저장 전';
phrases.editor.editorToolbar.changesSaved = '저장됨';
phrases.editor.editorToolbar.published = 'GitHub 저장됨';
CMS.registerLocale('ko', phrases);
initializeEditor();
const drafts = registerWritingTools(CMS, h);
let publishingDraft;
let pendingPublication;
let noticeTimer;
function showPublicationStatus(html, autoHide = false) {
  const status = document.getElementById('publish-status');
  clearTimeout(noticeTimer);
  status.hidden = false;
  status.innerHTML = '<span>' + html + '</span><button type="button" aria-label="알림 닫기">×</button>';
  status.querySelector('button').onclick = () => { clearTimeout(noticeTimer); status.hidden = true; };
  if (autoHide) noticeTimer = setTimeout(() => { status.hidden = true; }, 8000);
}
const actionsLink = '<a href="https://github.com/alex-roh/alex-roh.github.io/actions/workflows/deploy-astro.yml" target="_blank" rel="noopener noreferrer">Actions에서 진행 상황 보기 ↗</a>';
let publicationStorage;
try { publicationStorage = sessionStorage; } catch {}
const publication = createPublicationMonitor({ fetch: (...args) => fetch(...args), storage: publicationStorage,
  onStatus: ({ phase, elapsed, slug }) => {
    const minutes = Math.floor(elapsed / 60000);
    const seconds = Math.floor(elapsed / 1000) % 60;
    const duration = `${minutes}분 ${seconds}초`;
    window.cavePublicationLabel = phase === 'live' ? '최근 게시 · 블로그 반영 완료'
      : phase === 'delayed' ? '최근 게시 · 배포 확인 지연' : '최근 게시 · 배포 중';
    for (const label of document.querySelectorAll('.cave-published-label')) label.textContent = window.cavePublicationLabel;
    if (phase === 'live') showPublicationStatus(`블로그 반영이 완료되었습니다. <a href="/${encodeURIComponent(slug)}/" target="_blank" rel="noopener noreferrer">수정한 글 열기 ↗</a>`);
    else showPublicationStatus(`GitHub 저장 완료 · ${phase === 'delayed' ? '아직 블로그 반영을 확인하지 못했습니다. 계속 확인 중입니다.' : '빌드·배포 및 블로그 반영을 기다리는 중입니다.'} (${duration}) ${actionsLink}`);
  },
});
publication.resume();
const Preview = ({ entry, getAsset }) => {
  const data = entry.get('data');
  return h('article', { className: 'cms-preview', ref: attachPreview },
    h('header', {}, h('p', { className: 'eyebrow' }, 'CAVE · ARTICLE PREVIEW'),
      h('h1', {}, data.get('title'))),
    h('div', { className: 'prose', dangerouslySetInnerHTML: {
      __html: renderPreview(data.get('body') || '', entry.get('slug').replace(/\/index$/, ''), getAsset),
    } }));
};
CMS.registerPreviewTemplate('enai601', Preview);
CMS.registerPreviewTemplate('python', Preview);
CMS.registerPreviewTemplate('enpm703', Preview);
CMS.registerPreviewTemplate('enai601-guide', ({ entry }) => h('article', { className: 'cms-preview' },
  h('div', { className: 'prose', dangerouslySetInnerHTML: {
    __html: renderPreview(entry.get('data').get('body') || '', 'editorial-guide'),
  } })));

CMS.registerPreviewStyle('/admin/preview.css');
CMS.registerPreviewStyle('/admin/katex/katex.min.css');
CMS.registerEventListener({
  name: 'preSave',
  handler: ({ entry }) => {
    publishingDraft = CMS.editor.getCurrentEntry();
    const data = entry.get('data');
    if (entry.get('slug') === 'enai601-guide') { pendingPublication = undefined; return data; }
    const now = new Date().toISOString();
    pendingPublication = { slug: entry.get('slug').replace(/\/index$/, ''), timestamp: now,
      field: entry.get('newRecord') ? 'publishedAt' : 'updatedAt' };
    // Unknown historical publication times stay unknown.
    return entry.get('newRecord')
      ? data.set('publishedAt', now).delete('updatedAt')
      : data.set('updatedAt', now);
  },
});
CMS.registerEventListener({
  name: 'postSave',
  handler: ({ entry }) => {
    if (publishingDraft) drafts.published(publishingDraft).catch(() => {});
    if (!pendingPublication) {
      publication.stop();
      showPublicationStatus('편집 지침을 GitHub에 저장했습니다. 이후 작업은 수정된 지침 파일을 기준으로 진행합니다.', true);
      return;
    }
    publication.start({ ...pendingPublication, slug: entry?.get('slug')?.replace(/\/index$/, '') || pendingPublication.slug });
  },
});
CMS.init();
