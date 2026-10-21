export const publicationTimeZone = 'America/New_York';
export function formatPublicationTime(value) {
  const date = new Date(value);
  const local = new Intl.DateTimeFormat('ko-KR', {
    year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit',
    hourCycle: 'h23', timeZone: publicationTimeZone,
  }).format(date);
  const zone = new Intl.DateTimeFormat('en-US', { timeZone: publicationTimeZone, timeZoneName: 'short' })
    .formatToParts(date).find(part => part.type === 'timeZoneName')?.value;
  return `${local} ${zone}`;
}

// YAML timestamps saved by CMS editors can arrive as Date objects.
export function normalizeTimestampInput(value) {
  return value instanceof Date && !Number.isNaN(value.getTime()) ? value.toISOString() : value;
}
