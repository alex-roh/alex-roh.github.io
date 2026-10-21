"""B: 메인 프로그램에서 import하는 독립 문자열 모듈."""


def str_join(strings, sep=""):
    """내장 join을 사용하지 않고, 항목 사이에만 구분자를 넣는다."""
    result = ""
    for index, item in enumerate(strings):  # [05][12] 순서와 값을 함께 받는다.
        if index > 0:  # 첫 항목 앞에는 구분자가 없어야 한다.
            result += sep
        result += item
    return result  # 빈 입력이면 반복 없이 빈 문자열이 반환된다.


def str_insert(dest_str, ins_str, pos):
    """끝 위치도 유효하다. 잘못된 위치는 출력 후 None: M1의 raise와 다르다."""
    if pos < 0 or pos > len(dest_str):
        print("str_insert(): position input parameter out of range.")
        return None
    # [16] pos 앞부분 + 삽입 문자열 + pos부터의 뒷부분을 직접 만든 함수로 연결한다.
    return str_join([dest_str[:pos], ins_str, dest_str[pos:]])


def is_palindrome(text):
    if not isinstance(text, str):  # 숫자에는 문자열 역순 슬라이싱을 적용하지 않는다.
        print("is_palindrome(): the input parameter must be a string.")
        return None
    return text == text[::-1]  # 대소문자·문장부호를 그대로 비교한다.


def center_with_dots(text, width):
    padding = width - len(text)
    if padding < 0:
        raise ValueError("width must be at least the text length")
    left = padding // 2  # [16] 홀수 패딩의 남는 한 칸은 오른쪽으로 보낸다.
    right = padding - left
    return "." * left + text + "." * right  # 내장 center를 사용하지 않는다.
