import test from 'node:test';
import assert from 'node:assert/strict';
import { createPublicationMonitor, deployedSlug } from '../cms/publication.mjs';
import { renderPreview } from '../cms/preview.mjs';

const expected = { slug: 'sample', field: 'updatedAt', timestamp: '2026-10-24T05:00:00Z' };
const tick = () => new Promise(resolve => setImmediate(resolve));

test('only the live blog version confirms publication, including a newer superseding edit', () => {
  assert.equal(deployedSlug(expected, { posts: { sample: { updatedAt: '2026-10-24T04:00:00Z' } } }), null);
  assert.equal(deployedSlug(expected, { posts: { sample: { updatedAt: expected.timestamp } } }), 'sample');
  assert.equal(deployedSlug(expected, { posts: { sample: { updatedAt: '2026-10-24T05:00:01Z' } } }), 'sample');
  assert.equal(deployedSlug(expected, { posts: { another: { updatedAt: expected.timestamp } } }), null);
  assert.equal(deployedSlug({ ...expected, slug: '' }, { posts: { new: { updatedAt: expected.timestamp } } }), 'new');
});

test('deployment monitoring survives reload, keeps checking after three minutes, and finishes only on live data', async () => {
  const saved = new Map();
  const storage = { getItem: key => saved.get(key), setItem: (key, value) => saved.set(key, value), removeItem: key => saved.delete(key) };
  let callback;
  let time = 1000;
  let live = false;
  const states = [];
  const options = { storage, now: () => time, onStatus: state => states.push(state.phase),
    setTimer: fn => { callback = fn; }, clearTimer: () => { callback = null; },
    fetch: async () => ({ ok: true, json: async () => ({ posts: live ? { sample: { updatedAt: expected.timestamp } } : {} }) }) };
  const first = createPublicationMonitor(options);
  first.start(expected);
  await tick();
  assert.deepEqual(states, ['deploying']);
  assert.equal(saved.size, 1);
  first.stop();
  time += 181000;
  const resumed = createPublicationMonitor(options);
  resumed.resume();
  await tick();
  assert.equal(states.at(-1), 'delayed');
  assert.equal(typeof callback, 'function');
  live = true;
  await callback();
  assert.equal(states.at(-1), 'live');
  assert.equal(saved.size, 0);
});

test('a stale response for a previous save cannot claim the newest save is live', async () => {
  const responses = [];
  const states = [];
  const monitor = createPublicationMonitor({
    fetch: () => new Promise(resolve => responses.push(resolve)),
    storage: null, onStatus: state => states.push(state), setTimer: () => {}, clearTimer: () => {},
  });
  monitor.start(expected);
  monitor.start({ ...expected, timestamp: '2026-10-24T05:01:00Z' });
  responses[0]({ ok: true, json: async () => ({ posts: { sample: { updatedAt: expected.timestamp } } }) });
  await tick();
  assert.equal(states.some(state => state.phase === 'live'), false);
  responses[1]({ ok: false });
  await tick();
  assert.equal(states.some(state => state.phase === 'live'), false);
  monitor.stop();
});

test('short article-local image links preview unpublished blobs without changing published image links', () => {
  const proxy = { fileObj: new Blob(['png']), toString: () => 'blob:https://example.test/draft' };
  const html = renderPreview('![](figure.png)', 'sample', path => { assert.equal(path, 'figure.png'); return proxy; });
  assert.match(html, /src="blob:https:\/\/example.test\/draft"/);
  const published = renderPreview('![](figure.png)', 'sample', () => ({ toString: () => 'temporary-placeholder.svg' }));
  assert.match(published, /src="\/media\/sample\/figure.png"/);
});
