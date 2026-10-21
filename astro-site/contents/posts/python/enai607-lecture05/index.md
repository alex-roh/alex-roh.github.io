---
title: "[ENAI607] Lecture 05 — 클래스, 상속과 센서 객체 만들기"
description: "class·self·__init__·private·리스트 복사·클래스 변수·classmethod·super·오버라이딩·__str__·__eq__·__hash__를 이해하고 Sensor 예상문제를 완성하는 Python 노트"
date: 2026-10-20T03:00:00-04:00
update: 2026-10-20
tags:
  - python
  - ENAI607
series: "ENAI607 Python Programming"
---

센서 이름과 측정값을 묶어서 보관하고, 평균을 구하고, 새 측정값을 추가하고 싶다. 보정 기능이 있는 센서도 필요하지만 같은 코드를 두 번 작성하고 싶지는 않다. 이때 사용할 도구가 **클래스와 상속**이다.

이 글은 객체지향 문법을 처음부터 설명한 뒤, `Sensor`와 `CalibratedSensor`를 직접 만드는 예상문제 2번을 완성한다. 클래스 정의만 읽고 끝내지 않고 **호출 순서, 값이 저장되는 위치, 실행 결과, 잘못 쓰기 쉬운 코드**까지 함께 살펴본다. 개념부터 차례로 읽어도 되고, 필요한 함수 이름을 검색해 바로 찾아도 된다.

