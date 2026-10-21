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
