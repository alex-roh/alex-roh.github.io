import test from 'node:test';
import assert from 'node:assert/strict';
import { appendImage, createDraftController, draftKey, imageMarkdown, uploadPublicPath } from '../cms/drafts.mjs';
import { registerWritingTools } from '../cms/writing-tools.mjs';
import { renderPreview } from '../cms/preview.mjs';
import { config } from '../cms/config.mjs';
import { patchDecap } from '../cms/vendor-patches.mjs';
import { readFile } from 'node:fs/promises';

function fixture() {
  const records = new Map();
  const store = {
    async get(key) { return structuredClone(records.get(key)); },
    async put(key, value) { records.set(key, structuredClone(value)); },
    async delete(key) { records.delete(key); },
  };
  let current = { collection: 'python', slug: 'example/index', newRecord: false,
    fields: [{ name: 'title', widget: 'string' }, { name: 'body', widget: 'markdown' },
      { name: 'tags', widget: 'list' }, { name: 'series', widget: 'hidden' }],
    data: { title: 'Draft title', body: 'Unsaved text', tags: ['python'], series: 'Python' } };
  const editor = {
    getCurrentEntry: () => structuredClone(current),
    applyFieldPatch(patches) {
      for (const patch of patches) current.data[patch.path] = patch.value;
      return { applied: patches.map(patch => patch.path), rejected: [] };
    },
  };
  return { store, editor, records, current, setCurrent(entry) { current = entry; } };
}

test('manual drafts keep all fields and image bytes across a new editor session, separately per entry', async () => {
  const f = fixture();
  const controller = createDraftController(f.editor, f.store);
  const asset = { path: 'astro-site/public/uploads/plot.png', publicPath: '/uploads/plot.png',
    file: new Blob(['image bytes'], { type: 'image/png' }) };
  controller.remember(f.current, asset);
  await controller.save();
  const other = { ...f.current, collection: 'enai601' };
  f.setCurrent(other);
  assert.equal(await controller.get(), undefined);
  f.setCurrent(f.current);
  f.current.data = { title: 'Published title', body: 'Published text', tags: [], series: 'Keep hidden metadata' };
  const reloaded = createDraftController(f.editor, f.store);
  let uploaded = 0;
  await reloaded.restore(async file => { uploaded++; assert.equal(await file.text(), 'image bytes'); return asset; });
  assert.equal(uploaded, 1);
  assert.equal(f.current.data.title, 'Draft title');
  assert.equal(f.current.data.body, 'Unsaved text');
  assert.deepEqual(f.current.data.tags, ['python']);
  assert.equal(f.current.data.series, 'Keep hidden metadata');
});

test('failed writes and failed image restoration do not report success or replace text', async () => {
  const f = fixture();
  const controller = createDraftController(f.editor, f.store);
  controller.remember(f.current, { path: 'astro-site/public/uploads/x.png', file: new Blob(['x']) });
  await controller.save();
  f.current.data.body = 'Current editing';
  const reopened = createDraftController(f.editor, f.store);
  await assert.rejects(reopened.restore(async () => { throw Error('Upload failed'); }), /Upload failed/);
  assert.equal(f.current.data.body, 'Current editing');
  await assert.rejects(createDraftController(f.editor, { get: f.store.get, put: async () => { throw Error('Quota exceeded'); } }).save(), /Quota/);
  assert.ok(await controller.get());
});

test('publication clears only its matching draft, retaining drafts with different content', async () => {
  const f = fixture();
  const controller = createDraftController(f.editor, f.store);
  await controller.save();
  const published = structuredClone(f.current);
  f.current.data.body = 'A newer draft';
  await controller.save();
  await controller.published(published);
  assert.equal((await controller.get()).data.body, 'A newer draft');
  await controller.published(f.current);
  assert.equal(await controller.get(), undefined);
  assert.notEqual(draftKey(f.current), draftKey({ ...f.current, newRecord: true }));
});

test('each entry retains three selectable drafts and migrates its existing single draft', async () => {
  const f = fixture();
  await f.store.put(draftKey(f.current), { data: structuredClone(f.current.data), savedAt: '2026-10-24T00:00:00Z', assets: [] });
  const controller = createDraftController(f.editor, f.store);
  const legacy = await controller.get();
  assert.match(legacy.id, /^legacy:/);
  const saved = [];
  for (let i = 1; i <= 3; i++) {
    f.current.data.title = `Draft ${i}`;
    saved.push(await controller.save());
  }
  const history = await controller.list();
  assert.deepEqual(history.map(draft => draft.data.title), ['Draft 3', 'Draft 2', 'Draft 1']);
  await controller.restore(async () => {}, saved[0].id);
  assert.equal(f.current.data.title, 'Draft 1');
  await assert.rejects(controller.restore(async () => {}, legacy.id), /임시저장이 없습니다/);
  assert.equal((await controller.list()).length, 3);
});

test('image paths accept actual entry-folder uploads and collections explicitly override Decap defaults', () => {
  assert.equal(uploadPublicPath('astro-site/contents/posts/python/sample/actual.png'), '/media/sample/actual.png');
  assert.equal(uploadPublicPath('/astro-site/public/uploads/actual.png'), '/uploads/actual.png');
  assert.equal(uploadPublicPath('astro-site/public/uploads/actual.png'), '/uploads/actual.png');
  assert.throws(() => uploadPublicPath('unrelated/file.png'), /저장 경로/);
  for (const collection of config.collections.filter(collection => collection.folder)) {
    assert.equal(collection.media_folder, '/astro-site/public/uploads');
    assert.equal(collection.public_folder, '/uploads');
  }
});

