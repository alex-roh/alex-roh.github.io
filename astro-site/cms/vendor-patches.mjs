// The pinned Decap release does not offer a simple-mode publish-button override.
// Patch only these two render methods at build time; fail loudly on vendor drift.
export function patchDecap(source) {
  const newEntry = source.match(/renderNewEntrySimplePublishControls=\([\s\S]*?(?=renderSimpleDeployPreviewControls=)/)?.[0];
  const existing = source.match(/renderExistingEntrySimplePublishControls=\([\s\S]*?(?=renderNewEntrySimplePublishControls=)/)?.[0];
  const jsx = newEntry?.match(/renderButton:\(\)=>(\w+)\(/)?.[1];
  if (!jsx || !existing || !source.includes('showMediaButton:!0,controlMedia:')) {
    throw new Error('Decap editor customization no longer matches the pinned vendor. Review before upgrading.');
  }
  source = source.replace(newEntry,
    `renderNewEntrySimplePublishControls=()=>{const{onPersist,isPersisting,t}=this.props;return ${jsx}("button",{type:"button",className:"cave-publish-button",disabled:isPersisting,onClick:()=>{if(!isPersisting)onPersist()},children:t(isPersisting?"editor.editorToolbar.publishing":"editor.editorToolbar.publish")})};`);
  source = source.replace(existing,
    `renderExistingEntrySimplePublishControls=()=>{const{t}=this.props;return ${jsx}("span",{className:"cave-published-label",role:"status",children:window.cavePublicationLabel||t("editor.editorToolbar.published")})};`);
  return source.replace('showMediaButton:!0,controlMedia:', 'showMediaButton:!1,controlMedia:');
}
