import test from 'node:test';
import assert from 'node:assert/strict';
import { mapScroll } from '../cms/scroll-map.mjs';

test('source and preview scroll map the same blocks in both directions', () => {
  const points = [[0, 0], [600, 250], [1400, 1800], [2000, 2300]];
  for (const source of [0, 300, 600, 900, 1400, 1900, 2000]) {
    const preview = mapScroll(source, points);
    assert.ok(Math.abs(mapScroll(preview, points, 1) - source) < 0.0001);
  }
  assert.equal(mapScroll(600, points), 250);
  assert.equal(mapScroll(-10, points), 0);
  assert.equal(mapScroll(3000, points), 2300);
  assert.equal(mapScroll(2300, points, 1), 2000);
});

test('short or empty panes do not generate invalid scroll offsets', () => {
  assert.equal(mapScroll(10, []), 0);
  assert.equal(mapScroll(0, [[0, 0], [0, 0]]), 0);
  assert.equal(mapScroll(10, [[0, 0], [500, 0]], 1), 500);
});
