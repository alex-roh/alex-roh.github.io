---
title: "[ENAI607] Lecture 02 — 리스트, 튜플과 문자열 조작"
description: "인덱싱·슬라이싱·얕은 복사·append/extend·comprehension·tuple unpacking·strip/split/join·숫자 변환·f-string을 예제와 출력으로 이해하는 Python 노트"
date: 2026-10-20T04:00:00-04:00
update: 2026-10-20
tags:
  - python
  - ENAI607
series: "ENAI607 Python Programming"
seriesOrder: 2
---

`" sensor_A, 18.5, 21.0\n"`라는 문자열에서 센서 이름과 숫자를 꺼내려면 무엇부터 해야 할까? `split()`만 쓰면 공백이 남고, `float(fields[1:])`를 쓰면 리스트를 숫자 하나로 바꾸려다 오류가 난다. 이런 코드를 이해하려면 **지금 다루는 값이 문자열인지, 리스트인지, 숫자인지**부터 구분해야 한다.

이 글은 리스트·튜플·문자열의 공통 문법부터 시작해 값을 추가하고 지우는 방법, 복사, comprehension, 문자열 정리·분리·결합, f-string 출력까지 설명한다. 각 `python` 코드 블록은 초기값을 포함하므로 **복사해서 하나씩 독립 실행**할 수 있다. 실행하면 오류가 나는 문법 틀은 `text` 블록으로 구분했다.

처음이면 1–10절로 자료형과 슬라이싱을 이해한 뒤 11–18절에서 문자열을 다뤄 보자. 문자열 코드가 급하면 **13절 `strip` → 14절 `split` → 15절 `join` → 18절 종합 예제** 순서로 읽어도 된다. `Ctrl+F`나 블로그 본문 검색에서 함수 이름으로 바로 찾을 수 있다.

<a id="toc"></a>

## 빠른 목차 — 작업과 함수 이름으로 찾기

