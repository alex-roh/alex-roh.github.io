import { href } from '../lib/posts';
import { site } from '../site';
export function GET() {
 return new Response(`User-agent: *\n${import.meta.env.BASE_URL === '/' ? 'Allow: /' : `Disallow: ${import.meta.env.BASE_URL}`}\nSitemap: ${new URL(href('sitemap-index.xml'),site.url)}\n`);
}
