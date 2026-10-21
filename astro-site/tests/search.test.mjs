import { test } from 'node:test';
import assert from 'node:assert/strict';
import { searchPosts } from '../src/lib/search.mjs';
const posts=[
 {title:'Python 예외 처리',body:'사용자 정의 오류 InvalidDataError와 fields[1:]를 사용한다.',url:'/one/',description:'예외'},
 {title:'lambda 정렬',body:'예외 처리 후 정렬한다.',url:'/two/',description:'정렬'},
];
test('Korean title and body search, ranked with title first',()=> {
 assert.deepEqual(searchPosts(posts,'예외 처리').map(p=>p.url),['/one/','/two/']);
});
test('code punctuation and case insensitive search',()=> {
 assert.equal(searchPosts(posts,'fields[1:]')[0].url,'/one/');
 assert.equal(searchPosts(posts,'invaliddataerror')[0].url,'/one/');
});
test('empty or unknown query returns no results',()=> {
 assert.equal(searchPosts(posts,'  ').length,0);
 assert.equal(searchPosts(posts,'does-not-exist').length,0);
});
test('Unicode normalization',()=> {
 assert.equal(searchPosts(posts,'예외'.normalize('NFD'))[0].url,'/one/');
});
