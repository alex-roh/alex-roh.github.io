import { normalize } from './search.mjs';

// Search links reveal matching folded content; ordinary TOC/hash links are untouched.
export function revealSearchTarget(root, hash, query) {
  if (!query || !hash) return null;
  let id;
  try { id = decodeURIComponent(hash.slice(1)); } catch { return null; }
  const target = root.ownerDocument.getElementById(id);
  if (!target || !root.contains(target)) return null;
  for (let parent=target.parentElement; parent && root.contains(parent); parent=parent.parentElement) {
    if (parent.tagName === 'DETAILS') parent.open = true;
  }
  const depth = /^H[1-6]$/.test(target.tagName) ? Number(target.tagName[1]) : 0;
  const follows = (a,b) => Boolean(a.compareDocumentPosition(b) & 4);
  const end = depth ? [...root.querySelectorAll('h1,h2,h3,h4,h5,h6')]
    .find(h => follows(target,h) && Number(h.tagName[1]) <= depth) : undefined;
  for (const details of root.querySelectorAll('details')) {
    if ((target === root || follows(target,details)) && (!end || follows(details,end)) && normalize(details.textContent || '').includes(normalize(query))) {
      details.open = true;
    }
  }
  target.setAttribute('tabindex','-1');
  target.focus({preventScroll:true});
  target.scrollIntoView({block:'start',behavior:'instant'});
  return target;
}
