import { createMarkdownProcessor } from '@astrojs/markdown-remark';
import remarkMath from 'remark-math';

// Build-only extraction. Anchor IDs come from the same Astro render as the article,
// so punctuation, Korean headings and duplicate headings cannot drift apart.
export async function buildSearchSections(markdown, headings) {
  const sections = [{ body: '' }];
  let current = sections[0];
  const collect = () => tree => {
    function walk(node) {
      if (node.type === 'element' && /^h[1-6]$/.test(node.tagName)) {
        current = { body: '' }; sections.push(current);
        return; // Heading text is supplied by Astro, not duplicated in snippets.
      }
      if (node.type === 'text') current.body += node.value;
      else if (node.children) {
        for (const child of node.children) walk(child);
        if (node.type === 'element' && !['a','strong','em','code','span','del'].includes(node.tagName)) current.body += '\n';
      }
    }
    walk(tree);
  };
  const processor = await createMarkdownProcessor({syntaxHighlight:false, remarkPlugins:[remarkMath], rehypePlugins:[collect]});
  await processor.render(markdown);
  if (sections.length !== headings.length + 1) throw new Error('Search/article heading count mismatch');
  return sections.map((section, i) => ({
    heading: i ? headings[i-1].text : '글 도입부',
    anchor: i ? headings[i-1].slug : 'article-body',
    body: section.body.replace(/\s+/g, ' ').trim(),
  })).filter(section => section.body || section.anchor !== 'article-body');
}
