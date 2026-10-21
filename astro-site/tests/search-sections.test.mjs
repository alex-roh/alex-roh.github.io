import {test} from 'node:test';
import assert from 'node:assert/strict';
import {buildSearchSections} from '../src/lib/search-sections.mjs';
import {searchPosts} from '../src/lib/search.mjs';

test('extract code and folded content without treating fenced # as a heading',async()=>{
 const source='Introduction.\n\n## `strip()` 사용\n\nA **bold** 설명.\n\n```python\n# not a heading\nfields[1:]\n```\n\n<details>\n<summary>답</summary>\n\nHidden InvalidDataError.\n\n</details>\n\n## 다시\n\nNext.';
 const sections=await buildSearchSections(source,[{depth:2,text:'strip() 사용',slug:'real-anchor'},{depth:2,text:'다시',slug:'duplicate-1'}]);
 assert.equal(sections.length,3);
 assert.equal(sections[1].anchor,'real-anchor');
 assert.ok(sections[1].body.includes('A bold 설명.'));
 assert.ok(sections[1].body.includes('# not a heading'));
 assert.ok(sections[1].body.includes('fields[1:]'));
 assert.ok(sections[1].body.includes('Hidden InvalidDataError.'));
 assert.ok(!sections[1].body.includes('<details>'));
 assert.equal(sections[2].anchor,'duplicate-1');
});

test('reject mismatched headings rather than publish broken anchors',async()=>{
 await assert.rejects(buildSearchSections('## heading\n\nbody',[]),/heading count mismatch/);
});

const post={title:'Python 노트',url:'/preview/note/',description:'노트',sections:[
 {heading:'글 도입부',anchor:'article-body',body:'A starting paragraph.'},
 {heading:'정리 방법',anchor:'정리-방법',body:'Use InvalidDataError with fields[1:].'},
 {heading:'InvalidDataError 해설',anchor:'errors-1',body:'A detailed explanation.'},
]};

test('rank section headings first and link to the matching real anchor',()=>{
 const result=searchPosts([post],'invaliddataerror')[0];
 assert.equal(result.matches.length,2);
 assert.equal(result.url,'/preview/note/?search=invaliddataerror#errors-1');
 assert.equal(result.matches[1].url,'/preview/note/?search=invaliddataerror#'+encodeURIComponent('정리-방법'));
 assert.ok(result.matches[1].snippet.includes('InvalidDataError'));
});

test('exact code punctuation is preserved in query and snippet',()=>{
 const result=searchPosts([post],'fields[1:]')[0];
 assert.equal(new URL(result.url,'https://example.invalid').searchParams.get('search'),'fields[1:]');
 assert.ok(result.snippet.includes('fields[1:]'));
});

test('title-only matches still lead to the post rather than a guessed section',()=>{
 const result=searchPosts([post],'Python')[0];
 assert.equal(result.url,post.url);
 assert.equal(result.matches.length,0);
 assert.equal(result.snippet,'노트');
});

test('intro matches link to article body and Korean normalization works',()=>{
 assert.ok(searchPosts([post],'starting')[0].url.endsWith('#article-body'));
 assert.ok(searchPosts([post],'정리'.normalize('NFD'))[0].matches[0].heading.includes('정리'));
});

test('empty and unknown section query has no matches',()=>{
 assert.deepEqual(searchPosts([post],'  '),[]);
 assert.deepEqual(searchPosts([post],'no-such-token'),[]);
});
