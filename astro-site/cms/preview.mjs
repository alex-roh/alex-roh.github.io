import { unified } from 'unified';
import remarkParse from 'remark-parse';
import remarkGfm from 'remark-gfm';
import remarkMath from 'remark-math';
import remarkRehype from 'remark-rehype';
import rehypeRaw from 'rehype-raw';
import rehypeSanitize from 'rehype-sanitize';
import rehypeKatex from 'rehype-katex';
import rehypeStringify from 'rehype-stringify';
import { visit } from 'unist-util-visit';

// Sanitize before KaTeX so its own MathML and sizing classes survive.
export function renderPreview(markdown, slug, getAsset) {
  const processor = unified().use(remarkParse).use(remarkGfm).use(remarkMath)
    .use(() => tree => visit(tree, node => {
      if ((node.type === 'image' || node.type === 'link') && node.url && !/^(?:[a-z]+:|\/|#)/i.test(node.url)) {
        node.url = `/media/${encodeURIComponent(slug)}/${node.url}`;
      }
    }))
    .use(remarkRehype, { allowDangerousHtml: true }).use(rehypeRaw)
    .use(rehypeSanitize)
    .use(() => tree => {
      if (getAsset) visit(tree, 'element', node => {
        const src = node.properties?.src;
        if (node.tagName === 'img' && typeof src === 'string' && src.startsWith('/uploads/')) {
          // Resolve only sanitized upload URLs, never arbitrary author-supplied HTML.
          let path = src;
          try { path = decodeURI(src); } catch { /* A literal percent is a valid filename. */ }
          const asset = String(getAsset(path) || src);
          if (/^(?:blob:|https?:|\/)/.test(asset)) node.properties.src = asset;
        }
      });
      for (const node of tree.children) {
        if (node.type === 'element' && node.position) {
          node.properties ||= {};
          node.properties['data-source-line'] = node.position.start.line;
          node.properties['data-source-end'] = node.position.end.line;
        }
      }
    }).use(rehypeKatex, { strict: 'ignore', throwOnError: false })
    .use(rehypeStringify);
  return String(processor.processSync(markdown));
}
