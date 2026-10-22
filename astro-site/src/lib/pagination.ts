import type { Post } from './posts';
export const POSTS_PER_PAGE = 10;
export interface PostPage { posts: Post[]; currentPage: number; totalPages: number; total: number; }
export function postPages(posts: Post[]): PostPage[] {
  const totalPages = Math.max(1, Math.ceil(posts.length / POSTS_PER_PAGE));
  return Array.from({ length: totalPages }, (_, index) => ({
    posts: posts.slice(index * POSTS_PER_PAGE, (index + 1) * POSTS_PER_PAGE),
    currentPage: index + 1, totalPages, total: posts.length,
  }));
}
