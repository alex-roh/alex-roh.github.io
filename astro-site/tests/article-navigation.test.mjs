import test from 'node:test';
import assert from 'node:assert/strict';
import { activeHeadingIndex, revealOffset } from '../src/lib/article-navigation.mjs';

test('reading down and back up selects the corresponding heading', () => {
  assert.equal(activeHeadingIndex([-900, -100, 700], false), 1);
  assert.equal(activeHeadingIndex([-50, 750, 1550], false), 0);
  assert.equal(activeHeadingIndex([], true), -1);
});
test('the final section activates at the page bottom even if its heading cannot reach the threshold', () => {
  assert.equal(activeHeadingIndex([-500, 300], true), 1);
  assert.equal(activeHeadingIndex([-500, 300], false), 0);
});
test('an overflowing TOC follows in both directions and leaves visible links still', () => {
  assert.equal(revealOffset(0, 35, 500, 900, 940), 417);
  assert.equal(revealOffset(417, 35, 500, -100, -60), 270);
  assert.equal(revealOffset(417, 35, 500, 100, 140), 417);
  assert.equal(revealOffset(5, 35, 500, 10, 40), 0);
});
