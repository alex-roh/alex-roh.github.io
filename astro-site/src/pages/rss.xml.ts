import rss from '@astrojs/rss';
import { allPosts, postHref, excerpt, publicationDate } from '../lib/posts';
import { site } from '../site';
export async function GET() {
 return rss({title:site.title,description:site.description,site:site.url,items:(await allPosts()).map(p => ({title:p.data.title,pubDate:publicationDate(p),description:excerpt(p),link:postHref(p)}))});
}
