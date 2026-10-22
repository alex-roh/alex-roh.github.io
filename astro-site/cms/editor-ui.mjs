import { themeIcons } from '../src/lib/theme-icons.mjs';
import { mapScroll } from './scroll-map.mjs';

let disposePreview;
const themeKey = 'cave-theme';
const syncKey = 'cave-editor-scroll-sync';
function stored(key) { try { return localStorage.getItem(key); } catch { return null; } }
function save(key, value) { try { localStorage.setItem(key, value); } catch {} }
function theme() {
  const choice = stored(themeKey);
  return choice === 'light' || choice === 'dark' ? choice
    : matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
}
function applyTheme() { document.documentElement.dataset.theme = theme(); }

export function initializeEditor() {
  applyTheme();
  if (!stored('cms.md-mode')) save('cms.md-mode', 'raw');
  // The built-in ratio sync misses iframe document scroll events in this layout.
  // Use one source-aware synchronizer, avoiding two controllers fighting each other.
  save('cms.scroll-sync-enabled', 'false');
  addEventListener('storage', event => { if (event.key === themeKey) applyTheme(); });
  matchMedia('(prefers-color-scheme: dark)').addEventListener('change', applyTheme);
  const themeButton = document.createElement('button');
  themeButton.id = 'cave-editor-theme';
  themeButton.type = 'button';
  themeButton.className = 'theme-toggle';
  themeButton.innerHTML = themeIcons;
  const updateLabel = () => {
    const dark = document.documentElement.dataset.theme === 'dark';
    themeButton.setAttribute('aria-pressed', String(dark));
    themeButton.title = themeButton.ariaLabel = dark ? '라이트모드 켜기' : '다크모드 켜기';
  };
  themeButton.addEventListener('click', () => {
    save(themeKey, document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark');
    applyTheme();
  });
  new MutationObserver(updateLabel).observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });
  updateLabel();
  const brand = document.createElement('a');
  brand.id = 'cave-editor-brand';
  brand.href = '/admin/#/';
  brand.setAttribute('aria-label', 'Cave 관리자 메인');
  const wordmark = document.createElement('strong');
  wordmark.append('Cave');
  const dot = document.createElement('span');
  dot.textContent = '.';
  wordmark.append(dot);
  const label = document.createElement('span');
  label.className = 'cave-admin-label';
  label.textContent = 'Admin';
  brand.append(wordmark, label);
  document.body.append(brand, themeButton);
}

