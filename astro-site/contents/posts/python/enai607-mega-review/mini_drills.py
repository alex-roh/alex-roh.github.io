"""M1-M6 독립 연습 함수. 기본 실행은 입력을 기다리지 않는다."""
import sys

# === M1 ===
def insert_text(text, addition, pos):
    # 통합 B의 str_insert와 달리, 이 문제는 잘못된 위치에 예외를 요구한다.
    if pos < 0 or pos > len(text):
        raise ValueError("invalid position")
    # pos는 새 문자가 들어갈 위치다. 앞은 pos 미포함, 뒤는 pos부터 시작한다.
    return text[:pos] + addition + text[pos:]


def is_palindrome(text):
    # 이 미니 문제는 문자열 입력을 전제로 한다. 역순과 원래 값을 비교한다.
    return text == text[::-1]


def m1_demo():
    print(insert_text("ABCD", "xy", 2))  # ABxyCD
    print(is_palindrome("level"))  # True

# === M2 ===
def m2_demo():
    roster = {"Ava": {"grades": [80, 90]}}
    other = roster.copy()  # 새 바깥 dict만 생성. 내부 dict와 list는 공유한다.
    other["Ava"]["grades"].append(100)
    print(roster["Ava"]["grades"])  # [80, 90, 100]
    print(roster is other, roster == other)  # False True
    # 비교를 위해 초기 데이터를 다시 만든다. 이미 100이 추가된 원본을 복사하지 않는다.
    roster = {"Ava": {"grades": [80, 90]}}
    independent = {name: {"grades": record["grades"].copy()}
                   for name, record in roster.items()}
    independent["Ava"]["grades"].append(100)
    print(roster["Ava"]["grades"])  # [80, 90]
    print(roster is independent, roster == independent)  # False False
    return roster, independent

# === M3 ===
def apply_each(values, operation):
    # operation에는 함수가 들어온다. 반환값들로 새 리스트를 만들어 원본을 유지한다.
    return [operation(value) for value in values]


def multiply(x, factor=2):
    return x * factor  # factor를 생략하면 2, 이름으로 전달하면 해당 값 사용.


def m3_demo():
    values = [-2, -1, 3]
    print(apply_each(values, abs))  # [2, 1, 3]
    print(apply_each(values, lambda x: multiply(x)))  # [-4, -2, 6]
    print(multiply(5))  # 10: 기본 인자.
    print(multiply(5, factor=3))  # 15: 키워드 인자.

# === M4 ===
calls = 0  # 함수 호출마다 새로 만들지 않는 모듈 수준 변수.


def counted_square(x):
    global calls  # calls += 1이 지역 이름 재대입으로 해석되지 않게 한다.
    answer = x * x  # answer는 이번 호출만의 지역 변수다.
    calls += 1
    return answer


def m4_demo():
    before = calls
    print(counted_square(3))  # 9
    print(counted_square(4))  # 16
    print("Batch calls:", calls - before)  # 2
    print("Total calls:", calls)  # 처음 실행하면 2. 반복 호출 시 누적된다.

# === M5 ===
def read_nonnegative_integer():
    while True:
        raw = input("Nonnegative integer (q to quit): ")
        if raw == "q":
            break  # 가장 가까운 while만 끝낸 뒤 함수 마지막 return None으로 이동.
        try:
            number = int(raw)
        except ValueError:
            print("Invalid integer")
            continue  # 범위 검사를 실행하지 않고 입력부터 다시 받는다.
        if number < 0:
            print("Negative value")
            continue
        return number  # 정상 입력: 반복문뿐 아니라 이 함수 자체를 끝낸다.
    return None


def exit_program():
    print("Bye")
    sys.exit(0)  # SystemExit를 발생시켜 보통 스크립트를 종료한다.

# === M6 ===
def m6_demo():
    import numpy as np
    names = ["Ava", "Ben"]
    points = [8, 10]
    records = {(name, index): score
               for index, (name, score) in enumerate(zip(names, points), start=1)}
    print(records)  # {('Ava', 1): 8, ('Ben', 2): 10}
    a = np.array([[1, 2, 3], [4, 5, 6]])  # shape (2,3).
    b = np.array([10, 20, 30])  # shape (3,): 각 행의 세 열과 맞춰진다.
    result = a + b  # Python 리스트의 +가 아니라 NumPy 원소별 덧셈과 broadcasting.
    print(result)  # [[11 22 33], [14 25 36]]
    print(result.shape)  # (2,3).
    return records, result

# === MINI_MAIN ===
if __name__ == "__main__":
    if "--exit" in sys.argv:
        exit_program()
    elif "--input" in sys.argv:
        print("Returned:", read_nonnegative_integer())
    else:
        for demo in (m1_demo, m2_demo, m3_demo, m4_demo, m6_demo):
            print("---", demo.__name__, "---")
            demo()
        print("M5 입력 연습: python mini_drills.py --input")
        print("종료 연습: python mini_drills.py --exit")
