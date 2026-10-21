const display = value => value.normalize('NFKC').replace(/\s+/g, ' ').trim();
export const normalize = value => display(value).toLocaleLowerCase();

function snippet(body, needle, fallback) {
  const text = display(body);
  const offset = normalize(text).indexOf(needle);
  if (offset < 0) return fallback;
  const start = Math.max(0, offset - 55);
  const end = Math.min(text.length, Math.max(start + 180, offset + needle.length));
  return `${start ? '…' : ''}${text.slice(start, end)}${end < text.length ? '…' : ''}`;
}

function sectionUrl(url, anchor, query) {
  const separator = url.includes('?') ? '&' : '?';
  return `${url}${separator}search=${encodeURIComponent(query)}#${encodeURIComponent(anchor)}`;
}

export function searchPosts(posts, query) {
  const needle = normalize(query);
  if (!needle) return [];
  return posts.map(post => {
    const titleMatch = normalize(post.title).includes(needle);
    const matches = (post.sections || []).map(section => {
      const headingMatch = normalize(section.heading).includes(needle);
      const bodyMatch = normalize(section.body).includes(needle);
      return {...section, score: headingMatch ? 2 : bodyMatch ? 1 : 0,
        url: sectionUrl(post.url, section.anchor, query.trim()),
        snippet: snippet(section.body, needle, section.body.slice(0,180)),
      };
    }).filter(section => section.score).sort((a,b) => b.score-a.score);
    // Legacy indexes remain searchable during a cached-index deployment transition.
    const body = post.body || '';
    const legacyMatch = !post.sections && normalize(body).includes(needle);
    const score = titleMatch ? 3 : matches.length ? matches[0].score : legacyMatch ? 1 : 0;
    return {...post, postUrl:post.url, url:matches[0]?.url || post.url, matches, score,
      snippet:matches[0]?.snippet || snippet(body, needle, post.description)};
  }).filter(post => post.score > 0).sort((a,b) => b.score-a.score);
}
