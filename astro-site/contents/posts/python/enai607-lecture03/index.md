---
title: "[ENAI607] Lecture 03 — 딕셔너리, 제어문, 함수와 lambda"
description: "dict·copy·comprehension·if·while·enumerate·range·zip·def·global·lambda·정렬을 예제와 출력으로 찾는 오픈북 노트"
date: 2026-10-20
update: 2026-10-20
tags:
  - python
  - ENAI607
series: "ENAI607 Python Programming"
---

센서 이름마다 측정값을 모으고, 평균을 계산한 다음, 높은 순서대로 정렬하려면 어떤 문법이 필요할까?

이 글은 **딕셔너리, comprehension, 조건문과 반복문, 함수, 스코프, lambda와 정렬**을 처음부터 설명한다. 개념과 실행 예제, 예상 결과를 함께 읽고, 시험 중에는 목차와 함수 이름으로 필요한 코드를 찾을 수 있게 구성했다.

각 `python` 코드 블록은 필요한 초기값과 함수를 포함하므로 개별 실행할 수 있다. 문법 틀과 실행하면 안 되는 코드는 `text` 블록으로 구분했다. 예제는 Python 3.14 기준이다.

**찾는 방법:** 아래 목차를 클릭하거나 `Ctrl+F`로 `items`, `copy`, `enumerate`, `lambda`, `global`, `return` 같은 함수·키워드를 검색한다. 블로그의 검색은 본문도 검색하므로 한국어 설명과 영문 이름을 함께 적었다.

<a id="toc"></a>

## 빠른 목차 — 필요한 코드로 바로 이동

