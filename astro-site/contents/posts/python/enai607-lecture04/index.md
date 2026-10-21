---
title: "[ENAI607] Lecture 04 — 예외 처리, 모듈, 파일 입출력과 with"
description: "try·except·raise·finally·import·sys.path·open·readline·write·bytes·with를 예제와 출력으로 찾는 오픈북 노트"
date: 2026-10-20T01:45:00-04:00
update: 2026-10-20
tags:
  - python
  - ENAI607
series: "ENAI607 Python Programming"
---

파일을 읽다가 숫자가 아닌 값을 만나면 어떻게 할까? 오류를 처리하고 다음 줄로 넘어가려면 어떻게 해야 할까? 여러 파일에 함수를 나누면 어떻게 가져다 쓸까?

이 글은 **예외 처리, 모듈, 텍스트·바이너리 파일 입출력, `with` 문**을 처음부터 설명한다. 개념을 이해한 뒤 코드를 실행해 보고, 시험 중에는 목차와 함수 이름으로 필요한 예제를 찾을 수 있게 구성했다.

**사용법:** 상단 목차를 클릭하거나 `Ctrl+F`로 `ValueError`, `finally`, `readline`, `write`, `sys.path`, `EOF` 등을 검색한다. 오른쪽 자동 목차는 넓은 화면에서 본문을 따라 표시된다. 위의 `SERIES` 상자는 이 글의 목차가 아니라 같은 시리즈의 글 목록이다.

**예제 준비:** 파일 읽기 예제는 작업 폴더에 `hello.txt`가 있다고 가정한다. 해당 예제 앞에서 준비 파일 내용을 확인한다. `my_math.py`와 `use_math.py`는 각각 별도 파일로 저장한다. `python` 블록은 실행 코드, `text` 블록은 문법 틀·파일 내용·출력이다. 검증 기준은 Python 3.14다.

<a id="toc"></a>

## 빠른 목차 — 오류·파일·함수 이름으로 찾기

