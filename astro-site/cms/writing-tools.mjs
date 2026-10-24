import { appendImage, createDraftController, createDraftStore, draftKey, imageMarkdown } from './drafts.mjs';

export function registerWritingTools(CMS, h, store = createDraftStore(window.indexedDB)) {
  const drafts = createDraftController(CMS.editor, store);
  const markdown = CMS.getWidget('markdown');
  const Markdown = markdown.control;
  class WritingControl extends Markdown {
    constructor(props) {
      super(props);
      this.state = { ...this.state, images: [], message: '', busy: false, savedAt: null, revision: 0 };
      this.entryKey = draftKey(CMS.editor.getCurrentEntry());
    }
    componentDidMount() {
      super.componentDidMount?.();
      this.mounted = true;
      drafts.get().then(draft => {
        if (this.mounted && draft) this.setState({ savedAt: draft.savedAt });
      }).catch(() => this.tell('이 브라우저에서 임시저장 공간을 열 수 없습니다.'));
    }
    componentWillUnmount() { this.mounted = false; }
    tell(message) { if (this.mounted) this.setState({ message }); }
    refreshBody() { if (this.mounted) this.setState(state => ({ revision: state.revision + 1 })); }
    async perform(task) {
      if (this.state.busy) return;
      this.setState({ busy: true, message: '' });
      try { await task(); }
      catch (error) { this.tell(error.message || '작업에 실패했습니다. 다시 시도해 주세요.'); }
      finally { if (this.mounted) this.setState({ busy: false }); }
    }
    async upload(file) {
      if (!this.mounted || draftKey(CMS.editor.getCurrentEntry()) !== this.entryKey) throw new Error('편집 중인 글이 바뀌었습니다.');
      const result = await this.props.onPersistMedia(file, { field: this.props.field });
      const asset = result?.payload;
      if (!asset?.path || !asset.file) throw new Error(`${file.name}: 이미지를 올리지 못했습니다.`);
      // The backend supplies the actual sanitized filename, including any rename.
      if (!asset.path.startsWith('astro-site/public/uploads/')) throw new Error('이미지 저장 경로를 확인할 수 없습니다.');
      return { path: asset.path, file: asset.file, publicPath: asset.path.slice('astro-site/public'.length) };
    }
    async uploadFiles(files) {
      await this.perform(async () => {
        for (const source of files) {
          if (!source.type.startsWith('image/')) throw new Error(`${source.name}: 이미지 파일을 선택해 주세요.`);
          // Unique names prevent a new upload from replacing an existing article's image.
          const dot = source.name.lastIndexOf('.');
          const stem = dot > 0 ? source.name.slice(0, dot) : source.name;
          const extension = dot > 0 ? source.name.slice(dot) : '';
          const file = new File([source], `${stem}-${crypto.randomUUID()}${extension}`, { type: source.type });
          const entry = CMS.editor.getCurrentEntry();
          const asset = await this.upload(file);
          drafts.remember(entry, asset);
          if (this.mounted) this.setState(state => ({ images: [...state.images, asset.publicPath] }));
        }
        this.tell('이미지를 첨부했습니다. 본문 끝에 넣거나 Markdown을 복사하세요. 글을 게시하면 이미지도 함께 반영됩니다.');
      });
    }
    async saveDraft() {
      await this.perform(async () => {
        const draft = await drafts.save();
        if (this.mounted) this.setState({ savedAt: draft.savedAt });
        this.tell('이 브라우저에 임시저장했습니다. 블로그에는 게시되지 않습니다.');
      });
    }
    async restoreDraft() {
      if (!window.confirm('임시저장한 제목·태그·본문 등으로 현재 내용을 바꿀까요?')) return;
      await this.perform(async () => {
        const draft = await drafts.restore(file => this.upload(file));
        if (this.mounted) this.setState({ savedAt: draft.savedAt, images: draft.assets.map(asset => asset.publicPath) });
        this.refreshBody();
        this.tell('임시저장을 불러왔습니다. 내용을 확인한 뒤 게시하세요.');
      });
    }
    render() {
      const { busy, savedAt, images, message } = this.state;
      const editor = super.render();
      const button = (label, onClick, disabled = busy) => h('button', { type: 'button', onClick, disabled }, label);
      return h('div', { className: 'cave-writing-control' },
        h('section', { className: 'cave-writing-tools', 'aria-label': '글 작성 도구' },
          h('div', { className: 'cave-writing-actions' },
            button('이미지 업로드', () => this.fileInput.click()),
            h('input', { type: 'file', accept: 'image/*', multiple: true, hidden: true,
              ref: input => { this.fileInput = input; }, onChange: event => {
                const files = [...event.target.files]; event.target.value = ''; this.uploadFiles(files);
              } }),
            button('임시저장', () => this.saveDraft()),
            button('임시저장 불러오기', () => this.restoreDraft(), busy || !savedAt)),
          h('p', { className: 'cave-draft-note' }, savedAt
            ? `임시저장: ${new Date(savedAt).toLocaleString('ko-KR')} · 이 브라우저에 보관됩니다.`
            : '임시저장은 이 브라우저에 보관됩니다. 게시 전에는 임시저장 버튼을 눌러 주세요.'),
          h('p', { role: 'status', className: 'cave-writing-status' }, busy ? '처리 중…' : message),
          images.length > 0 && h('ul', { className: 'cave-uploaded-images' }, ...images.map(path =>
            h('li', { key: path },
              h('span', {}, path.split('/').at(-1)),
              h('input', { type: 'text', readOnly: true, value: imageMarkdown(path), 'aria-label': '이미지 Markdown',
                onFocus: event => event.target.select() }),
              button('본문 끝에 넣기', () => {
                this.props.onChange(appendImage(this.props.value, path)); this.refreshBody();
              }),
              button('Markdown 복사', () => this.perform(async () => {
                await navigator.clipboard.writeText(imageMarkdown(path)); this.tell('Markdown을 복사했습니다. 본문 원하는 위치에 붙여넣으세요.');
              })))))),
        // Slate takes its initial value only on mount. Refresh after an explicit
        // insert/restore so both modes show the same data that will be published.
        h(editor.type, { ...editor.props, key: this.state.revision }));
    }
  }
  CMS.registerWidget('markdown', WritingControl, markdown.preview, markdown.schema);
  return drafts;
}

export function removeDuplicateActions(phrases) {
  const labels = new Set([phrases.duplicate, phrases.publishAndDuplicate, phrases.published]);
  function update() {
    for (const element of document.querySelectorAll('#nc-root button, #nc-root [role="menuitem"]')) {
      if (labels.has(element.textContent.trim()) && !element.hasAttribute('data-cave-removed')) {
        element.setAttribute('data-cave-removed', '');
      }
    }
  }
  new MutationObserver(update).observe(document.body, { childList: true, subtree: true, characterData: true });
  update();
}
