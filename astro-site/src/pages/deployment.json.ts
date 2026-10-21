import { allPosts } from '../lib/posts';

export async function GET() {
  const posts = await allPosts();
  return new Response(JSON.stringify({
    builtAt: new Date().toISOString(),
    posts: Object.fromEntries(posts.map(post => [post.id, {
      publishedAt: post.data.publishedAt ?? null,
      updatedAt: post.data.updatedAt ?? null,
    }])),
  }), { headers: { 'Content-Type': 'application/json' } });
}
