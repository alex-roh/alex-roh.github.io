export interface SearchSection { heading: string; anchor: string; body: string; }
export interface SearchPost { title: string; url: string; body?: string; description: string; sections?: SearchSection[]; }
export interface SearchHit extends SearchSection { url: string; score: number; snippet: string; }
export function normalize(value: string): string;
export function searchPosts(posts: SearchPost[], query: string): (SearchPost & {postUrl:string; matches:SearchHit[]; score:number; snippet:string})[];
