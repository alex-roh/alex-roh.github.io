import { render } from 'astro:content';
import { allPosts, postHref, excerpt } from '../lib/posts';
import { buildSearchSections } from '../lib/search-sections.mjs';
export async function GET() {
 const posts = await allPosts();
 const index = await Promise.all(posts.map(async p => {
  const { headings } = await render(p);
  return {title:p.data.title, url:postHref(p), description:excerpt(p),
   sections:await buildSearchSections(p.body || '', headings)};
 }));
 return new Response(JSON.stringify(index), {headers:{'Content-Type':'application/json; charset=utf-8'}});
}