export function attachPreview(article) {
  disposePreview?.();
  disposePreview = undefined;
  if (!article) return;
  const previewDoc = article.ownerDocument;
  const previewWindow = previewDoc.defaultView;
  const pane = document.querySelector('[class*="PreviewPaneContainer-ControlPaneContainer"]');
  const editable = pane?.querySelector('[data-slate-editor="true"]');
  const controls = document.querySelector('[class*="ViewControls"]');
  if (!pane || !editable || !controls) return;
  let enabled = stored(syncKey) !== 'false';
  let leader = pane;
  let points = [];
  let frame;
  let layoutFrame;
  const syncButton = document.createElement('button');
  syncButton.className = 'cave-scroll-sync';
  syncButton.type = 'button';
  syncButton.textContent = '↕';
  const label = () => {
    syncButton.setAttribute('aria-pressed', String(enabled));
    syncButton.title = syncButton.ariaLabel = enabled ? '스크롤 동기화 켜짐 · 끄기' : '스크롤 동기화 꺼짐 · 켜기';
  };
  const scroller = () => previewDoc.scrollingElement;
  function measure() {
    const preview = scroller();
    if (!preview) return;
    const sourceMax = Math.max(0, pane.scrollHeight - pane.clientHeight);
    const previewMax = Math.max(0, preview.scrollHeight - previewWindow.innerHeight);
    const paneTop = pane.getBoundingClientRect().top;
    const lines = [...editable.children];
    const candidates = [[0, 0]];
    // Rich Text has no one-to-one Markdown lines: use proportional sync there.
    const blocks = editable.closest('[class*="RawEditorContainer"]') ? article.querySelectorAll('[data-source-line]') : [];
    for (const element of blocks) {
      const first = Number(element.dataset.sourceLine) - 1;
      const last = Number(element.dataset.sourceEnd) - 1;
      const rect = element.getBoundingClientRect();
      const start = lines[first];
      const end = lines[last];
      if (start) candidates.push([start.getBoundingClientRect().top - paneTop + pane.scrollTop, rect.top + preview.scrollTop]);
      if (end && last > first) candidates.push([end.getBoundingClientRect().bottom - paneTop + pane.scrollTop, rect.bottom + preview.scrollTop]);
    }
    candidates.sort((a, b) => a[0] - b[0]);
    points = [[0, 0]];
    for (const point of candidates) {
      const previous = points.at(-1);
      if (point[0] > previous[0] && point[1] > previous[1] && point[0] < sourceMax && point[1] < previewMax) points.push(point);
    }
    points.push([sourceMax, previewMax]);
  }
  function sync() {
    frame = undefined;
    if (!enabled) return;
    const preview = scroller();
    if (!preview) return;
    if (leader === pane) previewWindow.scrollTo({ top: mapScroll(pane.scrollTop, points), behavior: 'instant' });
    else pane.scrollTop = mapScroll(preview.scrollTop, points, 1);
  }
  function onSourceScroll() { if (leader === pane && !frame) frame = requestAnimationFrame(sync); }
  function onPreviewScroll() { if (leader !== pane && !frame) frame = requestAnimationFrame(sync); }
  const leadSource = () => { leader = pane; };
  const leadPreview = () => { leader = previewDoc; };
  function updateLayout() {
    cancelAnimationFrame(layoutFrame);
    layoutFrame = requestAnimationFrame(measure);
  }
  syncButton.addEventListener('click', () => {
    enabled = !enabled;
    save(syncKey, String(enabled));
    label();
    measure();
    sync();
  });
  label();
  controls.append(syncButton);
  const updateTheme = () => { previewDoc.documentElement.dataset.theme = document.documentElement.dataset.theme; };
  updateTheme();
  const themeObserver = new MutationObserver(updateTheme);
  themeObserver.observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });
  const contentObserver = new MutationObserver(updateLayout);
  contentObserver.observe(article, { childList: true, subtree: true, characterData: true });
  contentObserver.observe(editable, { childList: true, subtree: true, characterData: true });
  const sourceObserver = new MutationObserver(() => {
    if (!editable.isConnected && article.isConnected) attachPreview(article);
  });
  sourceObserver.observe(pane, { childList: true, subtree: true });
  const sizes = new ResizeObserver(updateLayout);
  sizes.observe(article);
  sizes.observe(editable);
  sizes.observe(pane);
  for (const event of ['wheel', 'pointerdown', 'touchstart', 'keydown']) {
    pane.addEventListener(event, leadSource, { passive: true, capture: true });
    previewDoc.addEventListener(event, leadPreview, { passive: true, capture: true });
  }
  pane.addEventListener('scroll', onSourceScroll, { passive: true });
  previewDoc.addEventListener('scroll', onPreviewScroll, { passive: true, capture: true });
  previewWindow.addEventListener('resize', updateLayout);
  previewDoc.fonts?.ready.then(updateLayout);
  updateLayout();
  disposePreview = () => {
    cancelAnimationFrame(frame);
    cancelAnimationFrame(layoutFrame);
    themeObserver.disconnect(); contentObserver.disconnect(); sourceObserver.disconnect(); sizes.disconnect();
    syncButton.remove();
    for (const event of ['wheel', 'pointerdown', 'touchstart', 'keydown']) {
      pane.removeEventListener(event, leadSource, true);
      previewDoc.removeEventListener(event, leadPreview, true);
    }
    pane.removeEventListener('scroll', onSourceScroll);
    previewDoc.removeEventListener('scroll', onPreviewScroll, true);
    previewWindow.removeEventListener('resize', updateLayout);
  };
}