| 찾는 작업 / 헷갈리는 문법 | 바로가기 |
| --- | --- |
| 핵심 문법을 한 화면에서 보기 | [0. 시험 직전 치트시트](#quick-reference) |
| 딕셔너리 생성·조회·추가·수정·삭제 | [1. dict 기본](#dictionary) |
| key로 가능한 타입, 없는 key, `in`, `get` | [key 규칙](#dict-keys) · [조회와 KeyError](#dict-access) · [멤버십](#dict-membership) |
| 같은 센서 이름에 측정값 이어 붙이기 | [덮어쓰기와 extend](#dict-accumulate) |
| `b = a`와 `a.copy()`의 차이 | [2. 별칭·얕은 복사](#copy) |
| `keys()` / `values()` / `items()` 구분 | [3. 딕셔너리 순회와 변환](#dict-iteration) |
| 리스트 comprehension vs 딕셔너리 comprehension | [4. comprehension](#comprehension) |
| comprehension의 `if` vs `if ... else` | [필터링과 값 선택](#comprehension-condition) |
| `if`, `elif`, `else`, 빈 리스트 조건 | [5. 조건문과 truth value](#conditionals) |
| `"HIGH" if avg >= 20 else "LOW"` | [조건 표현식](#conditional-expression) |
| `while`, `break`, `continue`, `pass` | [6. 반복 흐름](#while) |
| 번호 붙이기, `enumerate(start=1)` | [7. for와 enumerate](#for-enumerate) |
| `range()` 끝값·간격·역순 | [range](#range) |
| 두 리스트를 함께 돌기, 길이가 다를 때 | [8. zip](#zip) |
| `def`, `return`, `None`, docstring | [9. 함수 정의와 반환](#functions) |
| 위치 인자·키워드 인자·기본값 | [10. 함수 인자](#arguments) |
| 함수에서 원본 리스트가 바뀌는 이유 | [11. 객체 공유와 타입 검사](#parameter-sharing) |
| 지역·전역 변수, `global`, `UnboundLocalError` | [12. 스코프](#scope) |
| 함수 자체 전달 vs 함수 호출 결과 전달 | [13. 일급 객체](#first-class) |
| `lambda x: x[1]`, `sorted`, `sort`, 내림차순 | [14. lambda와 정렬](#lambda) |
| 센서별 평균·필터·정렬·상태·번호 연결 | [15. 종합 예제](#sensor-example) |
| 틀린 코드와 고치는 방법 비교 | [16. 실수 점검표](#pitfalls) |
| 공식 문서 | [17. 참고 자료](#sources) |

<a id="quick-reference"></a>

## 0. 시험 직전 치트시트

아래는 **문법 틀**이다. 실제 코드에서는 `key`, `value`, `condition` 등을 자기 변수로 바꾼다. 실행 예제는 각 절에 있다.

```text
# dictionary
d = {}                            # 빈 딕셔너리
d[key] = value                    # 추가 또는 덮어쓰기
d[key]                            # 조회; 없으면 KeyError
key in d                          # key의 존재 여부
del d[key]                        # 삭제
d.copy()                          # 얕은 복사
list(d.keys())                    # key 리스트
list(d.values())                  # value 리스트
list(d.items())                   # (key, value) 튜플 리스트

# comprehension
[expression for item in iterable]
[expression for item in iterable if condition]
{key_expr: value_expr for item in iterable}
{key_expr: value_expr for item in iterable if condition}

# control flow
value_if_true if condition else value_if_false
for number, item in enumerate(iterable, start=1):
for key, value in d.items():
for a, b in zip(first, second):
range(start, stop, step)           # stop 제외

# functions and sorting
def func(required, optional=0):
    return result

lambda argument: expression
sorted(d, key=lambda key: d[key], reverse=True)
sorted(d.items(), key=lambda pair: pair[1], reverse=True)
```

> **특히 기억:** `in d`는 key 검사, `items()`는 key/value 쌍, `copy()`는 내부 객체 공유, `range()`는 끝값 제외, `return` 생략 시 `None`, `sort()`의 반환값도 `None`이다.

<a id="dictionary"></a>

## 1. 딕셔너리 dict — key로 value 찾기

딕셔너리는 **key와 value의 대응 관계(mapping)를** 저장한다. key를 알면 대응하는 value를 찾는다. 리스트처럼 위치로 찾는 자료형은 아니다. 해시 테이블을 사용하므로 일반적인 key 조회가 효율적이다.

```python
readings = {
    "Ava": [10, 20, 30],
    "Ben": [5, 15],
}

print(readings["Ava"])  # [10, 20, 30]
print(len(readings))    # 2: 전체 측정값 수가 아니라 key/value 쌍 수
print({})              # {}: 빈 딕셔너리
```

value에는 숫자, 문자열, 리스트, 튜플, 다른 딕셔너리 등을 넣을 수 있다.

> **기억:** 딕셔너리는 **Python 3.7 이상에서 삽입 순서가 보장된다.** 다만 이름순·숫자순으로 자동 정렬되는 것은 아니다. 정렬이 필요하면 명시적으로 `sorted()`를 사용한다. [Python 공식 문서: dict](https://docs.python.org/3.14/library/stdtypes.html#mapping-types-dict)

<a id="dict-keys"></a>

### 1.1 key 규칙 — unique, hashable, immutable

딕셔너리의 key는 **hashable(해시 가능)이어야** 한다. 기본 타입에서는 문자열·숫자·해시 가능한 원소로 이루어진 튜플을 사용할 수 있고, 리스트나 딕셔너리는 사용할 수 없다.

| 타입 | key 사용 | 예 |
| --- | --- | --- |
| `str` | 가능 | `"Ava"` |
| `int`, `float`, `bool` | 가능 | `3`, `2.5`, `True` |
| 원소도 해시 가능한 `tuple` | 가능 | `(1, 2)` |
| `list`, `dict` | 불가 | `[1, 2]`, `{"a": 1}` |
| 내부에 리스트가 든 `tuple` | 불가 | `([1, 2], 3)` |

**같은 key에는 value가 하나만 연결된다.** 같은 key로 다시 저장하면 기존 값이 바뀐다.

```python
data = {"Ava": 10, "Ava": 20}
print(data)  # {'Ava': 20}

# 여러 값을 저장하려면 value를 리스트로 만든다.
data = {"Ava": [10, 20]}
print(data["Ava"])  # [10, 20]
```

**주의:** 딕셔너리 자체는 가변이지만, 모든 value 객체가 가변인 것은 아니다. `{"Ava": 10}`에서 `10`은 불변 정수다. `data["Ava"] = 20`은 정수 10을 변형하는 것이 아니라, key가 가리키는 객체를 교체한다.

<a id="dict-access"></a>

### 1.2 조회 — 대괄호와 KeyError

```python
averages = {"Ava": 24.0, "Ben": 15.0}
print(averages["Ava"])  # 24.0

try:
    print(averages["Cara"])
except KeyError:
    print("없는 센서")  # 없는 센서
```

**`get()`은** key가 없을 때 사용할 기본값을 지정한다.

```python
averages = {"Ava": 24.0}
print(averages.get("Ava"))        # 24.0
print(averages.get("Ben"))        # None
print(averages.get("Ben", 0.0))   # 0.0
print("Ben" in averages)          # False: get은 key를 추가하지 않는다.
```

**0.0을 기본값으로 쓰면 실제 평균 0.0과 센서가 없는 경우를 구분하기 어려울 수 있다.** 필요하면 `in`으로 존재 여부를 따로 확인한다.

### 1.3 추가·수정·삭제 — 대입과 del

```python
data = {"Ava": 10}
data["Ava"] = 20   # 기존 key: 수정
data["Ben"] = 15   # 새 key: 추가
print(data)        # {'Ava': 20, 'Ben': 15}

del data["Ben"]
print(data)        # {'Ava': 20}
```

`del data[없는_key]`도 `KeyError`를 발생시킨다. 추가와 수정은 같은 문법이며, key가 이미 있는지에 따라 결과가 달라진다.

<a id="dict-membership"></a>

### 1.4 in / not in — value가 아니라 key 검사

```python
data = {"Ava": 24.0, "Ben": 15.0}
print("Ava" in data)          # True
print("Cara" not in data)     # True
print(24.0 in data)           # False: key 중에는 24.0이 없다.
print(24.0 in data.values())  # True: value를 검사하려면 values()
```

<a id="dict-accumulate"></a>

### 1.5 같은 이름의 리스트에 값 누적하기

```python
data = {"Ava": [10.0, 20.0]}
name = "Ava"
values = [30.0, 40.0]

if name in data:
    data[name].extend(values)
else:
    data[name] = values

print(data)  # {'Ava': [10.0, 20.0, 30.0, 40.0]}
```

**`data[name] = values`는 교체, `data[name].extend(values)`는 기존 리스트에 원소들을 추가한다.** 누적한 직후 다시 대입하거나 `update()`로 같은 key를 덮으면 누적 결과가 사라진다.

`append(values)`는 리스트 자체를 원소 하나로 넣고, `extend(values)`는 리스트 속 원소들을 넣는다.

```python
a = [10, 20]
b = [10, 20]
a.append([30, 40])
b.extend([30, 40])
print(a)  # [10, 20, [30, 40]]
print(b)  # [10, 20, 30, 40]
```

<a id="copy"></a>

## 2. 복사 — 별칭, shallow copy, 내부 리스트 공유

`b = a`는 딕셔너리를 복제하지 않는다. 두 이름이 **같은 딕셔너리**를 가리킨다.

```python
a = {"Ava": [10, 20]}
b = a
b["Ben"] = [30]
print("Ben" in a)  # True
print(a is b)      # True
```

`a.copy()`는 **바깥 딕셔너리만 새로 만드는 얕은 복사(shallow copy)다**. 안쪽 value 객체는 공유한다.

```python
a = {"Ava": [10, 20], "Ben": 15}
b = a.copy()

print(a is b)                   # False: 바깥 딕셔너리는 다르다.
print(a["Ava"] is b["Ava"])     # True: 내부 리스트는 같다.

b["Ava"].append(30)
print(a["Ava"])                 # [10, 20, 30]: 원본에도 영향

b["Ben"] = 99
print(a["Ben"])                 # 15: b의 key/value 연결만 변경
```

**시험 포인트:** 내부 리스트를 수정하는 것과, 복사본에서 value를 통째로 교체하는 것은 다르다.

내부 리스트까지 독립시키려면 `deepcopy()`를 사용할 수 있다.

```python
from copy import deepcopy

a = {"Ava": [10, 20]}
b = deepcopy(a)
b["Ava"].append(30)
print(a)  # {'Ava': [10, 20]}
print(b)  # {'Ava': [10, 20, 30]}
```

<a id="dict-iteration"></a>

## 3. keys / values / items — 순회와 리스트 변환

| 표현 | 반복할 때 꺼내는 것 | 변수 받는 형태 |
| --- | --- | --- |
| `data` 또는 `data.keys()` | key | `for name in data:` |
| `data.values()` | value | `for value in data.values():` |
| `data.items()` | `(key, value)` 튜플 | `for name, value in data.items():` |

```python
data = {"Ava": 24.0, "Ben": 15.0}

for name in data:
    print(name)
# Ava
# Ben

for average in data.values():
    print(average)
# 24.0
# 15.0

for name, average in data.items():
    print(name, average)
# Ava 24.0
# Ben 15.0
```

`name, average`는 **튜플 언패킹(unpacking)이다**. `("Ava", 24.0)`의 첫 값을 `name`, 둘째 값을 `average`에 나눠 받는다. `(name, average)`처럼 괄호를 써도 된다.

### 3.1 dict → list

`keys()`, `values()`, `items()` 자체는 리스트가 아니라 **뷰(view)다**. 리스트가 필요하면 `list()`로 변환한다.

```python
data = {"Ava": 24.0, "Ben": 15.0}
print(list(data))           # ['Ava', 'Ben']
print(list(data.keys()))    # ['Ava', 'Ben']
print(list(data.values()))  # [24.0, 15.0]
print(list(data.items()))   # [('Ava', 24.0), ('Ben', 15.0)]
```

### 3.2 list of pairs → dict

```python
pairs = [("pi", 3.14), ("e", 2.72)]
constants = dict(pairs)
print(constants)  # {'pi': 3.14, 'e': 2.72}
```

각 원소는 key와 value **두 항목**으로 이루어져야 한다. 또 `dict`, `list`, `sum` 같은 내장 이름을 변수 이름으로 쓰면 해당 함수를 가려 버리므로 `data`, `readings`, `total` 같은 이름을 사용한다.

<a id="comprehension"></a>

## 4. comprehension — 리스트와 딕셔너리 만들기

### 4.1 기본형 — 값만 만들까, key/value를 만들까?

```text
[표현식 for 변수 in 반복할_대상]                   # list
{key_표현식: value_표현식 for 변수 in 반복할_대상}  # dict
```

```python
names = ["Joe", "Jill", "Nancy"]
lengths = [len(name) for name in names]
name_lengths = {name: len(name) for name in names}

print(lengths)       # [3, 4, 5]
print(name_lengths)  # {'Joe': 3, 'Jill': 4, 'Nancy': 5}
```

리스트는 결과 값만 순서대로 모은다. 딕셔너리는 **어느 이름에 해당하는 값인지** 연결해서 저장한다. `{표현식 for ...}`처럼 콜론이 없는 형태는 **set comprehension**이므로 딕셔너리와 구별한다.

### 4.2 일반 for문으로 풀어 읽기

```python
names = ["Joe", "Jill", "Nancy"]

# comprehension
a = {name: len(name) for name in names}

# 같은 작업을 하는 일반 반복문
b = {}
for name in names:
    b[name] = len(name)

print(a == b)  # True
```

**읽는 순서:** `names`에서 하나 꺼내 `name`에 넣는다 → `name`을 key로, `len(name)`을 value로 넣는다 → 다음 이름에 반복한다.

<a id="comprehension-condition"></a>

### 4.3 뒤의 if는 필터, 앞의 if/else는 값 선택

```python
names = ["Joe", "Jill", "Nancy"]

# 필터: J로 시작하지 않는 이름은 결과에 넣지 않는다.
filtered = {
    name: len(name)
    for name in names
    if name.startswith("J")
}
print(filtered)  # {'Joe': 3, 'Jill': 4}

# 값 선택: 모든 이름을 넣되 조건에 따라 value만 고른다.
labels = {
    name: ("LONG" if len(name) >= 4 else "SHORT")
    for name in names
}
print(labels)  # {'Joe': 'SHORT', 'Jill': 'LONG', 'Nancy': 'LONG'}
```

`startswith("J")`는 문자열이 `J`로 시작하는지 `True` 또는 `False`를 반환한다. 대소문자를 구분한다.

### 4.4 센서별 평균 딕셔너리 만들기

```python
def calculate_average(values):
    return sum(values) / len(values)

data = {"Ava": [10, 20, 30], "Ben": [5, 15]}
average_data = {
    sensor: calculate_average(values)
    for sensor, values in data.items()
}
print(average_data)  # {'Ava': 20.0, 'Ben': 10.0}

selected = [name for name, avg in average_data.items() if avg >= 15.0]
print(selected)  # ['Ava']
```

`data.items()`가 `(이름, 측정값 리스트)`를 한 쌍씩 준다. 함수의 전제는 측정값 리스트가 비어 있지 않다는 것이다.

### 4.5 원소마다 변환 — float(list)는 안 된다

```python
fields = ["Ava", "10", "20", "30"]
values = [float(field) for field in fields[1:]]
readings = {fields[0]: values}
print(readings)  # {'Ava': [10.0, 20.0, 30.0]}
```

**`fields[1:]`는 리스트이고, `float()`는 리스트 전체를 변환하지 않는다.** 리스트에서 하나씩 꺼내 `float(field)`로 바꾼 결과를 모은다. 숫자가 아닌 문자열이 있으면 `ValueError`가 발생한다.

```text
float(fields[1:])                   # 잘못된 코드: 리스트를 float로 변환
field in fields[1:]                 # 포함 여부 검사; 반복이 아님
[float(field) for field in fields[1:]]  # 원소마다 변환해 새 리스트 생성
```

**언제 쓰나?** 짧은 변환·필터의 결과를 새 리스트나 딕셔너리로 모을 때 사용한다. 여러 단계의 처리, 파일 출력, 예외 처리가 중심이면 일반 `for`문으로 풀어 쓰는 편이 읽기 쉽다. comprehension의 반복 변수는 그 comprehension 바깥에 새 변수로 남지 않는다.

<a id="conditionals"></a>

## 5. 조건문 — if / elif / else / 조건 표현식

### 5.1 if와 여러 갈래의 elif

```python
score = 75

if score >= 90:
    grade = "A"
elif score >= 70:
    grade = "B"
else:
    grade = "C"

print(grade)  # B
```

조건을 위에서부터 검사하고 **처음 참이 된 갈래 하나만** 실행한다. `if`를 여러 개 따로 쓰면 각각 검사하므로 여러 블록이 실행될 수 있다. 각 헤더 끝의 **콜론 `:`과 들여쓰기**를 기억한다.

Python에는 고전적인 `switch` 문은 없지만, Python 3.10부터 구조적 패턴 매칭인 `match/case`를 사용할 수 있다. 이 글에서는 여러 조건을 나누는 기본 문법인 `if/elif/else`에 집중한다. [Python 공식 문서: match](https://docs.python.org/3.14/tutorial/controlflow.html#match-statements)

### 5.2 복합 조건 — and / or / not / in

```python
x = 3
y = 6
numbers = [1, 2, 3]

if x < 5 and y not in numbers:
    print("조건 충족")  # 조건 충족

if x == 3 or y == 0:
    print("둘 중 하나 이상 참")  # 둘 중 하나 이상 참
```

`and`는 두 조건 모두, `or`는 하나 이상 참이면 조건을 만족한다. `not`은 참/거짓을 뒤집는다. **`=`는 대입, `==`는 같은 값인지 비교**한다.

### 5.3 truth value, 빈 리스트 검사

`if values:`는 리스트가 비어 있지 않은지 확인하는 데 사용할 수 있다.

```python
values = [10, 20]
if values:
    print("측정값 있음")  # 측정값 있음

values = []
if not values:
    print("빈 리스트")  # 빈 리스트

print(bool(0), bool(""), bool([]), bool({}), bool(None))
# False False False False False
print(bool("0"), bool([0]))
# True True: 비어 있지 않은 문자열과 리스트
```

**`[0]`의 원소가 0이어도 리스트가 비어 있지 않으므로 참이다.** 또 리스트가 아닌 일반 숫자에서 `if value:`는 0인지도 구분하므로, 모든 타입에서 “비어 있는지 검사”라는 뜻은 아니다.

<a id="conditional-expression"></a>

### 5.4 조건 표현식 conditional expression — 한 줄로 값 선택

```text
참일_때_값 if 조건 else 거짓일_때_값
```

```python
average = 20.0
status = "HIGH" if average >= 20.0 else "LOW"
print(status)  # HIGH: at least는 >=

x = 3
parity = "Even" if x % 2 == 0 else "Odd"
print(parity)  # Odd
```

`if/else` **문장(statement)이** 실행할 블록을 고르는 반면, 조건 **표현식(expression)은** 사용할 값 하나를 고른다. 그래서 대입문, `return`, comprehension, lambda 안에 넣을 수 있다.

```python
def average_or_zero(values):
    return sum(values) / len(values) if values else 0.0

print(average_or_zero([10, 20]))  # 15.0
print(average_or_zero([]))        # 0.0
```

선택된 쪽만 계산하므로 빈 리스트일 때 0으로 나누지 않는다. 다만 **빈 리스트의 평균이 수학적으로 0이라는 뜻은 아니다.** 위 함수가 빈 입력을 0으로 처리하도록 정한 것이다. 문제에서 입력이 비어 있지 않다고 보장하면 단순히 `sum(values) / len(values)`만 써도 된다.

<a id="while"></a>

## 6. while / break / continue / pass

### 6.1 while — 조건을 다시 검사하면서 반복

```python
x = 0
while x < 5:
    x += 1
    print(x, end=" ")
# 1 2 3 4 5
```

`while`은 반복 시작 전마다 조건을 확인한다. `x += 1`은 `x = x + 1`과 같은 증가 연산이다. 종료 조건에 영향을 주는 값이 바뀌지 않으면 무한 반복할 수 있다.

### 6.2 break — 반복문 전체를 즉시 종료

```python
x = 0
while x < 5:
    if x == 3:
        break
    x += 1
    print(x, end=" ")
# 1 2 3
```

출력은 3까지다. **3을 출력한 다음 반복에서** `x == 3`이 참이 되어 종료한다. `break` 검사가 증가·출력보다 앞인지 뒤인지에 따라 결과가 달라진다.

### 6.3 continue — 이번 반복의 남은 코드만 건너뛰기

```python
x = 0
while x < 5:
    x += 1
    if x == 3:
        continue
    print(x, end=" ")
# 1 2 4 5
```

**`continue`는 반복문을 끝내지 않는다.** 다음 조건 검사로 넘어간다. `while`에서 증가나 다음 줄 읽기 같은 상태 갱신을 `continue` 뒤에만 두면 해당 갱신을 건너뛰어 무한 반복할 수 있다.

### 6.4 pass — 아무것도 하지 않고 다음 문장으로

```python
for x in [1, 2, 3]:
    if x == 2:
        pass
    print(x, end=" ")
# 1 2 3: pass 뒤의 print도 실행된다.
```

| 문법 | 실제 역할 | 이후 흐름 |
| --- | --- | --- |
| `break` | 가장 안쪽 반복문 종료 | 반복문 다음 문장 |
| `continue` | 이번 반복의 나머지 생략 | 다음 반복 |
| `pass` | 아무것도 안 함, 빈 블록 자리 채움 | 바로 다음 문장 |
| `return` | 함수 종료 | 함수를 호출한 곳 |

> **기억:** `pass`는 “이번 반복을 건너뛰어라”가 아니다. 함수 안의 `break`도 함수 자체를 종료하지 않는다.

<a id="for-enumerate"></a>

## 7. for / enumerate / range

### 7.1 원소가 필요하면 for item in iterable

```python
names = ["Ava", "Ben", "Cara"]
for name in names:
    print(name, end=" ")
# Ava Ben Cara
```

리스트·튜플은 원소를, 문자열은 문자를, 딕셔너리는 key를 하나씩 꺼낸다.

```python
for character in "Ava":
    print(character, end=" ")
# A v a
```

**주의:** `for name in sensor`에서 `sensor`가 이름 문자열 하나라면 센서 목록이 아니라 **그 문자열의 문자들**을 반복한다.

### 7.2 enumerate — 번호와 원소를 함께 받기

```python
names = ["Ava", "Ben", "Cara"]

for index, name in enumerate(names):
    print(index, name)
# 0 Ava
# 1 Ben
# 2 Cara

for number, name in enumerate(names, start=1):
    print(number, name)
# 1 Ava
# 2 Ben
# 3 Cara
```

`enumerate()`는 `(번호, 원소)`를 준다. `number`는 예약어가 아니라 **번호를 받도록 직접 지은 변수 이름**이다. 기본 시작 번호는 0이고 `start=1`이면 1부터 센다. 원본 리스트의 실제 인덱스가 바뀌는 것은 아니다.

### 7.3 원소가 튜플이면 중첩 언패킹

```python
sorted_average_data = [("Ava", 24.0), ("Ben", 15.0)]

for number, (sensor, average) in enumerate(sorted_average_data, start=1):
    print(number, sensor, average)
# 1 Ava 24.0
# 2 Ben 15.0
```

첫 번째 반복에서 전달되는 항목은 `(1, ("Ava", 24.0))`이다. 바깥 쌍은 `number`와 안쪽 튜플로, 안쪽 쌍은 `sensor`와 `average`로 나눠 받는다.

<a id="range"></a>

### 7.4 range — stop 제외, step 방향 확인

```text
range(stop)               # start=0, step=1
range(start, stop)        # step=1
range(start, stop, step)
```

```python
print(list(range(5)))          # [0, 1, 2, 3, 4]
print(list(range(1, 5)))       # [1, 2, 3, 4]
print(list(range(1, 10, 2)))   # [1, 3, 5, 7, 9]
print(list(range(5, 0, -1)))   # [5, 4, 3, 2, 1]
print(list(range(1, 5, -1)))   # []: 증가해야 하는 구간에 음수 step
```

**끝값 `stop`은 항상 제외된다.** `range()`는 정수 범위를 위한 것이며 `step=0`은 허용하지 않는다. `range(1, 10, 2)`는 10까지 포함해서 2씩 가는 것이 아니다. 10에 도달하기 전까지만 생성한다.

<a id="zip"></a>

## 8. zip — 여러 iterable을 나란히 묶기

```python
numbers = [1, 2, 3, 4]
fruits = ["Apple", "Orange", "Pear"]

for number, fruit in zip(numbers, fruits):
    print(number, fruit)
# 1 Apple
# 2 Orange
# 3 Pear
```

**기본 `zip()`은 가장 짧은 입력 길이에서 끝난다.** 4에 대응하는 과일이 없어서 마지막 4는 사용하지 않는다. 반환값은 iterator이므로 내용을 바로 보고 싶으면 `list(zip(...))`로 감싼다.

```python
names = ["Ava", "Ben"]
averages = [24.0, 15.0]
print(list(zip(names, averages)))  # [('Ava', 24.0), ('Ben', 15.0)]
print(dict(zip(names, averages)))  # {'Ava': 24.0, 'Ben': 15.0}
```

**`enumerate()`는 번호를 붙이고, `zip()`은 입력들의 같은 위치 값을 묶는다.** 센서 이름에 중복이 있으면 `dict(zip(...))`에서도 나중 value가 앞의 값을 덮어쓴다.

<a id="functions"></a>

## 9. def / return / None / docstring

### 9.1 함수 정의와 호출

```python
def factorial(n):
    """Return n! for a nonnegative integer n."""
    result = 1
    while n > 0:
        result *= n
        n -= 1
    return result

answer = factorial(5)
print(answer)        # 120
print(factorial(0))  # 1
```

`def factorial(n):`은 **정의**, `factorial(5)`는 **호출**이다. 매개변수(parameter) `n`에 인자(argument) `5`가 전달된다. `return`을 만나면 그 값을 호출한 곳에 돌려주고 함수를 종료한다. 위 예제는 입력이 음이 아닌 정수라는 전제이며 타입·범위 검사를 생략했다.

### 9.2 print와 return은 다르다

```python
def show_total(a, b):
    print(a + b)

def calculate_total(a, b):
    return a + b

x = show_total(2, 3)       # 화면에 5 출력
y = calculate_total(2, 3)
print(x)                  # None
print(y)                  # 5
```

**화면에 출력했다고 값을 반환한 것은 아니다.** `return`이 없거나 값 없이 `return`하면 반환값은 `None`이다. `return` 뒤의 코드는 그 호출에서 실행되지 않는다. 반환값을 다른 계산에 사용하려면 변수에 받거나 식 안에 넣는다.

### 9.3 docstring과 help

함수 본문의 첫 문자열은 설명 문서인 **docstring**이 된다.

```python
def square(x):
    """Return x multiplied by itself."""
    return x * x

print(square.__doc__)  # Return x multiplied by itself.
help(square)           # 함수 이름, 매개변수, docstring 표시
```

### 9.4 여러 결과를 튜플로 반환

```python
def measurement_summary(values):
    return len(values), sum(values)

count, total = measurement_summary([10, 20, 30])
print(count, total)  # 3 60
```

`return a, b`는 튜플을 반환한다. `load_readings()`가 `(data, error)`를 반환한다면 호출할 때도 `data, error = load_readings(...)`처럼 나눠 받는다.

<a id="arguments"></a>

## 10. 함수 인자 — positional / keyword / default

### 10.1 위치 인자와 키워드 인자

```python
def power(base, exponent):
    return base ** exponent

print(power(2, 8))                   # 256: 위치 순서로 전달
print(power(exponent=8, base=2))     # 256: 이름으로 전달
print(power(2, exponent=8))         # 256: 위치 인자를 먼저
```

키워드 인자는 `이름=값`으로 전달하므로 서로의 순서를 바꿀 수 있다. 여기서 다루는 일반 호출에서는 **위치 인자를 먼저, 키워드 인자를 나중에** 쓴다. 하나의 매개변수에 값을 중복 지정하면 안 된다.

```text
power(base=2, 8)       # SyntaxError: 위치 인자가 키워드 인자 뒤에 있음
power(2, base=3)       # TypeError: base에 두 번 값을 지정
power(2)              # TypeError: exponent가 빠짐
```

### 10.2 기본값 default parameter

```python
def describe(x, y, z=0, message="Hello"):
    return x, y, z, message

print(describe(10, "a"))            # (10, 'a', 0, 'Hello')
print(describe(10, "a", 2))         # (10, 'a', 2, 'Hello')
print(describe(10, "a", 2, "Bye"))  # (10, 'a', 2, 'Bye')
print(describe(10, "a", message="Bye"))  # (10, 'a', 0, 'Bye')
```

위 예제처럼 일반적인 위치·키워드 매개변수를 정의할 때는 **기본값이 없는 매개변수 뒤에 기본값이 있는 매개변수**를 둔다. `def f(a=0, b):`처럼 쓰면 문법 오류다.

### 10.3 리스트를 기본값으로 두는 함정

기본값 객체는 호출마다 새로 만들어지는 것이 아니다. 함수 정의 시 만들어져 다음 호출에서도 사용될 수 있다.

```python
def collect_bad(value, bucket=[]):
    bucket.append(value)
    return bucket

print(collect_bad(1))  # [1]
print(collect_bad(2))  # [1, 2]: 이전 호출의 리스트 공유

def collect(value, bucket=None):
    if bucket is None:
        bucket = []
    bucket.append(value)
    return bucket

print(collect(1))  # [1]
print(collect(2))  # [2]
```

호출마다 새 리스트가 필요하면 `None`을 기본값으로 두고 함수 안에서 만든다. [Python 공식 문서: 기본 인자](https://docs.python.org/3.14/tutorial/controlflow.html#default-argument-values)

<a id="parameter-sharing"></a>

## 11. 함수 인자 — 객체 공유와 isinstance

### 11.1 원본 수정 mutation vs 이름 재대입 rebinding

함수의 매개변수는 전달된 **객체를 가리키는 이름**이다. 리스트 같은 가변 객체의 내부를 바꾸면 호출한 쪽에서도 변화가 보인다.

```python
def replace_first(values):
    values[0] = -1

numbers = [0, 1, 2]
replace_first(numbers)
print(numbers)  # [-1, 1, 2]
```

반면 매개변수 이름이 다른 객체를 가리키도록 재대입하면 호출한 쪽 이름의 연결은 바뀌지 않는다.

```python
def replace_list(values):
    values = [99, 100]  # 함수 안의 이름만 다른 리스트를 가리킨다.
    return values

numbers = [0, 1, 2]
result = replace_list(numbers)
print(numbers)  # [0, 1, 2]
print(result)   # [99, 100]
```

> **기억:** `values[0] = ...`와 `values = ...`는 다르다. 함수와 호출한 쪽은 전달된 객체를 공유하지만, 함수 안에서 매개변수에 재대입한다고 호출자 변수 자체가 다른 객체를 가리키게 되지는 않는다. 원본을 유지해야 하면 복사본을 전달하거나 함수 안에서 복사한다. [Python 공식 문서: 함수 정의](https://docs.python.org/3.14/tutorial/controlflow.html#defining-functions)

```python
def replace_first(values):
    values[0] = -1

numbers = [0, 1, 2]
replace_first(numbers.copy())
print(numbers)  # [0, 1, 2]
```

### 11.2 isinstance — 입력 타입 검사

```python
print(isinstance(3, int))          # True
print(isinstance(3.5, int))        # False
print(isinstance(3.5, (int, float)))  # True: 둘 중 하나면 됨

def square_integer(x):
    if not isinstance(x, int):
        raise TypeError("정수가 필요합니다.")
    return x * x

print(square_integer(4))  # 16

try:
    square_integer("4")
except TypeError as exc:
    print(exc)  # 정수가 필요합니다.
```

Python은 함수 정의의 매개변수 이름만으로 타입을 제한하지 않는다. 필요한 검사를 직접 작성한다. `isinstance()`는 하위 클래스도 인정한다.

**주의:** `bool`은 `int`의 하위 클래스이므로 `isinstance(True, int)`는 참이다. 문제에서 bool을 숫자로 허용하지 않는다면 별도로 제외해야 한다. 함수 정의에는 `:`를 쓰지만, 함수를 호출할 때는 `my_func(y)`처럼 끝에 `:`를 붙이지 않는다.

<a id="scope"></a>

## 12. 지역·전역 변수 — local / global / 스코프

### 12.1 함수 안의 대입은 기본적으로 지역 변수

```python
a = "One"
b = "Two"
c = "Three"

def update_values():
    print(a)   # One: 전역 변수 읽기
    global b
    b = 2      # 전역 이름 b에 재대입
    c = 3      # 새로운 지역 변수 c
    print(c)   # 3

update_values()
print(a)  # One
print(b)  # 2
print(c)  # Three: 전역 c는 그대로
```

| 행동 | global 필요? | 이유 |
| --- | --- | --- |
| 전역 변수 값을 읽기 | 보통 불필요 | 같은 이름의 지역 변수가 없으면 바깥 이름을 찾음 |
| 함수 안에서 전역 이름에 새 값을 대입 | 필요 | 기본 대입은 지역 이름을 만듦 |
| 전역 리스트에 `.append()` 호출 | 불필요 | 이름 재대입 없이 객체 내부를 수정 |
| 매개변수 리스트의 원소 수정 | 불필요 | 매개변수가 가리키는 객체 내부 수정 |

### 12.2 UnboundLocalError가 나는 이유

```python
count = 0

def increment_bad():
    count += 1

try:
    increment_bad()
except UnboundLocalError:
    print("지역 count를 대입 전에 읽었습니다.")

def increment():
    global count
    count += 1

increment()
print(count)  # 1
```

`count += 1`은 기존 값을 읽은 뒤 대입한다. 함수 안에 대입이 있으므로 `global` 선언이 없으면 `count`를 지역 이름으로 취급하는데, 읽을 시점에는 지역 값이 없어 오류가 난다.

가능하면 전역 변수 대신 입력과 반환값으로 상태를 전달하면 의존 관계가 명확해진다.

### 12.3 if / for / try는 별도 지역 범위를 만들지 않는다

```python
def count_examples():
    error = 0
    for text in ["bad", "10", "oops"]:
        try:
            float(text)
        except ValueError:
            error += 1
    return error

print(count_examples())  # 2
```

`error = 0`을 반복문 전에 한 번만 실행하고, 오류 때마다 같은 변수에 `+= 1`한다. `except` 안에서 `error = 0`을 다시 실행하면 누적되지 않는다.

<a id="first-class"></a>

## 13. 함수는 일급 객체 — 저장·전달·반환

함수 자체를 변수나 자료구조에 저장하고, 다른 함수에 전달하거나 반환할 수 있다.

### 13.1 함수 이름과 괄호 구분

```python
def add(a, b):
    return a + b

operation = add       # 함수 자체를 저장; 아직 실행하지 않음
result = add(2, 3)    # 함수를 실행하고 반환값을 저장

print(operation(4, 5))  # 9
print(result)           # 5
```

**`add`는 함수 객체, `add(2, 3)`은 호출 결과**다. 정렬의 `key`에도 일반적으로 함수 **호출 결과가 아니라 함수 자체**를 전달한다.

### 13.2 딕셔너리에 함수 저장, 인자로 함수 전달

```python
def add(a, b):
    return a + b

def multiply(a, b):
    return a * b

def apply_operation(operation, a, b):
    return operation(a, b)

operations = {"add": add, "mul": multiply}
print(operations["add"](2, 3))         # 5
print(apply_operation(multiply, 2, 3))  # 6
```

`operations["add"](2, 3)`은 먼저 딕셔너리에서 함수를 꺼내고, 이어서 괄호로 그 함수를 호출한다.

### 13.3 함수에서 함수를 반환

```python
def add(a, b):
    return a + b

def get_operation():
    return add

operation = get_operation()
print(operation(2, 3))  # 5
```

<a id="lambda"></a>

## 14. lambda / sorted / sort — 정렬 기준 함수

### 14.1 lambda 기본형 — 입력을 받아 표현식 결과 반환

```text
lambda 매개변수: 반환할_표현식
lambda 매개변수1, 매개변수2: 반환할_표현식
```

```python
triangle_area = lambda base, height: 0.5 * base * height
print(triangle_area(5, 4))  # 10.0

# 같은 동작을 하는 일반 함수
def area(base, height):
    return 0.5 * base * height

print(area(5, 4))  # 10.0
```

lambda는 이름 없는 짧은 함수다. 필요하면 위처럼 변수에 저장할 수 있지만, 주로 `key=` 같은 자리에 짧은 함수를 바로 전달할 때 사용한다.

**본문은 표현식 하나**이며 `return`을 쓰지 않는다. `if`문·`for`문 같은 문장은 넣을 수 없지만, **조건 표현식은 넣을 수 있다.**

```python
larger = lambda x, y: x if x > y else y
print(larger(0, 5))  # 5
print(larger(6, 4))  # 6
```

### 14.2 sort와 sorted — 원본 변경과 반환값

```python
names = ["Zoe", "Jonathan", "Carrie"]

alphabetical = sorted(names)
print(alphabetical)  # ['Carrie', 'Jonathan', 'Zoe']
print(names)         # ['Zoe', 'Jonathan', 'Carrie']: 원본 유지

result = names.sort(key=lambda name: len(name))
print(names)         # ['Zoe', 'Carrie', 'Jonathan']: 길이순으로 원본 변경
print(result)        # None
```

| 기능 | `sorted(iterable, key=..., reverse=...)` | `list.sort(key=..., reverse=...)` |
| --- | --- | --- |
| 반환값 | 새 리스트 | `None` |
| 원본 리스트 | 유지 | 직접 정렬 |
| 입력 | 다양한 iterable | 해당 리스트 |
| 내림차순 | `reverse=True` | `reverse=True` |

**틀리기 쉬운 코드:** `names = names.sort()`를 실행하면 `names`에 정렬된 리스트가 아니라 `None`이 저장된다. 새 리스트를 원하면 `names = sorted(names)`를 사용한다.

### 14.3 key는 비교 기준을 계산하는 함수

```python
names = ["Zoe", "Jonathan", "Carrie"]

def name_length(name):
    return len(name)

print(sorted(names, key=name_length))
# ['Zoe', 'Carrie', 'Jonathan']

print(sorted(names, key=lambda name: len(name), reverse=True))
# ['Jonathan', 'Carrie', 'Zoe']
```

`sorted()`가 각 원소를 `key` 함수에 전달한다. 함수가 반환한 값을 정렬 기준으로 사용하고, 결과에는 원래 원소를 넣는다. `lambda name: len(name)`은 문자열을 길이로 바꾸어 저장하라는 뜻이 아니다.

### 14.4 센서 이름만 평균순으로 정렬

```python
average_data = {"Ben": 15.0, "Cara": 12.0, "Ava": 24.0}

sorted_names = sorted(
    average_data,
    key=lambda sensor: average_data[sensor],
    reverse=True,
)
print(sorted_names)  # ['Ava', 'Ben', 'Cara']
```

딕셔너리 자체를 반복하면 **key인 이름**이 나온다. 람다는 그 이름을 받아 대응하는 평균을 반환한다. key 함수를 빼고 `sorted(average_data)`만 실행하면 평균이 아니라 **이름순**으로 정렬한다.

### 14.5 이름과 평균 쌍을 정렬 — lambda pair: pair[1]

```python
average_data = {"Ben": 15.0, "Cara": 12.0, "Ava": 24.0}

sorted_average_data = sorted(
    average_data.items(),
    key=lambda pair: pair[1],
    reverse=True,
)
print(sorted_average_data)
# [('Ava', 24.0), ('Ben', 15.0), ('Cara', 12.0)]
```

`pair`에는 `("Ben", 15.0)` 같은 튜플 하나가 들어온다. **`pair[0]`은 이름, `pair[1]`은 평균**이다. `lambda x: x[1]`로 써도 같으며, `x`라는 이름에 특별한 의미는 없다.

두 정렬 방식의 결과 타입을 구분한다.

```text
sorted(average_data, key=...)          → ['Ava', 'Ben', 'Cara']
sorted(average_data.items(), key=...)  → [('Ava', 24.0), ...]
```

`sorted()`는 딕셔너리를 입력해도 **리스트를 반환**한다. 이름과 평균을 같이 사용할 예정이면 두 번째 방식이 편하다. [Python 공식 문서: sorted](https://docs.python.org/3.14/library/functions.html#sorted)

### 14.6 같은 평균이면 이름순으로 정렬

```python
average_data = {"Ben": 20.0, "Cara": 15.0, "Ava": 20.0}

result = sorted(
    average_data.items(),
    key=lambda pair: (-pair[1], pair[0]),
)
print(result)  # [('Ava', 20.0), ('Ben', 20.0), ('Cara', 15.0)]
```

기준을 튜플로 반환하면 앞의 기준부터 비교한다. `-평균`으로 평균 내림차순, 이름으로 동률 시 오름차순을 만든다. 위 코드에는 `reverse=True`를 추가하지 않는다. 단순 정렬에서 동률이면 Python 정렬은 기존 순서를 유지하는 **안정 정렬(stable sort)이다**.

<a id="sensor-example"></a>

## 15. 종합 예제 — 평균 → 필터 → 정렬 → 번호와 상태

메모리에 있는 센서 데이터를 평균 계산부터 정렬·상태 출력까지 처리하는 예제다. **comprehension, 함수, lambda, 조건 표현식, enumerate**를 한 번에 확인할 수 있다.

```python
def calculate_average(values):
    return sum(values) / len(values)

data = {
    "Ava": [10.0, 20.0, 30.0, 20.0, 40.0],
    "Ben": [5.0, 15.0, 25.0],
    "Cara": [8.0, 12.0, 16.0],
}

# 1. 센서 이름 → 평균: dictionary comprehension
average_data = {
    sensor: calculate_average(values)
    for sensor, values in data.items()
}

# 2. 평균 15 이상인 이름만: filtering list comprehension
selected_sensors = [
    sensor for sensor, average in average_data.items()
    if average >= 15.0
]

# 3. (센서 이름, 평균)을 평균 내림차순으로 정렬
sorted_average_data = sorted(
    average_data.items(),
    key=lambda pair: pair[1],
    reverse=True,
)

# 4. 1부터 번호를 붙이고 조건 표현식으로 상태 지정
for number, (sensor, average) in enumerate(sorted_average_data, start=1):
    status = "HIGH" if average >= 20.0 else "LOW"
    print(
        f"{number}. {sensor}: count = {len(data[sensor])}, "
        f"average = {average:.2f}, status = {status}"
    )

print(f"Sensors with average >= 15.0: {selected_sensors}")
```

출력:

```text
1. Ava: count = 5, average = 24.00, status = HIGH
2. Ben: count = 3, average = 15.00, status = LOW
3. Cara: count = 3, average = 12.00, status = LOW
Sensors with average >= 15.0: ['Ava', 'Ben']
```

여기서 `len(data[sensor])`는 **해당 센서의 측정값 수**다. `len(data)`는 센서 수이므로 서로 다르다. `:.2f`는 **출력할 때 소수 둘째 자리까지 표시**하는 형식이며, 원래 평균 변수 값을 바꾸지 않는다. f-string은 문자열 안의 중괄호 `{}`에 계산값을 넣는 문법이다.

`selected_sensors`는 여기서는 원본 딕셔너리의 삽입 순서다. 이 목록도 평균순이어야 한다면 `average_data.items()` 대신 이미 정렬한 `sorted_average_data`를 순회한다.

<a id="pitfalls"></a>

## 16. 실수 점검표 — 시험 직전 확인

| 헷갈리는 코드 / 상황 | 실제 의미 / 수정 |
| --- | --- |
| `24 in data` | value가 아니라 key 검사. value 검사는 `24 in data.values()` |
| `data[없는_key]` | `KeyError`. 존재 확인 또는 필요에 맞는 `get()` |
| `data["Ava"] = values`를 반복 | 누적하지 않고 교체. 기존 리스트에는 `extend()` |
| `copy()`면 내부 리스트도 독립? | 얕은 복사이므로 내부 객체 공유 |
| `list(data)` | value가 아니라 key 리스트 |
| `for name, avg in data` | key 자체를 언패킹하려 함. 쌍이 필요하면 `data.items()` |
| `{value for value in numbers}` | dict가 아니라 set. dict는 `key: value` 필요 |
| `field in fields[1:]` | 포함 여부 검사. 반복은 `for field in fields[1:]` |
| `float(fields[1:])` | 리스트를 변환할 수 없음. 원소마다 `float()` 적용 |
| comprehension 뒤의 `if` | 조건을 통과한 원소만 넣는 필터 |
| 표현식 앞의 `A if 조건 else B` | 원소를 제외하지 않고 사용할 값 선택 |
| `if [0]:` | 비어 있지 않아서 참 |
| `pass`면 다음 반복으로? | 아님. 다음 반복으로 가려면 `continue` |
| `while`에서 `continue` | 상태 갱신을 건너뛰지 않는지 확인 |
| `range(1, 5)` | 1, 2, 3, 4; 5 제외 |
| `enumerate(data, start=1)` | 원본 인덱스 변경이 아니라 번호를 1부터 붙임 |
| 길이가 다른 두 입력을 `zip()` | 기본 동작은 짧은 입력에서 종료 |
| `print(answer)`만 있는 함수 | 반환값은 `None`. 계산값 반환은 `return answer` |
| `return a, b` | 튜플 반환. 호출 쪽에서 `x, y = ...` 가능 |
| `values[0] = ...` vs `values = ...` | 객체 내부 수정 vs 함수 안의 이름 재대입 |
| 함수 안에서 전역 변수에 `+=` | 지역 이름으로 해석될 수 있음. 스코프 확인 |
| 함수의 기본값이 `[]` | 호출 사이에 같은 리스트 공유 가능 |
| `lambda x: return x[1]` | 문법 오류. `lambda x: x[1]` |
| `key=함수()` | 보통 호출 결과를 전달하는 실수. 함수 자체인 `key=함수` |
| `names = names.sort()` | `names`에 `None` 저장. 새 리스트는 `sorted(names)` |
| `sorted(average_data)` | 평균이 아니라 key인 센서 이름순 |
| 정렬된 딕셔너리라고 생각한 `sorted(...)` | 반환 타입은 리스트 |

<a id="sources"></a>

## 17. 공식 문서

- [dict: key, 삽입 순서, copy, keys/values/items](https://docs.python.org/3.14/library/stdtypes.html#mapping-types-dict)
- [조건문·반복문·함수·기본값·lambda](https://docs.python.org/3.14/tutorial/controlflow.html)
- [함수 정의와 인자 전달](https://docs.python.org/3.14/tutorial/controlflow.html#defining-functions)
- [이름 바인딩과 지역·전역 범위](https://docs.python.org/3.14/reference/executionmodel.html#naming-and-binding)
- [sorted의 key와 reverse](https://docs.python.org/3.14/library/functions.html#sorted)
- [enumerate](https://docs.python.org/3.14/library/functions.html#enumerate), [range](https://docs.python.org/3.14/library/stdtypes.html#ranges), [zip](https://docs.python.org/3.14/library/functions.html#zip), [isinstance](https://docs.python.org/3.14/library/functions.html#isinstance)
