import { getCollection, type CollectionEntry } from 'astro:content';
export type Post = CollectionEntry<'posts'>;
import { href } from './urls';
export { href } from './urls';
export const groupSlug = (name: string) => name.replace(/\s/g, '-');
export const postHref = (post: Post) => href(`${post.id}/`);
// Display names can change while existing series bookmarks keep working.
const stableSeriesSlugs: Record<string, string> = {
  'ENAI601 Numerical Methods': 'ENAI601',
  'ENAI607 Python Programming': 'ENAI607-Python',
  'ENPM703 Deep Learning': 'ENPM703',
};
export const seriesSlug = (name: string) => stableSeriesSlugs[name] ?? groupSlug(name);
export const seriesHref = (name: string) => href(`series/${encodeURIComponent(seriesSlug(name))}/`);
export const tagHref = (name: string) => href(`tags/${encodeURIComponent(name)}/`);
export const publicationDate = (post: Post) => post.data.publishedAt ? new Date(post.data.publishedAt) : post.data.date;
export const dateValue = (post: Post) => publicationDate(post)?.getTime() ?? -Infinity;
export async function allPosts() {
  return (await getCollection('posts')).sort((a,b) => dateValue(b)-dateValue(a) || a.id.localeCompare(b.id));
}
export function seriesPosts(posts: Post[], name: string) {
  return posts.filter(p => p.data.series === name).sort((a,b) =>
    (b.data.seriesOrder ?? -Infinity)-(a.data.seriesOrder ?? -Infinity) ||
    b.data.title.localeCompare(a.data.title, 'ko', { numeric: true }));
}
export function formatDate(date?: Date) {
  return date ? new Intl.DateTimeFormat('ko-KR', { year:'numeric', month:'long', day:'numeric', timeZone:'UTC' }).format(date) : '';
}
export function excerpt(post: Post) {
  return post.data.description || (post.body || '').replace(/```[\s\S]*?```/g,' ').replace(/!?(?:\[([^\]]*)\])\([^)]*\)/g,'$1').replace(/<[^>]*>/g,' ').replace(/[#*`>|]/g,'').trim().slice(0,150);
}
