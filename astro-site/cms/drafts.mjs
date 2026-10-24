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
  const versions = value => (Array.isArray(value) ? value : value ? [value] : [])
    .map(draft => ({ ...draft, id: draft.id || `legacy:${draft.savedAt}` }));
  return {
    remember(entry, asset) {
      const key = draftKey(entry);
      const files = assets.get(key) || new Map();
      files.set(asset.path, asset);
      assets.set(key, files);
    },
    async get() {
      return (await this.list())[0];
    },
    async list() {
      const entry = editor.getCurrentEntry();
      return entry ? versions(await store.get(draftKey(entry))) : [];
    },
    async save() {
      const entry = editor.getCurrentEntry();
      if (!entry) throw new Error('편집 중인 글이 없습니다.');
      const key = draftKey(entry);
      const previous = versions(await store.get(key));
      const files = new Map(previous.flatMap(draft => draft.assets || []).map(asset => [asset.path, asset]));
      for (const [path, asset] of assets.get(key) || []) files.set(path, asset);
      const draft = { id: crypto.randomUUID(), data: entry.data, savedAt: new Date().toISOString(), assets: [...files.values()] };
      await store.put(key, [draft, ...previous].slice(0, 3));
      return draft;
    },
    async restore(upload, id) {
      const entry = editor.getCurrentEntry();
      if (!entry) throw new Error('편집 중인 글이 없습니다.');
      const key = draftKey(entry);
      const history = versions(await store.get(key));
      const draft = id ? history.find(draft => draft.id === id) : history[0];
      if (!draft) throw new Error('이 글의 임시저장이 없습니다.');
      const data = { ...draft.data };
      const restoredAssets = [];
      for (const asset of draft.assets) {
        if (draftKey(editor.getCurrentEntry()) !== key) throw new Error('편집 중인 글이 바뀌었습니다.');
        const restored = assets.get(key)?.get(asset.path) || await upload(asset.file);
        if (restored.path !== asset.path) {
          if (restored.path.split('/').at(-1) !== asset.path.split('/').at(-1) || !asset.publicPath || !restored.publicPath) {
            throw new Error('이미지 경로가 달라 복원을 중단했습니다.');
          }
          // Older browser drafts used /uploads; retain their images when moving
          // them into the article folder and shorten only the Markdown target.
          const oldUrl = imageMarkdown(asset.publicPath).slice(4, -1);
          const newUrl = imageMarkdown(restored.publicPath).slice(4, -1);
          data.body = (data.body || '').replaceAll(`](${oldUrl})`, `](${newUrl})`);
        }
        restoredAssets.push(restored);
        this.remember(entry, restored);
      }
      if (draftKey(editor.getCurrentEntry()) !== key) throw new Error('편집 중인 글이 바뀌었습니다.');
      const result = editor.applyFieldPatch(editablePatches(entry, data));
      if (result.rejected.length) throw new Error('일부 항목을 불러오지 못했습니다. 임시저장은 보관되어 있습니다.');
      return { ...draft, data, assets: restoredAssets };
    },
    async published(entry) {
      const key = draftKey(entry);
      const history = versions(await store.get(key));
      // A draft saved with different content must not be discarded by a later publication.
      const remaining = history.filter(draft => !editablePatches(entry, draft.data).every(patch =>
        JSON.stringify(entry.data[patch.path]) === JSON.stringify(patch.value)));
      if (remaining.length) await store.put(key, remaining);
      else await store.delete(key);
      assets.delete(key);
    },
  };
}

export function uploadPublicPath(path) {
  const normalized = path.replace(/^\/+/, '');
  if (normalized.startsWith('astro-site/public/uploads/')) return normalized.slice('astro-site/public'.length);
  // Accept entry-relative assets returned by older, already-cached CMS config too.
  const match = normalized.match(/^astro-site\/contents\/posts\/[^/]+\/(?:[^/]+\/)?([^/]+)$/);
  if (match) return match[1];
  throw new Error('이미지 저장 경로를 확인할 수 없습니다.');
}

export function imageMarkdown(path) {
  const url = path.split('/').map(segment => encodeURIComponent(segment)
    .replace(/[!'()*]/g, character => `%${character.charCodeAt(0).toString(16).toUpperCase()}`)).join('/');
  return `![](${url})`;
}

export function appendImage(body, path) {
  return `${body || ''}${body ? '\n\n' : ''}${imageMarkdown(path)}\n`;
}
