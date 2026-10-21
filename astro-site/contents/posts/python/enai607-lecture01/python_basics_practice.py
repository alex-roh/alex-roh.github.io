"""Lecture 01 종합 연습. Python 표준 라이브러리만 사용한다."""
import math


def factorial_demo():
    # 먼저 문자열을 받고, 정수로 변환한 뒤 범위를 따로 검사한다.
    text = input("Nonnegative integer: ")
    try:
        number = int(text)
    except ValueError:
        print("Invalid integer")
    else:
        if number < 0:
            print("The integer must be nonnegative")
        else:
            remaining = number
            factorial = 1
            while remaining > 1:
                factorial *= remaining
                remaining -= 1
            print(f"{number:d}! = {factorial:d}")


def arithmetic_demo():
    print("-11 / 2:", -11 / 2)
    print("-11 // 2:", -11 // 2)
    print("int(-11 / 2):", int(-11 / 2))
    print("-11 % 2:", -11 % 2)
    print("round(2.5), round(3.5):", round(2.5), round(3.5))
    print("0.1 + 0.2:", 0.1 + 0.2)
    print("isclose:", math.isclose(0.1 + 0.2, 0.3))


def reference_demo():
    a = [10, 20]
    b = a
    print("Same object:", a is b)
    a.append(30)
    print("After append:", a, b)
    a = [99]
    print("After rebinding:", a, b)


def logic_demo():
    print('bool("False"):', bool("False"))
    print("bool([0]):", bool([0]))
    print("5 and 2:", 5 and 2)
    print("0 or 20:", 0 or 20)
    reading = 0
    print("reading is None:", reading is None)
    count = 0
    print("Short circuit:", count != 0 and 10 / count > 2)


def main():
    print("1: arithmetic, 2: references, 3: logic, 4: factorial")
    choice = input("Choose 1-4: ").strip()
    if choice == "1":
        arithmetic_demo()
    elif choice == "2":
        reference_demo()
    elif choice == "3":
        logic_demo()
    elif choice == "4":
        factorial_demo()
    else:
        print("Invalid choice")


if __name__ == "__main__":
    main()
