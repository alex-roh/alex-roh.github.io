import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import { unified } from '@astrojs/markdown-remark';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import { localAssets } from './src/plugins/local-assets.mjs';

export default defineConfig({
  site: 'https://alex-roh.github.io',
  base: process.env.SITE_BASE || '/',
  trailingSlash: 'always',
  output: 'static',
  integrations: [sitemap()],
  markdown: {
    processor: unified({
      remarkPlugins: [remarkMath, localAssets],
      rehypePlugins: [[rehypeKatex, { strict: 'ignore' }]],
    }),
    shikiConfig: { themes: { light: 'github-light', dark: 'github-dark' }, wrap: false },
  },
});
