---
title: "[ENAI607] 연습문제 Set C — 중첩 데이터, 함수 객체, 날짜 클래스 풀이"
description: "P7·P8·P9 영어 원문과 한국어 전체 번역, 한국어 주석 코드, 얕은 복사·함수 전달·전역 카운터·윤년과 안전한 날짜 갱신을 실행 흐름으로 읽는 풀이"
date: 2026-10-20T12:06:06-04:00
update: 2026-10-20
tags:
  - python
  - ENAI607
series: "ENAI607 Python Programming"
seriesOrder: 9
---

Set C의 **문제 7·8·9**를 코드와 함께 읽는 풀이 노트다. 각 문제는 **영어 원문 → 한국어 전체 번역 → 전체 코드와 실행 결과 → 요구사항별 코드 해설 → 실수와 변형** 순서로 정리했다. 문제 본문은 일반 문단으로 읽을 수 있고, 코드와 출력 예시만 코드 블록으로 표시했다.

코드의 `[P7.2-A]`, `[P8.4-C]`, `[P9.3-B]` 주석은 원문의 요구사항 번호와 연결된다. 예를 들어 “실패한 날짜 변경은 원본을 유지해야 한다”는 요구사항은 `[P9.3-B]`의 **검증 전에는 필드를 수정하지 않는 순서**로 구현했다. 설명을 읽을 때 그 코드로 돌아가 확인하면 된다.

PDF의 영어 문구·점수·예시를 보존하되 반복 머리글과 쪽 번호는 제외했다. 한국어 번역에는 세부 제한과 예시도 포함했다. 원문의 출제 참고 범위는 번역해 남겼지만, 풀이 이해를 위해 슬라이드를 대조할 필요는 없다.

## 빠른 목차 — 막힌 개념에서 코드로 바로 찾기

