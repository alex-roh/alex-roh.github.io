"""예상문제 1: 센서 파일을 읽고 정렬된 summary.txt를 만든다."""
from pathlib import Path
import argparse

# 터미널의 현재 폴더가 아니라 이 코드 파일의 폴더를 기준으로 한다.
BASE_DIR = Path(__file__).resolve().parent


def load_readings(filename):
    data = {}        # 센서 이름 -> 유효한 실수 측정값 리스트
    invalid_lines = 0

    # filename이 절대 경로면 그대로 사용하고, 상대 경로면 BASE_DIR에 붙인다.
    with open(BASE_DIR / filename, "rt", encoding="utf-8") as fobj:
        for line in fobj:
            if not line.strip():
                continue  # 빈 줄과 공백만 있는 줄은 오류로 세지 않는다.

            fields = [field.strip() for field in line.split(",")]
            try:
                # 숫자 항목이 없으면 빈 리스트 평균이 생기므로 미리 거른다.
                # 빈 이름도 유효한 센서로 저장하지 않는 추가 검증이다.
                if len(fields) < 2 or not fields[0]:
                    raise ValueError("센서 이름과 숫자 한 개 이상이 필요함")

                # 이 줄의 숫자를 전부 바꾼 뒤에만 data에 반영한다.
                # 하나라도 실패하면 이 줄에서 앞서 바꾼 값도 저장되지 않는다.
                values = [float(field) for field in fields[1:]]
            except ValueError:
                invalid_lines += 1  # 잘못된 필드 수가 아니라 잘못된 줄 수
                continue

            name = fields[0]
            if name in data:
                data[name].extend(values)  # 반복된 이름은 기존 목록에 이어 붙임
            else:
                data[name] = values

    return data, invalid_lines  # 두 값을 튜플로 반환


def calculate_average(values):
    # 문제에서 비어 있지 않은 리스트를 받는다고 했으므로 그대로 계산한다.
    return sum(values) / len(values)


def write_summary(data, invalid_lines, output_filename="summary.txt"):
    # 요구사항: 딕셔너리 comprehension으로 센서별 평균을 만든다.
    average_data = {
        sensor: calculate_average(values) for sensor, values in data.items()
    }

    # 요구사항: sorted + key에 전달한 lambda.
    # 첫 키를 -평균으로 만들면 평균이 큰 것이 먼저 온다.
    # 평균이 같으면 이름 오름차순으로 정해 입력 순서에 영향받지 않게 한다.
    sorted_names = sorted(
        average_data, key=lambda sensor: (-average_data[sensor], sensor)
    )

    # 요구사항: 필터가 있는 리스트 comprehension. 보고서와 같은 순서로 나열.
    selected_sensors = [
        sensor for sensor in sorted_names if average_data[sensor] >= 15.0
    ]

    with open(BASE_DIR / output_filename, "wt", encoding="utf-8") as fobj:
        for number, sensor in enumerate(sorted_names, start=1):
            average = average_data[sensor]
            status = "HIGH" if average >= 20.0 else "LOW"  # 조건 표현식
            fobj.write(
                f"{number}. {sensor}: count = {len(data[sensor])}, "
                f"average = {average:.2f}, status = {status}\n"
            )
        fobj.write(f"Invalid lines: {invalid_lines}\n")
        # write()는 문자열 하나만 받으므로 리스트도 f-string 안에서 문자열화.
        fobj.write(f"Sensors with average >= 15.0: {selected_sensors}\n")


def main(filename):
    data, invalid_lines = load_readings(filename)
    write_summary(data, invalid_lines)
    print((BASE_DIR / "summary.txt").read_text(encoding="utf-8"), end="")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="센서 파일에서 summary.txt 생성")
    # 실행 예: python problem_1.py sensor_data.txt
    # 인자를 생략하면 같은 폴더의 sensor_data.txt를 사용한다.
    parser.add_argument("filename", nargs="?", default="sensor_data.txt")
    main(parser.parse_args().filename)
