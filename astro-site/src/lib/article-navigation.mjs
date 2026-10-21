export function activeHeadingIndex(tops, atEnd, threshold = 160) {
  if (!tops.length) return -1;
  if (atEnd) return tops.length - 1;
  let active = 0;
  tops.forEach((top, i) => { if (top <= threshold) active = i; });
  return active;
}

// Move only the inner list. scrollIntoView can also move the article itself.
export function revealOffset(scrollTop, viewportTop, viewportHeight, itemTop, itemBottom, padding = 12) {
  if (itemTop < viewportTop + padding) return Math.max(0, scrollTop + itemTop - viewportTop - padding);
  if (itemBottom > viewportTop + viewportHeight - padding) return scrollTop + itemBottom - viewportTop - viewportHeight + padding;
  return scrollTop;
}

export function keepItemVisible(container, item) {
  if (!container || !item || !container.clientHeight) return;
  const box = container.getBoundingClientRect();
  const target = item.getBoundingClientRect();
  container.scrollTop = revealOffset(container.scrollTop, box.top + container.clientTop, container.clientHeight, target.top, target.bottom);
}
