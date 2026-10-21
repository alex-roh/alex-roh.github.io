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
export function renderPreview(markdown, slug) {
  const processor = unified().use(remarkParse).use(remarkGfm).use(remarkMath)
    .use(() => tree => visit(tree, node => {
      if ((node.type === 'image' || node.type === 'link') && node.url && !/^(?:[a-z]+:|\/|#)/i.test(node.url)) {
        node.url = `/media/${encodeURIComponent(slug)}/${node.url}`;
      }
    }))
    .use(remarkRehype, { allowDangerousHtml: true }).use(rehypeRaw)
    .use(rehypeSanitize)
    .use(() => tree => {
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