test('the pinned vendor renders one direct publish action and no standalone media button', async () => {
  const original = await readFile('node_modules/decap-cms/dist/decap-cms.js', 'utf8');
  const patched = patchDecap(original);
  assert.ok(patched.includes('showMediaButton:!1,controlMedia:'));
  const method = patched.match(/renderNewEntrySimplePublishControls=[\s\S]*?(?=renderSimpleDeployPreviewControls=)/)[0];
  assert.doesNotMatch(method, /dropdown|Duplicate|AndNew/);
  const jsx = original.match(/renderNewEntrySimplePublishControls=[\s\S]*?renderButton:\(\)=>(\w+)\(/)[1];
  let publications = 0;
  const props = { onPersist: () => publications++, isPersisting: false, t: text => text };
  const widget = new Function(jsx, 'props', `return new class { constructor(){this.props=props} ${method} }`)
    ((type, props) => ({ type, props }), props);
  const button = widget.renderNewEntrySimplePublishControls();
  assert.equal(button.type, 'button');
  button.props.onClick();
  assert.equal(publications, 1);
  props.isPersisting = true;
  const pending = widget.renderNewEntrySimplePublishControls();
  assert.equal(pending.props.disabled, true);
  pending.props.onClick();
  assert.equal(publications, 1);
  assert.throws(() => patchDecap('unexpected vendor'), /pinned vendor/);
});

test('restore refuses to put one article draft into another article during an upload', async () => {
  const f = fixture();
  const controller = createDraftController(f.editor, f.store);
  controller.remember(f.current, { path: 'astro-site/public/uploads/x.png', file: new Blob(['x']) });
  await controller.save();
  const other = { ...structuredClone(f.current), slug: 'other/index', data: { body: 'Other text' } };
  await assert.rejects(createDraftController(f.editor, f.store).restore(async () => {
    f.setCurrent(other); return { path: 'astro-site/public/uploads/x.png' };
  }), /바뀌었습니다/);
  assert.equal(other.data.body, 'Other text');
});

test('image Markdown preserves the body and safely encodes filenames', () => {
  assert.equal(imageMarkdown('/uploads/figure [1](test).png'), '![figure \\[1\\](test)](/uploads/figure%20%5B1%5D%28test%29.png)');
  assert.equal(appendImage('Existing text', '/uploads/a.png'), 'Existing text\n\n![a](/uploads/a.png)\n');
  assert.equal(appendImage('', '/uploads/a.png'), '![a](/uploads/a.png)\n');
});

test('only sanitized uploaded images resolve to local preview blobs', () => {
  const requested = [];
  const html = renderPreview('![plot](/uploads/plot.png)\n\n<img src="javascript:alert(1)" onerror="alert(1)">', 'sample', path => {
    requested.push(path); return 'blob:https://example.test/image';
  });
  assert.deepEqual(requested, ['/uploads/plot.png']);
  assert.match(html, /src="blob:https:\/\/example.test\/image"/);
  assert.doesNotMatch(html, /javascript:|onerror/);
});

test('writing tools use the CMS media pipeline and remount Slate after insertion and restore', async () => {
  const f = fixture();
  const h = (type, props, ...children) => ({ type, props: { ...props, children } });
  class Markdown {
    constructor(props) { this.props = props; this.state = { mode: 'raw' }; }
    setState(change) { Object.assign(this.state, typeof change === 'function' ? change(this.state) : change); }
    handleMode(mode) { this.setState({ mode }); }
    render() { return h('native-markdown', { value: this.props.value }); }
  }
  let WritingControl;
  const CMS = { editor: f.editor, getWidget: () => ({ control: Markdown }),
    registerWidget(name, control) { assert.equal(name, 'markdown'); WritingControl = control; } };
  const previousWindow = globalThis.window;
  globalThis.window = { confirm: () => true };
  try {
    registerWritingTools(CMS, h, f.store);
    const control = new WritingControl({ value: f.current.data.body,
      field: {}, onChange(value) { f.current.data.body = value; control.props.value = value; },
      onPersistMedia: async file => ({ payload: { path: 'astro-site/contents/posts/python/example/actual.png', file } }),
    });
    control.componentDidMount();
    await control.uploadFiles([new File(['png'], 'Original.PNG', { type: 'image/png' })]);
    assert.deepEqual(control.state.images, ['/media/example/actual.png']);
    assert.equal(control.state.mode, 'raw');
    const tree = control.render();
    const walk = node => node && typeof node === 'object' ? [node, ...[node.props?.children || []].flat(Infinity).flatMap(walk)] : [];
    const insert = walk(tree).find(node => node.type === 'button' && node.props.children[0] === '본문 끝에 넣기');
    insert.props.onClick();
    assert.match(f.current.data.body, /!\[actual\]\(\/media\/example\/actual.png\)/);
    assert.equal(control.state.revision, 1);
    await control.saveDraft();
    f.current.data.body = control.props.value = 'Changed again';
    await control.restoreDraft();
    assert.match(f.current.data.body, /!\[actual\]/);
    assert.equal(control.state.revision, 2);
    const richText = walk(control.render()).find(node => node.type === 'button' && node.props.children[0] === '리치 텍스트');
    assert.equal(richText.props['aria-pressed'], false);
    richText.props.onClick();
    const modeButtons = walk(control.render()).filter(node => node.type === 'button' && Object.hasOwn(node.props, 'aria-pressed'));
    assert.deepEqual(modeButtons.map(button => button.props['aria-pressed']), [false, true]);
    control.componentWillUnmount();
  } finally { globalThis.window = previousWindow; }
});
