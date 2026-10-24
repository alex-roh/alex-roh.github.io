// IndexedDB keeps image Blobs alongside the text, without localStorage's small quota.
export function draftKey(entry) {
  return entry ? `${entry.collection}:${entry.newRecord ? 'new' : entry.slug}` : null;
}

export function editablePatches(entry, data) {
  return entry.fields.filter(field => field.widget !== 'hidden' && Object.hasOwn(data, field.name))
    .map(field => ({ path: field.name, value: data[field.name] }));
}

export function createDraftStore(indexedDB) {
  let connection;
  async function database() {
    connection ??= new Promise((resolve, reject) => {
      const request = indexedDB.open('cave-editor-drafts', 1);
      request.onupgradeneeded = () => request.result.createObjectStore('drafts');
      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
    }).catch(error => { connection = undefined; throw error; });
    return connection;
  }
  async function run(mode, operation) {
    const db = await database();
    return new Promise((resolve, reject) => {
      const transaction = db.transaction('drafts', mode);
      const request = operation(transaction.objectStore('drafts'));
      transaction.oncomplete = () => resolve(request.result);
      transaction.onerror = transaction.onabort = () => reject(transaction.error || new Error('Draft storage failed'));
    });
  }
  return {
    get: key => run('readonly', store => store.get(key)),
    put: (key, value) => run('readwrite', store => store.put(value, key)),
    delete: key => run('readwrite', store => store.delete(key)),
  };
}

export function createDraftController(editor, store) {
  const assets = new Map();
  return {
    remember(entry, asset) {
      const key = draftKey(entry);
      const files = assets.get(key) || new Map();
      files.set(asset.path, asset);
      assets.set(key, files);
    },
    async get() {
      const entry = editor.getCurrentEntry();
      return entry ? store.get(draftKey(entry)) : undefined;
    },
    async save() {
      const entry = editor.getCurrentEntry();
      if (!entry) throw new Error('편집 중인 글이 없습니다.');
      const key = draftKey(entry);
      const previous = await store.get(key);
      const files = new Map((previous?.assets || []).map(asset => [asset.path, asset]));
      for (const [path, asset] of assets.get(key) || []) files.set(path, asset);
      const draft = { data: entry.data, savedAt: new Date().toISOString(), assets: [...files.values()] };
      await store.put(key, draft);
      return draft;
    },
    async restore(upload) {
      const entry = editor.getCurrentEntry();
      if (!entry) throw new Error('편집 중인 글이 없습니다.');
      const key = draftKey(entry);
      const draft = await store.get(key);
      if (!draft) throw new Error('이 글의 임시저장이 없습니다.');
      for (const asset of draft.assets) {
        if (draftKey(editor.getCurrentEntry()) !== key) throw new Error('편집 중인 글이 바뀌었습니다.');
        const restored = assets.get(key)?.get(asset.path) || await upload(asset.file);
        if (restored.path !== asset.path) throw new Error('이미지 경로가 달라 복원을 중단했습니다.');
        this.remember(entry, restored);
      }
      if (draftKey(editor.getCurrentEntry()) !== key) throw new Error('편집 중인 글이 바뀌었습니다.');
      const result = editor.applyFieldPatch(editablePatches(entry, draft.data));
      if (result.rejected.length) throw new Error('일부 항목을 불러오지 못했습니다. 임시저장은 보관되어 있습니다.');
      return draft;
    },
    async published(entry) {
      const key = draftKey(entry);
      const draft = await store.get(key);
      // A draft saved with different content must not be discarded by a later publication.
      if (draft && editablePatches(entry, draft.data).every(patch =>
        JSON.stringify(entry.data[patch.path]) === JSON.stringify(patch.value))) await store.delete(key);
      assets.delete(key);
    },
  };
}

export function imageMarkdown(path) {
  const name = path.split('/').at(-1);
  const alt = name.replace(/\.[^.]+$/, '').replace(/[\\[\]]/g, '\\$&');
  const url = path.split('/').map(segment => encodeURIComponent(segment)
    .replace(/[!'()*]/g, character => `%${character.charCodeAt(0).toString(16).toUpperCase()}`)).join('/');
  return `![${alt}](${url})`;
}

export function appendImage(body, path) {
  return `${body || ''}${body ? '\n\n' : ''}${imageMarkdown(path)}\n`;
}