| 찾는 작업 / 문법 | 바로가기 |
| --- | --- |
| 핵심 문법 한눈에 보기 | [0. 치트시트](#quick-reference) |
| 예외가 발생하면 어디로 가는가 | [1. 예외와 전파](#exceptions) |
| `raise ValueError(...)`, 사용자 정의 오류 | [2. raise와 custom exception](#raise) |
| `try`, `except`, `as exc`, 여러 오류 잡기 | [3. except](#except) |
| `TypeError`와 `ValueError`, 상속·처리 순서 | [4. 예외 종류와 계층](#hierarchy) |
| `else`는 언제 실행되나 | [5. try의 else](#try-else) |
| `finally`, 미처리 예외, 함수 반환 | [6. 정리와 실행 순서](#finally) |
| `import math`, `import numpy as np` | [7. 모듈과 namespace](#modules) |
| 직접 만든 `.py` 파일 import하기 | [8. 사용자 모듈](#own-module) |
| 모듈이 안 찾아짐, `sys.path`, `.pth` | [9. 모듈 검색 경로](#module-path) |
| 수정한 모듈이 반영되지 않음 | [import 캐시와 reload](#module-cache) |
| `open()`, r/w/a, t/b, 인코딩 | [10. 파일 열기](#open) |
| 파일은 있는데 `FileNotFoundError` | [상대 경로와 BASE_DIR](#file-path) |
| `readline`, `readlines`, `read`, `for line in fobj` | [11. 파일 읽기](#read) |
| 빈 줄과 EOF, 첫 줄 건너뛰기 | [EOF와 빈 줄](#eof) · [while로 읽기](#read-while) |
| `strip`, `split`, 빈 줄 제외 | [12. 문자열 전처리](#strip-split) |
| `write`, `writelines`, 줄바꿈, f-string | [13. 파일 쓰기](#write) |
| `rb`, `wb`, bytes, hex | [14. 바이너리 파일](#binary) |
| 자동 close, `with open`, 예외 처리 결합 | [15. context manager](#with) |
| 센서 파일 전체 처리와 보고서 예제 | [16. 종합 예제](#sensor-example) |
| 자주 틀리는 코드 비교 | [17. 실수 점검표](#pitfalls) |
| 공식 문서 | [18. 참고 자료](#sources) |

<a id="quick-reference"></a>

## 0. 시험 직전 치트시트

아래는 **문법 틀**이다. 실제 실행 예제는 각 절에 있다.

```text
try:
    오류가_날_수_있는_작업
except ValueError as exc:
    값_변환_오류_처리
except OSError as exc:
    파일_OS_오류_처리
else:
    try가_예외_없이_끝났을_때_실행
finally:
    정상_예외_여부와_관계없이_정리

raise ValueError("잘못된 값")

class InvalidDataError(Exception):
    pass

import math
math.sin(math.pi / 6)              # 각도는 라디안
import numpy as np
import my_math                    # my_math.py, 확장자 없이 import

with open(path, "r", encoding="utf-8") as fobj:
    for line in fobj:
        fields = line.strip().split(",")

with open(path, "w", encoding="utf-8") as fobj:
    fobj.write(f"average = {average:.2f}\n")

with open(path, "rb") as fobj:
    data = fobj.read(4)            # 최대 4바이트, 반환값 bytes
```

> **특히 기억:** `except`는 오류 메시지가 아니라 **예외 클래스**로 매칭한다. `readline()`의 EOF는 `''`, 빈 줄은 보통 `'\n'`이다. `write()`와 `writelines()`는 줄바꿈을 자동 추가하지 않는다. `'w'`는 열 때 기존 내용을 지운다. `with`는 파일을 닫아 주지만 오류까지 자동으로 처리하지는 않는다.

<a id="exceptions"></a>

## 1. 예외 exception — 오류 발생과 전파

예외는 실행 중 문제가 생겼을 때 정상 처리 흐름을 중단하고 오류 처리 코드로 이동하게 하는 장치다. 파일·디스크 같은 외부 상황이나, 0으로 나누기·잘못된 인덱스 같은 코드 문제를 처리할 수 있다.

실행 순서는 다음과 같다.

1. 문제가 생기면 예외 객체가 발생한다.
2. 현재 코드를 감싼 `try`의 처리기 중 **종류가 맞는 `except`를** 찾는다.
3. 없으면 호출한 함수 쪽으로 전달되어 처리기를 계속 찾는다.
4. 끝까지 처리기가 없으면 일반 스크립트 실행은 traceback을 출력하며 종료된다.

### 1.1 오류가 난 뒤 같은 try의 나머지는 실행하지 않는다

```python
try:
    print("변환 시작")
    number = float("hello")
    print("이 줄은 실행되지 않음")
except ValueError:
    print("숫자로 변환할 수 없음")

print("처리 후 계속")
# 변환 시작
# 숫자로 변환할 수 없음
# 처리 후 계속
```

**처리 후 오류가 났던 줄로 돌아가 재실행하는 것이 아니다.** 다음 입력을 시도하려면 반복문 등의 흐름을 직접 작성해야 한다.

### 1.2 함수 밖에서도 잡을 수 있다

```python
def convert(text):
    return float(text)

def load_one(text):
    return convert(text)

try:
    load_one("hello")
except ValueError:
    print("호출한 쪽에서 잡음")
# 호출한 쪽에서 잡음
```

`convert()` → `load_one()` → 호출한 쪽 순으로 전파된다. 각 함수가 꼭 직접 `except`를 가져야 하는 것은 아니다.

<a id="raise"></a>

## 2. raise — 직접 오류 발생시키기

```text
raise 예외클래스("오류 메시지")
```

### 2.1 기존 예외 클래스와 원하는 메시지

```python
def divide(numerator, denominator):
    if denominator == 0:
        raise ZeroDivisionError("분모는 0일 수 없습니다.")
    return numerator / denominator

print(divide(10, 2))  # 5.0

try:
    divide(10, 0)
except ZeroDivisionError as exc:
    print(exc)  # 분모는 0일 수 없습니다.
```

`ZeroDivisionError`는 **종류**, 괄호 안 문자열은 **메시지**, `exc`는 발생한 **예외 객체를 받는 변수**다. `raise`는 메시지를 출력하고 계속하는 명령이 아니다. 정상 흐름을 중단한다.

### 2.2 사용자 정의 예외 custom exception

```python
class InvalidDataError(Exception):
    pass

def validate_name(name):
    if not name.strip():
        raise InvalidDataError("센서 이름이 비어 있습니다.")
    return name.strip()

try:
    validate_name("   ")
except InvalidDataError as exc:
    print(exc)  # 센서 이름이 비어 있습니다.
```

`Exception`을 상속하면 나만의 오류 종류를 만들 수 있다. `pass`는 본문에 추가 동작이 없다는 뜻이다. 보통 이름 끝에 `Error`를 붙인다.

### 2.3 float의 ValueError는 자동으로 내 오류가 되지 않는다

```python
class InvalidDataError(Exception):
    pass

fields = ["Ava", "10", "hello"]

try:
    if not fields[0]:
        raise InvalidDataError("이름 없음")
    values = [float(field) for field in fields[1:]]
except (InvalidDataError, ValueError) as exc:
    print(type(exc).__name__)  # ValueError
```

`float()`는 원래 정의된 대로 `ValueError`를 발생시킨다. `InvalidDataError`를 만들었다고 숫자 변환 오류의 종류가 바뀌지는 않는다. 같은 처리를 할 거라면 위처럼 **예외 클래스들의 튜플**로 잡는다.

모든 잘못된 입력을 내 오류 종류로 통일하려면 변환 오류를 잡고 새 예외를 발생시킨다. **`raise ... from exc`는 원인을 연결한다.**

```python
class InvalidDataError(Exception):
    pass

def to_number(text):
    try:
        return float(text)
    except ValueError as exc:
        raise InvalidDataError(f"숫자가 아닙니다: {text}") from exc

try:
    to_number("hello")
except InvalidDataError as exc:
    print(exc)                    # 숫자가 아닙니다: hello
    print(type(exc.__cause__).__name__)  # ValueError
```

<a id="except"></a>

## 3. try / except / as exc — 오류 잡기

### 3.1 기본형

```python
try:
    number = int("abc")
except ValueError as exc:
    print(type(exc).__name__)  # ValueError
    print("입력값을 정수로 바꿀 수 없습니다.")
```

`except ValueError:`처럼 객체 변수 없이도 쓸 수 있다. 오류 메시지나 세부 정보가 필요하면 `as exc`로 받는다. `exc`, `err`, `error`는 자유롭게 정한 변수 이름이다.

### 3.2 여러 종류를 다르게 처리

```python
def get_number(values, index):
    try:
        return float(values[index])
    except IndexError:
        return "인덱스 오류"
    except ValueError:
        return "숫자 변환 오류"

print(get_number(["10", "bad"], 0))  # 10.0
print(get_number(["10", "bad"], 1))  # 숫자 변환 오류
print(get_number(["10", "bad"], 5))  # 인덱스 오류
```

처리기가 여러 개여도 **처음 매칭되는 하나**가 실행된다. `except`에서 새 오류가 생기면 같은 `try`에 붙은 다음 `except`가 잡아 주는 구조가 아니다. 그 새 오류도 바깥으로 전파된다.

### 3.3 여러 종류를 같은 방식으로 처리

```python
for value in ["hello", None]:
    try:
        float(value)
    except (ValueError, TypeError) as exc:
        print(type(exc).__name__)
# ValueError
# TypeError
```

**주의:** `except ValueError or TypeError:`라고 쓰지 않는다. 여러 예외를 묶을 때는 `(ValueError, TypeError)`를 사용한다.

<a id="hierarchy"></a>

## 4. 예외 종류와 상속 계층

| 예외 클래스 | 주된 의미 | 예 |
| --- | --- | --- |
| `ZeroDivisionError` | 0으로 나누기 | `1 / 0` |
| `OverflowError` | 표현 가능한 범위를 넘는 연산 등 | `math.exp(1000)` |
| `IndexError` | 시퀀스 인덱스 범위 초과 | `[1, 2][5]` |
| `KeyError` | 딕셔너리에 key 없음 | `{"a": 1}["b"]` |
| `TypeError` | 작업에 맞지 않는 타입 | `float([1, 2])` |
| `ValueError` | 타입은 받지만 값이 부적절 | `float("hello")` |
| `AttributeError` | 객체에 해당 속성·메서드 없음 | `(3).append(1)` |
| `AssertionError` | `assert` 조건 거짓 | `assert 1 == 2` |
| `OSError` | OS·파일 관련 문제 | 파일·권한·장치 문제 |
| `FileNotFoundError` | 경로에 파일이 없음 | `open("missing.txt")` |
| `EOFError` | 입력을 더 받을 수 없음 | `input()`이 EOF를 만남 |
| `RuntimeError` | 다른 구체적 분류로 표현하지 않은 실행 오류 | 직접 `raise RuntimeError(...)` |
| `NotImplementedError` | 구현이 필요한 동작의 자리 | 직접 `raise NotImplementedError(...)` |

관련 계층의 일부만 나타내면 다음과 같다.

```text
Exception
├─ ArithmeticError
│  ├─ OverflowError
│  └─ ZeroDivisionError
├─ LookupError
│  ├─ IndexError
│  └─ KeyError
├─ OSError
│  ├─ FileNotFoundError
│  └─ PermissionError
├─ RuntimeError
│  └─ NotImplementedError
├─ AssertionError
├─ AttributeError
├─ EOFError
├─ TypeError
└─ ValueError
```

**기억할 점:** Python 3에서 `IOError`와 `EnvironmentError`는 `OSError`의 별칭이다. 새 코드에서는 `OSError`를 사용하면 된다.

### 4.1 부모 예외로 자식 예외를 잡을 수 있다

```python
try:
    number = 1 / 0
except ArithmeticError:
    print("산술 오류 처리")  # 산술 오류 처리
```

`except Exception:`은 여기 나온 여러 종류를 넓게 잡는다. 하지만 어떤 오류인지 구분하기 어려워지므로 예상한 예외를 구체적으로 쓰는 편이 좋다. `KeyboardInterrupt`, `SystemExit`까지 모두 잡는다는 뜻은 아니다.

### 4.2 구체적인 자식 예외를 먼저 작성

```python
try:
    number = 1 / 0
except ZeroDivisionError:
    print("분모 0")  # 분모 0
except ArithmeticError:
    print("그 밖의 산술 오류")
```

`ArithmeticError`를 먼저 쓰면 `ZeroDivisionError`도 그쪽에서 처리되어 아래 처리기는 실행되지 않는다.

<a id="try-else"></a>

## 5. try의 else는 성공했을 때만

`try`의 `else`는 **try 블록이 예외 없이 정상 완료됐을 때** 실행한다. `if`에 붙는 `else`와 구분한다. 아래 코드는 입력 하나가 잘못되면 그 줄의 값을 저장하지 않는다.

```python
data = {}
error = 0
lines = ["Ava,10,20", "Bad,3,hello", "Ben,5,15"]

for line in lines:
    fields = line.split(",")
    try:
        values = [float(field) for field in fields[1:]]
    except ValueError:
        error += 1
    else:
        data[fields[0]] = values

print(data)   # {'Ava': [10.0, 20.0], 'Ben': [5.0, 15.0]}
print(error)  # 1
```

숫자 변환이 전부 끝나기 전에는 딕셔너리를 수정하지 않으므로 잘못된 줄의 일부만 들어가지 않는다. `error = 0`은 반복문 밖에서 한 번만 실행해야 누적된다.

**주의:** `else` 안에서 발생한 오류는 같은 `try`의 `except`가 잡지 않는다. 또 `try`에서 `return`, `break`, `continue`로 빠져나가면 `else`도 실행하지 않는다. 성공한 경우에만 해야 하는 작업을 `else`에 분리하면 보호하려는 작업 범위가 명확해진다. [Python 공식 문서: 예외 처리](https://docs.python.org/3.14/tutorial/errors.html#handling-exceptions)

<a id="finally"></a>

## 6. finally — 정리 코드와 세 가지 실행 흐름

### 6.1 정상·처리한 예외·미처리 예외

| 경우 | 실행 순서 |
| --- | --- |
| 오류 없음 | `try` → `else`(있으면) → `finally` → 이후 코드 |
| 오류를 현재 `except`가 처리 | 오류까지의 `try` → 매칭 `except` → `finally` → 이후 코드 |
| 현재 `except`가 처리 못 함 | 오류까지의 `try` → `finally` → 바깥 처리기로 전파 |

처리기가 정상적으로 끝나고, `finally`에서도 추가 예외나 흐름 변경이 없다는 전제다. **미처리 예외가 있으면 `finally` 바로 다음 문장까지 무조건 실행된다는 뜻이 아니다.**

```python
def demonstrate(text):
    try:
        print("try")
        number = int(text)
    except ValueError:
        print("except")
    else:
        print("else", number)
    finally:
        print("finally")
    print("after")

demonstrate("10")
# try
# else 10
# finally
# after

demonstrate("bad")
# try
# except
# finally
# after
```

### 6.2 미처리 예외도 finally를 거쳐 전파

```python
def inner():
    try:
        print("inner try")
        raise TypeError("잘못된 타입")
    except ValueError:
        print("이 처리기는 매칭되지 않음")
    finally:
        print("inner finally")
    print("이 줄은 실행되지 않음")

try:
    inner()
except TypeError:
    print("outer except")
# inner try
# inner finally
# outer except
```

### 6.3 return 전에 정리도 수행

```python
def get_value():
    try:
        return 10
    finally:
        print("정리")

print(get_value())
# 정리
# 10
```

`finally` 안에서 `return`하면 기존 반환값이나 예외를 덮을 수 있으므로 정리 블록에 불필요한 `return`을 넣지 않는다. 여기서 “항상 실행”은 일반적인 Python 제어 흐름에서의 의미이며 프로세스 강제 종료나 전원 차단까지 보장하지 않는다.

### 6.4 open 자체가 실패했을 때의 정리

`finally`에 `fo.close()`를 넣기만 하면 충분할까? **`open()` 자체가 실패하면 `fo`가 아직 대입되지 않았을 수 있다.** 이때 무조건 `fo.close()`를 호출하면 새로운 오류가 생겨 원래 문제를 가린다.

수동 정리의 기본형은 다음과 같다. 아래는 문법 틀이므로 `path`와 본문은 실제 코드로 바꿔야 한다.

```text
fo = None
try:
    fo = open(path, "r", encoding="utf-8")
    ...
except OSError as exc:
    print(exc)
finally:
    if fo is not None:
        fo.close()
```

파일은 보통 [15절의 `with open(...)`](#with)으로 더 간단하게 정리한다. 또 **일반적인 파일 순회나 `readline()`은 끝에 도달했다고 `EOFError`를 발생시키지 않는다.** `except EOFError`로 파일이 없는 문제를 처리할 수는 없다. 이 차이는 [EOF 절](#eof)에서 확인한다.

<a id="modules"></a>

## 7. 모듈 module — import와 namespace

모듈은 관련 함수와 객체를 묶는 단위다. 직접 만드는 경우 보통 `.py` 파일 하나가 모듈이 된다. 표준 라이브러리나 확장 모듈에는 컴파일된 구현도 있다.

모듈마다 **namespace(이름 공간)가** 있어 같은 함수 이름을 구분한다. 예를 들어 `math.exp`, `cmath.exp`, `numpy.exp`는 모두 `exp`라는 이름을 쓰지만 소속 모듈이 다르다.

### 7.1 import module_name

```python
import math

print(math.pi)                     # 3.141592653589793
print(math.sin(math.pi / 6))        # 약 0.5
print(round(math.sin(math.pi / 6), 2))  # 0.5
```

**`math.sin()`의 입력은 라디안이다.** 30도를 입력하려면 `math.pi / 6` 또는 `math.radians(30)`을 사용한다. 부동소수점 계산 때문에 결과가 `0.49999999999999994`처럼 나올 수 있다.

### 7.2 import ... as ... — 별칭 alias

```python
import numpy as np

x = np.array([1, 2, 3])
print(x.dot(x))  # 14: 1*1 + 2*2 + 3*3
```

`np`는 NumPy를 가리키도록 정한 별칭이다. `.dot()`은 이 1차원 배열 예제에서는 내적을 계산한다. NumPy는 표준 라이브러리가 아니므로 **현재 실행 인터프리터에 설치**되어 있어야 한다.

### 7.3 from ... import ...와의 차이

```python
from math import pi, sin

print(round(sin(pi / 6), 2))  # 0.5
```

| 문법 | 호출 방법 | 현재 이름 공간에 들어오는 이름 |
| --- | --- | --- |
| `import math` | `math.sin(...)` | `math` |
| `import math as m` | `m.sin(...)` | `m` |
| `from math import sin` | `sin(...)` | `sin` |

`from ... import *`는 출처와 이름 충돌을 파악하기 어려워지므로 시험 코드에서도 필요한 이름만 명시하는 편이 좋다.

<a id="own-module"></a>

## 8. 사용자 모듈 — my_math.py 만들고 사용하기

다음처럼 두 파일을 같은 폴더에 둔다.

```text
practice/
├─ my_math.py
└─ use_math.py
```

### 8.1 my_math.py — 상수와 함수 정의

아래 코드 블록은 **`my_math.py`에 저장**한다.

```python
"""원의 넓이를 계산하는 간단한 모듈."""

PI = 3.14

def area(radius):
    return PI * radius * radius
```

첫 문자열은 모듈 docstring이다. 대문자 `PI`는 상수로 사용한다는 관례이며, Python이 재대입을 강제로 금지하는 것은 아니다.

**기억할 점:** 함수에서 모듈의 전역 변수 값을 **읽기만 한다면 `global PI`는 필요 없다.** 모듈의 이름에 함수 안에서 재대입할 때 `global`이 필요하다.

### 8.2 use_math.py — 모듈 이름으로 접근

다음 블록은 **`use_math.py`에 저장하고 실행**한다.

```python
import my_math

print(my_math.PI)        # 3.14
print(my_math.area(10))  # 314.0
print(my_math.__doc__)   # 원의 넓이를 계산하는 간단한 모듈.
```

**`import my_math.py`가 아니라 `import my_math`다.** 모듈 이름을 `math.py`, `random.py`, `numpy.py`처럼 기존 모듈과 같게 짓지 않는다. 내 파일이 먼저 발견되어 원래 모듈을 가리는 문제가 생길 수 있다.

### 8.3 import할 때 실행하지 않을 테스트 코드

아래는 별도 모듈 `sensor_utils.py`를 만든다고 가정한 독립 예제다.

```python
def average(values):
    return sum(values) / len(values)

def main():
    print(average([10, 20, 30]))

if __name__ == "__main__":
    main()
```

직접 실행하면 `__name__`이 `"__main__"`이라 테스트가 실행된다. 다른 파일에서 `import sensor_utils`하면 함수는 정의되지만 `main()`은 자동 호출하지 않는다. 반면 가드 밖의 최상위 코드는 최초 import 때 실행될 수 있다.

<a id="module-path"></a>

## 9. 모듈 검색 경로 — sys.path / .pth / import 캐시

### 9.1 sys.path는 디렉터리 목록

```python
import sys

print(sys.executable)  # 현재 실행 중인 Python의 위치
print(sys.prefix)      # 현재 환경의 설치 기준 경로
print(sys.path)        # 모듈 검색 경로 리스트
```

`sys.path`에는 **모듈 파일 자체가 아니라 모듈을 담은 폴더**가 들어간다. 일반적으로 스크립트가 있는 폴더가 검색 경로에 포함되므로 같은 폴더의 `my_math.py`는 별도 경로 설정 없이 import할 수 있다.

다른 폴더를 추가하는 문법은 아래와 같다. 환경마다 다른 절대 경로를 코드에 박으면 컴퓨터나 프로젝트 위치가 바뀔 때 코드를 수정해야 한다.

```text
import sys
sys.path.append(r"C:\path\to\modules")  # 디렉터리
import my_math
```

**기억할 점:** `sys.path`는 모듈을 찾는 경로이고, `Path.cwd()`는 파일의 상대 경로를 해석할 현재 작업 폴더다. 둘은 역할이 다르므로 파일이 안 열린다고 `sys.path`부터 바꾸지 않는다.

### 9.2 .pth — 검색 경로를 파일로 등록

`.pth` 파일에 검색할 디렉터리를 한 줄씩 적는 방식이다. 예를 들어 `my_modules.pth` 내용은 다음과 같다.

```text
C:\Projects\shared_modules
D:\Courses\ENAI607\modules
```

**기억할 점:** `.pth` 파일은 일반적으로 **`site`가 처리하는 `site-packages` 디렉터리**에 둔다. `sys.prefix` 폴더에 놓기만 하면 자동 적용된다고 가정하지 않는다.

```python
import site

print(site.getsitepackages())      # 이 환경의 site-packages 후보
print(site.getusersitepackages())  # 사용자별 site-packages 경로
```

가상환경마다 경로와 활성화 여부가 다르다. 과제 폴더 안에 함께 쓰는 모듈을 두는 것이 간단한 경우라면 굳이 `.pth`를 만들 필요는 없다. [Python 공식 문서: site와 .pth](https://docs.python.org/3.14/library/site.html)

<a id="module-cache"></a>

### 9.3 수정한 모듈이 반영되지 않으면 — import 캐시

보통 같은 인터프리터 세션에서 이미 가져온 모듈은 캐시된다. 파일을 수정하고 `import my_math`를 다시 쓴다고 매번 다시 실행되는 것은 아니다.

```python
import importlib
import my_math

importlib.reload(my_math)
print(my_math.area(10))  # 314.0
```

**기억할 점:** 새 모듈을 최초 import할 때마다 인터프리터를 재시작해야 하는 것은 아니다. 콘솔에서 이미 import한 파일을 수정한 경우에는 재시작하거나 `importlib.reload()`를 사용할 수 있다. `from my_math import area`로 별도 이름에 받은 함수까지 자동 갱신된다고 생각하지 않는다.

### 9.4 ModuleNotFoundError 점검 순서

1. 파일 이름·철자·확장자가 맞는가? `my_math.py.txt`가 아닌가?
2. 실행 스크립트 옆에 모듈이 있는가? 아니라면 검색 경로 안에 있는가?
3. IDE가 선택한 인터프리터가 맞는가? `sys.executable`로 확인한다.
4. 외부 패키지라면 그 인터프리터에 설치되어 있는가?
5. 내 파일 이름이 기존 모듈을 가리고 있지 않은가?

<a id="open"></a>

## 10. open — 파일 객체, 모드, 인코딩과 경로

```text
fobj = open(file_path, mode, encoding="utf-8")
...
fobj.close()
```

`open()`은 열린 파일 객체를 반환한다. 파일 이름 문자열 자체가 반환되는 것이 아니다. 자원을 정리하려면 `close()`하거나 [with 문](#with)을 사용한다.

### 10.1 r / w / a — 읽기·덮어쓰기·추가

| 모드 | 동작 | 파일이 없으면 | 파일이 이미 있으면 |
| --- | --- | --- | --- |
| `'r'`, `'rt'` | 텍스트 읽기 | `FileNotFoundError` | 내용 유지 |
| `'w'`, `'wt'` | 텍스트 쓰기 | 새로 생성 | **open 시 기존 내용 삭제** |
| `'a'`, `'at'` | 텍스트 끝에 추가 | 새로 생성 | 기존 내용 뒤에 이어 씀 |
| `'rb'` | 바이너리 읽기 | `FileNotFoundError` | 내용 유지 |
| `'wb'` | 바이너리 쓰기 | 새로 생성 | 기존 내용 삭제 |

`'r'`와 `'t'`가 기본값이다. `open("hello.txt")`는 기본적으로 텍스트 읽기다. 파일을 만들 수 있어도 **상위 폴더가 없으면** 여전히 오류가 날 수 있다.

**텍스트 모드**는 `str`, **바이너리 모드**는 `bytes`를 읽고 쓴다. `encoding`은 텍스트에서 문자와 바이트 사이 변환을 지정한다. 한글 파일은 실제 저장 인코딩과 맞춰 `encoding="utf-8"` 등을 명시한다. 파일이 UTF-8이 아닌데 UTF-8로 읽으면 `UnicodeDecodeError`가 날 수 있다.

### 10.2 w와 a의 차이 확인

아래는 실습용 `mode_demo.txt`를 만들고 덮어쓴다.

```python
with open("mode_demo.txt", "w", encoding="utf-8") as fobj:
    fobj.write("first\n")

with open("mode_demo.txt", "a", encoding="utf-8") as fobj:
    fobj.write("second\n")

with open("mode_demo.txt", "r", encoding="utf-8") as fobj:
    print(repr(fobj.read()))  # 'first\nsecond\n'

with open("mode_demo.txt", "w", encoding="utf-8") as fobj:
    fobj.write("replacement\n")

with open("mode_demo.txt", "r", encoding="utf-8") as fobj:
    print(repr(fobj.read()))  # 'replacement\n'
```

<a id="file-path"></a>

### 10.3 FileNotFoundError — 현재 폴더와 스크립트 폴더는 다를 수 있다

`open("sensor_data.txt")`는 일반적으로 **현재 작업 폴더(current working directory)에서** 찾는다. `.py` 파일 옆에서 자동으로 찾는다는 뜻이 아니다.

```python
from pathlib import Path

print(Path.cwd())  # 실행한 프로세스의 현재 작업 폴더
```

스크립트 옆에 있는 파일을 읽으려면 다음처럼 기준 경로를 잡는다. 이 블록은 **`.py` 파일에 저장해서 실행**하며, 그 옆에 `hello.txt`를 둔다.

```python
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

with open(BASE_DIR / "hello.txt", "r", encoding="utf-8") as fobj:
    print(fobj.read(), end="")
```

`__file__`은 실행 파일의 경로다. 일반 대화형 콘솔이나 노트북에는 없을 수 있다. `/`는 여기서는 `Path`의 경로 결합 연산이고, 숫자 나눗셈이 아니다.

Windows 경로를 문자열로 직접 쓸 때는 역슬래시 이스케이프도 주의한다.

```text
r"C:\Users\Alex\Documents\hello.txt"   # raw 문자열
"C:/Users/Alex/Documents/hello.txt"     # 슬래시 사용
"C:\\Users\\Alex\\Documents\\hello.txt"  # 역슬래시 이스케이프
```

<a id="read"></a>

## 11. 텍스트 읽기 — readline / readlines / read / 파일 순회

다음 공통 준비 코드를 한 번 실행하면 읽기 예제에 쓸 **`hello.txt`가** 만들어진다. 첫 줄, 빈 줄, 마지막 줄이 있으며 마지막 줄 끝에는 줄바꿈이 없다.

```python
with open("hello.txt", "w", encoding="utf-8") as fobj:
    fobj.write("Ava,10,20\n\nBen,5,15")
```

### 11.1 읽기 메서드의 반환값 비교

| 코드 | 반환 타입 | 읽는 범위 | EOF일 때 |
| --- | --- | --- | --- |
| `fobj.readline()` | `str` | 다음 한 줄 | `''` |
| `fobj.readlines()` | `list[str]` | 남은 모든 줄 | `[]` |
| `fobj.read()` | `str` | 남은 전체 텍스트 | `''` |
| `for line in fobj` | 매 반복에서 `str` | 한 줄씩 | 반복 종료 |

**읽기는 파일의 현재 위치에서 진행한다.** 한 번 전부 읽은 파일 객체에서 다시 `read()`하면 처음으로 돌아가지 않고 `''`가 나온다. 다시 열거나 `seek(0)`으로 위치를 돌려야 한다.

<a id="eof"></a>

### 11.2 빈 줄과 EOF는 다르다 — repr로 확인

```python
with open("hello.txt", "r", encoding="utf-8") as fobj:
    print(repr(fobj.readline()))  # 'Ava,10,20\n'
    print(repr(fobj.readline()))  # '\n': 빈 줄이지만 EOF는 아님
    print(repr(fobj.readline()))  # 'Ben,5,15': 마지막 줄에 \n이 없을 수도 있음
    print(repr(fobj.readline()))  # '': EOF
```

**`repr()`은 `\n` 같은 보이지 않는 문자를 확인할 때 유용**하다. `readline()`은 줄바꿈 문자가 있으면 포함하여 반환한다. 마지막 줄에는 없을 수도 있다.

EOF(End of File)에 도달했을 때 일반적인 파일 `readline()`은 `''`, 바이너리 `read()`는 `b''`를 반환한다. **이를 `EOFError`와 혼동하지 않는다.** `input()`이 더 이상 입력을 받을 수 없을 때 발생하는 `EOFError`와는 다른 동작이다.

<a id="read-while"></a>

### 11.3 while + readline — 현재 줄 처리 후 다음 줄 읽기

```python
fobj = open("hello.txt", "r", encoding="utf-8")
line = fobj.readline()

while line != "":
    print(line, end="")
    line = fobj.readline()

fobj.close()
```

흐름은 **처음 한 줄 읽기 → 그 줄 처리 → 다음 줄 읽기**다. 반복문 첫머리에서 또 읽으면 첫 줄을 건너뛴다. 위 코드는 직접 `close()`하는 형태다. `with`를 쓰면 예외가 발생할 때의 정리까지 간단해진다.

**주의:** 빈 줄을 무시하려고 `continue`할 때 다음 줄을 읽지 않으면 같은 빈 줄을 계속 처리할 수 있다. 파일을 직접 순회하는 아래 형태라면 그 실수를 줄일 수 있다.

### 11.4 for line in fobj — 줄 단위 처리

```python
with open("hello.txt", "r", encoding="utf-8") as fobj:
    for line in fobj:
        print(line, end="")
```

파일 전체를 리스트로 만들지 않고 한 줄씩 처리한다. 큰 파일에서 `readlines()`로 모두 담는 것보다 메모리 사용을 줄일 수 있다.

`print(line)`은 `line` 안의 `\n` 뒤에 `print()`의 줄바꿈을 하나 더 붙일 수 있다. 원래 줄바꿈을 유지하려면 **`print(line, end="")`를** 사용한다.

### 11.5 readlines — 줄 리스트

```python
with open("hello.txt", "r", encoding="utf-8") as fobj:
    lines = fobj.readlines()

print(lines)  # ['Ava,10,20\n', '\n', 'Ben,5,15']
print(len(lines))  # 3: 빈 줄도 하나의 줄
```

**`readlines()`가 리스트를 반환한다고 자동으로 줄바꿈을 제거하는 것은 아니다.**

### 11.6 파일 위치 확인과 seek

```python
with open("hello.txt", "r", encoding="utf-8") as fobj:
    first = fobj.read()
    second = fobj.read()
    print(repr(second))  # ''

    fobj.seek(0)
    print(fobj.read() == first)  # True
```

<a id="strip-split"></a>

## 12. strip / split / 빈 줄 제외

파일 줄을 데이터로 변환할 때 자주 함께 쓰는 문자열 처리다.

### 12.1 strip은 양끝 정리, split은 구분자로 나누기

```python
line = "  Ava , 10 , 20  \n"

print(line.strip())  # Ava , 10 , 20
print(line.strip().split(","))  # ['Ava ', ' 10 ', ' 20']

fields = [field.strip() for field in line.split(",")]
print(fields)  # ['Ava', '10', '20']
```

`line.strip()`은 줄 전체 양끝만 정리한다. **각 필드의 공백까지 제거하려면 필드마다 `strip()`한다**. 문자열은 불변이므로 반환값을 사용해야 한다. `line.strip()`만 호출하고 결과를 버리면 원래 `line`은 바뀌지 않는다.

### 12.2 빈 줄은 먼저 제외

```python
with open("hello.txt", "r", encoding="utf-8") as fobj:
    for line in fobj:
        if not line.strip():
            continue
        fields = [field.strip() for field in line.split(",")]
        print(fields)
# ['Ava', '10', '20']
# ['Ben', '5', '15']
```

`for line in fobj`가 다음 줄로 이동하므로 여기서는 `continue` 앞에 `readline()`을 추가하지 않는다. 빈 줄을 오류 개수에 포함하지 않으려면 숫자 변환과 오류 집계 전에 제외한다.

### 12.3 측정값이 없는 경우도 직접 검사

```python
fields = ["Ava"]
values = [float(field) for field in fields[1:]]
print(values)  # []: 예외가 발생하지 않는다.
```

**빈 리스트를 순회하는 comprehension은 그냥 빈 리스트를 만든다.** 측정값이 최소 하나 있어야 한다면 `len(fields) < 2`를 검사해 직접 오류를 발생시켜야 한다. `Ava,`는 빈 문자열 `''`를 숫자로 변환하려 하므로 `ValueError`가 발생한다.

<a id="write"></a>

## 13. 텍스트 쓰기 — write / writelines / 줄바꿈

### 13.1 write는 문자열 하나를 받는다

```python
sensor = "Ava"
average = 24.0

with open("summary_demo.txt", "w", encoding="utf-8") as fobj:
    count = fobj.write(f"{sensor}: average = {average:.2f}\n")

print(count)  # 21: 쓴 문자열의 문자 수
```

`fobj.write(text)`는 **문자열 하나**를 받아 쓰고 문자 수를 반환한다. 여러 인자를 따로 받는 `print()`와 다르다. 숫자나 리스트를 쓰려면 먼저 문자열로 표현한다.

```text
fobj.write("평균:", average)       # 오류: 인자 두 개
fobj.write(average)                # 오류: float를 직접 전달
fobj.write(f"평균: {average}\n")   # 문자열 하나로 만들어 전달
```

`write()`는 **줄바꿈을 자동으로 붙이지 않는다.** 줄마다 구분하려면 문자열 끝에 `\n`을 넣는다. `f"{average:.2f}"`는 소수 둘째 자리까지 표시하며, 평균 변수 자체를 바꾸지 않는다.

### 13.2 여러 문자열을 한 줄씩 쓰기

```python
names = ["Jill", "Jack", "Joe", "Jennifer"]

with open("names_demo.txt", "w", encoding="utf-8") as fobj:
    for name in names:
        fobj.write(name + "\n")

with open("names_demo.txt", "r", encoding="utf-8") as fobj:
    print(repr(fobj.read()))
# 'Jill\nJack\nJoe\nJennifer\n'
```

### 13.3 writelines도 줄바꿈을 만들지 않는다

```python
with open("joined_demo.txt", "w", encoding="utf-8") as fobj:
    fobj.writelines(["Ava", "Ben"])

with open("joined_demo.txt", "r", encoding="utf-8") as fobj:
    print(repr(fobj.read()))  # 'AvaBen'

with open("joined_demo.txt", "w", encoding="utf-8") as fobj:
    fobj.writelines(["Ava\n", "Ben\n"])

with open("joined_demo.txt", "r", encoding="utf-8") as fobj:
    print(repr(fobj.read()))  # 'Ava\nBen\n'
```

이름이 `writelines`라고 해서 자동으로 각 항목을 한 줄로 쓰는 것은 아니다. **각 문자열에 `\n`이 있어야 한다.** 리스트뿐 아니라 문자열들을 제공하는 iterable도 받을 수 있다.

### 13.4 리스트를 출력 형식으로 바꾸기

```python
selected_sensors = ["Ava", "Ben"]

with open("selected_demo.txt", "w", encoding="utf-8") as fobj:
    fobj.write(f"Sensors: {selected_sensors}\n")
    fobj.write("Names: " + ", ".join(selected_sensors) + "\n")

with open("selected_demo.txt", "r", encoding="utf-8") as fobj:
    print(fobj.read(), end="")
# Sensors: ['Ava', 'Ben']
# Names: Ava, Ben
```

f-string에 리스트를 넣으면 대괄호와 따옴표가 포함된 리스트 표현이 나온다. 구분자로 이름만 연결하고 싶으면 문자열의 `join()`을 사용한다.

### 13.5 파일에서의 print도 가능

```python
with open("print_demo.txt", "w", encoding="utf-8") as fobj:
    print("average =", 24.0, file=fobj)

with open("print_demo.txt", "r", encoding="utf-8") as fobj:
    print(repr(fobj.read()))  # 'average = 24.0\n'
```

`print(..., file=fobj)`는 여러 인자를 받고 기본 줄바꿈도 넣는다. 문제에서 `write()` 사용을 요구하면 그 요구대로 작성한다.

<a id="binary"></a>

## 14. 바이너리 파일 — bytes / rb / wb / hex

텍스트는 문자를 인코딩·디코딩해서 다루지만 바이너리는 **바이트 열 자체**를 다룬다. 이미지나 임의의 이진 데이터를 읽을 때 사용한다.

### 14.1 bytes.fromhex와 hex

```python
data = bytes.fromhex("F0 45 2B C8")
print(type(data).__name__)  # bytes
print(len(data))           # 4: 바이트 수
print(data.hex())          # f0452bc8
print(bytes.hex(data))     # f0452bc8: 같은 결과
```

16진수 두 자리가 바이트 하나를 나타낸다. `bytes.fromhex()`는 16진수 문자열을 `bytes`로 만들고, `.hex()`는 다시 읽기 쉬운 16진수 문자열을 만든다.

### 14.2 파일에 쓰고 다시 읽기

```python
original = bytes.fromhex("F0 45 2B C8")

with open("binary_demo.bin", "wb") as fobj:
    written = fobj.write(original)

with open("binary_demo.bin", "rb") as fobj:
    data = fobj.read(4)
    remaining = fobj.read(4)

print(written)           # 4: 쓴 바이트 수
print(data.hex())        # f0452bc8
print(data == original)  # True
print(remaining)         # b'': EOF
```

**`read(4)`는 최대 4바이트를 읽는다.** 남은 데이터가 2바이트뿐이면 2바이트만 반환한다. 개수를 생략한 `read()`는 남은 데이터를 전부 읽는다.

바이너리 모드에서는 `encoding="utf-8"`을 지정하지 않는다. `wb`로 연 파일에는 문자열이 아니라 `bytes`를 전달한다.

```text
open("data.bin", "rb", encoding="utf-8")  # 오류: 바이너리에 encoding 지정
fobj.write("hello")                      # wb 파일에는 str을 쓸 수 없음
fobj.write(b"hello")                     # bytes라면 가능
```

### 14.3 문자와 바이트 변환 — encode / decode

```python
text = "한글"
encoded = text.encode("utf-8")
decoded = encoded.decode("utf-8")

print(len(text))     # 2: 문자 수
print(len(encoded))  # 6: UTF-8 바이트 수
print(decoded)       # 한글
```

`str.encode()`는 문자열 → 바이트, `bytes.decode()`는 바이트 → 문자열이다. 바이트 수와 문자 수는 같지 않을 수 있다. 파일을 텍스트 모드로 열면 이런 인코딩·디코딩을 파일 객체가 맡는다.

<a id="with"></a>

## 15. with — context manager와 자동 close

파일은 읽기·쓰기가 끝나면 닫아야 한다. 직접 `close()`를 호출하는 대신 **정리 작업을 보장하는 문맥 관리자(context manager)를** 사용할 수 있다. `open()`이 반환하는 파일 객체는 문맥 관리자로 동작한다.

```text
with open(path, mode, encoding="utf-8") as fobj:
    파일을_사용하는_코드
# with 블록에서 나왔으므로 파일은 닫힌 상태
```

### 15.1 블록을 나오면 닫힌다

```python
with open("hello.txt", "r", encoding="utf-8") as fobj:
    print(fobj.closed)  # False
    first_line = fobj.readline()

print(fobj.closed)      # True
print(first_line.strip())  # Ava,10,20
```

`fobj`라는 변수 이름은 블록 밖에서도 남을 수 있지만 **파일은 이미 닫혀 있다.** 닫힌 파일 객체로 다시 읽거나 쓰려고 하면 `ValueError`가 발생한다. 읽어 놓은 문자열인 `first_line`은 그대로 사용할 수 있다.

### 15.2 처리 도중 예외가 나도 정리

```python
try:
    with open("hello.txt", "r", encoding="utf-8") as fobj:
        raise ValueError("파일 처리 중 문제")
except ValueError:
    print(fobj.closed)  # True
```

파일 열기가 성공해서 `with` 본문에 들어왔다면, 본문을 예외나 `return` 등으로 나갈 때도 파일 정리가 수행된다. **열기 자체가 실패하면 정리할 열린 파일이 없다.** 이때 `fobj`가 대입되었다고 가정하지 않는다.

### 15.3 with는 오류를 잡는 문법이 아니다

```python
try:
    with open("missing_example.txt", "r", encoding="utf-8") as fobj:
        print(fobj.read())
except FileNotFoundError:
    print("입력 파일을 찾을 수 없습니다.")
except OSError as exc:
    print(f"그 밖의 파일 오류: {exc}")
```

`with`는 자원 정리, `try/except`는 오류에 대한 대응을 맡는다. 파일이 없으면 여전히 `FileNotFoundError`가 발생한다. 구체적인 `FileNotFoundError`를 부모인 `OSError`보다 먼저 적는다.

### 15.4 읽는 파일과 쓰는 파일을 함께 열기

```python
with open("hello.txt", "r", encoding="utf-8") as source:
    with open("copy_demo.txt", "w", encoding="utf-8") as target:
        for line in source:
            target.write(line)

print(source.closed, target.closed)  # True True
```

두 파일 모두 블록을 나올 때 닫힌다. 이 예제는 텍스트 복사이며, 이미지 같은 바이너리 데이터는 `rb`와 `wb`로 처리해야 한다.

<a id="sensor-example"></a>

## 16. 종합 예제 — 센서 파일 검증과 summary.txt

**목표:** 파일을 읽고, 빈 줄을 제외하고, 잘못된 줄은 전체를 버리며, 같은 센서의 값을 누적한다. 그다음 평균을 내림차순으로 정렬해 파일에 보고서를 쓴다.

작업 폴더에 **`sensor_data.txt`를** 다음 내용으로 저장한다. `Bad`는 숫자 변환 실패, `NoValues`는 측정값 없음, `,1,2`는 이름 없음이다. 빈 줄은 오류가 아니다.

```text
Ava,10,20,30
Ben,5,15,25
Ava,20,40
Cara,8,12,16
Bad,3,hello,4

NoValues
,1,2
```

아래 전체 코드는 **같은 폴더의 `.py` 파일에 저장하여 실행**한다.

```python
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

class InvalidDataError(Exception):
    pass

def load_readings(filename):
    data = {}
    error = 0

    with open(filename, "r", encoding="utf-8") as fobj:
        for line in fobj:
            if not line.strip():
                continue

            fields = [field.strip() for field in line.split(",")]
            name = fields[0]

            try:
                if not name:
                    raise InvalidDataError("센서 이름이 없습니다.")
                if len(fields) < 2:
                    raise InvalidDataError("측정값이 없습니다.")
                values = [float(field) for field in fields[1:]]
            except (InvalidDataError, ValueError):
                error += 1
            else:
                if name in data:
                    data[name].extend(values)
                else:
                    data[name] = values

    return data, error

def calculate_average(values):
    return sum(values) / len(values)

def write_summary(filename, data, error):
    averages = {
        name: calculate_average(values)
        for name, values in data.items()
    }
    sorted_data = sorted(
        averages.items(), key=lambda pair: pair[1], reverse=True
    )
    selected = [name for name, avg in averages.items() if avg >= 15.0]

    with open(filename, "w", encoding="utf-8") as fobj:
        for number, (name, avg) in enumerate(sorted_data, start=1):
            status = "HIGH" if avg >= 20.0 else "LOW"
            fobj.write(
                f"{number}. {name}: count = {len(data[name])}, "
                f"average = {avg:.2f}, status = {status}\n"
            )
        fobj.write(f"Invalid lines: {error}\n")
        fobj.write(f"Sensors with average >= 15.0: {selected}\n")

def main():
    try:
        data, error = load_readings(BASE_DIR / "sensor_data.txt")
        write_summary(BASE_DIR / "summary.txt", data, error)
    except OSError as exc:
        print(f"파일 입출력 오류: {exc}")
    else:
        print(f"보고서 저장 완료. 잘못된 줄: {error}")

if __name__ == "__main__":
    main()
```

`summary.txt` 내용:

```text
1. Ava: count = 5, average = 24.00, status = HIGH
2. Ben: count = 3, average = 15.00, status = LOW
3. Cara: count = 3, average = 12.00, status = LOW
Invalid lines: 3
Sensors with average >= 15.0: ['Ava', 'Ben']
```

**핵심 설계:** 숫자 변환이 모두 성공한 뒤에만 `else`에서 저장한다. 파일 자체를 열거나 쓰지 못하는 문제는 바깥 `OSError` 처리기로 전달한다. 함수는 전체 스크립트에 의존하지 않도록 파일 경로를 매개변수로 받고, 실행 진입점에서 `BASE_DIR`을 붙인다.

테스트할 때는 정상 예제뿐 아니라 아래 입력도 확인한다.

| 테스트 입력 | 기대 동작 |
| --- | --- |
| 빈 파일 | 센서 없음, 오류 0, 마지막 요약 두 줄 작성 |
| 빈 줄·공백만 있는 줄 | 센서에도 오류에도 추가하지 않음 |
| `Ava,10` | 측정값 하나인 정상 줄 |
| 같은 센서 이름 반복 | 기존 리스트에 값 추가 |
| `Bad,1,hello,3` | 일부도 저장하지 않고 오류 1 증가 |
| `NoValues` 또는 `Ava,` | 잘못된 줄로 집계 |
| `,1,2` | 빈 이름으로 저장하지 않고 오류 집계 |
| 입력 파일 없음 | 파일 오류 메시지, 보고서 작성 중단 |

센서 이름은 사람 이름인지 판별하지 않는다. `Sensor_01`이나 `123`을 금지하는 별도 규칙이 없다면 문자열 이름으로 쓸 수 있다.

<a id="pitfalls"></a>

## 17. 실수 점검표 — 증상으로 찾기

| 증상 / 잘못된 가정 | 원인과 수정 |
| --- | --- |
| Python에서 `try/catch` | Python 키워드는 `try/except` |
| 오류 메시지 문자열로 except 작성 | 메시지가 아니라 예외 클래스로 매칭 |
| `raise`하면 메시지만 출력하고 계속? | 정상 흐름을 중단하고 처리기로 이동 |
| custom exception을 만들었는데 float 오류가 안 잡힘 | `float()`는 `ValueError`; 함께 잡거나 변환해서 다시 raise |
| `except ValueError or TypeError` | 튜플 `(ValueError, TypeError)`로 작성 |
| 부모 예외 except를 먼저 둠 | 자식 예외도 먼저 잡아 버림. 구체적인 예외부터 |
| 예외 처리 후 실패한 try 줄부터 다시 실행? | 아님. 재시도는 반복문으로 직접 작성 |
| 오류 없이 끝났을 때만 할 작업 | `try`의 `else` 사용 |
| `finally` 다음 줄은 무조건 실행? | 미처리 예외가 있으면 정리 후 바깥으로 전파 |
| `open()` 실패 후 `fo.close()` | fo가 없을 수 있음. `with` 또는 초기화와 None 검사 |
| `import my_math.py` | 확장자 없이 `import my_math` |
| `sys.path`에 `.py` 파일 경로를 넣음 | 그 파일을 담은 디렉터리를 넣어야 함 |
| 모듈을 수정했는데 콘솔 결과가 그대로 | import 캐시. 재시작 또는 reload |
| `.pth`를 아무 폴더에 놓음 | `site`가 처리하는 site-packages 위치 확인 |
| 파일이 옆에 있는데 못 찾음 | 현재 작업 폴더와 스크립트 폴더 차이 확인 |
| `'w'`로 열었는데 옛 내용이 사라짐 | 정상 동작. 끝에 추가하려면 `'a'` |
| `readline()`이 끝에 도달하면 EOFError? | 일반적으로 `''` 반환 |
| 빈 줄과 파일 끝을 똑같이 취급 | 빈 줄 `'\n'`과 EOF `''` 구분 |
| 반복문 위·안에서 연속으로 readline | 첫 줄을 건너뛸 수 있음. 처리 후 다음 줄 읽기 |
| 파일 내용을 출력하면 빈 줄이 추가됨 | line의 `\n`과 print의 기본 줄바꿈이 겹침 |
| readlines가 자동으로 줄바꿈 삭제? | 아님. 각 문자열에 남을 수 있음 |
| 두 번째 read가 빈 문자열 | 이미 EOF. 다시 열거나 `seek(0)` |
| strip을 호출했는데 원본 그대로 | 새 문자열을 반환하므로 재대입하거나 반환값 사용 |
| `[float(x) for x in []]`에서 오류 기대 | 빈 리스트가 만들어짐. 값 유무는 직접 검사 |
| `write("평균", average)` | write는 문자열 하나만 받음. f-string으로 결합 |
| writelines면 자동으로 한 줄씩? | 항목에 `\n`을 직접 포함해야 함 |
| rb/wb에 encoding 인자 | 바이너리에서는 지정하지 않음 |
| read(4)는 언제나 길이 4? | 남은 데이터가 적으면 더 짧게 반환 |
| with를 썼으니 파일 없음 오류도 없어짐? | 자동 close와 예외 처리는 별개 |

<a id="sources"></a>

## 18. 공식 문서

- [오류·예외 처리·raise·사용자 정의 예외·finally](https://docs.python.org/3.14/tutorial/errors.html)
- [모듈·검색 경로·독립 실행 진입점](https://docs.python.org/3.14/tutorial/modules.html)
- [site와 .pth 파일](https://docs.python.org/3.14/library/site.html)
- [텍스트·바이너리 파일 읽기와 쓰기](https://docs.python.org/3.14/tutorial/inputoutput.html#reading-and-writing-files)
- [open 함수의 모드와 인코딩](https://docs.python.org/3.14/library/functions.html#open)
