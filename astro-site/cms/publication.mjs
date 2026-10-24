export function deployedSlug(expected, deployment) {
  const posts = deployment?.posts || {};
  if (expected.slug) {
    const timestamp = Date.parse(posts[expected.slug]?.[expected.field]);
    return timestamp >= Date.parse(expected.timestamp) ? expected.slug : null;
  }
  return Object.keys(posts).find(slug => Date.parse(posts[slug][expected.field]) === Date.parse(expected.timestamp)) || null;
}

// Confirm the version actually served by the blog, rather than equating a Git
// commit or even a completed build with a live publication.
export function createPublicationMonitor({ fetch, storage, onStatus, now = Date.now,
  setTimer = setTimeout, clearTimer = clearTimeout }) {
  const key = 'cave-pending-publication';
  let generation = 0;
  let timer;
  function stop() { generation++; clearTimer(timer); }
  function write(value) { try { value ? storage.setItem(key, JSON.stringify(value)) : storage.removeItem(key); } catch {} }
  function start(expected) {
    stop();
    const current = generation;
    const publication = { ...expected, startedAt: expected.startedAt || now() };
    write(publication);
    async function check() {
      const elapsed = Math.max(0, now() - publication.startedAt);
      onStatus({ phase: elapsed >= 180000 ? 'delayed' : 'deploying', expected: publication, elapsed });
      try {
        const response = await fetch(`/deployment.json?v=${now()}`, { cache: 'no-store', signal: AbortSignal.timeout(15000) });
        const deployment = response.ok ? await response.json() : null;
        if (current !== generation) return;
        const slug = deployedSlug(publication, deployment);
        if (slug) {
          write(null);
          onStatus({ phase: 'live', expected: publication, slug, elapsed });
          return;
        }
      } catch { /* A transient fetch failure never means publication succeeded. */ }
      if (current === generation) timer = setTimer(check, elapsed >= 180000 ? 15000 : 5000);
    }
    void check();
  }
  return {
    start, stop,
    resume() {
      try {
        const saved = JSON.parse(storage.getItem(key));
        if (saved?.timestamp && ['publishedAt', 'updatedAt'].includes(saved.field)) start(saved);
      } catch {}
    },
  };
}
