"""문제 4: 문자열을 수정하지 않고 새 문자열을 만드는 작은 모듈."""


def str_join(strings, sep=""):
    # [P4.1-A] 인자를 생략하면 sep는 빈 문자열이므로 원소끼리 바로 연결된다.
    result = ""
    for index, item in enumerate(strings):
        # [P4.1-B] 첫 원소 앞에는 구분자를 넣지 않는다.
        # 두 번째 원소부터 '구분자 + 현재 원소'를 추가하면 끝에도 남지 않는다.
        if index > 0:
            result += sep
        result += item
    # [P4.1-C] 빈 리스트면 반복문이 0번 실행되어 빈 문자열을 반환한다.
    return result


def str_insert(dest_str, ins_str, pos):
    # [P4.2-A] 끝에 붙이는 위치 len(dest_str)도 유효하므로 <=를 쓴다.
    if not isinstance(pos, int) or not 0 <= pos <= len(dest_str):
        print("str_insert(): position input parameter out of range.")
        return None
    # [P4.2-B] 왼쪽은 pos 직전까지, 오른쪽은 pos부터다.
    left = dest_str[:pos]
    right = dest_str[pos:]
    # [P4.2-C] 내장 .join() 대신 위에서 직접 만든 함수를 호출해야 한다.
    return str_join([left, ins_str, right])


def is_palindrome(text):
    # [P4.3-A] 타입부터 확인해야 정수 등에 슬라이싱을 시도하지 않는다.
    if not isinstance(text, str):
        print("is_palindrome(): the input parameter must be a string.")
        return None
    # [P4.3-B] -1 간격으로 역순 문자열을 만들고 원문과 그대로 비교한다.
    return text == text[::-1]


def center_with_dots(text, width):
    # [P4.3-C] 문제의 전제: width는 len(text) 이상의 정수다.
    padding = width - len(text)
    left_count = padding // 2
    right_count = padding - left_count  # 홀수면 나머지 한 개가 오른쪽으로 간다.
    # [P4.3-D] str.center()를 호출하지 않고 반복·연결로 새 문자열 생성.
    return "." * left_count + text + "." * right_count