| 찾는 작업 / 헷갈리는 문법 | 바로가기 |
| --- | --- |
| 핵심 문법 모아 보기 | [0. 바로 찾는 요약표](#quick-reference) |
| `list`, `tuple`, `str` 차이와 mutable | [1. 세 가지 시퀀스](#sequences) |
| `len`, 음수 인덱스, 중첩 리스트 | [2. 인덱싱](#indexing) |
| `[start:stop:step]`, `[::-1]`, 끝값 제외 | [3. 슬라이싱](#slicing) |
| `b = a`, `copy`, 얕은 복사, `deepcopy` | [4. 참조와 복사](#copy) |
| 한 칸 교체 vs 슬라이스 교체 | [5. 리스트 수정](#list-assignment) |
| `append`, `extend`, `insert`, `+`, `+=` | [6. 추가·연결](#list-addition) |
| `pop`, `del`, `remove`, `clear` | [7. 삭제](#list-deletion) |
| `in`, `index`, `count`, `sort`, `sorted` | [8. 조회와 정렬](#list-search-sort) |
| comprehension 기본형과 조건문 위치 | [9. 리스트 comprehension](#comprehension) |
| `(value,)`, 튜플 내부 리스트, unpacking | [10. 튜플](#tuples) |
| 따옴표, 여러 줄, `\n`, `\t`, 경로 | [11. 문자열 기본](#strings) |
| `int`, `float`, `str`, 2진수 변환 | [12. 숫자와 문자열 변환](#conversion) |
| 앞뒤 공백·개행 제거, `strip`, `rstrip` | [13. strip](#strip) |
| 구분자로 분리, `split`, 빈 필드 | [14. split](#split) |
| 문자열 목록을 연결하는 `join` | [15. join](#join) |
| `find`, `in`, `replace`, 대소문자·접두사 | [16. 검색과 변경](#string-methods) |
| `.2f`, `.4e`, `8.1f`, `d`, `b`, `x` | [17. f-string](#formatting) |
| 한 줄 데이터 → 이름·실수 목록 → 보고서 | [18. 종합 예제](#parsing-example) |
| 자주 나는 오류와 고치는 방법 | [19. 오류 검색표](#pitfalls) |
| 직접 풀어 보는 출력 예측·문자열 처리 | [20. 연습과 해설](#practice) |

<a id="quick-reference"></a>

## 0. 바로 찾는 요약표

아래는 실제 초기값이 생략된 문법 요약이다. 실행 예제는 각 절에서 확인한다.

```text
# 시퀀스 공통
len(x)                  # 원소 개수; 문자열이면 코드 포인트 개수
x[0]                    # 첫 원소
x[-1]                   # 마지막 원소
x[1:4]                  # 인덱스 1, 2, 3
x[::2]                  # 0, 2, 4, ...
x[::-1]                 # 역순

# 리스트
b = a                   # 같은 리스트를 가리킴
b = a.copy()            # 새 바깥 리스트; 내부 객체는 공유
a.append(item)          # item 하나를 추가
a.extend(items)         # items에서 원소를 꺼내 하나씩 추가
a.insert(index, item)   # index 앞에 item 하나 삽입
item = a.pop(index)     # 위치로 삭제하고 그 값을 반환
a.remove(value)         # 값으로 첫 일치 항목 삭제
a.sort()                # 원본을 정렬; 반환값 None
b = sorted(a)           # 새 정렬 리스트 반환
[expression for item in iterable if condition]

# 튜플
single = (value,)       # 원소 하나면 쉼표 필수
name, score = record   # 원소를 변수들에 풀어 넣기

# 문자열
s.strip()               # 앞뒤 공백 제거; 내부 공백은 유지
s.split(",")            # 문자열 → 문자열 리스트
",".join(parts)         # 문자열 리스트 → 문자열
float(s)                # 숫자 문자열 하나 → 실수 하나
[float(x) for x in parts] # 문자열 목록의 각 항목을 실수로
s.find("key")           # 처음 위치; 없으면 -1
s.replace("old", "new") # 바꾼 새 문자열 반환
f"{value:.2f}"          # 소수점 아래 두 자리로 표시
```

<a id="sequences"></a>

## 1. list·tuple·str — 순서가 있는 시퀀스

시퀀스(sequence)는 **원소에 순서가 있고 인덱스로 접근하는 자료형**이다. 여기서 순서가 있다는 말은 자동 정렬된다는 뜻이 아니다. `[30, 10, 20]`도 입력한 순서가 유지되는 리스트다. 인덱스는 0부터 시작하며 Python은 끝에서 세는 음수 인덱스도 지원한다.

| 자료형 | 생성 예 | 원소 종류 | 생성 후 원소 교체·추가·삭제 |
| --- | --- | --- | --- |
| 리스트 `list` | `[10, 20, 30]` | 서로 다른 타입도 가능 | 가능: mutable |
| 튜플 `tuple` | `(10, 20, 30)` | 서로 다른 타입도 가능 | 튜플 자체는 불가능: immutable |
| 문자열 `str` | `"Python"` | Unicode 문자 | 불가능: immutable |

리스트·튜플에는 객체 자체를 안에 복제해 넣는 것이 아니라 **객체를 가리키는 참조**가 저장된다. 이 때문에 같은 내부 리스트를 공유하는 일이 생긴다. 4절에서 실제 변경 결과로 확인한다.

```python
numbers = [10, 20, 30]
mixed = [3, 0.125, "Apple"]
record = ("sensor_A", 21.5)
text = "Python"
empty = []
print(len(numbers), len(record), len(text), len(empty))
# 3 2 6 0
print(mixed[2])  # Apple
```

빈 리스트 `[]`, 빈 튜플 `()`, 빈 문자열 `""`는 모두 길이가 0이고 조건식에서 거짓으로 취급된다. `" "`는 공백 한 글자가 있으므로 길이가 1이고 참이다.

<a id="indexing"></a>

## 2. 인덱싱 — 원소 하나를 꺼내기

```python
names = ["Alice", "Bob", "Carol", "David", "Eve"]
print(names[0])   # Alice
print(names[2])   # Carol
print(names[-1])  # Eve
print(names[-2])  # David
print(names[-5])  # Alice
```

| 값 | Alice | Bob | Carol | David | Eve |
| --- | --- | --- | --- | --- | --- |
| 양수 인덱스 | `0` | `1` | `2` | `3` | `4` |
| 음수 인덱스 | `-5` | `-4` | `-3` | `-2` | `-1` |

길이가 5면 마지막 양수 인덱스는 `4`다. `names[5]` 또는 `names[-6]`은 `IndexError`가 난다. `names[-1]`도 빈 리스트에서는 오류가 난다.

### 2.1 중첩 리스트와 대괄호 두 개

```python
w = [3, 2, ["a", "b", "c"], 1]
print(w[2])     # ['a', 'b', 'c']
print(w[2][1])  # b
print(len(w))   # 4: 내부 리스트도 바깥에서는 원소 하나
print(len(w[2])) # 3
```

`w[2][1]`은 먼저 `w[2]`를 꺼내고, 그 결과인 `['a', 'b', 'c']`에서 인덱스 1을 꺼낸다. 일반 중첩 리스트에서는 `w[2, 1]`로 쓰지 않는다. NumPy의 2차원 배열 인덱싱과 구분한다.

<a id="slicing"></a>

## 3. 슬라이싱 — 구간과 간격 고르기

```text
sequence[start:stop:step]
         시작  끝   간격
```

**시작은 포함하고 끝은 제외한다.** `x[1:4]`는 1, 2, 3번 원소를 선택하며 4번 원소는 선택하지 않는다. 기본 간격은 `1`이다.

```python
x = [0, 1, 2, 3, 4]
print(x[1:3])    # [1, 2]
print(x[:2])     # [0, 1]
print(x[2:])     # [2, 3, 4]
print(x[:])      # [0, 1, 2, 3, 4]
print(x[-3:-1])  # [2, 3]
print(x[::2])    # [0, 2, 4]
print(x[1::2])   # [1, 3]
print(x[1:100])  # [1, 2, 3, 4]: 슬라이스 경계는 범위에 맞춰짐
print(x[3:1])    # []: 양의 간격으로는 3에서 1까지 갈 수 없음
```

`x[2]`는 원소 하나를 꺼내므로 여기서는 `int`다. `x[2:3]`은 길이가 1이어도 리스트다. **`fields[1]`과 `fields[1:]`도 타입이 다르다.** 숫자 변환에서 자주 틀리는 지점이다.

### 3.1 음수 간격과 역순

```python
x = [0, 1, 2, 3, 4]
print(x[::-1])   # [4, 3, 2, 1, 0]
print(x[4:0:-1]) # [4, 3, 2, 1]: stop=0은 포함하지 않음
print(x[4::-2])  # [4, 2, 0]
print(x[3::-2])  # [3, 1]
print(x[4:-1:-1]) # []
```

`x[4:-1:-1]`에서 명시한 `-1`은 마지막 원소의 위치인 4로 해석된다. 시작과 끝이 같아서 비어 있다. **전체 역순은 끝 경계를 직접 적지 않은 `x[::-1]`을 쓰면 된다.** 간격 `0`은 허용되지 않으며 `ValueError`가 난다.

문자열과 튜플도 같은 슬라이싱 문법을 쓴다. 결과는 각각 문자열과 튜플이다.

```python
text = "Python"
record = (10, 20, 30, 40)
print(text[1:4])   # yth
print(text[::-1])  # nohtyP
print(record[1:3]) # (20, 30)
```

<a id="copy"></a>

## 4. `b = a`는 복사가 아니다 — 참조·얕은 복사·깊은 복사

### 4.1 같은 리스트를 두 이름으로 가리키기

```python
a = [10, 20, 30]
b = a
b[0] = 99
print(a)       # [99, 20, 30]
print(b is a)  # True
```

`b = a`는 새 리스트를 만들지 않는다. 같은 리스트에 `a`, `b`라는 이름 두 개가 붙는다. `b[0]`을 바꾸면 `a[0]`도 같은 변경을 보게 된다. `is`는 같은 객체인지, `==`는 값이 같은지를 확인한다.

### 4.2 바깥 리스트만 새로 만드는 얕은 복사

```python
a = [10, 20, 30]
b = a.copy()  # a[:] 또는 list(a)도 얕은 복사
b[0] = 99
print(a)       # [10, 20, 30]
print(b)       # [99, 20, 30]
print(b is a)  # False
```

하지만 안에 리스트가 들어 있으면 이야기가 다르다.

```python
a = [[1, 2], [3, 4]]
b = a.copy()
b[0].append(9)
print(a)            # [[1, 2, 9], [3, 4]]
print(b)            # [[1, 2, 9], [3, 4]]
print(a is b)       # False: 바깥 리스트는 다름
print(a[0] is b[0]) # True: 내부 리스트는 공유
b[1] = [100]
print(a)            # [[1, 2, 9], [3, 4]]: b의 슬롯 교체는 별개
print(b)            # [[1, 2, 9], [100]]
```

**얕은 복사는 내부 객체까지 독립시키지 않는다.** 중첩된 리스트까지 따로 바꾸고 싶다면 `copy.deepcopy()`가 필요하다.

```python
from copy import deepcopy
a = [[1, 2], [3, 4]]
b = deepcopy(a)
b[0].append(9)
print(a)  # [[1, 2], [3, 4]]
print(b)  # [[1, 2, 9], [3, 4]]
```

### 4.3 `[[0] * 3] * 2`에서 두 행이 함께 바뀌는 이유

```python
wrong = [[0] * 3] * 2
wrong[0][0] = 9
print(wrong) # [[9, 0, 0], [9, 0, 0]]

right = [[0] * 3 for _ in range(2)]
right[0][0] = 9
print(right) # [[9, 0, 0], [0, 0, 0]]
```

첫 코드는 같은 내부 리스트를 두 번 참조한다. 두 번째는 반복할 때마다 내부 리스트를 새로 만든다. `_`는 여기서 반복 횟수만 필요하고 반복 변수의 값은 쓰지 않겠다는 관례다.

<a id="list-assignment"></a>

## 5. 리스트 수정 — 원소 교체와 구간 교체는 다르다

```python
x = [0, 1, 2, 3, 4]
x[1] = -1
x[2] = ["a", "b"]
print(x) # [0, -1, ['a', 'b'], 3, 4]

y = [0, 1, 2, 3, 4]
y[1:3] = ["a", "b", "c"]
print(y) # [0, 'a', 'b', 'c', 3, 4]
```

`x[2] = [...]`는 **슬롯 하나에 리스트 하나를 넣는다.** `y[1:3] = [...]`는 해당 구간의 원소들을 오른쪽 iterable의 원소들로 교체한다. 기본 간격의 슬라이스 대입은 교체 전후 길이가 달라도 되므로 리스트 길이가 늘거나 줄 수 있다.

간격을 지정한 확장 슬라이스 대입은 선택된 칸 수와 새 원소 수가 같아야 한다.

```python
x = [0, 1, 2, 3, 4]
x[::2] = [10, 20, 30]
print(x) # [10, 1, 20, 3, 30]
```

`x[::2] = [10]`처럼 개수를 맞추지 않으면 `ValueError`다.

<a id="list-addition"></a>

## 6. `append`·`extend`·`insert`·`+`·`+=`

| 방법 | 하는 일 | 오른쪽이 `[3, 4]`라면 |
| --- | --- | --- |
| `x.append([3, 4])` | 객체 하나를 맨 뒤에 넣음 | 중첩 리스트 원소 하나 추가 |
| `x.extend([3, 4])` | iterable의 원소를 하나씩 맨 뒤에 넣음 | `3`, `4` 두 원소 추가 |
| `x.insert(1, [3, 4])` | 인덱스 1 앞에 객체 하나 삽입 | 중첩 리스트 원소 하나 삽입 |
| `x + [3, 4]` | 연결한 새 리스트를 반환 | 원본 `x`는 유지 |
| `x += [3, 4]` | 리스트 `x` 자체를 확장 | 원본을 함께 보는 별칭에도 반영 |

```python
a = [1, 2]
b = [1, 2]
c = [1, 2]
a.append([3, 4])
b.extend([3, 4])
c.insert(1, [3, 4])
print(a) # [1, 2, [3, 4]]
print(b) # [1, 2, 3, 4]
print(c) # [1, [3, 4], 2]
```

**`extend`에 숫자 하나를 넣을 수는 없다.** `extend(5)`는 반복할 수 없는 정수라서 `TypeError`다. 숫자 하나면 `append(5)`를 쓴다. 문자열은 반복 가능하므로 `extend("ab")`는 `'a'`, `'b'`를 각각 추가한다.

```python
x = [1]
x.append("ab")
print(x) # [1, 'ab']
y = [1]
y.extend("ab")
print(y) # [1, 'a', 'b']
```

### 6.1 `x = x + ...`와 `x += ...`의 참조 차이

```python
a = [1, 2]
alias = a
a = a + [3]
print(a, alias) # [1, 2, 3] [1, 2]

b = [1, 2]
alias_b = b
b += [3]
print(b, alias_b) # [1, 2, 3] [1, 2, 3]
```

`a + [3]`은 새 리스트를 만들고 `a`가 그것을 가리키게 한다. 리스트의 `+=`는 기존 리스트를 바꾼다. 리스트 `+`의 양쪽은 리스트여야 하지만 `extend()`는 튜플 같은 다른 iterable도 받을 수 있다.

<a id="list-deletion"></a>

## 7. 삭제 — `pop`은 위치, `remove`는 값

```python
x = [10, 20, 30, 20]
last = x.pop()
print(last, x) # 20 [10, 20, 30]
first = x.pop(0)
print(first, x) # 10 [20, 30]
x.remove(20)
print(x) # [30]
```

| 방법 | 기준 | 삭제한 값 반환? | 실패 조건 |
| --- | --- | --- | --- |
| `x.pop()` | 마지막 원소 | 예 | 빈 리스트면 `IndexError` |
| `x.pop(i)` | 인덱스 | 예 | 범위 밖이면 `IndexError` |
| `del x[i]` | 인덱스 | 반환 표현식이 아님 | 범위 밖이면 `IndexError` |
| `del x[a:b]` | 슬라이스 | 반환 표현식이 아님 | 빈 구간이면 변화 없음 |
| `x.remove(value)` | 첫 번째로 같은 값 | 아니오: `None` | 없으면 `ValueError` |
| `x.clear()` | 전체 | 아니오: `None` | 빈 리스트에서도 가능 |

```python
fruits = ["apple", "orange", "pear", "orange"]
fruits.remove("orange")
print(fruits) # ['apple', 'pear', 'orange']: 첫 일치만 삭제

x = [0, 1, 2, 3, 4]
del x[1:3]   # x[1:3] = []도 같은 구간을 삭제
print(x)     # [0, 3, 4]
x.clear()
print(x)     # []
```

`del x`는 리스트를 비우는 것이 아니라 변수 이름 `x`를 지운다. 다른 이름이 그 리스트를 참조하고 있다면 객체는 계속 사용할 수 있다.

<a id="list-search-sort"></a>

## 8. 포함 확인·위치 검색·정렬

```python
fruits = ["apple", "orange", "pear", "orange"]
print("orange" in fruits)     # True
print("banana" not in fruits) # True
print(fruits.index("orange")) # 1: 첫 일치 위치
print(fruits.count("orange")) # 2: 개수
```

리스트의 `in`, `index`, `remove`는 값의 동등성 `==`를 기준으로 찾는다. `index()`는 없으면 `-1`이 아니라 **`ValueError`를 발생시킨다.** 오류를 피하려면 `if value in fruits:`로 먼저 확인할 수 있다.

### 8.1 `sort()`는 원본을 바꾸고 `sorted()`는 새 리스트를 준다

```python
x = [4, 0, 2, 1, 3]
y = sorted(x)
print(x) # [4, 0, 2, 1, 3]
print(y) # [0, 1, 2, 3, 4]
result = x.sort(reverse=True)
print(x)      # [4, 3, 2, 1, 0]
print(result) # None
```

**`x = x.sort()`로 쓰면 `x`에 `None`이 들어간다.** 원본 변경이 목적이면 `x.sort()`만 호출한다. 정렬된 복사본이 필요하면 `x = sorted(x)`를 쓴다.

문자열 숫자를 그대로 정렬하면 사전식 순서이고, 숫자로 변환하면 수치 순서다.

```python
tokens = ["10", "2", "30"]
print(sorted(tokens)) # ['10', '2', '30']
print(sorted([int(token) for token in tokens])) # [2, 10, 30]
print(sorted(tokens, key=int)) # ['2', '10', '30']: 결과 원소는 문자열
```

`key=int`는 정렬 비교에 사용할 값만 정수로 만든다. `[6, 5, "apple"]`처럼 기본적으로 순서를 비교할 수 없는 타입이 섞여 있으면 `sort()`에서 `TypeError`가 난다. `key`와 `lambda`를 이용한 자세한 정렬은 [Lecture 03](/enai607-lecture03/)에서도 다룬다.

<a id="comprehension"></a>

## 9. 리스트 comprehension — 원소마다 계산해서 새 리스트 만들기

```text
[결과식 for 변수 in 반복할_대상]
[결과식 for 변수 in 반복할_대상 if 남길_조건]
```

**먼저 `for`를 읽고, 마지막에 앞쪽 결과식을 계산한다.** `[2 * x for x in range(5)]`는 `x`에 0부터 4까지 차례로 넣고, 매번 `2 * x`를 결과 리스트에 넣는다는 뜻이다. `range(5)`는 0, 1, 2, 3, 4를 제공한다.

```python
doubled = [2 * x for x in range(5)]
print(doubled) # [0, 2, 4, 6, 8]

expanded = []
for x in range(5):
    expanded.append(2 * x)
print(expanded) # [0, 2, 4, 6, 8]: 같은 작업

multiples = [x for x in range(20) if x % 4 == 0]
print(multiples) # [0, 4, 8, 12, 16]
```

### 9.1 뒤의 `if`는 필터, 앞의 `if ... else`는 값 선택

```python
values = [-2, 0, 3]
positive = [x for x in values if x > 0]
clipped = [x if x > 0 else 0 for x in values]
print(positive) # [3]: 조건을 못 맞춘 원소는 빠짐
print(clipped)  # [0, 0, 3]: 원소 수를 유지하며 값 선택
```

### 9.2 숫자 변환도 원소 하나씩 한다

```python
fields = ["sensor_A", "18.5", "21.0"]
values = [float(field) for field in fields[1:]]
print(values) # [18.5, 21.0]
print(type(fields[1]).__name__)  # str
print(type(fields[1:]).__name__) # list
```

`fields[1:]`는 문자열 여러 개를 담은 리스트다. `float()`는 그 리스트 전체를 한 번에 바꾸는 함수가 아니다. **각 원소를 `float(field)`로 바꾸고 바깥 대괄호로 다시 모으는 것**이 comprehension이다.

원소마다 같은 변환을 해서 새 리스트가 필요하면 comprehension이 잘 맞는다. 여러 단계의 처리, 로그 출력, `try/except`, 복잡한 분기가 필요하면 보통 `for`문이 더 읽기 쉽다. `print()`를 반복할 목적으로 comprehension을 쓰면 불필요한 `None` 리스트까지 만들어진다.

<a id="tuples"></a>

## 10. 튜플 — 항목 구성이 고정된 시퀀스

```python
record = ("sensor_A", 21.5)
empty = ()
single = ("alone",)
not_tuple = ("alone")
print(len(record), len(empty), len(single)) # 2 0 1
print(type(single).__name__)    # tuple
print(type(not_tuple).__name__) # str
print(record[0])                # sensor_A
print(record[:1])               # ('sensor_A',)
print((1, 2) + (3, 4))          # (1, 2, 3, 4)
```

**원소 하나짜리 튜플을 만드는 핵심은 쉼표다.** 괄호만으로는 튜플이 되지 않는다. 일반적인 튜플 표현식에서 원소를 묶는 것은 쉼표이며, 빈 튜플은 `()`로 쓴다.

튜플에는 `append`, `extend`, `remove`, `sort`가 없다. `record[0] = "new"`도 `TypeError`다. `t = t + (new_item,)`은 기존 튜플을 바꾸는 것이 아니라 새 튜플을 만들어 이름을 다시 연결한다.

### 10.1 튜플 안의 리스트는 바뀔 수 있다

```python
items = [0, 1, 2]
t = ("a", items, "c")
t[1].append(3)
print(t) # ('a', [0, 1, 2, 3], 'c')
```

튜플이 고정하는 것은 **각 칸에 어떤 객체를 연결했는가**다. 연결된 객체가 리스트라면 그 리스트의 내용까지 불변이 되는 것은 아니다.

리스트는 딕셔너리 key가 될 수 없다. 튜플은 **모든 원소가 hashable일 때만** key가 될 수 있다. `(1, 2)`는 가능하지만 `(1, [2, 3])`은 내부 리스트 때문에 불가능하다. 튜플이 항상 더 빠르다는 식으로 고르기보다, 값의 묶음이 고정되어야 하는지를 기준으로 고른다.

### 10.2 packing·unpacking·값 교환

```python
record = "sensor_A", 21.5 # packing: 튜플 생성
name, average = record   # unpacking: 두 값을 두 변수로
print(name, average)     # sensor_A 21.5

a, b = 1, 2
a, b = b, a
print(a, b) # 2 1

first, *middle, last = [10, 20, 30, 40]
print(first, middle, last) # 10 [20, 30] 40
```

별표 없이 풀어 넣을 때는 변수 개수와 원소 개수가 같아야 한다. `a, b = (1, 2, 3)`은 `ValueError`다. `*middle`은 남은 값들을 **리스트로 받는다.** 한 대입 대상에는 별표 변수를 하나만 둘 수 있다. unpacking은 튜플 외에 리스트와 문자열 등에도 적용된다.

### 10.3 리스트 ↔ 튜플 변환

```python
t = (1, 2, 3)
items = list(t)
items.append(4)
print(items)       # [1, 2, 3, 4]
print(tuple(items)) # (1, 2, 3, 4)
print(t)           # (1, 2, 3)
```

<a id="strings"></a>

## 11. 문자열 — 따옴표·인덱싱·불변성·이스케이프

문자열은 `'...'` 또는 `"..."`로 만든다. 시작과 끝의 따옴표가 맞아야 한다. 다른 종류의 따옴표는 문자열 안에 그대로 넣을 수 있다.

```python
greeting = "Hello"
quote = "It's Python"
dialogue = 'He said "Hello".'
print(quote)     # It's Python
print(dialogue)  # He said "Hello".
print(greeting[1])   # e
print(greeting[1:3]) # el
print(len(greeting)) # 5
```

### 11.1 불변이지만 변수에 새 문자열을 대입할 수는 있다

```python
text = "Hello"
changed = text[:2] + "z" + text[3:]
print(text)    # Hello
print(changed) # Hezlo
text = text[1:3]
print(text)    # el
```

`text[2] = "z"`는 오류다. 위 코드는 새 문자열을 만든다. 변수 `text`에 다른 문자열을 대입하는 것과 기존 문자열 객체의 한 글자를 바꾸는 것은 다르다.

### 11.2 `print()`와 `repr()` — 보이는 개행과 실제 내용

```python
text = """This is
a multiline
string"""
print(text)
# This is
# a multiline
# string
print(repr(text)) # 'This is\na multiline\nstring'
```

`print(text)`는 개행을 실제 줄바꿈으로 출력한다. `repr(text)`는 디버깅할 때 쓸 수 있는 표현으로 `\n`을 보이게 한다. `print()`가 문자열 양끝에 따옴표를 붙여 주는 것은 아니다. 리스트를 출력할 때 내부 문자열에 보이는 따옴표와 구분한다.

| 이스케이프 | 뜻 | 주의 |
| --- | --- | --- |
| `\n` | 줄바꿈 | 문자 `n`과 다름 |
| `\t` | 탭 | 고정 개수의 공백과 동일하지 않음 |
| `\\` | 역슬래시 하나 | Windows 경로에서 자주 사용 |
| `\'`, `\"` | 따옴표 | 같은 따옴표를 문자열 안에 넣을 때 |
| `\b` | 백스페이스 제어 문자 | 문자열에서 이전 문자를 삭제하는 함수가 아님 |

```python
text = "name\tvalue\nA\t21.5"
print(repr(text)) # 'name\tvalue\nA\t21.5'
path = r"C:\Users\Alex\data.txt"
print(path)      # C:\Users\Alex\data.txt
```

`r"..."`는 역슬래시 이스케이프 처리를 대부분 막는 raw string이다. 단, **raw string도 역슬래시 하나로 끝낼 수는 없다.** `r"C:\data\"` 같은 코드는 따옴표 처리가 깨진다. `"C:/data/"`처럼 슬래시를 쓰거나 일반 문자열에서 역슬래시를 이중으로 적는다.

### 11.3 한글과 UTF-8

Python의 `str`는 Unicode 텍스트이고, UTF-8은 텍스트를 바이트로 인코딩하는 방식이다. 문자열 객체 자체가 곧 UTF-8 바이트라는 뜻은 아니다.

```python
text = "안녕"
encoded = text.encode("utf-8")
print(len(text))    # 2
print(len(encoded)) # 6: UTF-8에서는 이 두 글자가 각각 3바이트
print(encoded.decode("utf-8")) # 안녕
```

`len(str)`는 Unicode 코드 포인트 수다. 결합 문자나 일부 이모지는 화면에 한 글자로 보여도 길이가 여러 개일 수 있다. 파일을 읽고 쓸 때의 인코딩은 [Lecture 04](/enai607-lecture04/)에서 다룬다.

<a id="conversion"></a>

## 12. 문자열과 숫자 변환 — `int`·`float`·`str`

```python
print("12" + "3")       # 123: 문자열 연결
print(int("12") + 3)    # 15: 숫자 덧셈
print(float("123.45"))  # 123.45
print(int("101"))       # 101: 기본은 10진수
print(int("101", 2))    # 5: 문자열 101을 2진수로 해석
print(int("ff", 16))    # 255
print(str(123.45))      # 123.45: 반환 타입은 str
print(type(str(123.45)).__name__) # str
```

`int(text, base)`는 문자열을 지정한 진법으로 읽는다. 일반적으로 2–36을 지정하며, `base=0`은 `0b`, `0o`, `0x` 접두사로 진법을 판별한다. `int("101", 2)`를 **10진수 101을 2진수 문자열로 바꾸는 기능으로 혼동하면 안 된다.** 반대 방향의 출력은 f-string의 `:b`를 쓴다.

| 입력 | 결과 또는 오류 | 이유 |
| --- | --- | --- |
| `float(" 21.5 ")` | `21.5` | 숫자 앞뒤 공백은 허용 |
| `float("1e3")` | `1000.0` | 과학적 표기 지원 |
| `int("3.0")` | `ValueError` | 정수 문자열 형식이 아님 |
| `float("")` | `ValueError` | 빈 문자열은 숫자가 아님 |
| `float("1,200")` | `ValueError` | 쉼표를 자동 제거하지 않음 |
| `float(["1", "2"])` | `TypeError` | 리스트 전체를 실수 하나로 바꿀 수 없음 |

`int(float("3.9"))`는 `3`이 된다. 이것은 반올림이 아니라 0 방향으로 소수 부분을 버리는 변환이다. `int(float(...))`를 오류 회피용으로 무조건 쓰면 소수 정보를 잃으므로 요구하는 값이 정수인지 먼저 판단한다.

<a id="strip"></a>

## 13. `strip()` — 앞뒤만 정리한다

**`strip()`은 문자열 양끝의 공백 문자들을 제거한 새 문자열을 반환한다.** 기본 공백 문자에는 스페이스·탭·줄바꿈 등이 들어간다. 문자열 중간 공백은 유지한다.

```python
line = " \t sensor A,  21.5 \n"
clean = line.strip()
print(repr(clean)) # 'sensor A,  21.5'
print(repr(line))  # ' \t sensor A,  21.5 \n': 원본은 그대로
print(repr("   \n".strip())) # ''
```

빈 줄을 무시할 때는 `if not line.strip():`를 쓸 수 있다. 공백만 있는 줄도 빈 줄처럼 처리한다. 반면 빈 문자열 `""`과 원소 하나가 빈 문자열인 리스트 `[""]`는 다르다. `[""]`는 길이가 1이라 참이다.

| 메서드 | 지우는 위치 |
| --- | --- |
| `s.strip()` | 왼쪽과 오른쪽 끝 |
| `s.lstrip()` | 왼쪽 끝 |
| `s.rstrip()` | 오른쪽 끝 |
| `s.rstrip("\r\n")` | 오른쪽 끝의 CR·LF 문자들만 |

### 13.1 `strip(chars)`는 단어를 지우는 함수가 아니다

```python
print("abbaVALUEba".strip("ab")) # VALUE
print("Arthur".lstrip("Art"))   # hur
print("Arthur".removeprefix("Art")) # hur
print("rAtArthur".lstrip("Art")) # hur: r,A,t를 반복해서 제거
print("rAtArthur".removeprefix("Art")) # rAtArthur
```

`strip("ab")`는 양끝에 있는 `'a'` 또는 `'b'`를 반복해서 지운다. 정확히 `"ab"`라는 묶음만 제거하는 것이 아니다. `"Art"`에서도 `'A'`, `'r'`, `'t'`가 개별 제거 대상이며 대소문자를 구분한다. 파일 확장자나 접두어처럼 **정확한 문자열 한 덩어리**를 제거하려면 `removesuffix(".txt")`, `removeprefix("sensor_")`를 쓴다.

<a id="split"></a>

## 14. `split()` — 문자열을 잘라 문자열 리스트로 만든다

```python
line = "sensor_A,18.5,21.0"
fields = line.split(",")
print(fields) # ['sensor_A', '18.5', '21.0']
print(type(fields).__name__) # list
print(type(fields[1]).__name__) # str
```

구분자는 결과에 들어가지 않는다. **숫자처럼 보여도 `split()` 결과의 각 항목은 아직 문자열이다.** `fields[1] + fields[2]`는 문자열 연결이고, 숫자 계산은 `float()` 변환 후에 해야 한다.

### 14.1 `split()`과 `split(" ")`는 다르다

```python
text = "  A   B\tC\n"
print(text.split())    # ['A', 'B', 'C']
print(text.split(" ")) # ['', '', 'A', '', '', 'B\tC\n']
print("".split())      # []
print("".split(","))   # ['']
print("A,,B,".split(",")) # ['A', '', 'B', '']
print("Mississippi".split("ss")) # ['Mi', 'i', 'ippi']
```

인자를 생략하면 연속된 공백 문자들을 하나의 구분 구간으로 취급하고, 앞뒤 공백 때문에 빈 항목을 만들지 않는다. 구분자를 명시하면 그 문자열을 정확히 기준으로 자르고, 연속 구분자나 양끝 구분자는 빈 항목을 만든다. `split("")`는 빈 구분자라서 `ValueError`다.

### 14.2 `line.strip().split(",")`만으로 각 필드의 공백이 없어질까?

```python
line = "  sensor_A , 18.5 , 21.0 \n"
print(line.strip().split(","))
# ['sensor_A ', ' 18.5 ', ' 21.0']
fields = [field.strip() for field in line.split(",")]
print(fields) # ['sensor_A', '18.5', '21.0']
```

첫 코드는 줄 전체의 **맨 앞과 맨 뒤만** 정리한다. 쉼표 안쪽에 있는 공백은 그대로다. 두 번째 코드는 다음 과정을 짧게 쓴 것이다.

```python
line = "  sensor_A , 18.5 , 21.0 \n"
fields = []
for field in line.split(","):
    clean_field = field.strip()
    fields.append(clean_field)
print(fields) # ['sensor_A', '18.5', '21.0']
```

### 14.3 횟수 제한 `maxsplit`, 오른쪽부터 `rsplit`, 줄별 `splitlines`

```python
print("name=value=extra".split("=", 1)) # ['name', 'value=extra']
print("a/b/c".rsplit("/", 1)) # ['a/b', 'c']
print("A\r\nB\nC".splitlines()) # ['A', 'B', 'C']
```

`maxsplit=1`이면 구분자를 최대 한 번 사용한다. 인자 없는 `split()`과 달리 `splitlines()`는 줄 단위로 나눈다. 따옴표 안에 쉼표가 들어갈 수 있는 실제 CSV 형식은 단순 `split(",")`만으로 처리할 수 없다. 그런 입력에는 표준 라이브러리 `csv.reader`를 사용한다.

<a id="join"></a>

## 15. `join()` — 구분자가 문자열들을 연결한다

```text
"구분자".join(문자열을_담은_iterable)
```

**리스트에 호출하는 것이 아니라 연결에 쓸 문자열에 호출한다.** `parts.join(",")`가 아니라 `",".join(parts)`다.

```python
parts = ["My", "name", "is"]
print(" ".join(parts))  # My name is
print("**".join(parts)) # My**name**is
print("".join(parts))   # Mynameis
print(", ".join(["A", "B", "C"])) # A, B, C
print(", ".join([]))   # 빈 문자열이라 빈 줄 출력
```

숫자 리스트는 먼저 각 값을 문자열로 바꿔야 한다.

```python
values = [18.5, 21.0, 23.5]
print(", ".join([str(value) for value in values]))
# 18.5, 21.0, 23.5
print(", ".join([f"{value:.2f}" for value in values]))
# 18.50, 21.00, 23.50
```

`join()`은 원소마다 숫자 변환을 대신 해 주지 않는다. `", ".join([1, 2])`는 `TypeError`다. 또한 `join(split(...))`이 언제나 원래 문자열을 되돌리는 것은 아니다. `split()`로 여러 공백을 합쳐 버렸다면 원래 공백 개수 정보는 사라진다.

<a id="string-methods"></a>

## 16. 문자열 검색과 변경 — `in`·`find`·`replace`

### 16.1 포함 여부와 위치를 구분한다

```python
text = "Hello"
print("ell" in text)     # True
print("xyz" not in text) # True
print(text.find("ell"))  # 1
print(text.find("xyz"))  # -1
print(text.index("ell")) # 1
```

`in`은 존재 여부, `find()`는 첫 위치를 준다. 문자열 `index()`도 위치를 주지만 없으면 `ValueError`다. 리스트에는 `find()`가 없다.

**`if text.find("H"):`로 존재 여부를 검사하면 틀린다.** 첫 위치인 `0`은 거짓이고, 실패 값인 `-1`은 참이기 때문이다. 존재 여부는 `if "H" in text:`로 쓰거나 `find(...) != -1`로 확인한다.

```python
text = "Hello"
print(bool(text.find("H")))   # False: 찾았지만 위치가 0
print(bool(text.find("xyz"))) # True: 못 찾았지만 -1은 참
print("H" in text)            # True
```

### 16.2 문자열 변경 메서드는 새 문자열을 반환한다

```python
text = " A-B-B "
print(repr(text.replace("B", "C")))    # ' A-C-C '
print(repr(text.replace("B", "C", 1))) # ' A-C-B '
print(repr(text))                # ' A-B-B ': 원본은 그대로
text = text.strip().replace("-", "_").lower()
print(text) # a_b_b
```

`replace(old, new, count)`의 `count`를 생략하면 모든 일치 부분을 바꾼다. 공백 하나를 없애는 `replace(" ", "")`는 내부 공백까지 제거하지만 `strip()`은 양끝만 처리한다. 둘은 목적이 다르다.

```python
name = "Sensor_A"
print(name.lower())                 # sensor_a
print(name.upper())                 # SENSOR_A
print(name.startswith("Sensor_"))   # True
print(name.endswith("_A"))          # True
print(name.removeprefix("Sensor_")) # A
print("data.txt".removesuffix(".txt")) # data
```

`startswith()`·`endswith()`는 참/거짓을, `removeprefix()`·`removesuffix()`는 새 문자열을 반환한다. 대소문자를 무시하고 비교하려면 양쪽을 같은 방식으로 정규화한다. 일반 Unicode 텍스트의 대소문자 무시 비교에는 `casefold()`도 사용할 수 있다.

<a id="formatting"></a>

## 17. f-string — 값과 출력 형식 넣기

```text
f"문자열 {표현식:형식지정자} 문자열"
```

앞에 `f`를 붙이면 `{...}` 안의 변수가 값으로 바뀐다. 콜론 `:` 뒤에는 출력 형식을 적는다. 표현식에는 변수뿐 아니라 계산식과 함수 호출도 들어갈 수 있다.

```python
name = "Joe"
age = 23
values = [18.5, 21.0, 23.5]
print(f"Hi, I am {name}, and my age is {age}.")
# Hi, I am Joe, and my age is 23.
print(f"count={len(values)}, average={sum(values) / len(values):.2f}")
# count=3, average=21.00
print("name={name}") # name={name}: f를 빠뜨리면 그대로 나옴
print(f"{{name}} = {name}") # {name} = Joe: 중괄호 자체는 두 번
```

### 17.1 소수점·과학적 표기·정수 진법

| 형식 | 뜻 | 예 |
| --- | --- | --- |
| `.2f` | 고정 소수점, 소수점 아래 2자리 | `21.00` |
| `.4e` | 과학적 표기, 소수점 아래 4자리 | `2.1764e+04` |
| `8.1f` | 최소 전체 너비 8칸, 소수점 아래 1자리 | 앞쪽을 공백으로 채움 |
| `d` | 정수를 10진수로 | `1987` |
| `b` | 정수를 2진수로 | `11111000011` |
| `x` | 정수를 소문자 16진수로 | `7c3` |
| `04d` | 최소 너비 4칸, 앞을 0으로 채움 | `0007` |

```python
n = 1987
x = 21764.32
print(f"{n:d} in binary: {n:b}") # 1987 in binary: 11111000011
print(f"{n:x}")                 # 7c3
print(f"Distance: {x:.4e}")      # Distance: 2.1764e+04
print(repr(f"{x:8.1f}"))        # ' 21764.3'
print(f"{7:04d}")               # 0007
```

`8.1f`는 **소수점 앞에 8자리**가 아니다. 부호와 소수점, 소수 부분을 포함한 전체 표시 너비를 최소 8칸으로 잡는다. `21764.3`은 7글자라 앞에 공백이 한 칸 붙는다. 값이 너비보다 길면 잘라 내지 않고 필요한 만큼 출력한다.

### 17.2 정렬·퍼센트·반올림 표시

```python
name = "A"
print(repr(f"{name:<6}")) # 'A     ': 왼쪽 정렬
print(repr(f"{name:>6}")) # '     A': 오른쪽 정렬
print(repr(f"{name:^5}")) # '  A  ': 가운데 정렬
print(f"{0.875:.1%}")     # 87.5%: 100을 곱해 표시

x = 3.14159
formatted = f"{x:.2f}"
print(formatted, type(formatted).__name__) # 3.14 str
print(x) # 3.14159: 원래 수치는 바뀌지 않음
```

`.2f`는 반올림된 **표시 문자열**을 만든다. 저장된 수치를 바꾸지 않으며, 부동소수점의 이진 표현 때문에 일부 소수의 반올림 결과가 직관과 다를 수 있다. 숫자로 계속 계산하려면 원래 숫자를 쓰고, 보고서에 쓸 때 형식을 적용한다.

<a id="parsing-example"></a>

## 18. 종합 예제 — 문자열 한 줄에서 보고서까지

목표 입력은 쉼표로 구분된 **센서 이름 하나 + 숫자 한 개 이상**이다. 이름은 공백 제거 후 비어 있지 않아야 하고, 숫자 필드는 `float()`로 변환할 수 있어야 한다. 따옴표로 감싼 쉼표를 처리하는 CSV 파서는 아니다.

```text
"  sensor_A , 18.5 , 21.0 , 23.5 \n"   문자열 한 개
               ↓ split(",")
['  sensor_A ', ' 18.5 ', ' 21.0 ', ' 23.5 \n']
               ↓ 각 field.strip()
['sensor_A', '18.5', '21.0', '23.5']    문자열 리스트
               ↓ 첫 항목은 이름, 나머지는 float
name = 'sensor_A'
values = [18.5, 21.0, 23.5]            실수 리스트
               ↓ sum / len, f-string, join
sensor_A: count=3, average=21.00, readings=[18.50, 21.00, 23.50]
```

### 18.1 바로 실행하는 전체 코드

```python
line = "  sensor_A , 18.5 , 21.0 , 23.5 \n"

if not line.strip():
    print("빈 줄: 건너뜀")
else:
    fields = [field.strip() for field in line.split(",")]
    if len(fields) < 2 or not fields[0]:
        print("오류: 센서 이름과 숫자 한 개 이상이 필요함")
    else:
        name = fields[0]
        try:
            values = [float(field) for field in fields[1:]]
        except ValueError:
            print("오류: 숫자로 바꿀 수 없는 필드가 있음")
        else:
            average = sum(values) / len(values)
            readings = ", ".join([f"{value:.2f}" for value in values])
            print(f"{name}: count={len(values)}, average={average:.2f}, "
                  f"readings=[{readings}]")

# sensor_A: count=3, average=21.00, readings=[18.50, 21.00, 23.50]
```

`try` 안에서 문자열을 실수로 바꾸다가 `ValueError`가 나면 `except`를 실행한다. 오류 없이 끝났을 때만 `else`에서 평균을 계산한다. 이 예제는 예외 처리 전체 문법을 외우기 위한 것보다 **문자열 처리 단계에서 결과 타입이 어떻게 바뀌는지** 확인하는 데 초점을 둔다.

### 18.2 왜 이 순서인가?

1. `line.strip()`으로 공백만 있는 줄인지 먼저 검사한다. `"".split(",")`는 `[]`가 아니라 `[""]`이기 때문이다.
2. `split(",")`로 필드를 나눈 후 각 필드에 `strip()`을 적용한다.
3. `len(fields) < 2`이면 숫자가 하나도 없으므로 평균을 계산하지 않는다.
4. `not fields[0]`으로 빈 이름을 거른다. 이름이 실제 사람 이름인지·등록된 센서인지는 별도의 허용 목록이나 이름 규칙으로 검사해야 한다.
5. `fields[1:]`의 각 문자열을 `float(field)`로 바꾼다. 중간에 빈 필드가 있어도 `float("")`에서 오류가 나므로 빠뜨리지 않는다.
6. `join()`에 넣기 전에 각 숫자를 `.2f` 형식의 문자열로 만든다.

`float()`는 `"nan"`, `"inf"`도 받아들인다. 유한한 측정값만 허용하려면 변환 후 `math.isfinite(value)`로 추가 검사해야 한다. 허용 여부는 입력 규칙에 따라 정한다.

같은 센서 이름의 측정값을 딕셔너리에 누적하고 정렬하는 과정은 [Lecture 03](/enai607-lecture03/), 실제 파일에서 줄을 읽고 오류를 집계하는 과정은 [Lecture 04](/enai607-lecture04/)로 이어진다.

종합 예제를 여러 입력으로 실행하고 결과를 확인하는 [다운로드용 연습 코드](sequence_string_practice.py)도 준비했다. 이 파일은 외부 패키지나 입력 파일 없이 실행할 수 있다.

<a id="pitfalls"></a>

## 19. 오류 검색표 — 원인과 수정 방향

| 증상 / 코드 | 원인 | 수정 방향 |
| --- | --- | --- |
| `IndexError: list index out of range` | `x[len(x)]` 접근 또는 빈 리스트의 `x[-1]` | 유효 범위·빈 리스트 확인 |
| `'str' object does not support item assignment` | `s[0] = "A"` | 슬라이싱·연결·`replace`로 새 문자열 생성 |
| `'tuple' object does not support item assignment` | 튜플 칸을 변경 | 새 튜플 생성 또는 리스트로 변환 |
| `float(fields[1:])`의 `TypeError` | 문자열 목록을 실수 하나로 변환 | `[float(x) for x in fields[1:]]` |
| `could not convert string to float` | 빈 필드·오타·단위 문자열 등 | 원본 필드 확인 후 검증·오류 처리 |
| `x = x.append(value)` 후 `None` | 원본 변경 메서드 반환값을 대입 | `x.append(value)`만 호출 |
| `x = x.sort()` 후 `None` | `sort()`도 반환값이 `None` | `x.sort()` 또는 `x = sorted(x)` |
| `x.extend(5)`의 `TypeError` | 정수는 iterable이 아님 | `x.append(5)` |
| `parts.join(",")`의 `AttributeError` | 메서드 호출 주체가 반대 | `",".join(parts)` |
| `join()`의 `expected str instance` | 원소 중 숫자가 있음 | 각 값을 `str()` 또는 f-string으로 변환 |
| `remove`·`index`의 `ValueError` | 해당 값이 없음 | `in`으로 먼저 검사하거나 예외 처리 |
| `if s.find(...)` 조건이 반대로 동작 | 0은 거짓, -1은 참 | `in` 또는 `find(...) != -1` |
| 튜플 unpacking의 `too many/not enough values` | 변수 개수와 원소 개수가 다름 | 개수를 맞추거나 별표 변수 활용 |
| `split()` 후 필드 양끝에 공백 | `split`은 각 필드의 공백을 지우지 않음 | 필드마다 `strip()` 적용 |
| `(value)`가 튜플이 아님 | 원소 하나의 쉼표가 빠짐 | `(value,)` |
| `a.copy()` 후 내부 리스트도 바뀜 | 얕은 복사라 내부 객체 공유 | 필요하면 `deepcopy()` |
| f-string에 `{name}`이 그대로 출력 | 앞의 `f`가 없음 | `f"...{name}..."` |
| `.2f`의 `Unknown format code` | 값이 숫자가 아닌 문자열 | 숫자 변환 후 형식 지정 |

<a id="practice"></a>

## 20. 연습 — 출력부터 예측해 보기

각 질문의 답을 먼저 생각한 뒤 펼쳐 보자. 코드 실행으로 확인할 수 있다.

<details>
<summary>1. x[1:4:2]는 어떤 인덱스를 고를까?</summary>

`x = [0, 1, 2, 3, 4]`라면 인덱스 1, 3을 골라 `[1, 3]`이 된다. 끝 인덱스 4는 제외다.

</details>

<details>
<summary>2. append([3, 4])와 extend([3, 4])의 결과 길이는?</summary>

원래 `x = [1, 2]`라면 `append` 후 길이는 3, `extend` 후 길이는 4다. 전자는 리스트 하나, 후자는 원소 두 개를 추가한다.

</details>

<details>
<summary>3. " A B ".strip()은 "AB"일까?</summary>

아니다. `"A B"`다. 내부 공백은 유지한다. 내부 공백까지 지우려는 요구라면 `replace(" ", "")` 등을 검토한다.

</details>

<details>
<summary>4. "A,,B,".split(",")는 몇 칸일까?</summary>

4칸이다. `['A', '', 'B', '']`가 된다. 빈 숫자 필드를 검사할 때 이 특성이 중요하다.

</details>

<details>
<summary>5. "temp, 18.5, 21.0"에서 숫자 평균을 구하려면?</summary>

```python
line = "temp, 18.5, 21.0"
fields = [field.strip() for field in line.split(",")]
values = [float(field) for field in fields[1:]]
print(sum(values) / len(values)) # 19.75
```

이 입력처럼 값이 유효하고 비어 있지 않다는 전제의 예제다. 일반 입력 검증은 18절을 따른다.

</details>

<details>
<summary>6. ("A", [1, 2])는 불변이며 딕셔너리 key로 쓸 수 있을까?</summary>

튜플의 슬롯 자체는 교체할 수 없지만 내부 리스트에는 `append()`를 할 수 있다. 리스트가 hashable이 아니므로 이 튜플은 딕셔너리 key로 쓸 수 없다.

</details>

<details>
<summary>7. 7을 "0007", 0.25를 "25.0%"로 출력하려면?</summary>

```python
print(f"{7:04d}")    # 0007
print(f"{0.25:.1%}") # 25.0%
```

</details>

<details>
<summary>8. [" 3 ", "", " 5 "]에서 빈 항목을 빼고 정수 리스트를 만들려면?</summary>

```python
tokens = [" 3 ", "", " 5 "]
values = [int(token) for token in tokens if token.strip()]
print(values) # [3, 5]
```

여기서는 **빈 항목을 버리라는 요구**가 있으므로 필터를 쓴다. 센서 데이터에서 빈 필드를 오류로 세라는 요구라면 이 코드는 적절하지 않다. 입력을 조용히 버리지 말고 검증해야 한다.

</details>