| 찾는 내용 | 원문·번역 | 전체 코드·결과 | 코드를 읽는 해설 | 실수·변형 |
| --- | --- | --- | --- | --- |
| 중첩 인덱싱·append·insert·교환 | [문제 7](#p7-original) | [student_records.py](#p7-code) | [중첩 구조와 복사](#p7-explain) | [점검표](#p7-variants) |
| copy·공유 참조·is와 == | [P7.2 포함](#p7-original) | [복사 실험 코드](#p7-code) | [어느 객체를 바꾸는가](#p7-explain) | [독립성 확인](#p7-variants) |
| 튜플 키·기본 튜플 정렬 | [P7.3·P7.4 포함](#p7-original) | [조회·수정·정렬](#p7-code) | [키 하나와 비교 순서](#p7-explain) | [변형](#p7-variants) |
| complex·atan2·zip·기본 인자 | [문제 8](#p8-original) | [complex_samples.py](#p8-code) | [반환값과 인자](#p8-explain) | [점검표](#p8-variants) |
| 함수 객체 전달·global·호출 횟수 | [P8.4 포함](#p8-original) | [operation 처리 코드](#p8-code) | [함수 이름과 괄호](#p8-explain) | [누적값과 batch](#p8-variants) |
| Date·윤년·private·조회표·예외 | [문제 9](#p9-original) | [date_validation.py](#p9-code) | [검증 후 저장](#p9-explain) | [경계와 상태 보존](#p9-variants) |
| 실행 파일·자동 검증 | [준비](#setup) | [전체 ZIP](practice_set_c.zip) | [19개 테스트](#verification) | [마지막 확인](#final-check) |

<a id="setup"></a>

## 0. 파일을 준비하고 실행하기

[전체 풀이·테스트 ZIP](practice_set_c.zip)을 **같은 폴더에** 풀면 된다. 세 문제 모두 Python 표준 라이브러리만 사용하므로 별도 패키지 설치가 필요 없다. VS Code·PyCharm에서 해당 폴더를 열고 같은 Python 인터프리터를 선택한다.

```text
practice_set_c/
    student_records.py    # 문제 7: 중첩 자료구조와 복사 실험
    complex_samples.py    # 문제 8: 복소수와 함수 전달
    date_validation.py    # 문제 9: Date 클래스와 필수 예외 테스트
    test_set_c.py         # 19개 자동 테스트
    README.md
```

```text
python student_records.py
python complex_samples.py
python date_validation.py
python test_set_c.py
```

터미널의 현재 위치가 파일을 푼 폴더인지 확인한다. PowerShell에서 따옴표로 감싼 Python 실행 파일 경로를 쓸 때는 앞에 `&`를 붙인다. 각 파일의 `if __name__ == "__main__":`는 **직접 실행할 때만 main을 호출**하도록 하는 부분이다. 테스트에서 import하면 시연 코드가 자동으로 실행되지 않는다.

<details>
<summary>공통 안내 · English / 한국어</summary>

<section class="problem-statement" lang="en">

#### English · 공통 안내

ENAI 607 Python Programming for Engineering AI Fall 2026 | Practice Midterm - Set C UNOFFICIAL PRACTICE MATERIAL - NOT AN ACTUAL EXAM OR ASSIGNED HOMEWORK Instructions. Write and test three Python programs. Read the complete statement of each problem before starting. Your implementation must satisfy the detailed specifications, including data types, required Python constructs, input validation, and the described behavior in non-example cases. The sample outputs are partial tests, not complete solutions. No solution code is included. Why Set C? Set A emphasized files, comprehensions, sorting, class inheritance, and line/histogram plots. Set B emphasized string utilities, loop control, matrices, and scatter/bar plots. Set C focuses on nested mutable data, compound dictionary keys, first-class functions and function arguments, complex numbers, and date validation - all based on topics from Lectures 1-5, the Exercises, and Homework. Suggested practice scores: 35 + 30 + 35 = 100 points. These original questions do not predict the actual examination.

</section>

<section class="problem-statement" lang="ko">

#### 한국어 · 공통 안내 전체 번역

**ENAI 607 — 공학 AI를 위한 Python 프로그래밍 / 2026년 가을 / 연습 중간고사 Set C**

**비공식 연습 자료이며, 실제 시험이나 정식으로 부여된 과제가 아니다.**

**지침:** Python 프로그램 세 개를 작성하고 테스트하시오. 각 문제를 시작하기 전에 문제 전체를 읽으시오. 자료형, 지정된 Python 문법, 입력 검증, 예제 외의 경우에 대한 동작을 포함하여 상세 요구사항을 충족해야 한다. 예제 출력은 일부 테스트일 뿐 완전한 풀이가 아니다. 원문에는 정답 코드가 포함되어 있지 않다.

**Set C를 만든 이유:** Set A는 파일, 컴프리헨션, 정렬, 클래스 상속, 선 그래프·히스토그램을 강조했다. Set B는 문자열 유틸리티, 반복문 제어, 행렬, 산점도·막대그래프를 강조했다. Set C는 **중첩된 가변 데이터, 복합 딕셔너리 키, 일급 함수와 함수 인자, 복소수, 날짜 검증**에 집중하며 모두 Lectures 1–5, Exercises, Homework의 주제를 바탕으로 한다. 제안 배점은 35 + 30 + 35 = 총 100점이다. 이 문제들은 새로 만든 연습문제이며 실제 시험의 출제 예측이 아니다.

</section>

</details>


## 문제 7. 학생 기록, 중첩 복사와 튜플 키

<a id="p7-original"></a>

### 7-1. 문제 원문과 한국어 전체 번역

<section class="problem-statement" lang="en">

#### English · 문제 원문

##### Problem 7. Student Records, Nested Data, and Tuple Keys (35 points)

Write and test a Python script that stores student records in a list of dictionaries and separately maintains a lookup table whose keys are tuples. The exercise is designed to distinguish indexing a nested structure, mutating a list contained in a dictionary, copying only an outer container, and creating truly independent nested lists. Use ordinary Python built-in types; do not use pandas or NumPy.

##### P7.1. Construct and modify nested records (11 points)

Create a list named students with exactly four records in the order shown below. Every record must be a dictionary with the keys "name" (a string) and "grades" (a list of grade strings). Store the grade strings exactly as shown.

Without recreating the whole list, perform these operations in order: (a) append grade "A" to Krissie's grade list; (b) exchange the first and second grades of Paul; (c) insert a new dictionary for Joel, whose grades are ["A", "C", "B", "B"], immediately before Krissie. Use indexing and the appropriate list methods, not string substitutions or printed hard-coded answers.

```python
students = [
    {"name": "Jodie",   "grades": ["A", "A-", "B"]},
    {"name": "Paul",    "grades": ["C", "B", "B"]},
    {"name": "Krissie", "grades": ["A-", "A", "B", "A+", "A"]},
    {"name": "Peter",   "grades": ["D", "XF"]}
]
# After the three operations, students[2]["name"] is "Joel".
# After the operations, len(students) is 5.
```

Print the number of students, the name and number of grades of the third student (counting from index 0), and the complete grade lists of Paul and Krissie. Do not assume that every student has the same number of grades.

##### P7.2. Shallow copies, references, and independence (10 points)

Set backup = students.copy(). Change the first grade stored in the dictionary at backup[0] to "B+". Display the first grade of students[0] and explain in a Python comment why it changed even though you called copy(). Next, replace backup[0] with an entirely new dictionary. Verify and print whether the name in students[0] changed. For this part, you must distinguish modification of a shared nested object from reassignment of an item in the outer list.

Now construct independent, a new list of dictionaries in which each record has a separate grade list. You may use a list comprehension, but you must create a fresh grade list for every record (copying the outer list alone is not sufficient). Change one grade in independent and demonstrate that students remains unchanged. Finally, print the result of students is backup and briefly explain the difference between is and ==.

##### P7.3. Dictionaries with tuple keys (9 points)

Build a dictionary named accounts whose keys are two-item tuples of (username, passcode) and whose values are integer account numbers. Do not encode a pair as a concatenated string. Perform the following operations: look up ("jill", 545); safely check whether ("joe", 172) is present without raising a KeyError; change Ted's account number to 576644; add ("sasha", 988) with account number 111111; delete the Gwen entry; and print the number of remaining records. Use dictionary indexing for updates, the in operator for the presence test, and del for deletion.

```python
accounts = {
    ("joe",  786): 123456,
    ("jill", 545): 444567,
    ("ted",  346): 578345,
    ("gwen", 172): 771988
}
# Expected: accounts[("jill", 545)] == 444567
# Expected: ("joe", 172) is absent.
```

##### P7.4. Sorting a list of tuples (5 points)

Create the following list of product (name, price) tuples. Sort it in ascending order by calling products.sort() without a key function. Print the resulting list and state in a comment how Python orders tuples if their first elements are equal. In this problem you must use the default tuple comparison, not sorted(..., key=lambda ...).

```python
products = [("widget", 5.28), ("gadget", 10.44),
            ("widget", 5.55), ("cool stuff", 6.87)]
# Expected sorted order starts with ("cool stuff", 6.87).
```

Source inspiration: Exercise 3, E3.2; Homework 3, H3.4-H3.5; Homework 2, H2.1; Lecture 1 (identity vs. equality); Lecture 2 (nested lists, shallow copying); Lecture 3 (dictionary keys).

</section>

<section class="problem-statement" lang="ko">

#### 한국어 · 전체 번역

##### 문제 7. 학생 기록, 중첩 데이터와 튜플 키 (35점)

학생 기록을 **딕셔너리의 리스트**에 저장하고, 별도로 **튜플을 키로 사용하는 조회 딕셔너리**를 관리하는 Python 스크립트를 작성하고 테스트하시오. 이 문제는 중첩 자료구조의 인덱싱, 딕셔너리 안에 들어 있는 리스트의 변경, 바깥 컨테이너만 복사하기, 실제로 독립된 내부 리스트 만들기를 구분하기 위한 것이다. 일반 Python 내장 타입을 사용하고, **pandas나 NumPy는 사용하지 마시오.**

##### P7.1. 중첩 기록 생성과 수정 (11점)

아래 순서대로 정확히 네 개의 기록이 있는 `students` 리스트를 만드시오. 각 기록은 문자열인 `"name"`과 성적 문자열 리스트인 `"grades"`를 키로 갖는 딕셔너리여야 한다. 성적 문자열은 아래와 정확히 동일하게 저장하시오.

**전체 리스트를 새로 만들지 말고** 다음 작업을 순서대로 수행하시오.

1. Krissie의 성적 리스트 끝에 `"A"`를 추가한다.
2. Paul의 첫 번째 성적과 두 번째 성적을 교환한다.
3. 성적이 `["A", "C", "B", "B"]`인 Joel의 새 딕셔너리를 Krissie 바로 앞에 삽입한다.

인덱싱과 적절한 리스트 메서드를 사용하시오. 문자열 치환을 사용하거나 결과를 하드코딩해서 출력하면 안 된다.

```python
students = [
    {"name": "Jodie",   "grades": ["A", "A-", "B"]},
    {"name": "Paul",    "grades": ["C", "B", "B"]},
    {"name": "Krissie", "grades": ["A-", "A", "B", "A+", "A"]},
    {"name": "Peter",   "grades": ["D", "XF"]}
]
# 세 작업 후 students[2]["name"]은 "Joel"이다.
# 작업 후 len(students)는 5다.
```

학생 수, 세 번째 학생의 이름과 성적 개수, Paul과 Krissie의 전체 성적 리스트를 출력하시오. 원문은 인덱스가 0부터 시작한다고 명시한다. 학생마다 성적 개수가 같다고 가정하지 마시오.

##### P7.2. 얕은 복사, 참조와 독립성 (10점)

`backup = students.copy()`로 설정하시오. `backup[0]`의 딕셔너리에 저장된 첫 번째 성적을 `"B+"`로 바꾸시오. `students[0]`의 첫 번째 성적을 표시하고, `copy()`를 호출했는데도 왜 바뀌었는지 Python 주석으로 설명하시오.

그다음 `backup[0]`을 완전히 새로운 딕셔너리로 교체하시오. `students[0]`의 이름이 바뀌었는지 확인하여 출력하시오. 이 부분에서는 **공유하는 내부 객체의 수정**과 **바깥 리스트 항목의 재대입**을 구분해야 한다.

이제 각 기록이 별도의 성적 리스트를 갖도록, 딕셔너리의 새 리스트 `independent`를 만드시오. 리스트 컴프리헨션을 사용해도 되지만, **모든 기록마다 새 성적 리스트를 만들어야 한다.** 바깥 리스트만 복사하는 것으로는 충분하지 않다. `independent`의 성적 하나를 바꾸고, `students`는 바뀌지 않았음을 보여 주시오. 마지막으로 `students is backup`의 결과를 출력하고 `is`와 `==`의 차이를 간단히 설명하시오.

##### P7.3. 튜플 키를 사용하는 딕셔너리 (9점)

두 항목의 튜플 `(username, passcode)`를 키로, 정수 계좌 번호를 값으로 갖는 `accounts` 딕셔너리를 만드시오. 두 항목을 이어 붙인 문자열로 표현하지 마시오. 다음 작업을 수행하시오.

- `("jill", 545)`를 조회한다.
- `KeyError`를 일으키지 않고 `("joe", 172)`의 존재 여부를 안전하게 확인한다.
- Ted의 계좌 번호를 `576644`로 바꾼다.
- 계좌 번호가 `111111`인 `("sasha", 988)`을 추가한다.
- Gwen 항목을 삭제한다.
- 남은 기록 수를 출력한다.

수정에는 **딕셔너리 인덱싱**, 존재 검사에는 **`in` 연산자**, 삭제에는 **`del`을 사용**하시오.

```python
accounts = {
    ("joe",  786): 123456,
    ("jill", 545): 444567,
    ("ted",  346): 578345,
    ("gwen", 172): 771988
}
# 예상: accounts[("jill", 545)] == 444567
# 예상: ("joe", 172)는 없다.
```

##### P7.4. 튜플 리스트 정렬 (5점)

아래 제품 `(name, price)` 튜플 리스트를 만드시오. **key 함수를 전달하지 않고 `products.sort()`를 호출**하여 오름차순으로 정렬하시오. 결과 리스트를 출력하고, 튜플의 첫 번째 원소가 같을 때 Python이 어떤 방식으로 순서를 정하는지 주석으로 설명하시오. 이 문제에서는 `sorted(..., key=lambda ...)`가 아니라 **기본 튜플 비교를 사용**해야 한다.

```python
products = [("widget", 5.28), ("gadget", 10.44),
            ("widget", 5.55), ("cool stuff", 6.87)]
# 정렬된 결과의 시작은 ("cool stuff", 6.87)이다.
```

**출제 참고 범위:** Exercise 3의 E3.2, Homework 3의 H3.4–H3.5, Homework 2의 H2.1, Lecture 1의 동일성·동등성, Lecture 2의 중첩 리스트·얕은 복사, Lecture 3의 딕셔너리 키.

</section>

<a id="p7-code"></a>

### 7-2. 전체 정답 코드와 실제 실행 결과

파일 이름: [student_records.py](student_records.py). 아래 본문 코드와 다운로드 파일은 같다.

```python
"""문제 7: 중첩 자료구조, 얕은 복사, 튜플 키와 기본 정렬."""


def create_students():
    students = [
        {"name": "Jodie", "grades": ["A", "A-", "B"]},
        {"name": "Paul", "grades": ["C", "B", "B"]},
        {"name": "Krissie", "grades": ["A-", "A", "B", "A+", "A"]},
        {"name": "Peter", "grades": ["D", "XF"]},
    ]
    # [P7.1-A] 리스트 -> 딕셔너리 -> 성적 리스트 순서로 찾아간다.
    students[2]["grades"].append("A")
    # [P7.1-B] 오른쪽 두 값을 먼저 구한 뒤 왼쪽 두 자리에 교환한다.
    grades = students[1]["grades"]
    grades[0], grades[1] = grades[1], grades[0]
    # [P7.1-C] 삽입 전 Krissie의 인덱스는 2다. 삽입 후에는 3이 된다.
    students.insert(2, {"name": "Joel", "grades": ["A", "C", "B", "B"]})
    return students


def demonstrate_copies(students):
    # [P7.2-A] 바깥 리스트만 새로 만든다. 내부 딕셔너리는 공유한다.
    backup = students.copy()
    backup[0]["grades"][0] = "B+"
    print("Original first grade after nested edit:", students[0]["grades"][0])
    # 공유 딕셔너리 안의 공유 성적 리스트를 수정했으므로 원본에도 보인다.
    old_name = students[0]["name"]
    # [P7.2-B] 이번에는 backup의 0번 칸이 가리키는 대상을 바꾼다.
    backup[0] = {"name": "Replacement", "grades": ["C"]}
    print("Original name changed:", students[0]["name"] != old_name)
    # [P7.2-C] 매번 새 딕셔너리와 새 성적 리스트를 만들어 공유를 끊는다.
    independent = [
        {"name": record["name"], "grades": record["grades"].copy()}
        for record in students
    ]
    independent[0]["grades"][0] = "A+"
    print("Independent first grade:", independent[0]["grades"][0])
    print("Original first grade:", students[0]["grades"][0])
    print("students is backup:", students is backup)
    # is는 같은 객체인지, ==는 값이 같은지를 비교한다.
    return backup, independent


def create_accounts():
    accounts = {
        ("joe", 786): 123456,
        ("jill", 545): 444567,
        ("ted", 346): 578345,
        ("gwen", 172): 771988,
    }
    # [P7.3] 키는 문자열 두 개가 아니라 (문자열, 정수) 튜플 하나다.
    print("Jill account:", accounts[("jill", 545)])
    print("(joe, 172) present:", ("joe", 172) in accounts)
    accounts[("ted", 346)] = 576644
    accounts[("sasha", 988)] = 111111
    del accounts[("gwen", 172)]
    print("Remaining accounts:", len(accounts))
    return accounts


def sort_products():
    products = [("widget", 5.28), ("gadget", 10.44),
                ("widget", 5.55), ("cool stuff", 6.87)]
    # [P7.4] 첫 원소(이름)부터 비교하고, 같으면 다음 원소(가격)를 비교한다.
    products.sort()
    return products


def main():
    students = create_students()
    print("Student count:", len(students))
    third = students[2]  # 세 번째 학생은 인덱스 2: 원문의 Joel 예시와 일치한다.
    print("Third student:", third["name"], "grade count:", len(third["grades"]))
    print("Paul grades:", students[1]["grades"])
    print("Krissie grades:", students[3]["grades"])
    demonstrate_copies(students)
    create_accounts()
    print("Sorted products:", sort_products())


if __name__ == "__main__":
    main()
```

**실제 실행 결과:**

```text
Student count: 5
Third student: Joel grade count: 4
Paul grades: ['B', 'C', 'B']
Krissie grades: ['A-', 'A', 'B', 'A+', 'A', 'A']
Original first grade after nested edit: B+
Original name changed: False
Independent first grade: A+
Original first grade: B+
students is backup: False
Jill account: 444567
(joe, 172) present: False
Remaining accounts: 4
Sorted products: [('cool stuff', 6.87), ('gadget', 10.44), ('widget', 5.28), ('widget', 5.55)]
```

<a id="p7-explain"></a>

### 7-3. 코드를 읽는 해설 — 같은 내부 객체를 보고 있는가?

#### P7.1: 대괄호를 왼쪽부터 하나씩 해석한다

```python
students[2]["grades"].append("A")
```

| 코드 | 여기까지 얻는 객체 | 타입 |
| --- | --- | --- |
| `students` | 학생 기록 전체 | list |
| `students[2]` | 삽입 전 Krissie의 기록 | dict |
| `students[2]["grades"]` | Krissie의 성적 전체 | list |
| `.append("A")` | 그 리스트 맨 끝에 성적 하나 추가 | 기존 리스트 수정 |

**`[2]`는 리스트의 위치, `["grades"]`는 딕셔너리의 키다.** 대괄호 모양이 같아도 왼쪽 객체의 타입에 따라 의미가 달라진다. 첫 번째 성적까지 내려가려면 `students[2]["grades"][0]`이다. `students[2][0]`은 성적을 뜻하지 않는다. 딕셔너리에서 숫자 키 `0`을 찾으려다 `KeyError`가 난다.

`append()`는 성적 리스트를 직접 수정한다. `students[2]["grades"] = students[2]["grades"].append("A")`처럼 쓰면 반환값 `None`이 저장되어 성적 리스트를 잃는다. **수정 메서드의 실행 결과를 다시 대입하지 않는다.**

`grades = students[1]["grades"]`도 복사는 아니다. 두 이름이 같은 성적 리스트를 가리키므로 `grades[0], grades[1] = grades[1], grades[0]`이 Paul의 실제 성적을 바꾼다. 오른쪽의 원래 두 값을 먼저 구하므로 임시 변수 없이 교환할 수 있다.

| 시점 | index 0 | index 1 | index 2 | index 3 | index 4 |
| --- | --- | --- | --- | --- | --- |
| 처음 | Jodie | Paul | Krissie | Peter | 없음 |
| `insert(2, Joel기록)` 후 | Jodie | Paul | Joel | Krissie | Peter |

`insert(i, value)`는 **기존 i번 원소 앞에 삽입**한다. 따라서 성적 추가는 Krissie가 2번일 때 먼저 하고, Joel을 삽입한 뒤 Krissie를 출력할 때는 3번을 사용한다. 세 번째 학생은 `students[2]`인 Joel이다. 원문의 “third student (counting from index 0)” 표현은 뒤에 주어진 `students[2]["name"] == "Joel"` 예시와 함께 읽으면 된다. 인덱스 3 학생을 요구한 것으로 해석하지 않았다.

성적 개수는 `len(students[2]["grades"])`다. `len(students[2])`는 딕셔너리 키 개수인 **2**를 센다. 이 자료의 성적 개수는 학생 순서대로 3·3·4·6·2다.

#### P7.2: copy()는 어디까지 새로 만드는가?

```python
backup = students.copy()
backup[0]["grades"][0] = "B+"
```

`copy()`로 바깥 리스트는 새로 생겼다. 그러나 각 칸에는 **기존 딕셔너리를 가리키는 참조가 복사**된다. `students[0]`과 `backup[0]`은 여전히 같은 딕셔너리이며, 그 안의 성적 리스트도 같다.

| 확인식 / 변경 | 결과 | 이유 |
| --- | --- | --- |
| `students is backup` | `False` | 바깥 리스트는 별개 |
| 복사 직후 `students == backup` | `True` | 안에 든 값은 같음 |
| 복사 직후 `students[0] is backup[0]` | `True` | 0번 딕셔너리는 공유 |
| `backup[0]["grades"][0] = "B+"` | 원본 첫 성적도 B+ | 공유한 내부 리스트 수정 |
| `backup[0] = 새딕셔너리` | 원본 이름은 Jodie 유지 | backup의 바깥 칸만 다른 대상을 참조 |

**“내부 객체를 바꾸기”와 “내 리스트의 한 칸을 다른 객체로 교체하기”를 구분**하면 된다. `backup[0]["name"] = "Replacement"`였다면 공유 딕셔너리의 이름을 바꾸므로 원본 이름도 바뀐다. 실제 풀이의 `backup[0] = {...}`와는 다른 동작이다.

```python
independent = [
    {"name": record["name"], "grades": record["grades"].copy()}
    for record in students
]
```

이 컴프리헨션의 반복 대상은 학생 딕셔너리다. 한 번 반복할 때마다 `{...}`로 **새 딕셔너리를 만들고**, `.copy()`로 **새 성적 리스트를 만든다.** 이름과 성적 문자열은 불변이므로 문자열 자체까지 복제할 필요는 없다. 그래서 `independent[0]["grades"][0] = "A+"`는 원본의 B+를 유지한다.

`[record.copy() for record in students]`만으로는 부족하다. 딕셔너리는 새로 만들지만 그 안의 성적 리스트는 공유한다. 현재 스키마는 “딕셔너리 안에 문자열 리스트 하나”이므로 풀이의 복사가 충분하다. 성적 원소까지 리스트·딕셔너리인 더 깊은 구조로 바뀌면 그 깊이도 따로 복사해야 한다. 이 코드를 임의의 깊이에 대응하는 범용 깊은 복사로 외우면 안 된다.

**`is`는 객체 동일성, `==`는 값의 동등성**이다. “값이 같으니까 같은 객체”도 아니고 “객체가 다르니까 값도 다름”도 아니다. 예를 들어 `[1, 2] == [1, 2]`는 참이지만 따로 만든 두 리스트는 별개다.

#### P7.3: 튜플 두 항목이 합쳐져 키 하나다

```python
accounts[("jill", 545)]       # 444567
("joe", 172) in accounts     # False
accounts[("ted", 346)] = 576644
del accounts[("gwen", 172)]
```

`accounts[("jill", 545)]`는 키 두 개를 차례대로 조회하는 코드가 아니다. **`("jill", 545)`라는 튜플 하나를 키로 조회**한다. `accounts["jill"][545]`였다면 바깥 딕셔너리에서 `"jill"`을 찾은 뒤 다시 인덱싱하는 전혀 다른 구조다.

키가 `("joe", 786)`인 항목이 있어도 `("joe", 172)`는 없다. 두 원소가 모두 일치해야 같은 키다. `in accounts`는 기본적으로 **값이 아닌 키를 검사**하며, 키가 없어도 예외 없이 `False`를 준다. 없는 키를 바로 `accounts[("joe", 172)]`로 읽으면 `KeyError`가 난다.

딕셔너리 대입은 키가 이미 있으면 값 수정, 없으면 새 항목 추가다. 따라서 Ted 수정으로 개수가 늘지는 않는다. 처음 4개 → Sasha 추가로 5개 → Gwen 삭제로 **4개**다.

키는 해시 가능한 객체여야 한다. 이 문제의 튜플 원소인 문자열과 정수는 해시 가능하다. 리스트 자체는 키가 될 수 없고, 튜플이어도 안에 리스트가 들어 있으면 키로 사용할 수 없다. “튜플이면 언제나 딕셔너리 키가 가능하다”로 외우지 않는다.

#### P7.4: key가 없으면 튜플 자체를 왼쪽부터 비교한다

```python
products.sort()
# [('cool stuff', 6.87), ('gadget', 10.44),
#  ('widget', 5.28), ('widget', 5.55)]
```

먼저 이름을 비교하여 `cool stuff` → `gadget` → `widget` 순이다. 이름이 같은 widget 두 개는 두 번째 원소 가격을 비교하여 5.28 → 5.55가 된다. **가격 전체를 기준으로 정렬한 결과가 아니다.** 그래서 더 저렴한 widget 5.28보다 gadget 10.44가 앞선다.

`products.sort()`는 원본 리스트를 정렬하고 `None`을 반환한다. `products = products.sort()`라고 쓰지 않는다. 앞선 Set A는 `sorted(..., key=lambda ...)`가 요구사항이었지만, 이번 문제는 **key 없는 `.sort()` 자체가 요구사항**이다.

<a id="p7-variants"></a>

### 7-4. 실수와 변형 — 자료구조에서 어느 층을 바꿀까?

| 문제 조건 / 실수 | 구현할 위치·이유 |
| --- | --- |
| 학생 수와 성적 수가 다름 | `len(students)`와 `len(record["grades"])` 구분 |
| 학생 삽입 위치 변경 | 삽입 뒤 기존 학생의 인덱스도 밀리는지 확인 |
| 이름으로 학생을 찾으라고 바뀜 | 각 record의 `"name"`을 검사한 뒤 해당 성적 리스트 수정 |
| 복사 후 원본이 바뀜 | 바깥 리스트·딕셔너리·성적 리스트 중 공유된 층 확인 |
| 서로 독립된 성적 기록 필요 | 새 dict + 새 grades 리스트 생성 |
| 키 조합이 하나라도 다름 | 다른 튜플 키이며 존재하지 않을 수 있음 |
| 가격순 정렬로 요구가 바뀜 | 그때는 `key=lambda item: item[1]` 검토. 현재 문제에는 사용 금지 |

복사 문제를 풀 때는 값 출력만 보지 말고 `independent[i] is students[i]`, `independent[i]["grades"] is students[i]["grades"]`도 확인해 보자. 둘 다 `False`여야 이 문제의 내부 리스트 독립성까지 증명된다.


## 문제 8. 복소수와 함수 객체 전달

<a id="p8-original"></a>

### 8-1. 문제 원문과 한국어 전체 번역

<section class="problem-statement" lang="en">

#### English · 문제 원문

##### Problem 8. Complex Samples and Functions as Objects (30 points)

Write and test a Python script that converts complex measurements from rectangular form to polar form, associates sample names with samples, and passes functions as arguments to another function. Use built-in Python types and the standard math module. Do not use NumPy for this problem. Pay attention to the distinction between a function object and the value returned when that function is called.

##### P8.1. Rectangular-to-polar conversion (9 points)

Define a function with the exact header rec_to_pol(x) whose input is a complex number. Return a two-item tuple consisting of the magnitude followed by the phase angle in radians. Calculate the magnitude using abs() and the phase using math.atan2(x.imag, x.real), which correctly handles the four quadrants. Do not return a list, and do not print the result from inside the function. Test both positive and negative real components.

```python
print(rec_to_pol(1 + 1j))
# approximately (1.4142135623730951, 0.7853981633974483)
print(rec_to_pol(3 + 4j))
# approximately (5.0, 0.9272952180016122)
```

##### P8.2. Building a tuple of tuples using zip() (8 points)

Define create_tuple(names, samples, num). The function shall pair the first num names with the first num complex samples, preserving their order, and return a tuple whose items are (name, sample) tuples. You must use zip() to pair the values and tuple() to construct the outer tuple. Assume num is a nonnegative integer. If either input sequence contains fewer than num elements, return None; in particular, zip() must not silently shorten the requested output. If num is zero, return an empty tuple.

```python
names = ["S1", "S2", "S3", "EXTRA"]
samples = [1 + 1j, 3 + 4j, -1 + 1j]
print(create_tuple(names, samples, 2))
# (('S1', (1+1j)), ('S2', (3+4j)))
print(create_tuple(names, samples, 4))  # None
```

##### P8.3. Default and keyword arguments (6 points)

Define apply_gain(x, gain=1.0). It shall return a new complex value equal to x multiplied by gain. Demonstrate one call with the default gain, one call with the second argument supplied positionally, and one call using the keyword argument gain=. Show that passing a complex input does not require making a defensive list copy. Give the outputs of the following calls to two decimal places when applicable:

```python
print(apply_gain(3 + 4j))
print(apply_gain(3 + 4j, 2))
print(apply_gain(3 + 4j, gain=0.5))
```

##### P8.4. First-class functions and global scope (7 points)

Define apply_function(samples, operation). For every complex value in samples, call operation(value) and append its returned value to a result list. Return that list without changing samples. The operation parameter must be treated as a function object; the caller is responsible for passing a function, not a precomputed value. Demonstrate two calls: one passing the built-in function abs, and one passing your own rec_to_pol. Do not write two separate specialized processing functions.

Add a module-level integer variable conversion_count = 0. Each successful call to rec_to_pol() must increment it by one using a global conversion_count declaration within that function. After processing three samples through apply_function(samples, rec_to_pol), print the number of conversions performed. Be aware that direct test calls to rec_to_pol() also increment the counter. Add one comment distinguishing a local variable from a global variable.

Source inspiration: Homework 4, H4.2-H4.3; Lecture 1 (numeric types and math functions); Lecture 3 pp.22, 26-32 (zip, positional/keyword/default arguments, local/global scope, functions as objects).

</section>

<section class="problem-statement" lang="ko">

#### 한국어 · 전체 번역

##### 문제 8. 복소수 표본과 객체로서의 함수 (30점)

직교형 복소수 측정값을 극형으로 변환하고, 표본 이름과 표본을 연결하며, 함수를 다른 함수의 인자로 전달하는 Python 스크립트를 작성하고 테스트하시오. Python 내장 타입과 표준 `math` 모듈을 사용하시오. **이 문제에서는 NumPy를 사용하지 마시오.** 함수 객체와, 함수를 호출했을 때 반환되는 값의 차이에 주의하시오.

##### P8.1. 직교형을 극형으로 변환 (9점)

복소수를 입력받는, 정확히 `rec_to_pol(x)`라는 헤더의 함수를 정의하시오. **크기, 라디안 단위의 위상각 순서로 구성된 두 항목 튜플**을 반환하시오. 크기는 `abs()`, 위상은 네 사분면을 올바르게 처리하는 `math.atan2(x.imag, x.real)`로 계산하시오. 리스트를 반환하지 말고, 함수 내부에서 결과를 출력하지 마시오. 실수부가 양수인 경우와 음수인 경우를 모두 테스트하시오.

```python
print(rec_to_pol(1 + 1j))
# 대략 (1.4142135623730951, 0.7853981633974483)
print(rec_to_pol(3 + 4j))
# 대략 (5.0, 0.9272952180016122)
```

##### P8.2. zip()으로 튜플의 튜플 만들기 (8점)

`create_tuple(names, samples, num)`을 정의하시오. 처음 `num`개의 이름과 처음 `num`개의 복소수 표본을 원래 순서대로 짝지어, 항목이 `(name, sample)` 튜플인 **바깥 튜플**을 반환하시오. 짝짓기에는 **`zip()`**, 바깥 튜플 생성에는 **`tuple()`을 반드시 사용**해야 한다.

`num`은 음이 아닌 정수라고 가정하시오. 어느 한 입력 시퀀스라도 원소가 `num`개보다 적으면 `None`을 반환하시오. 특히 **`zip()` 때문에 요청한 결과가 조용히 짧아지면 안 된다.** `num`이 0이면 빈 튜플을 반환하시오.

```python
names = ["S1", "S2", "S3", "EXTRA"]
samples = [1 + 1j, 3 + 4j, -1 + 1j]
print(create_tuple(names, samples, 2))
# (('S1', (1+1j)), ('S2', (3+4j)))
print(create_tuple(names, samples, 4))  # None
```

##### P8.3. 기본 인자와 키워드 인자 (6점)

`apply_gain(x, gain=1.0)`을 정의하시오. x에 gain을 곱한 값과 같은 새 복소수 값을 반환해야 한다. 기본 gain으로 한 번, 두 번째 인자를 위치 인자로 전달하여 한 번, `gain=`이라는 키워드 인자로 한 번 호출하시오. 복소수 입력을 전달할 때 방어적인 리스트 복사가 필요하지 않음을 보이시오. 가능한 경우 소수점 아래 두 자리로 아래 호출의 출력을 제시하시오.

```python
print(apply_gain(3 + 4j))
print(apply_gain(3 + 4j, 2))
print(apply_gain(3 + 4j, gain=0.5))
```

##### P8.4. 일급 함수와 전역 범위 (7점)

`apply_function(samples, operation)`을 정의하시오. samples의 모든 복소수에 대해 `operation(value)`를 호출하고, 반환된 값을 결과 리스트에 추가하시오. samples를 변경하지 않고 결과 리스트를 반환하시오. operation 매개변수는 **함수 객체로 취급**해야 한다. 호출하는 쪽은 미리 계산한 값이 아니라 함수를 전달할 책임이 있다.

내장 함수 `abs`를 전달하는 호출과 직접 만든 `rec_to_pol`을 전달하는 호출을 각각 보여 주시오. 용도별로 특화한 처리 함수를 두 개 따로 작성하면 안 된다.

모듈 수준의 정수 변수 `conversion_count = 0`을 추가하시오. `rec_to_pol()`이 성공적으로 호출될 때마다 내부의 **`global conversion_count` 선언을 사용**해 카운터를 1씩 증가시켜야 한다. `apply_function(samples, rec_to_pol)`로 표본 세 개를 처리한 다음 수행한 변환 횟수를 출력하시오. `rec_to_pol()`의 직접 테스트 호출도 카운터를 증가시킨다는 점에 주의하시오. 지역 변수와 전역 변수의 차이를 설명하는 주석 하나를 추가하시오.

**출제 참고 범위:** Homework 4의 H4.2–H4.3, Lecture 1의 수치 타입·수학 함수, Lecture 3의 22·26–32쪽(zip, 위치·키워드·기본 인자, 지역·전역 범위, 객체로서의 함수).

</section>

<a id="p8-code"></a>

### 8-2. 전체 정답 코드와 실제 실행 결과

파일 이름: [complex_samples.py](complex_samples.py). 아래 본문 코드와 다운로드 파일은 같다.

```python
"""문제 8: 복소수, 튜플, 인자 전달과 일급 함수."""
import math

# [P8.4-A] 함수 바깥, 모듈 전체에서 사용하는 누적 카운터다.
conversion_count = 0


def rec_to_pol(x):
    global conversion_count
    # [P8.1] atan2의 순서는 (허수부, 실수부)이며 각도 단위는 라디안이다.
    magnitude = abs(x)
    phase = math.atan2(x.imag, x.real)
    # 계산이 성공한 뒤에만 횟수를 증가시킨다.
    conversion_count += 1
    # magnitude와 phase는 이 호출 안에서만 사용하는 지역 변수다.
    return magnitude, phase  # 쉼표로 두 값을 묶으면 튜플이다.


def create_tuple(names, samples, num):
    # [P8.2-A] zip이 짧은 쪽에서 멈추기 전에 요청 개수를 검증한다.
    if len(names) < num or len(samples) < num:
        return None
    # [P8.2-B] 필요한 앞부분만 짝짓고, 바깥 결과를 튜플로 만든다.
    return tuple(zip(names[:num], samples[:num]))


def apply_gain(x, gain=1.0):
    # [P8.3] complex는 불변이다. 곱의 결과를 반환하며 x 자체를 수정하지 않는다.
    return x * gain


def apply_function(samples, operation):
    # [P8.4-B] operation에는 abs나 rec_to_pol 같은 함수 자체가 들어온다.
    result = []
    for value in samples:
        result.append(operation(value))
    return result


def main():
    # 음의 실수부까지 검사한다. 이 직접 호출들도 카운터에 포함된다.
    for x in (1 + 1j, 3 + 4j, -1 + 1j):
        print("Polar:", x, rec_to_pol(x))
    names = ["S1", "S2", "S3", "EXTRA"]
    samples = [1 + 1j, 3 + 4j, -1 + 1j]
    print("Paired samples:", create_tuple(names, samples, 2))
    print("Too many requested:", create_tuple(names, samples, 4))
    print("Zero requested:", create_tuple(names, samples, 0))
    x = 3 + 4j
    # [P8.3] 각각 기본 인자, 위치 인자, 키워드 인자 사용이다.
    gained = [apply_gain(x), apply_gain(x, 2), apply_gain(x, gain=0.5)]
    for value in gained:
        print(f"Gain result: {value.real:.2f}{value.imag:+.2f}j")
    print("Original complex:", x)
    print("Magnitudes:", apply_function(samples, abs))
    # [P8.4-C] 괄호 없이 함수를 전달한다. 반복문 안에서 세 번 호출된다.
    before = conversion_count
    print("Polar samples:", apply_function(samples, rec_to_pol))
    print("Conversions in this batch:", conversion_count - before)
    print("Total conversions:", conversion_count)
    print("Original samples:", samples)


if __name__ == "__main__":
    main()
```

**실제 실행 결과:**

```text
Polar: (1+1j) (1.4142135623730951, 0.7853981633974483)
Polar: (3+4j) (5.0, 0.9272952180016122)
Polar: (-1+1j) (1.4142135623730951, 2.356194490192345)
Paired samples: (('S1', (1+1j)), ('S2', (3+4j)))
Too many requested: None
Zero requested: ()
Gain result: 3.00+4.00j
Gain result: 6.00+8.00j
Gain result: 1.50+2.00j
Original complex: (3+4j)
Magnitudes: [1.4142135623730951, 5.0, 1.4142135623730951]
Polar samples: [(1.4142135623730951, 0.7853981633974483), (5.0, 0.9272952180016122), (1.4142135623730951, 2.356194490192345)]
Conversions in this batch: 3
Total conversions: 6
Original samples: [(1+1j), (3+4j), (-1+1j)]
```

<a id="p8-explain"></a>

### 8-3. 코드를 읽는 해설 — 함수를 넘기고, 안에서 호출한다

#### P8.1: 복소수의 실수부·허수부로 크기와 각도를 구한다

`3 + 4j`는 실수부 3, 허수부 4인 복소수다. Python에서 허수 단위는 `j`로 적는다. `x.real`과 `x.imag`는 속성이므로 `x.real()`처럼 호출하지 않는다.

| 코드 | `x = 3 + 4j`일 때 | 의미 |
| --- | --- | --- |
| `x.real` | `3.0` | 가로 좌표인 실수부 |
| `x.imag` | `4.0` | 세로 좌표인 허수부 |
| `abs(x)` | `5.0` | 원점에서의 거리, 크기 |
| `math.atan2(x.imag, x.real)` | 약 `0.9273` | 양의 실수축에서의 위상각, 라디안 |
| `return magnitude, phase` | `(5.0, 0.9273...)` | 크기·각도 순서의 튜플 |

크기는 실수부²+허수부²의 제곱근이다. `abs()`는 복소수에서도 이 크기를 계산한다. `math.atan2(y, x)`는 **세로 좌표가 먼저** 들어간다. 순서를 반대로 쓰면 각도가 달라진다.

왜 `math.atan(x.imag / x.real)`로 쓰면 안 될까? `1+1j`와 `-1-1j`는 그 비율이 모두 1이지만 실제 방향은 다르다. 실수부 0에서는 나눗셈도 불가능하다. `atan2`는 두 좌표의 부호를 함께 사용해 사분면을 구분한다. 예를 들어 `-1+1j`의 위상은 약 **2.3562 라디안**이다.

반환값은 튜플이므로 `magnitude, phase = rec_to_pol(x)`로 풀어 받을 수 있다. `return [magnitude, phase]`는 리스트여서 요구사항과 다르다. 함수 내부에서 `print()`만 하면 호출자에게 결과가 전달되지 않는다. 풀이에서는 **반환은 함수 안에서, 출력은 호출한 곳에서** 한다.

문제가 각도를 도 단위로 바꾸라고 하면 `math.degrees(phase)`를 사용할 수 있다. 그러나 현재 반환 단위는 반드시 라디안이다. `0j`는 크기 0이며 방향은 수학적으로 정해지지 않는다. 이 구현은 요구한 `atan2`의 동작에 따라 각도 `0.0`을 반환한다.

#### P8.2: zip의 자동 종료가 이 문제에서는 함정이다

```python
if len(names) < num or len(samples) < num:
    return None
return tuple(zip(names[:num], samples[:num]))
```

이 코드는 **검증 → 잘라내기 → 짝짓기 → 튜플로 확정** 순서다.

1. 둘 중 하나라도 요청 개수보다 짧으면 `None`이다. 따라서 `and`가 아니라 **`or`를 사용한다.**
2. `names[:num]`과 `samples[:num]`은 각각 앞에서 num개다. 끝 인덱스는 포함하지 않는다.
3. `zip()`이 같은 위치의 원소를 `(이름, 복소수)` 튜플로 묶는다.
4. `tuple()`이 zip 반복자를 소비하여 바깥 튜플을 만든다.

| 요청 | 입력 상태 | 반환값 |
| --- | --- | --- |
| `num=2` | 이름 4개·표본 3개 | `(('S1', (1+1j)), ('S2', (3+4j)))` |
| `num=4` | 표본이 3개라 부족 | `None` |
| `num=0` | 빈 입력도 허용 | `()` |

**슬라이싱은 범위를 넘겨도 보통 오류를 내지 않고, zip은 짧은 쪽에 맞춰 끝난다.** 길이 검사 없이 `tuple(zip(names[:4], samples[:4]))`만 쓰면 4개를 요청했는데도 3개짜리를 반환한다. 바로 이 상황을 문제에서 금지했다.

반환값 `None`과 빈 튜플 `()`도 구분하자. `None`은 요청을 충족할 수 없다는 실패 신호, `()`는 0개 요청을 정상적으로 처리한 결과다. num이 음수가 아닌 정수라는 조건은 문제에서 보장하므로 추가 검증을 요구하지 않는다.

#### P8.3: 위치 인자·키워드 인자·기본값은 같은 매개변수에 도착한다

```python
def apply_gain(x, gain=1.0):
    return x * gain
```

| 호출 | x | gain | 반환값 |
| --- | --- | --- | --- |
| `apply_gain(3+4j)` | `3+4j` | 기본값 `1.0` | `3+4j` |
| `apply_gain(3+4j, 2)` | `3+4j` | 위치로 전달한 `2` | `6+8j` |
| `apply_gain(3+4j, gain=0.5)` | `3+4j` | 이름으로 전달한 `0.5` | `1.5+2j` |

`gain=1.0`은 함수 정의에서 **생략했을 때 쓸 기본값**이고, 호출의 `gain=0.5`는 **어느 매개변수에 넣을지 지정한 키워드 인자**다. 모양은 비슷해도 사용 위치에 따라 역할이 다르다.

complex는 불변이다. 곱셈은 계산된 값을 돌려주며 원래 x를 변경하지 않는다. 리스트 복사와 달리 `x.copy()`를 할 필요도, 그런 메서드도 없다. gain이 1일 때조차 “반드시 별도 객체인가”를 `is`로 검사할 필요는 없다. 요구사항의 핵심은 **결과 값과 원본 불변성**이다.

표시만 소수점 두 자리로 만들 때는 `f"{value.real:.2f}{value.imag:+.2f}j"`를 사용했다. `.2f`는 소수점 두 자리, `+`는 허수부가 양수여도 `+` 부호를 표시한다. 함수의 실제 반환값을 문자열로 바꾸거나 반올림한 것은 아니다.

#### P8.4: rec_to_pol과 rec_to_pol(x)는 전혀 다른 인자다

```python
apply_function(samples, rec_to_pol)
```

이때 `operation = rec_to_pol`처럼 함수 자체가 매개변수에 들어온다. `apply_function` 내부의 `operation(value)`에서 비로소 호출된다.

| 전달한 두 번째 인자 | 실제로 전달되는 것 | 이후 동작 |
| --- | --- | --- |
| `abs` | 내장 함수 객체 | 매 표본에 `abs(value)` 호출 |
| `rec_to_pol` | 직접 만든 함수 객체 | 매 표본에 `rec_to_pol(value)` 호출 |
| `rec_to_pol(3+4j)` | 이미 계산한 `(5.0, 각도)` 튜플 | 나중에 튜플을 함수처럼 호출하려 하여 오류 |
| `rec_to_pol()` | 인자 없이 즉시 호출 시도 | 필수 인자 x가 없어 전달 전에 오류 |

**함수를 전달할 때는 이름, 함수를 실행할 때는 이름(인자)로 읽자.** 함수도 변수에 담고 다른 함수에 넘길 수 있는 객체라는 것이 일급 함수의 핵심이다. 이 문제에서는 lambda를 새로 만들 필요가 없다.

```python
result = []
for value in samples:
    result.append(operation(value))
return result
```

첫 표본 `1+1j`에 operation이 abs라면 약 `1.4142`가 추가된다. operation이 rec_to_pol이면 `(1.4142..., 0.7854...)` 튜플이 추가된다. **같은 반복문에서 전달한 함수에 따라 결과 타입이 달라진다.** 앞의 것은 숫자 리스트, 뒤의 것은 튜플 리스트다. 원본 samples에는 대입하거나 append하지 않으므로 그대로 남는다.

#### 전역 카운터: 왜 3번 처리했는데 누적값은 6일까?

```python
conversion_count = 0

def rec_to_pol(x):
    global conversion_count
    magnitude = abs(x)
    phase = math.atan2(x.imag, x.real)
    conversion_count += 1
    return magnitude, phase
```

`magnitude`와 `phase`는 매 호출 안에서 쓰는 지역 변수다. `conversion_count`는 함수 바깥에서 정의한 전역 변수다. `+= 1`은 값을 읽기만 하는 것이 아니라 **새 정수 값을 전역 이름에 다시 대입**한다. 그래서 `global conversion_count`가 필요하다. 선언을 빼면 이 이름을 지역 변수로 판단한 채 초기값을 읽으려 하므로 `UnboundLocalError`가 난다.

**함수 안에서 카운터를 0으로 초기화하면 매번 다시 시작하므로 안 된다.** 또한 계산이 성공한 뒤 증가시켜야 실패한 호출을 세지 않는다.

| 실행 시점 | 증가량 | 누적값 |
| --- | --- | --- |
| 모듈 초기화 | 0 | 0 |
| 양·음 실수부 직접 테스트 3회 | +3 | 3 |
| `apply_function(samples, abs)` | +0 | 3 |
| `apply_function(samples, rec_to_pol)` | +3 | 6 |

따라서 batch 직전의 `before = conversion_count`를 저장하고 **`conversion_count - before`로 이번 처리 횟수 3을 출력**한다. 전체 누적값은 6이다. 둘을 함께 표시해 직접 호출까지 누적된다는 요구사항을 드러냈다. 확인하려고 rec_to_pol을 한 번 더 실행하는 것조차 카운터를 바꾼다.

<a id="p8-variants"></a>

### 8-4. 실수와 변형 — 반환 타입·인자·호출 횟수 점검

| 조건 / 실수 | 구현·확인할 곳 |
| --- | --- |
| 사분면이 틀리거나 실수부 0에서 오류 | 나눗셈 atan 대신 `atan2(허수부, 실수부)` |
| 튜플 대신 리스트 반환 | `return magnitude, phase` / 바깥 `tuple(zip(...))` |
| 이름 또는 표본 한쪽만 부족 | 길이 조건을 `or`로 연결 |
| 원본 표본에 결과를 덮어씀 | 새 `result` 리스트에 append |
| 함수 전달 중 괄호를 붙임 | `operation`에 함수 객체가 들어오는지 확인 |
| 누적 횟수가 예상과 다름 | 직접 호출·추가 검사 호출까지 합산, batch 전후 차이 계산 |
| 결과에 gain을 다른 값으로 적용 | `apply_gain(x, gain=값)` 호출만 변경 |
| 다른 처리를 표본마다 적용 | callable 하나를 operation으로 전달; 공통 반복문 재사용 |

테스트에서 전역 카운터를 보고 싶으면 `import complex_samples as cs` 후 `cs.conversion_count`를 읽으면 된다. `from complex_samples import conversion_count`로 정수 값을 가져온 뒤 모듈의 이름이 새 정수로 갱신되어도, 가져온 쪽 이름이 자동으로 같은 값으로 재대입되지는 않는다.


## 문제 9. 윤년 검증과 안전한 Date 클래스

<a id="p9-original"></a>

### 9-1. 문제 원문과 한국어 전체 번역

<section class="problem-statement" lang="en">

#### English · 문제 원문

##### Problem 9. A Date Class with Leap-Year Validation (35 points)

Write and test a Python script defining a Date class that represents a valid calendar date with a year, month, and day. This exercise emphasizes a combination of Boolean logic, private helper methods, class variables used as lookup tables, and safe updates of object state. Do not import datetime or calendar and do not use an existing date-validation library. For this exercise, assume years are positive integers and use the ordinary Gregorian leap-year rule.

##### P9.1. Class variables and construction (9 points)

Define the class variables DAYS_PER_MONTH and MONTH_NAMES. The first must contain the numbers of days for January through December in a normal year, in month order, and the second must contain the twelve corresponding English month names. Define a constructor `__init__`(self, year, month, day). On valid input, save the three values in private instance variables. A year must be a positive integer, a month an integer from 1 through 12, and a day an integer within the allowed range for that specific month and year. Do not assume that every month contains 31 days.

##### P9.2. Leap years and a private helper (12 points)

Implement a private helper method `__valid_date`(self, year, month, day) that returns True for a valid date and False otherwise. Both the constructor and the set_date() method below must call this same helper; do not duplicate the full validation logic in two methods. For this practice question, reject a constructor with invalid arguments by raising ValueError("Invalid date"). A leap year is divisible by 4 but not by 100, or divisible by 400. Use the logical operators and, or, and not as appropriate. In a leap year, February has 29 days; otherwise, it has 28 days. Do not permanently modify DAYS_PER_MONTH when processing a leap year.

```python
# Leap-year cases that your logic must distinguish:
# 1600: leap year       1700: not a leap year
# 1900: not a leap year 2000: leap year
# 2024: leap year       2023: not a leap year
```

##### P9.3. Getters, formatted string, and safe updates (9 points)

Implement get_year(), get_month(), and get_day() to return the stored integer fields. Override `__str__`() to return a string formatted exactly like February 29, 2000 for the appropriate date; obtain the month name from MONTH_NAMES rather than writing twelve separate branches. Define set_date(year, month, day) to validate the complete proposed date before changing any instance variable. A valid update must change all three fields and return True. An invalid update must print Invalid date, return False, and leave the original date entirely unchanged.

##### P9.4. Required tests (5 points)

Create and print valid Date objects for February 29, 2000 and February 29, 2024. Verify that Date(1900, 2, 29), Date(2023, 2, 29), and Date(2024, 4, 31) raise ValueError, and catch the exceptions with try/except so that the test program continues. Start with Date(2024, 2, 29), call set_date(2023, 2, 29), and print the original date again to prove that the invalid update did not change any field. Finally, call set_date(2023, 3, 1) and print the new date.

```python
# Selected expected outcomes:
# str(Date(2000, 2, 29)) == "February 29, 2000"
# set_date(2023, 2, 29) on a valid 2024-02-29 object -> False
# The object still represents February 29, 2024.
# set_date(2023, 3, 1) -> True; date is March 1, 2023.
```

Source inspiration: Exercise 5, E5.1 (Date class and leap-year requirements); Lecture 1 (logical operators and comparisons); Lecture 5 (constructors, private attributes, class variables, methods and `__str__`); Lecture 4 (ValueError handling). The exception/return conventions here are practice-specific; follow the requirements above.

Before you submit your practice: Check every named requirement, especially copy-versus-alias behavior, tuple key lookups, default arguments, functions passed by reference, leap-year century cases, and preservation of object state after invalid input. No answers are included in this set.

</section>

<section class="problem-statement" lang="ko">

#### 한국어 · 전체 번역

##### 문제 9. 윤년을 검증하는 Date 클래스 (35점)

연·월·일로 유효한 달력 날짜를 나타내는 `Date` 클래스를 정의하는 Python 스크립트를 작성하고 테스트하시오. 이 문제는 불리언 논리, private 보조 메서드, 조회표로 사용하는 클래스 변수, 객체 상태를 안전하게 갱신하는 방법을 함께 다룬다.

**`datetime`이나 `calendar`를 import하지 말고, 기존 날짜 검증 라이브러리를 사용하지 마시오.** 이 문제에서는 연도가 양의 정수라고 가정하며 일반적인 그레고리력 윤년 규칙을 사용하시오.

##### P9.1. 클래스 변수와 생성 (9점)

클래스 변수 `DAYS_PER_MONTH`와 `MONTH_NAMES`를 정의하시오. 첫 번째에는 평년의 1월부터 12월까지 각 달의 일수를 월 순서대로, 두 번째에는 그에 대응하는 영어 월 이름 열두 개를 넣어야 한다.

생성자 `__init__(self, year, month, day)`를 정의하시오. 유효한 입력이면 세 값을 **private 인스턴스 변수에 저장**하시오. 연도는 양의 정수, 월은 1부터 12까지의 정수, 일은 **해당 월·해당 연도에서 허용하는 범위 내의 정수**여야 한다. 모든 달이 31일까지 있다고 가정하지 마시오.

##### P9.2. 윤년과 private 보조 메서드 (12점)

유효한 날짜이면 `True`, 아니면 `False`를 반환하는 private 보조 메서드 `__valid_date(self, year, month, day)`를 구현하시오. 생성자와 아래 `set_date()`가 **동일한 보조 메서드를 호출**해야 한다. 두 메서드에 전체 검증 로직을 중복해서 작성하면 안 된다.

이 연습문제에서는 유효하지 않은 생성자 인자를 **`ValueError("Invalid date")`를 발생시켜 거부**하시오. 윤년은 다음 조건 중 하나를 만족한다.

- 4로 나누어떨어지고, 100으로는 나누어떨어지지 않는다.
- 또는 400으로 나누어떨어진다.

필요에 따라 논리 연산자 `and`, `or`, `not`을 사용하시오. 윤년의 2월은 29일, 평년의 2월은 28일이다. **윤년을 처리하면서 `DAYS_PER_MONTH`를 영구적으로 수정하지 마시오.**

```text
# 윤년 로직이 구분해야 하는 경우:
# 1600: 윤년       1700: 평년
# 1900: 평년       2000: 윤년
# 2024: 윤년       2023: 평년
```

##### P9.3. getter, 형식화된 문자열과 안전한 갱신 (9점)

저장된 정수 필드를 반환하는 `get_year()`, `get_month()`, `get_day()`를 구현하시오. `__str__()`를 재정의하여 해당 날짜에 맞는, **정확히 `February 29, 2000` 같은 형식의 문자열**을 반환하시오. 열두 개의 분기를 만드는 대신 `MONTH_NAMES`에서 월 이름을 가져오시오.

`set_date(year, month, day)`를 정의하시오. **인스턴스 변수 하나라도 변경하기 전에 제안된 날짜 전체를 검증**해야 한다.

- 유효한 갱신은 세 필드를 모두 바꾸고 `True`를 반환해야 한다.
- 유효하지 않은 갱신은 `Invalid date`를 출력하고 `False`를 반환하며, **원래 날짜 전체를 그대로 유지**해야 한다.

##### P9.4. 필수 테스트 (5점)

2000년 2월 29일과 2024년 2월 29일에 해당하는 유효한 `Date` 객체를 만들고 출력하시오. `Date(1900, 2, 29)`, `Date(2023, 2, 29)`, `Date(2024, 4, 31)`이 `ValueError`를 발생시키는지 검증하고, 테스트 프로그램이 계속 실행되도록 `try/except`로 예외를 처리하시오.

`Date(2024, 2, 29)`로 시작하여 `set_date(2023, 2, 29)`를 호출한 뒤, 원래 날짜를 다시 출력하여 잘못된 갱신이 어느 필드도 바꾸지 않았음을 증명하시오. 마지막으로 `set_date(2023, 3, 1)`을 호출하고 새 날짜를 출력하시오.

```text
# 예상 결과 일부:
# str(Date(2000, 2, 29)) == "February 29, 2000"
# 유효한 2024-02-29 객체에서 set_date(2023, 2, 29) -> False
# 객체는 여전히 February 29, 2024를 나타낸다.
# set_date(2023, 3, 1) -> True; 날짜는 March 1, 2023이다.
```

**출제 참고 범위:** Exercise 5의 E5.1(Date 클래스·윤년 요구사항), Lecture 1의 논리 연산자·비교, Lecture 5의 생성자·private 속성·클래스 변수·메서드·`__str__`, Lecture 4의 `ValueError` 처리. 여기의 예외·반환값 규칙은 이 연습문제에 정한 규칙이므로 위 요구사항을 따르시오.

**연습 제출 전 확인:** 모든 명시적 요구사항, 특히 복사와 별칭의 차이, 튜플 키 조회, 기본 인자, 함수 참조 전달, 윤년의 세기 경계, 잘못된 입력 후 객체 상태 보존을 확인하시오. 원문 Set C에는 정답이 포함되어 있지 않다.

</section>

<a id="p9-code"></a>

### 9-2. 전체 정답 코드와 실제 실행 결과

파일 이름: [date_validation.py](date_validation.py). 아래 본문 코드와 다운로드 파일은 같다.

```python
"""문제 9: 윤년 검사와 검증 후에만 변경하는 Date 클래스."""


class Date:
    # [P9.1-A] 모든 객체가 함께 참조하는 조회표다. 튜플로 두어 실수로 바꾸지 않는다.
    DAYS_PER_MONTH = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
    MONTH_NAMES = ("January", "February", "March", "April", "May", "June",
                   "July", "August", "September", "October", "November", "December")

    def __init__(self, year, month, day):
        # [P9.1-B] 잘못된 날짜로 객체가 생성되지 않게 먼저 검증한다.
        if not self.__valid_date(year, month, day):
            raise ValueError("Invalid date")
        self.__year = year
        self.__month = month
        self.__day = day

    def __valid_date(self, year, month, day):
        # [P9.2-A] bool도 isinstance(..., int)는 True이므로 여기서는 정확한 int만 허용한다.
        if type(year) is not int or type(month) is not int or type(day) is not int:
            return False
        # 월을 인덱스로 쓰기 전에 범위를 확인해야 한다.
        if year <= 0 or not 1 <= month <= 12:
            return False
        # [P9.2-B] 월 1~12를 조회표 인덱스 0~11로 바꾼다.
        max_day = self.DAYS_PER_MONTH[month - 1]
        leap = (year % 4 == 0 and year % 100 != 0) or year % 400 == 0
        if month == 2 and leap:
            max_day = 29  # 지역 변수만 바꾼다. 공유 조회표는 그대로 둔다.
        return 1 <= day <= max_day

    def get_year(self):
        return self.__year

    def get_month(self):
        return self.__month

    def get_day(self):
        return self.__day

    def __str__(self):
        # [P9.3-A] 화면에 출력하지 말고 문자열을 반환한다.
        name = self.MONTH_NAMES[self.__month - 1]
        return f"{name} {self.__day}, {self.__year}"

    def set_date(self, year, month, day):
        # [P9.3-B] 세 값 전체를 검증하기 전에는 어떤 필드도 수정하지 않는다.
        if not self.__valid_date(year, month, day):
            print("Invalid date")
            return False
        self.__year = year
        self.__month = month
        self.__day = day
        return True


def main():
    print(Date(2000, 2, 29))
    print(Date(2024, 2, 29))
    # [P9.4-A] 예외를 잡아야 다음 테스트까지 계속 실행할 수 있다.
    for year, month, day in [(1900, 2, 29), (2023, 2, 29), (2024, 4, 31)]:
        try:
            Date(year, month, day)
        except ValueError as error:
            print(f"Rejected {year}-{month:02d}-{day:02d}: {error}")
    date = Date(2024, 2, 29)
    print("Invalid update accepted:", date.set_date(2023, 2, 29))
    print("After invalid update:", date)
    print("Valid update accepted:", date.set_date(2023, 3, 1))
    print("After valid update:", date)


if __name__ == "__main__":
    main()
```

**실제 실행 결과:**

```text
February 29, 2000
February 29, 2024
Rejected 1900-02-29: Invalid date
Rejected 2023-02-29: Invalid date
Rejected 2024-04-31: Invalid date
Invalid date
Invalid update accepted: False
After invalid update: February 29, 2024
Valid update accepted: True
After valid update: March 1, 2023
```

<a id="p9-explain"></a>

### 9-3. 코드를 읽는 해설 — 먼저 검증하고, 통과하면 저장한다

#### P9.1: 공통 조회표와 객체마다 다른 날짜를 나눈다

| 저장 위치 | 예 | 의미 |
| --- | --- | --- |
| 클래스 변수 | `Date.DAYS_PER_MONTH` | 모든 날짜가 참고하는 평년 월별 일수 |
| 클래스 변수 | `Date.MONTH_NAMES` | 모든 날짜가 참고하는 영어 월 이름 |
| private 인스턴스 변수 | `self.__year`, `self.__month`, `self.__day` | 객체 하나가 나타내는 날짜 |
| 지역 변수 | `max_day`, `leap` | 이번 검증 과정에서만 쓰는 계산값 |

조회표는 클래스 본문에 한 번 정의하고, 인스턴스 필드는 생성자의 self에 저장한다. 예를 들어 `Date(2000, 2, 29)`와 `Date(2024, 2, 29)`는 같은 월 이름 표를 보지만 연도 필드는 다르다.

문제는 조회표가 리스트인지 튜플인지 지정하지 않았다. 풀이에서는 **수정할 필요 없는 공통 표를 튜플로 정의**했다. 각 객체에서 표를 바꾸는 대신 필요한 일수만 지역 변수로 계산한다.

`__year`처럼 앞에 밑줄 두 개를 붙이면 클래스 이름을 포함하도록 이름이 변환되는 name mangling이 적용된다. 외부에서 `date.__year`로 바로 읽는 방식을 피하고 getter를 사용한다. 이것은 보안 장벽이라기보다 의도치 않은 접근·이름 충돌을 줄이는 장치다. `__str__`처럼 앞뒤에 두 개가 있는 특수 메서드는 같은 방식으로 생각하지 않는다.

#### P9.2: 타입 → 범위 → 월별 일수 순서가 중요하다

```python
if type(year) is not int or type(month) is not int or type(day) is not int:
    return False
if year <= 0 or not 1 <= month <= 12:
    return False
max_day = self.DAYS_PER_MONTH[month - 1]
```

문자열 연도를 정수와 비교하거나 실수 월을 리스트 인덱스로 사용하기 전에 타입을 확인한다. **이번 구현은 bool도 정수 날짜로 받지 않는 정책**이다. Python에서 `isinstance(True, int)`는 참이므로 정확한 int를 확인했다. 숫자 문자열 `"2024"`나 정수와 값이 같은 `2024.0`을 임의로 변환해서 허용하지 않는다.

월은 1~12지만 표의 인덱스는 0~11이다. 그래서 `month - 1`이다. 2월은 인덱스 1에서 28을 가져온다. **월 범위를 먼저 검사하지 않으면 월 0이 인덱스 -1로 바뀌어 12월을 읽는 오류**가 생긴다. 13월은 인덱스 범위 오류가 날 수 있다.

```python
leap = (year % 4 == 0 and year % 100 != 0) or year % 400 == 0
if month == 2 and leap:
    max_day = 29
return 1 <= day <= max_day
```

`%`는 나머지다. `year % 4 == 0`은 “4로 나누어떨어진다”라는 뜻이다. “4의 배수” 조건 하나만으로는 1900년을 잘못 받아들인다.

| 연도 | 4의 배수 | 100의 배수 | 400의 배수 | 윤년 여부 |
| --- | --- | --- | --- | --- |
| 1600 | 예 | 예 | 예 | 참 |
| 1700 | 예 | 예 | 아니오 | 거짓 |
| 1900 | 예 | 예 | 아니오 | 거짓 |
| 2000 | 예 | 예 | 예 | 참 |
| 2024 | 예 | 아니오 | 아니오 | 참 |
| 2023 | 아니오 | 아니오 | 아니오 | 거짓 |

왼쪽 묶음은 “4의 배수이면서 100의 배수는 아니다”, 오른쪽은 “400의 배수다”다. 둘 중 하나가 참이면 된다. 괄호로 논리 묶음을 드러내면 시험 때 읽기 쉽다. 단순히 `year % 4 == 0 and year % 100 != 0`로 끝내면 2000년을 잘못 거부한다.

윤년이어도 4월은 여전히 30일이다. **2월이면서 윤년일 때만** max_day를 29로 바꾼다. `self.DAYS_PER_MONTH`를 수정하지 않으므로 윤년 객체를 만든 뒤 평년 날짜를 검사해도 2월 기준이 28로 유지된다.

`__valid_date()`는 **전달받은 year·month·day**를 검사해야 한다. `self.__year` 같은 기존 필드를 읽어서 검사하면 아직 필드가 없는 생성자에서는 오류가 나고, setter에서는 새 제안이 아닌 예전 날짜를 검사하게 된다.

#### P9.3: 생성 실패와 갱신 실패의 규칙이 다르다

| 호출 | 검증 실패 시 동작 | 검증 성공 시 동작 |
| --- | --- | --- |
| `Date(year, month, day)` | `raise ValueError("Invalid date")` | 세 private 필드를 저장하여 초기화 |
| `date.set_date(year, month, day)` | `Invalid date` 출력, `False` 반환, 기존 필드 유지 | 세 필드 변경 후 `True` 반환 |

둘 다 `self.__valid_date(...)`를 호출한다. 같은 검증을 복제하면 생성자에서 고친 윤년 로직이 setter에는 빠지는 문제가 생길 수 있다.

생성자가 실패할 때 `return False`로 처리하면 안 된다. `__init__()`는 별도 값을 반환하는 일반 함수가 아니며, `None` 이외를 반환하면 오류다. **잘못된 객체의 생성을 막기 위해 예외를 발생**시키라는 문제 규칙을 따른다.

반대로 setter는 이미 존재하는 유효한 객체를 대상으로 한다. **실패해도 이전 날짜가 유효하게 남아 있어야 한다.** 아래와 같은 순서는 잘못이다.

```python
# 잘못된 순서: 새 날짜를 검증하기 전에 원래 연도를 잃는다.
self.__year = year
if not self.__valid_date(year, month, day):
    return False
```

2024-02-29에 2023-02-29를 제안하면 연도만 2023으로 바뀌어, 거부했는데 객체 안에는 유효하지 않은 날짜가 남는다. 풀이에서는 실패 경로에 필드 대입이 하나도 없다.

| 단계 | year | month | day | 반환값 |
| --- | --- | --- | --- | --- |
| `Date(2024, 2, 29)` 생성 | 2024 | 2 | 29 | 객체 생성 |
| `set_date(2023, 2, 29)` 실패 후 | **2024** | **2** | **29** | `False` |
| `set_date(2023, 3, 1)` 성공 후 | 2023 | 3 | 1 | `True` |

“연도는 유효하니까 먼저 저장”처럼 한 필드씩 검증·갱신하지 말고, **전체 날짜 검증이 끝난 뒤 세 필드를 저장**한다. 2월의 허용 일수는 연도와 함께 결정되므로 필드들이 서로 독립적이지 않다.

#### __str__는 출력문이 아니라 문자열을 돌려주는 메서드다

```python
name = self.MONTH_NAMES[self.__month - 1]
return f"{name} {self.__day}, {self.__year}"
```

2월이면 MONTH_NAMES의 인덱스 1에서 `"February"`를 얻는다. 반환 형식은 **월 이름 + 공백 + 일 + 쉼표 + 공백 + 연도**다. `print(date)`나 `str(date)`가 이 문자열을 사용한다. 메서드 내부에서 `print(...)`만 하면 기본 반환값은 None이므로 `__str__ returned non-string` 오류가 난다.

getter는 단순히 자기 필드를 반환한다. `get_year()`에 유효성 검사 전체를 다시 넣을 필요는 없다. 생성과 갱신을 통과한 객체의 값을 읽는 역할이다.

#### P9.4: 예외를 잡아야 거부된 다음 경우도 테스트한다

```python
try:
    Date(1900, 2, 29)
except ValueError as error:
    print(error)  # Invalid date
```

`try` 안에서 생성자가 ValueError를 발생시키면 그 아래 코드를 건너뛰고 except로 간다. 예외를 처리한 뒤 다음 테스트를 진행한다. 잘못된 날짜 세 개를 한 try 안에 연속으로 만들면 첫 실패 뒤의 두 호출은 실행되지 않는다. 그래서 풀이에서는 **반복문 안에 try/except를 두어 각각 검사**한다.

`print("Invalid update accepted:", date.set_date(...))`는 인자를 계산하는 과정에서 setter를 먼저 실행한다. setter의 `Invalid date`가 먼저 출력되고, 그 뒤 바깥 print가 `Invalid update accepted: False`를 출력한다. 실행 결과의 두 줄 순서는 이 때문이다.

<a id="p9-variants"></a>

### 9-4. 실수와 변형 — 경계와 상태 보존이 점수다

| 조건 / 실수 | 수정·검사할 위치 |
| --- | --- |
| 평년 2월 29일을 허용함 | 윤년 식과 max_day 결정 |
| 1900·2000을 같은 결과로 처리 | 100년 예외 + 400년 예외의 예외 |
| 4월 31일을 허용함 | 월별 조회표와 day 범위 |
| 월 0·13에서 잘못된 조회 / IndexError | 인덱싱보다 먼저 월 범위 검사 |
| 실수·문자열·bool이 날짜로 들어옴 | 타입 검사 정책을 명확히 유지 |
| 실패했는데 연도만 바뀜 | 필드 대입을 검증 통과 뒤로 이동 |
| 윤년 검사 뒤 다른 객체의 평년도 달라짐 | 공유 DAYS_PER_MONTH 대신 지역 max_day 사용 |
| 문자열 형식을 바꾸라고 함 | `__str__()`에서만 표현 변경, 저장은 정수 유지 |
| setter 실패도 예외를 내라고 바뀜 | 실패 경로 규칙만 변경. 현재는 출력 + False가 필수 |

유효하지 않은 입력을 막는 것만으로 충분하지 않다. **실패 이후 객체의 세 필드가 원래 그대로인지** 확인해야 안전한 갱신을 증명할 수 있다.


<a id="verification"></a>

## 10. 검증 — 예제 외에 확인한 것

[test_set_c.py](test_set_c.py)의 **19개 테스트가 모두 통과**했다. 각 테스트 안에서 여러 입력과 경계값을 추가로 확인했다. 프로그램의 출력만 비교하지 않고, 객체가 실제로 공유·분리됐는지와 실패 뒤의 상태까지 검사했다.

| 문제 | 테스트 수 | 확인한 내용 |
| --- | --- | --- |
| 7 | 4개 | 학생 순서·성적 교환·추가·길이, 얕은 복사에서 공유된 dict, 독립된 모든 성적 리스트, 튜플 키·추가·수정·삭제·개수, 기본 튜플 정렬 |
| 8 | 8개 | 네 사분면과 좌표축·0의 극형, 튜플 반환·함수 내부 출력 없음, 실패 호출 미집계, zip 순서·각 입력 부족·0개, 세 gain 인자 형식, 원본 유지, 전달한 함수의 매 원소 호출, batch와 누적 횟수 |
| 9 | 7개 | 1600·1700·1900·2000·2024·2023 윤년, 평년 모든 달의 말일과 0일·초과일, 타입·연월 범위, 정확한 문자열, 공유 일수 표 보존, 잘못된 갱신 후 세 필드 보존, 올바른 갱신, 생성자와 setter의 동일 helper 호출 |

테스트의 `unittest`, `patch` 등은 검증 도구다. 풀이의 핵심으로 외울 부분은 본문의 일반 Python 코드다. 현재 구현은 날짜에서 bool을 거부하고, 문제 8의 num은 문제에서 보장한 비음수 정수라는 전제를 따른다.

<a id="final-check"></a>

## 11. 코드로 되짚는 마지막 확인

- **P7.1:** 지금 사용하는 인덱스가 Joel 삽입 전인가, 후인가? `len()`이 성적 리스트를 세고 있는가?
- **P7.2:** 바깥 리스트만 새로 생겼는가? 내부 dict와 grades 리스트도 새로 생겼는가? 내부 수정과 바깥 칸 재대입을 구분했는가?
- **P7.3:** 키가 `(문자열, 정수)` 튜플 하나인가? 없는 키는 `in`으로 검사했는가?
- **P7.4:** `.sort()`에 key를 넣지 않았는가? 이름이 같으면 가격을 비교한다는 사실을 설명할 수 있는가?
- **P8.1:** `atan2(허수부, 실수부)`이고 크기·라디안 위상 순서의 튜플인가?
- **P8.2:** zip 전에 양쪽 길이를 검사했는가? 0개는 `()`, 부족한 요청은 `None`인가?
- **P8.3:** 기본·위치·키워드 인자를 각각 시연하고, 원래 복소수는 유지되는가?
- **P8.4:** 전달은 `rec_to_pol`, 내부 호출은 `operation(value)`인가? 직접 호출도 누적 카운터에 포함했는가?
- **P9.1–2:** 타입·월 범위 검사 전에 조회표를 읽지 않는가? 1900년과 2000년 결과가 다른가? 같은 private helper를 사용하는가?
- **P9.3–4:** 검증 전에 필드를 하나라도 바꾸지 않는가? 생성 실패는 ValueError, 갱신 실패는 출력·False·상태 유지인가?

관련 개념을 더 찾아보려면 [리스트·튜플·슬라이싱](/enai607-lecture02/), [딕셔너리·함수·인자와 전역 범위](/enai607-lecture03/), [예외 처리·모듈](/enai607-lecture04/), [클래스·private·클래스 변수](/enai607-lecture05/) 글로 이어진다. [Set A](/enai607-practice-set-a/)와 [Set B](/enai607-practice-set-b/)는 다른 요구사항을 같은 방식으로 코드에 연결한다.
