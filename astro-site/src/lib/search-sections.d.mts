import type { SearchSection } from './search.mjs';
export function buildSearchSections(markdown: string, headings: {depth:number; text:string; slug:string}[]): Promise<SearchSection[]>;
