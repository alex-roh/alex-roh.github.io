export const repository = 'alex-roh/alex-roh.github.io';
export const sourceRoot = 'astro-site';
// The deployed Worker URL is set after creating the free Worker.
export const authBaseUrl = 'https://cave-cms-auth.roheunyoung.workers.dev';

const fields = [
  { label: '제목', name: 'title', widget: 'string' },
  { label: '요약', name: 'description', widget: 'text', required: false },
  { label: '태그', name: 'tags', widget: 'list', required: false },
  { label: '시리즈', name: 'series', widget: 'hidden' },
  { label: '시리즈 순서', name: 'seriesOrder', widget: 'number', value_type: 'int', required: false },
  { label: '기존 게시일', name: 'date', widget: 'hidden', required: false },
  { label: '기존 수정일', name: 'update', widget: 'hidden', required: false },
  { label: '최초 게시 시각', name: 'publishedAt', widget: 'hidden', required: false },
  { label: '수정 시각', name: 'updatedAt', widget: 'hidden', required: false },
  { label: '본문', name: 'body', widget: 'markdown', modes: ['raw'], hint: '왼쪽에서 Markdown을 수정하고 오른쪽에서 수식과 본문을 확인하세요. ↕ 버튼으로 양방향 스크롤 동기화를 켜거나 끌 수 있습니다. 게시하면 자동 배포됩니다.' },
];

export const config = {
  backend: {
    name: 'github', repo: repository, branch: 'main',
    base_url: authBaseUrl, auth_endpoint: 'auth',
    commit_messages: { update: 'Edit {{collection}}: {{slug}}', create: 'Publish {{collection}}: {{slug}}' },
  },
  site_url: 'https://alex-roh.github.io', display_url: 'https://alex-roh.github.io',
  locale: 'ko', publish_mode: 'simple',
  media_folder: `${sourceRoot}/public/uploads`, public_folder: '/uploads',
  collections: [
    ['enai601', 'ENAI601 Numerical Methods', 'enai601'],
    ['python', 'ENAI607 Python Programming', 'python'],
  ].map(([name, label, category]) => ({
    name, label, folder: `${sourceRoot}/contents/posts/${category}`,
    create: true, delete: false, extension: 'md', format: 'yaml-frontmatter',
    path: '{{slug}}/index', slug: '{{slug}}', identifier_field: 'title',
    preview_path: '{{dirname}}/',
    // Folder assets may include README.md; only real series articles are entries.
    filter: { field: 'series', value: label },
    fields: fields.map(field => field.name === 'series' ? { ...field, default: label } : field),
  })),
};
