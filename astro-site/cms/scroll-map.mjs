// Piecewise mapping keeps the same Markdown block near the top of both panes.
export function mapScroll(position, points, from = 0) {
  const to = 1 - from;
  if (!points.length) return 0;
  if (position <= points[0][from]) return points[0][to];
  for (let i = 1; i < points.length; i++) {
    const a = points[i - 1], b = points[i];
    if (position <= b[from]) {
      const span = b[from] - a[from];
      return span > 0 ? a[to] + (b[to] - a[to]) * (position - a[from]) / span : b[to];
    }
  }
  return points.at(-1)[to];
}
