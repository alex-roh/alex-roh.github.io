import { visit } from 'unist-util-visit';
import path from 'node:path';
export function localAssets() {
  return (tree, file) => {
    const slug = path.basename(path.dirname(file.path));
    const base = (process.env.SITE_BASE || '').replace(/\/$/, '');
    visit(tree, node => {
      if ((node.type === 'image' || node.type === 'link') && node.url && !/^(?:[a-z]+:|\/|#)/i.test(node.url)) {
        node.url = `${base}/media/${slug}/${node.url}`;
      }
    });
  };
}