**읽는 순서:** 처음이면 1–12절로 문법을 익히고 13–16절에서 센서 문제를 푼다. 마지막 17–18절은 값 비교와 딕셔너리 키까지 포함한 객체 문법 복습이다. 시간이 촉박하면 [요구사항 표](#requirements) → [전체 풀이](#solution) → [검증](#tests) → [실수 점검표](#pitfalls) 순서로 읽는다.

각 짧은 `python` 블록은 필요한 클래스를 포함한 독립 예제다. `text` 블록은 문법 틀이나 예상 출력이다. 전체 풀이는 하나의 `.py` 파일로 실행하며, 별도 테스트 파일도 글 끝에서 받을 수 있다. 예제와 전체 풀이를 Python 3.12에서 실행해 검증했다.

## 빠른 목차 — 문법과 필요한 작업으로 찾기

| 찾는 내용 | 바로가기 |
| --- | --- |
| 핵심 문법 한눈에 보기 | [0. 치트시트](#quick-reference) |
| 클래스·객체·인스턴스·속성·메서드 | [1. 객체의 구성](#objects) |
| `class`, `pass`, 점 연산자 | [2. 빈 클래스와 속성](#empty-class) |
| `__init__`, `self`, 기본 매개변수 | [3. 초기화](#init) |
| `obj.method()`에서 `self`는 어디서 오는가 | [4. 인스턴스 메서드](#instance-methods) |
| `TypeError`, `ValueError`, 잘못된 객체 방지 | [5. 입력 검증](#validation) |
| `__values`, `_Class__values`, 캡슐화 | [6. private와 getter](#private) |
| 입력 리스트·반환 리스트를 둘 다 복사하는 이유 | [7. 복사와 독립성](#copy) |
| `self.x`와 `Class.x`, 공유 리스트 함정 | [8. 클래스 변수](#class-variables) |
| `@classmethod`, `cls`, 생성 개수 세기 | [9. 클래스 메서드](#classmethod) |
| 자식 클래스, `isinstance`, `issubclass` | [10. 상속](#inheritance) |
| `super().__init__`, `super().get_average()` | [11. super와 오버라이딩](#super) |
| `print(obj)`, `__str__`, 소수 둘째 자리 | [12. 객체 출력](#str) |
| 예상문제 2번에서 무엇을 구현해야 하나 | [13. 요구사항과 설계](#requirements) |
| `Sensor`, `CalibratedSensor` 전체 실행 코드 | [14. 전체 풀이](#solution) |
| ID·복사·검증·보정 평균을 줄별로 이해하기 | [15. 풀이 해설](#walkthrough) |
| 자동 테스트와 경계 조건 | [16. 검증](#tests) |
| `==`, `is`, `__eq__`, `NotImplemented` | [17. 객체 비교](#equality) |
| `__hash__`, `Point`, 딕셔너리 키 | [18. 해시](#hash) |
| 자주 틀리는 코드와 원인 | [19. 실수 점검표](#pitfalls) |
| 스스로 풀어볼 질문과 정답 | [20. 확인 문제](#review) |

<a id="quick-reference"></a>

## 0. 핵심 문법 치트시트

아래는 **문법 틀**이다. 실제 실행 코드는 뒤의 예제를 사용한다.

```text
class Sensor:
    next_id = 0                         # 클래스 전체의 공유 정보

    def __init__(self, name, readings):
        self.__name = name              # 객체마다 다른 정보
        self.__values = readings.copy() # 외부 입력과 분리
        self.__id = Sensor.next_id
        Sensor.next_id += 1

    def get_values(self):
        return self.__values.copy()     # 반환할 때도 분리

    @classmethod
    def get_sensor_count(cls):
        return Sensor.next_id

class CalibratedSensor(Sensor):
    def __init__(self, name, readings, scale, offset):
        super().__init__(name, readings)
        self.__scale = scale
        self.__offset = offset

    def get_average(self):
        return self.__scale * super().get_average() + self.__offset
```

> **먼저 기억할 다섯 줄:** `self`는 이번 호출의 객체, `cls`는 호출받은 클래스다. `__init__`는 객체를 초기화하며 계산 결과를 반환하는 함수가 아니다. `__values`도 리스트를 그대로 반환하면 외부에서 바꿀 수 있다. 자식까지 공통 ID를 쓰려면 `Sensor.next_id`를 증가시킨다. `super()`는 부모 객체를 새로 만드는 것이 아니라 같은 객체에 대해 상위 구현을 호출한다.

<a id="objects"></a>

## 1. 클래스와 객체 — 데이터와 기능을 한곳에 묶기

**객체는 데이터와 그 데이터를 다루는 기능을 함께 가진다.** 센서라면 다음과 같이 나눌 수 있다.

| 용어 | 의미 | 센서에서의 예 |
| --- | --- | --- |
| class | 객체를 만드는 정의, 설계 | `Sensor` |
| object / instance | 그 클래스로 만든 실제 객체 | `s1`, `s2`가 가리키는 센서 |
| attribute / field / instance variable | 객체에 저장한 정보 | 이름, ID, 측정값 |
| method | 객체와 관련된 함수 | `get_average()`, `add_value()` |
| instantiation | 새 인스턴스를 만드는 동작 | `Sensor("Ava", [10, 20])` |

`s1`은 객체 자체를 담는 상자라기보다 **객체를 가리키는 이름**이다. 다른 이름을 대입하면 같은 객체를 가리킬 수도 있다. 이 때문에 객체를 독립적으로 만드는 것과 기존 객체에 이름을 하나 더 붙이는 것을 구분해야 한다.

```python
class Sensor:
    def __init__(self, name):
        self.name = name

s1 = Sensor("Ava")
same_sensor = s1
s2 = Sensor("Ben")

same_sensor.name = "Changed"
print(s1.name)        # Changed
print(s2.name)        # Ben
print(s1 is same_sensor)  # True
print(s1 is s2)           # False
```

`s1`과 `same_sensor`는 같은 객체를 가리키므로 한쪽에서 바꾼 이름이 다른 쪽에서도 보인다. 반면 `s2`는 따로 생성한 객체다.

객체지향의 두 가지 주요 도구도 함께 기억한다.

- **캡슐화:** 사용자는 메서드를 통해 기능을 사용하고, 내부 저장 방식과 검증 규칙은 클래스가 관리한다.
- **상속:** 이미 있는 클래스의 기능을 이어받아 더 구체적인 클래스를 만든다. 같은 코드의 중복을 줄인다.

<a id="empty-class"></a>

## 2. `class`, `pass`, 점 연산자

처음에는 빈 클래스를 만들고 객체에 속성을 붙일 수 있다.

```python
class Circle:
    pass

circle = Circle()
circle.x = 3.0
circle.y = -1.0
circle.radius = 5.0

print(circle.x)                         # 3.0
print(f"{2 * 3.14 * circle.radius:.2f}") # 31.40

circle.radius = 2.0
print(f"{2 * 3.14 * circle.radius:.2f}") # 12.56
```

`pass`는 “아직 실행할 내용이 없다”는 자리 표시다. `class Circle:` 다음에 들여쓴 본문이 필요하므로 사용한다. `Circle()`이 객체를 만들고, `circle.radius`의 점은 그 객체의 속성을 지정한다.

이 방식은 간단한 기록에는 쓸 수 있지만, 사용자가 `radius`를 붙이는 일을 잊으면 해당 속성이 없다. 생성될 때 필요한 상태를 한 번에 만들기 위해 `__init__`를 쓴다.

<a id="init"></a>

## 3. `__init__`와 `self` — 생성될 때 초기화하기

### 3.1 매개변수 `radius`와 속성 `self.radius`는 다르다

```python
class Circle:
    def __init__(self, radius, x=0.0, y=0.0):
        self.radius = radius
        self.x = x
        self.y = y

c1 = Circle(1.0)
c2 = Circle(2.0, 1.0, -1.0)

print(c1.radius, c1.x, c1.y)  # 1.0 0.0 0.0
print(c2.radius, c2.x, c2.y)  # 2.0 1.0 -1.0
```

`Circle(1.0)`을 호출하면 새 객체에 대해 `__init__`가 실행된다. `self`에는 그 객체가 자동으로 전달되고, `radius`에는 `1.0`이 전달된다. `x`, `y`는 생략했으므로 기본값을 사용한다.

`self.radius = radius`를 오른쪽부터 읽으면 다음과 같다.

1. 매개변수 `radius`로 전달받은 값을 읽는다.
2. `self`가 가리키는 객체의 `radius` 속성에 저장한다.
3. 메서드 실행이 끝나도 객체를 통해 그 값을 사용할 수 있다.

반면 `radius = radius`라고만 쓰면 지역 이름에 대입할 뿐 객체 속성을 만들지 않는다. 클래스 내부라고 해서 `self.`가 자동으로 붙지는 않는다.

### 3.2 `self`를 생성 호출에 직접 넣지 않는다

| 정의 | 올바른 호출 | 전달되는 의미 |
| --- | --- | --- |
| `__init__(self, radius)` | `Circle(2.0)` | 새 객체는 자동, `radius=2.0` |
| `set_radius(self, radius)` | `c.set_radius(3.0)` | `self=c`, `radius=3.0` |
| `area(self)` | `c.area()` | `self=c` |

`self`는 관례적인 이름이지 특별한 예약어는 아니다. 그렇지만 읽는 사람과 도구가 익숙한 이름이므로 그대로 사용하는 편이 좋다.

**정확한 구분:** 보통 `__init__`를 생성자라고 부르지만, 엄밀하게는 이미 생성된 객체의 초기화 메서드다. 이 단계에서는 `__new__`를 구현할 필요가 없다. `__init__`에서 `return 123`처럼 값을 반환하면 `TypeError`가 발생한다. 초기화할 속성을 저장하고 끝내면 된다.

<a id="instance-methods"></a>

## 4. 인스턴스 메서드 — 이번 객체의 데이터를 다루기

```python
class Circle:
    def __init__(self, radius):
        self.radius = radius

    def set_radius(self, radius):
        self.radius = radius

    def area(self):
        return 3.14 * self.radius ** 2

c = Circle(2.0)
print(c.area())        # 12.56
c.set_radius(10.0)
print(c.area())        # 314.0
print(Circle.area(c))  # 314.0
```

`c.area()`는 이 예제에서 `Circle.area(c)`와 같은 객체를 대상으로 실행된다. 점 앞의 `c`가 메서드의 첫 매개변수 `self`로 전달되는 것이다.

`area`는 결과를 `return`하므로 `result = c.area()`처럼 값을 받아 계산에 사용할 수 있다. `set_radius`는 속성만 바꾸고 명시적인 반환값이 없으므로 `None`을 반환한다. `c = c.set_radius(10)`처럼 쓰면 `c`가 `None`이 되어 버린다.

또한 `c.area`는 메서드 자체이고, `c.area()`는 실행한 결과다. 괄호가 빠지면 계산하지 않는다.

<a id="validation"></a>

## 5. 입력 검증 — 잘못된 상태의 객체를 만들지 않기

센서의 측정값은 숫자이고 음수가 아니어야 한다고 하자. 숫자가 아닌 값과 숫자이지만 허용 범위를 벗어난 값은 구분한다.

| 입력 | 문제 | 예외 |
| --- | --- | --- |
| `"hello"`, `[1, 2]` | 필요한 숫자 타입이 아님 | `TypeError` |
| `-3`, `-0.5` | 숫자이지만 음수 | `ValueError` |
| `0`, `2`, `2.5` | 유효한 측정값 | 허용 |

```python
class Reading:
    def __init__(self, value):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError("value must be numeric")
        if not value >= 0:
            raise ValueError("value must be nonnegative")
        self.value = value

for value in [0, 2.5, "hello", -3]:
    try:
        reading = Reading(value)
        print("OK:", reading.value)
    except (TypeError, ValueError) as exc:
        print(type(exc).__name__, str(exc))
```

```text
OK: 0
OK: 2.5
TypeError value must be numeric
ValueError value must be nonnegative
```

**왜 타입을 먼저 검사할까?** `"hello" < 0` 같은 비교는 그 자체로 오류다. 먼저 허용한 숫자 타입인지 확인하고, 그다음 범위를 확인하면 오류 원인을 분명히 할 수 있다.

이 글의 센서 구현에서는 numeric을 기본 숫자 타입인 `int`, `float`로 다룬다. `bool`은 `int`의 하위 클래스지만 측정값으로 받지 않는 정책을 명시적으로 적용했다. 문제에 별도 숫자 타입이나 bool 허용 기준이 제시되면 그 기준에 맞춘다. 문자열 `"3"`을 자동으로 숫자 3으로 바꾸지는 않는다.

`if not value >= 0:`는 `if not (value >= 0):`와 같다. 보통 숫자에서는 음수 검사와 같고, `float("nan")`처럼 0 이상이라는 비교가 참이 아닌 값도 거부한다. 일반적인 양수·음수만 다룰 때는 `if value < 0:`가 더 익숙한 표현이다.

검증은 생성할 때만 필요한 것이 아니다. `add_value()`처럼 나중에 데이터를 추가하는 메서드에서도 같은 규칙을 적용해야 한다. **검증을 통과한 뒤에 실제 데이터를 바꾼다.**

<a id="private"></a>

## 6. private 변수와 캡슐화

### 6.1 `name`, `_name`, `__name`의 차이

| 이름 예 | 의미 |
| --- | --- |
| `self.name` | 외부에서 보통 직접 접근하는 공개 속성 |
| `self._name` | 내부용으로 다루라는 관례. 접근은 가능 |
| `self.__name` | 이름 맹글링 적용. 우발적인 직접 접근·이름 충돌을 줄임 |
| `__init__`, `__str__` | 앞뒤에 밑줄 두 개가 있는 특별 메서드 이름 |

`__values`와 `__init__`는 같은 종류의 이름이 아니다. private 스타일의 맹글링은 앞에 밑줄 두 개가 있고 뒤에는 같은 두 개가 없는 이름에 적용된다.

```python
class MyClass:
    def __init__(self, x, y):
        self.x = x
        self.__y = y

    def get_y(self):
        return self.__y

obj = MyClass(1, 2)
print(obj.x)       # 1
print(obj.get_y()) # 2

try:
    print(obj.__y)
except AttributeError:
    print("direct access failed")

print(obj._MyClass__y)  # 2: 원리를 보여주는 예, 일반 사용법은 아님
```

`MyClass` 안의 `__y`는 대체로 `_MyClass__y`라는 이름으로 바뀐다. 이것이 **name mangling**이다. Java나 C++의 접근 제한자처럼 외부 접근을 보안적으로 차단하는 기능은 아니다. 사용자는 `get_y()`라는 공개 인터페이스를 통해 사용하는 것이 의도된 방식이다.

### 6.2 이름만 가려서는 데이터 보호가 끝나지 않는다

`self.__values`라는 이름을 사용해도 getter가 내부 리스트 자체를 반환하면 외부에서 리스트 내용을 바꿀 수 있다. **private 이름과 리스트 복사는 서로 다른 문제를 해결한다.**

<a id="copy"></a>

## 7. 리스트 복사 — 입력과 반환, 두 군데가 중요하다

### 7.1 생성할 때 입력 리스트를 그대로 저장하면

```python
class BadSensor:
    def __init__(self, readings):
        self.__values = readings

    def get_values(self):
        return self.__values

source = [10, 20]
sensor = BadSensor(source)
source[0] = -999
print(sensor.get_values())  # [-999, 20]

exported = sensor.get_values()
exported.append(777)
print(sensor.get_values())  # [-999, 20, 777]
```

외부 코드가 센서의 검증 메서드를 한 번도 부르지 않았는데 내부 값이 바뀌었다. `source`, `self.__values`, `exported`가 같은 리스트를 가리키기 때문이다.

### 7.2 생성할 때 복사하고, 반환할 때도 복사한다

```python
class SafeSensor:
    def __init__(self, readings):
        self.__values = readings.copy()

    def get_values(self):
        return self.__values.copy()

source = [10, 20]
sensor = SafeSensor(source)
source[0] = -999

exported = sensor.get_values()
exported.append(777)

print(source)              # [-999, 20]
print(exported)            # [10, 20, 777]
print(sensor.get_values()) # [10, 20]
```

| 복사 위치 | 막는 문제 |
| --- | --- |
| `__init__`의 `readings.copy()` | 호출자가 원래 입력 리스트를 나중에 수정함 |
| `get_values()`의 `self.__values.copy()` | 호출자가 반환받은 리스트를 수정함 |

이 문제의 원소는 숫자라서 얕은 복사인 `.copy()`로 충분하다. 리스트 안에 다시 가변 리스트가 들어가는 구조라면 내부 객체 공유도 따로 생각해야 한다.

<a id="class-variables"></a>

## 8. 인스턴스 변수와 클래스 변수

### 8.1 각 객체의 이름과 전체의 카운터

```python
class Counter:
    total = 0

    def __init__(self, name):
        self.name = name
        Counter.total += 1

a = Counter("Ava")
b = Counter("Ben")

print(a.name, b.name)           # Ava Ben
print(Counter.total)           # 2
print(a.total, b.total)        # 2 2
```

`self.name`은 각 객체에 저장된다. `Counter.total`은 클래스에 저장된다. 객체에서 `a.total`을 읽을 때 그 객체에 같은 이름의 속성이 없으면 클래스의 값을 찾을 수 있다.

### 8.2 `self.total += 1`은 왜 다른가

```python
class WrongCounter:
    total = 0

    def __init__(self):
        self.total += 1

a = WrongCounter()
b = WrongCounter()
print(WrongCounter.total) # 0
print(a.total, b.total)   # 1 1
```

`self.total += 1`은 값을 읽은 다음 결과를 `self.total`에 대입한다. 여기서는 클래스의 0을 읽고, 각 인스턴스에 1을 저장하여 클래스 속성을 가려 버렸다. 전체 개수를 세려면 의도한 공유 변수에 직접 대입해야 한다.

### 8.3 가변 리스트를 클래스 변수로 두는 함정

```python
class BadBucket:
    values = []

a = BadBucket()
b = BadBucket()
a.values.append(10)
print(b.values)  # [10]
```

두 객체가 클래스의 같은 리스트를 사용한다. 객체별 리스트가 필요하면 `__init__` 안에서 `self.values = []`처럼 각 객체에 새 리스트를 만든다. 센서 전체가 공유해야 하는 값은 ID 카운터이고, **측정값 리스트는 센서마다 따로 가져야 한다.**

<a id="classmethod"></a>

## 9. `@classmethod`와 `cls`

### 9.1 객체가 없어도 호출할 수 있는 메서드

```python
class Account:
    interest = 0.03

    def __init__(self, amount):
        self.amount = amount

    def get_amount(self):
        return (1 + Account.interest) * self.amount

    @classmethod
    def set_interest(cls, interest):
        cls.interest = interest

Account.set_interest(0.10)
account = Account(100)
print(Account.interest)      # 0.1
print(f"{account.get_amount():.1f}")  # 110.0
```

`@classmethod`는 바로 아래 함수를 클래스 메서드로 만든다. `Account.set_interest(0.10)`에서는 `cls`에 `Account`가 자동으로 전달된다. 이 예제처럼 객체를 만들기 전에 호출해도 된다.

| 종류 | 첫 매개변수 | 자동으로 받는 대상 | 센서 예 |
| --- | --- | --- | --- |
| 인스턴스 메서드 | `self` | 특정 객체 | `s1.add_value(40)` |
| 클래스 메서드 | `cls` | 호출받은 클래스 | `Sensor.get_sensor_count()` |

클래스 메서드에는 특정 센서 객체가 자동으로 전달되지 않는다. 따라서 `self.__values`를 사용해 “어느 센서의 평균”을 구할 수는 없다. 다른 객체를 매개변수로 받거나 새 객체를 만드는 것은 가능하지만, 이 문제의 개수 조회에는 필요하지 않다.

### 9.2 센서 문제에서는 왜 `return Sensor.next_id`인가

일반적인 클래스 메서드는 `cls.variable`로 해당 클래스를 다루는 것이 자연스럽다. 하지만 이 문제는 **Sensor와 모든 자식 센서가 하나의 번호표를 공유해야 한다.** 그래서 증가시키는 곳도 읽는 곳도 `Sensor.next_id`로 통일한다.

```text
@classmethod
def get_sensor_count(cls):
    return Sensor.next_id
```

`cls`를 받는 문법은 유지한다. 이 문제의 설계상 최상위 공유 카운터를 의도적으로 지정한 것이다. `CalibratedSensor.get_sensor_count()`로 불러도 같은 전체 개수가 나온다.

<a id="inheritance"></a>

## 10. 상속 — 보정 센서도 센서다

상속은 **is-a 관계**를 나타낸다. 보정 센서는 센서의 한 종류이므로 `CalibratedSensor(Sensor)`라고 정의할 수 있다. 모든 센서가 보정 센서인 것은 아니다.

```python
class Sensor:
    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name

class CalibratedSensor(Sensor):
    pass

base = Sensor("Ava")
child = CalibratedSensor("Ben")

print(child.get_name())                    # Ben
print(isinstance(child, CalibratedSensor)) # True
print(isinstance(child, Sensor))           # True
print(isinstance(base, CalibratedSensor))  # False
print(issubclass(CalibratedSensor, Sensor))# True
```

자식이 `__init__`를 정의하지 않으면 여기서는 상속받은 초기화 메서드를 사용한다. 이름을 저장하는 코드와 `get_name()`을 자식에 다시 쓸 필요가 없다.

부모·슈퍼클래스·기반 클래스는 같은 방향의 용어이고, 자식·서브클래스·파생 클래스도 같은 방향이다.

<a id="super"></a>

## 11. `super()`와 메서드 오버라이딩

### 11.1 자식 생성자가 있으면 부모 초기화를 직접 연결한다

```python
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def set_salary(self, salary):
        self.salary = salary

    def get_earnings(self):
        return self.salary

class Manager(Employee):
    def __init__(self, name, salary, bonus):
        super().__init__(name, salary)
        self.bonus = bonus

    def get_earnings(self):
        return super().get_earnings() + self.bonus

employee = Employee("Jack", 70000)
manager = Manager("Joe", 80000, 20000)
employee.set_salary(75000)
manager.set_salary(85000)

print(employee.get_earnings())  # 75000
print(manager.name)            # Joe
print(manager.get_earnings())   # 105000
print(employee.salary)         # 75000
```

`Manager`가 자신의 `__init__`를 정의했기 때문에 `Employee.__init__`가 저절로 추가 실행되는 것은 아니다. `super().__init__(name, salary)`를 호출하여 같은 객체에 부모 쪽 속성을 초기화한다. 그다음 자식만의 `bonus`를 저장한다.

이 예제의 `super()`는 부모 구현으로 연결한다. 더 일반적으로는 메서드 탐색 순서에서 다음 구현을 찾는 도구이며, 여기서는 단일 상속이므로 부모로 이해해도 된다.

### 11.2 오버라이딩과 부모 호출을 구분하기

부모와 같은 이름의 메서드를 자식에서 다시 정의하는 것이 **오버라이딩**이다. `manager.get_earnings()`는 자식 구현을 선택하고, 그 안의 `super().get_earnings()`는 부모가 계산하는 급여를 가져온다.

센서 문제에서는 다음 순서다.

```text
s2.get_average()
    → CalibratedSensor.get_average(self=s2)
        → super().get_average(): 원래 측정값 평균 5.0
        → 1.5 * 5.0 + 2.0
        → 9.5 반환
```

자식 메서드 안에서 원래 평균을 구한다고 `self.get_average()`를 다시 호출하면 같은 자식 메서드가 반복 호출되어 `RecursionError`가 발생할 수 있다. **부모의 원래 평균이 필요하므로 `super().get_average()`를 호출한다.**

### 11.3 private 이름은 자식에서 새 이름으로 해석된다

`Sensor`에서 선언한 `self.__values`는 `_Sensor__values`다. `CalibratedSensor` 안에서 새로 `self.__values`라고 쓰면 `_CalibratedSensor__values`라는 다른 이름으로 해석된다. 상속받았다고 같은 철자의 private 이름에 곧바로 접근할 수 있는 것은 아니다.

부모의 데이터를 다룰 때는 부모가 제공한 `get_values()`, `add_value()`, `get_average()`를 사용한다. 보정 평균은 `super().get_average()`를 통해 구하면 내부 이름을 알 필요도 없고 평균 계산을 중복 작성할 필요도 없다.

<a id="str"></a>

## 12. `__str__` — `print(sensor)`의 출력 만들기

```python
class Label:
    def __init__(self, name, average):
        self.name = name
        self.average = average

    def __str__(self):
        return f"{self.name}: average = {self.average:.2f}"

obj = Label("Ava", 25)
print(obj)        # Ava: average = 25.00
print(str(obj))   # Ava: average = 25.00
```

`print(obj)`와 `str(obj)`는 객체의 문자열 표현을 구하는 데 `__str__`를 사용한다. 이 메서드는 **문자열을 반환해야 한다.** 안에서 `print(...)`만 실행하면 반환값이 `None`이어서 오류가 난다.

`:.2f`는 숫자를 소수 둘째 자리까지 표시하는 문자열 서식이다. 센서 내부의 평균 값을 두 자리 숫자로 바꾸어 저장한다는 뜻은 아니다. `__str__`에서는 데이터를 바꾸기보다 현재 상태를 읽어서 문자열을 만드는 것이 좋다.

부모의 `__str__` 안에서 `self.get_average()`를 호출하면, 자식 객체에서는 자식이 오버라이딩한 평균 메서드가 선택된다. 따라서 보정 센서용 문자열 메서드를 별도로 복사하지 않아도 보정 평균을 출력할 수 있다.

<a id="requirements"></a>

## 13. 예상문제 2번 — 요구사항을 코드 설계로 바꾸기

만들 객체는 두 종류다. 기본 센서는 이름·측정값·ID를 보관한다. 보정 센서는 기본 센서의 기능을 그대로 사용하면서 평균을 `scale * 원래 평균 + offset`으로 계산한다.

### 13.1 무엇을 어디에 저장할까

| 저장 위치 | 변수 | 이유 |
| --- | --- | --- |
| `Sensor` 클래스 | `next_id = 0` | 모든 센서가 함께 쓰는 다음 번호 |
| 센서 객체 | `__id` | 생성 때 받은 자기 번호 |
| 센서 객체 | `__name` | 자기 이름 |
| 센서 객체 | `__values` | 자기 측정값 리스트. private로 보관 |
| 보정 센서 객체 | `__scale`, `__offset` | 자기 보정 계수 |

ID를 먼저 고정해 두어야 한다. `get_id()`에서 `Sensor.next_id`를 그대로 반환하면 현재까지의 공통 카운터만 읽으므로 센서 자신의 번호가 되지 않는다.

### 13.2 메서드별 완성 조건

| 메서드 / 기능 | 충족해야 하는 조건 |
| --- | --- |
| `Sensor.__init__(name, readings)` | 빈 이름·빈 리스트 거부, 각 값 검증, 입력 리스트 복사, ID 배정 |
| `get_id()`, `get_name()` | 저장한 자기 ID·이름 반환 |
| `get_values()` | 내부 원본이 아닌 새 리스트 반환 |
| `add_value(value)` | 생성자와 같은 값 검증 후 추가 |
| `get_average()` | 저장한 값의 산술평균 반환 |
| `__str__()` | ID·이름·개수·소수 둘째 자리 평균을 포함한 문자열 |
| `get_sensor_count()` | `@classmethod`, `cls` 사용. 자식 포함 누적 생성 개수 반환 |
| `CalibratedSensor.__init__()` | scale은 양수 숫자, offset은 숫자. 부모 초기화는 `super()` |
| 자식 `get_average()` | 부모 평균 메서드를 호출하고 scale·offset 적용 |
| 객체 독립성 | 생성·보정·리스트 반환이 다른 센서 값을 바꾸면 안 됨 |
| 검증 코드 | 기본 예제, 입력·반환 복사, 혼합 ID, 음수 추가의 예외 처리 |

문제에서는 이름과 readings 컨테이너가 각각 문자열과 리스트 타입이라고 가정할 수 있다. 따라서 여기서는 컨테이너 타입까지 중복 검사하지 않고 이름의 빈 문자열 여부와 리스트 내용에 집중한다.

**권장 구현 순서:** 유효성 검사 → 입력 복사 → 자기 ID 배정 → 공통 카운터 증가 → getter·추가·평균 → 문자열·클래스 메서드 → 자식 보정 → 테스트.

<a id="solution"></a>

## 14. 전체 풀이 — `sensor_classes.py`

아래 전체 블록을 하나의 `sensor_classes.py` 파일로 저장해 실행한다. 기존의 연습용 `Sensor` 정의와 섞지 말고 새 실행에서 시작하면 ID는 0부터, 생성 개수는 0부터 출발한다. 강의용 작은 예제의 클래스와 변수는 이 파일에 추가하지 않는다.

```python
"""Lecture 05: Sensor and CalibratedSensor, runnable Problem 2 solution."""


class Sensor:
    next_id = 0

    def __init__(self, name, readings):
        if not name:
            raise ValueError("name must not be empty")
        if not readings:
            raise ValueError("readings must not be empty")

        for value in readings:
            self._validate_value(value)

        self.__name = name
        self.__values = readings.copy()
        self.__id = Sensor.next_id
        Sensor.next_id += 1

    def _validate_value(self, value):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError("reading must be numeric")
        if not value >= 0:
            raise ValueError("reading must be nonnegative")

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_values(self):
        return self.__values.copy()

    def add_value(self, value):
        self._validate_value(value)
        self.__values.append(value)

    def get_average(self):
        return sum(self.__values) / len(self.__values)

    def __str__(self):
        return (
            f"Sensor {self.get_id()} ({self.get_name()}): "
            f"count = {len(self.__values)}, "
            f"average = {self.get_average():.2f}"
        )

    @classmethod
    def get_sensor_count(cls):
        return Sensor.next_id


class CalibratedSensor(Sensor):
    def __init__(self, name, readings, scale, offset):
        if isinstance(scale, bool) or not isinstance(scale, (int, float)):
            raise TypeError("scale must be numeric")
        if not scale > 0:
            raise ValueError("scale must be positive")
        if isinstance(offset, bool) or not isinstance(offset, (int, float)):
            raise TypeError("offset must be numeric")

        super().__init__(name, readings)
        self.__scale = scale
        self.__offset = offset

    def get_average(self):
        original_average = super().get_average()
        return self.__scale * original_average + self.__offset


def main():
    source = [10, 20, 30]
    s1 = Sensor("Ava", source)
    s2 = CalibratedSensor("Ben", [4, 6], 1.5, 2.0)

    print(s1.get_average())
    print(s2.get_average())
    s1.add_value(40)
    print(s1.get_average())
    print(Sensor.get_sensor_count())

    print("IDs:", s1.get_id(), s2.get_id())
    print("Names:", s1.get_name(), s2.get_name())

    source[0] = 999
    print("After changing input:", s1.get_values())
    exported = s1.get_values()
    exported[0] = -999
    print("After changing returned list:", s1.get_values())

    s2.add_value(8)
    print("Child readings:", s2.get_values())
    print("Child average:", s2.get_average())
    print(s1)
    print(s2)
    print("Count through child:", CalibratedSensor.get_sensor_count())

    try:
        s1.add_value(-5)
    except ValueError as exc:
        print(f"ValueError: {exc}")
    print("After failed add:", s1.get_values())


if __name__ == "__main__":
    main()
```

처음부터 이 파일만 실행했을 때의 출력은 다음과 같다.

```text
20.0
9.5
25.0
2
IDs: 0 1
Names: Ava Ben
After changing input: [10, 20, 30, 40]
After changing returned list: [10, 20, 30, 40]
Child readings: [4, 6, 8]
Child average: 11.0
Sensor 0 (Ava): count = 4, average = 25.00
Sensor 1 (Ben): count = 3, average = 11.00
Count through child: 2
ValueError: reading must be nonnegative
After failed add: [10, 20, 30, 40]
```

첫 네 줄은 요구된 기본 예제다. 이후 줄에서는 모든 getter, 입력·반환 리스트의 독립성, 자식의 상속 메서드, 문자열 출력과 예외 처리까지 확인한다.

<a id="walkthrough"></a>

## 15. 전체 풀이를 다시 읽기 — 중요한 다섯 갈림길

### 15.1 `_validate_value()`를 두 곳에서 재사용하는 이유

생성자에는 측정값이 여러 개 들어오므로 `for value in readings:`로 하나씩 검증한다. `add_value()`에는 한 개만 들어오므로 그 값 하나를 검증한다. 두 경우 모두 같은 규칙이어야 하므로 일반 인스턴스 메서드 `_validate_value(self, value)`에 모았다.

`self._validate_value(value)`에서 `self`를 다시 인자로 적지 않는다. 이 메서드는 성공하면 별도 값을 반환하지 않고 끝난다. 실패하면 `raise`로 즉시 빠져나오므로 그다음 대입·추가가 실행되지 않는다.

`self.__values.append(value)`가 검증보다 앞에 있으면 잘못된 값이 이미 리스트에 들어간 후에 오류를 내게 된다. 이 풀이에서는 **검증 → 상태 변경** 순서를 유지한다.

### 15.2 번호를 나눠 주는 순서

```text
처음: Sensor.next_id = 0

s1 생성:
  s1.__id에 현재 번호 0 저장
  Sensor.next_id를 1로 증가

s2 생성:
  s2.__id에 현재 번호 1 저장
  Sensor.next_id를 2로 증가

결과:
  s1의 ID = 0
  s2의 ID = 1
  다음 번호 = 2
  누적 생성 개수 = 2
```

`__id`는 설명을 위한 객체별 표기이며 외부에서 `s1.__id`로 직접 읽는다는 뜻이 아니다. 실제로는 `get_id()`를 쓴다.

번호가 0부터 시작하고 성공한 생성마다 정확히 한 번 증가하므로 `next_id`가 누적 생성 개수 역할도 한다. 객체를 `del`하더라도 생성 이력은 줄지 않는다. 실행 중간에 `Sensor.next_id = 0`으로 초기화하면 기존 ID와 충돌할 수 있으므로 하지 않는다.

### 15.3 `self.next_id`, `type(self).next_id`, `cls.next_id`를 무심코 증가시키지 않기

`self.next_id += 1`은 객체에 별도 값을 만들 수 있다. `type(self).next_id += 1`은 자식 클래스에 카운터를 따로 만들 수 있다. 클래스 메서드에서 `cls.next_id += 1`을 쓸 때도 호출받은 자식 클래스에 새 속성이 생길 수 있다.

모든 센서에 공통 번호가 필요하므로 증가식은 **`Sensor.next_id += 1`로 통일한다.** 부모의 초기화 메서드는 자식 객체에서도 실행되지만, 그 안의 이 문장은 항상 같은 공유 카운터를 사용한다.

### 15.4 실패한 보정 센서가 카운터를 올리면 안 된다

자식 생성자는 scale·offset을 먼저 검사한 뒤 `super().__init__()`를 호출한다. scale이 0이거나 숫자가 아닌 offset이면 부모 생성에 도달하지 않는다. 따라서 번호를 소비하지 않고 끝난다.

부모도 이름·리스트·각 측정값을 모두 검증하고 복사한 뒤에 ID를 배정한다. 여기서는 **초기화에 성공한 센서만 세는 정책**을 사용한다. 기본 요구 예제의 개수 2를 만족하며 실패한 초기화도 테스트한다.

### 15.5 평균 보정은 보고할 때 계산하고 원래 측정값은 보존한다

`[4, 6]`의 원래 평균은 5.0이다. 보정값은 `1.5 * 5.0 + 2.0 = 9.5`다. `get_values()`는 여전히 `[4, 6]`을 반환한다.

보정 후 `add_value(8)`을 실행하면 원래 값은 `[4, 6, 8]`, 원래 평균은 6.0, 보정 평균은 11.0이 된다. 읽을 때마다 원본 리스트에 scale·offset을 다시 적용해 저장하지 않으므로 보정을 여러 번 호출해도 값이 누적 변형되지 않는다.

offset은 음수도 허용된다. 예를 들어 원래 평균이 0, scale이 1, offset이 -2이면 보정 평균은 -2다. **원래 측정값이 음수가 아니어야 한다는 조건과 보정 평균의 부호는 구분한다.** scale은 0보다 커야 하지만 offset은 양수일 필요가 없다.

<a id="tests"></a>

## 16. 테스트 — 예제 숫자만 맞으면 끝일까

아니다. 평균 20.0과 9.5만 맞아도, 복사·상속·ID·예외 처리에서 요구사항을 놓칠 수 있다. 아래 테스트는 전체 풀이 파일과 같은 폴더에 `test_sensor_classes.py`로 저장한다.

```python
import unittest
from sensor_classes import Sensor, CalibratedSensor


class SensorTests(unittest.TestCase):
    def test_required_examples(self):
        before = Sensor.get_sensor_count()
        s1 = Sensor("Ava", [10, 20, 30])
        s2 = CalibratedSensor("Ben", [4, 6], 1.5, 2.0)
        self.assertEqual(s1.get_average(), 20.0)
        self.assertEqual(s2.get_average(), 9.5)
        s1.add_value(40)
        self.assertEqual(s1.get_average(), 25.0)
        self.assertEqual(Sensor.get_sensor_count(), before + 2)

    def test_private_list_copies(self):
        for factory in (lambda xs: Sensor("A", xs),
                        lambda xs: CalibratedSensor("B", xs, 2, 1)):
            source = [4, 6]
            sensor = factory(source)
            source[0] = 999
            returned = sensor.get_values()
            returned[1] = 999
            self.assertEqual(sensor.get_values(), [4, 6])
            self.assertIsNot(sensor.get_values(), sensor.get_values())

    def test_ids_across_subclasses(self):
        class ExtraSensor(Sensor):
            pass
        start = Sensor.get_sensor_count()
        objects = [Sensor("A", [0]), CalibratedSensor("B", [0], 1, 0),
                   ExtraSensor("C", [0]), Sensor("D", [0])]
        self.assertEqual([s.get_id() for s in objects], list(range(start, start + 4)))
        self.assertEqual(CalibratedSensor.get_sensor_count(), start + 4)
        self.assertIsInstance(Sensor.__dict__["get_sensor_count"], classmethod)

    def test_invalid_readings_and_names(self):
        for name, readings, error in [("", [1], ValueError), ("A", [], ValueError),
                                      ("A", [-1], ValueError), ("A", [1, "2"], TypeError),
                                      ("A", [True], TypeError)]:
            with self.subTest(name=name, readings=readings):
                count = Sensor.get_sensor_count()
                with self.assertRaises(error):
                    Sensor(name, readings)
                self.assertEqual(Sensor.get_sensor_count(), count)

    def test_invalid_calibration_does_not_count(self):
        for scale, offset, error in [(0, 0, ValueError), (-1, 0, ValueError),
                                    ("1", 0, TypeError), (1, "0", TypeError),
                                    (True, 0, TypeError)]:
            with self.subTest(scale=scale, offset=offset):
                count = Sensor.get_sensor_count()
                with self.assertRaises(error):
                    CalibratedSensor("B", [1], scale, offset)
                self.assertEqual(Sensor.get_sensor_count(), count)

    def test_rejected_add_keeps_state(self):
        sensor = Sensor("A", [0, 2])
        for value, error in [(-1, ValueError), ("3", TypeError)]:
            with self.assertRaises(error):
                sensor.add_value(value)
            self.assertEqual(sensor.get_values(), [0, 2])

    def test_child_methods_and_dynamic_string(self):
        sensor = CalibratedSensor("Ben", [4, 6], 1.5, 2)
        sensor.add_value(8)
        self.assertEqual(sensor.get_values(), [4, 6, 8])
        self.assertEqual(sensor.get_average(), 11.0)
        self.assertIn("average = 11.00", str(sensor))
        self.assertIn("Ben", str(sensor))
        self.assertIn(str(sensor.get_id()), str(sensor))
        self.assertIn("count = 3", str(sensor))

    def test_independent_objects_and_negative_offset(self):
        a = Sensor("A", [10, 20])
        b = CalibratedSensor("B", [0], 1, -2)
        self.assertEqual(b.get_average(), -2)
        b.add_value(4)
        self.assertEqual(a.get_values(), [10, 20])
        self.assertEqual(a.get_average(), 15)
        self.assertEqual(b.get_name(), "B")


if __name__ == "__main__":
    unittest.main(verbosity=2)
```

터미널 실행 명령이다. `text`는 Python 코드가 아니라 터미널에 입력할 내용이다.

```text
python sensor_classes.py
python -m unittest -v test_sensor_classes
```

자동 테스트 결과는 **8개 테스트 통과**다. 일부 테스트는 여러 오류 입력을 `subTest`로 검사하므로 검사한 조건 수는 8개보다 많다.

| 확인할 것 | 왜 필요한가 |
| --- | --- |
| 입력 리스트를 수정한 뒤 센서 값 확인 | 생성 시 복사했는지 검사 |
| 반환 리스트의 원소를 수정한 뒤 다시 조회 | getter가 원본을 노출하지 않는지 검사 |
| 부모·자식·추가 자식·부모 순으로 생성 | 클래스별 ID 분리 오류 탐지 |
| 잘못된 생성 전후의 개수 비교 | 실패한 생성이 카운터를 소비하는지 검사 |
| 자식에서 상속받은 `add_value`, `get_values` 사용 | 부모 기능을 실제로 재사용하는지 확인 |
| 자식 `str()`의 보정 평균 확인 | 오버라이딩 메서드가 선택되는지 검사 |
| 음수 추가 전후의 원본 비교 | 오류가 났어도 상태가 망가지지 않는지 검사 |
| offset이 음수인 정상 입력 | offset도 무조건 양수로 제한하는 실수 탐지 |

각 테스트는 실행 전 생성 개수를 읽고 증가분을 확인한다. 테스트 순서가 바뀌어도 “항상 count가 2일 것”이라는 가정에 의존하지 않는다. 프로그램의 `main()`도 import할 때 저절로 실행되지 않도록 `if __name__ == "__main__":` 아래에서만 호출했다.

<a id="equality"></a>

## 17. `object`, `==`, `is`, `__eq__`

### 17.1 모든 클래스는 `object`에서 이어진다

`class Point:`는 기본적으로 `object`를 상속하는 클래스다. `__init__`, `__str__`, `__eq__`, `__hash__` 같은 특별 메서드를 자신의 클래스에서 정의하여 기본 동작을 바꿀 수 있다.

| 문법 | 관련 메서드 / 의미 |
| --- | --- |
| `ClassName(...)` | 객체를 만들고 `__init__`로 초기화 |
| `str(obj)`, `print(obj)` | `__str__`로 문자열 표현 |
| `a == b` | `__eq__`로 동등성 비교 |
| `a != b` | `__ne__` 등 비교 규약 사용 |
| `a is b` | 같은 객체인지 검사. `__eq__`와 별개 |
| `hash(obj)` | `__hash__`로 해시 계산 |

`__eq__`를 직접 정의하면 기본 `__ne__`가 이를 바탕으로 동작할 수 있으므로 보통 `!=`만을 위해 별도 코드를 중복 작성하지 않아도 된다.

### 17.2 값이 같은 것과 같은 객체인 것은 다르다

```python
class Point:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    def __eq__(self, other):
        if not isinstance(other, Point):
            return NotImplemented
        return self.__x == other.__x and self.__y == other.__y

    def __str__(self):
        return f"Point({self.__x}, {self.__y})"

p1 = Point(1, 2)
p2 = Point(1, 2)
p3 = Point(3, 4)

print(p1 == p2)   # True: 좌표 값이 같음
print(p1 is p2)   # False: 따로 만든 객체
print(p1 != p3)   # True
print(p1 == "x")  # False
print(p1)         # Point(1, 2)
```

`other`는 비교하는 반대편 값이다. 타입을 확인하지 않고 `other.__x`부터 읽으면 문자열과 비교했을 때 `AttributeError`가 날 수 있다.

`return NotImplemented`는 “이 상대 타입과의 비교는 이 메서드에서 처리하지 않는다”는 신호다. `raise NotImplementedError`와는 다르다. Python이 비교 규약에 따라 상대편 처리 등을 시도하고, 이 예제의 `p1 == "x"`는 최종적으로 `False`가 된다.

**센서 문제에 `__eq__`를 추가해야 할까?** 요구사항에는 없다. 서로 다른 센서 두 개가 우연히 같은 이름·측정값을 갖는다고 같은 센서인지도 별도 설계 문제다. 14절 풀이에는 불필요한 동등성 규칙을 추가하지 않았다.

<a id="hash"></a>

## 18. `__hash__` — 객체를 딕셔너리 키로 쓰기

### 18.1 동등성과 해시는 함께 생각한다

딕셔너리는 키를 찾을 때 해시와 동등성 비교를 사용한다. **두 객체가 같다면 해시도 같아야 한다.** 반대는 성립하지 않는다. 해시가 같더라도 서로 다른 객체일 수 있다.

`__eq__`만 새로 정의하고 `__hash__`를 정의하지 않은 일반적인 클래스는 기본적으로 해시 불가능하게 된다. 좌표가 같은 `Point`를 같은 키로 찾게 하려면 동등성과 일치하는 해시 규칙도 필요하다.

```python
class Point:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    def __eq__(self, other):
        if not isinstance(other, Point):
            return NotImplemented
        return self.__x == other.__x and self.__y == other.__y

    def __hash__(self):
        return hash((self.__x, self.__y))

    def __str__(self):
        return f"Point({self.__x}, {self.__y})"

p1 = Point(0.1, 0.0)
p2 = Point(1.2, -3.5)
p3 = Point(0.1, 0.0)

labels = {p1: "A", p2: "B"}
print(p1 == p3)              # True
print(p1 is p3)              # False
print(hash(p1) == hash(p3))  # True
print(labels[p2])            # B
print(labels[p3])            # A
print(p2)                    # Point(1.2, -3.5)
```

`labels[p3]`를 만들 때는 `p3` 자체를 키로 넣지 않았지만, `p1`과 동등한 좌표·해시를 가지므로 같은 항목을 찾는다. 해시 숫자 자체를 암기할 필요는 없다. Python 버전·플랫폼·키 타입 등에 따라 달라질 수 있으며, 핵심은 같은 실행 안에서 동등성 규칙을 지키는 것이다.

### 18.2 키로 쓴 뒤 비교 기준이 되는 값을 바꾸지 않기

위 `Point`는 좌표를 바꾸는 메서드를 제공하지 않고, 생성 후 좌표를 그대로 쓰는 방식으로 사용한다. `__x`, `__y`라는 이름만으로 완전한 불변성이 강제되는 것은 아니다. 맹글링된 이름을 찾아 값을 바꾸는 행동까지 막아 주지는 않는다.

키로 넣은 뒤 좌표를 바꾸면 해시와 동등성의 기준이 달라져 정상적인 키 조회를 보장할 수 없다. 반대로 “모든 가변 객체는 무조건 딕셔너리 키가 될 수 없다”도 정확하지 않다. 기본적인 객체 정체성으로 비교·해시하는 사용자 객체도 있다. 여기서 지켜야 할 규칙은 **이 클래스가 비교와 해시에 사용하는 값이 키로 쓰이는 동안 변하지 않는 것**이다.

다른 해시 조합으로 `hash(x) ^ hash(y)`도 볼 수 있다. `^`는 거듭제곱이 아니라 비트 XOR이고, 거듭제곱은 `**`다. 이 글은 순서 있는 두 좌표를 묶는 의도가 드러나는 `hash((x, y))`를 사용했다. 해시가 꼭 특정 숫자여야 하는 문제는 아니다.

<a id="pitfalls"></a>

## 19. 실수 점검표 — 코드가 돌아가도 요구사항을 놓칠 수 있다

| 틀리기 쉬운 코드 / 생각 | 문제 | 수정 방향 |
| --- | --- | --- |
| `name = name` | 객체에 이름을 저장하지 않음 | `self.__name = name` |
| `Sensor(self, "Ava", values)` | 생성 호출에 self를 직접 넣음 | `Sensor("Ava", values)` |
| `def get_average():` | 호출 시 객체를 받을 매개변수 없음 | `def get_average(self):` |
| `__init__`에서 계산값 return | 초기화 메서드의 반환 규약 위반 | 속성 초기화 후 종료 |
| `self.__values = readings` | 외부 입력과 같은 리스트 공유 | `readings.copy()` |
| `return self.__values` | 반환값으로 내부 상태 변경 가능 | `self.__values.copy()` |
| 측정값을 클래스 리스트에 저장 | 다른 센서와 데이터가 섞임 | 객체별 리스트 사용 |
| `self.next_id += 1` | 객체별 그림자 속성 생성 가능 | `Sensor.next_id += 1` |
| 자식 타입별로 next_id 증가 | 부모·자식 간 ID 중복 가능 | 계층 전체의 공통 카운터 사용 |
| `get_id()`가 next_id 반환 | 자기 번호 대신 현재 공통값 반환 | 생성 때 저장한 `__id` 반환 |
| `get_sensor_count()`에 데코레이터 없음 | 클래스 메서드 요구사항 불충족 | `@classmethod`와 `cls` |
| 음수 검사보다 append 먼저 | 예외 후에도 잘못된 값이 남음 | 검증 후 append |
| 자식 `__init__`에서 부모 호출 누락 | 부모의 이름·측정값·ID 미초기화 | `super().__init__(...)` |
| 보정 평균에서 `self.get_average()` | 같은 메서드 재귀 호출 | `super().get_average()` |
| 부모 평균 계산을 자식에 복사 | 상위 구현 호출 요구사항 불충족 | 부모 메서드 결과 재사용 |
| 평균 조회 시 원본 readings를 보정해서 덮음 | 여러 번 조회할수록 원본 변형 | 보고할 평균만 보정 |
| offset도 양수만 받음 | 음수 offset이라는 정상 입력 거부 | offset은 숫자 여부 검사 |
| `__str__` 안에서 print만 사용 | 문자열 대신 None 반환 | f-string을 return |
| 자식에서 `self.__values` 직접 사용 | 부모 private 이름과 다른 이름 | 부모의 공개 메서드 사용 |
| `==`와 `is`를 같은 뜻으로 사용 | 값 동등성과 정체성 혼동 | 비교 의도 구분 |
| 값 비교만 만들고 임의의 hash 사용 | 동등한 키의 해시 규약 위반 | 비교 필드로 일관된 hash 정의 |

<a id="review"></a>

## 20. 확인 문제 — 답을 보기 전에 직접 예상하기

### 20.1 개념 질문

1. `s1.add_value(40)`의 `self`에는 무엇이 전달되는가?
2. 생성자에서 복사했는데도 getter에서 다시 복사하는 이유는 무엇인가?
3. `Sensor.next_id`는 2인데 첫 센서의 ID가 0인 이유는 무엇인가?
4. 부모와 자식에서 서로 ID 0이 나왔다면 어느 코드를 의심해야 하는가?
5. 보정 센서가 `add_value()`를 다시 정의하지 않아도 호출할 수 있는 이유는 무엇인가?
6. `super().__init__()`는 별도의 부모 객체를 하나 더 만드는가?
7. `__str__` 안의 `self.get_average()`는 자식에서 어느 구현을 선택하는가?
8. 보정 평균이 음수이면 원래 음수 측정값을 허용했다는 뜻인가?
9. `__eq__`에서 반환하는 `NotImplemented`는 오류를 발생시키는가?
10. 서로 다른 `Point` 객체로 같은 딕셔너리 항목을 찾으려면 무엇이 일치해야 하는가?

**정답:** 1. `s1`이 가리키는 센서 객체. 2. 입력을 통한 변경과 반환값을 통한 변경은 별개의 경로이기 때문. 3. 각 객체에는 배정 당시의 번호를 저장하고 공통 카운터는 이후 증가하기 때문. 4. `self.next_id`, `type(self).next_id`, 자식별 카운터를 의심한다. 5. 부모 메서드를 상속했기 때문. 6. 아니다. 같은 객체에 부모 초기화 코드를 적용한다. 7. 오버라이딩된 자식 평균. 8. 아니다. 음수 offset으로도 가능하다. 9. 아니다. 미지원 비교를 Python에 알리는 반환값이다. 10. 두 객체의 동등성 규칙이 성립하고 해시가 같아야 한다.

### 20.2 손으로 설명해 볼 흐름

`CalibratedSensor("Ben", [4, 6], 1.5, 2.0)`을 생성하고 `get_average()`를 호출했을 때를 다음 순서로 설명할 수 있으면 된다.

1. 보정 인자의 타입과 양수 scale을 확인한다.
2. 부모 초기화가 이름·측정값을 검증하고 리스트를 복사한다.
3. 공통 번호표에서 ID 하나를 받고 카운터를 증가시킨다.
4. 객체에 자기 보정 계수를 저장한다.
5. 평균 조회는 자식의 메서드를 선택한다.
6. 부모 메서드로 원래 평균 5.0을 얻는다.
7. `1.5 * 5.0 + 2.0`으로 9.5를 반환한다.
8. 원래 측정값 `[4, 6]`과 다른 센서의 값은 변하지 않는다.

## 참고 자료

용어와 Python 동작을 더 확인할 때 사용할 공식 문서다. 본문의 예제는 이 글 안에서 이해하고 실행할 수 있도록 구성했다.

- [Python 공식 문서: 클래스, 인스턴스, 상속, private 변수](https://docs.python.org/3/tutorial/classes.html)
- [Python 공식 문서: classmethod, isinstance, super](https://docs.python.org/3/library/functions.html)
- [Python 공식 문서: 특별 메서드와 해시 규약](https://docs.python.org/3/reference/datamodel.html)
- [Python 공식 문서: unittest](https://docs.python.org/3/library/unittest.html)
