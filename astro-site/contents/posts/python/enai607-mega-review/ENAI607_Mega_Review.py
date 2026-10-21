"""Mega Review: A-H 통합 풀이. 기본 실행에는 키보드 입력이나 그래프 창이 없다."""

# === SETUP ===
from pathlib import Path
import math
import random
import sys
import numpy as np
import matplotlib

# 기본 실행은 PNG 저장만 한다. --show일 때만 환경의 그래픽 backend를 사용한다.
if "--show" not in sys.argv:
    matplotlib.use("Agg")
import matplotlib.pyplot as plt
import lab_strings  # [01] 같은 폴더의 모듈. 호출할 때 lab_strings.를 붙인다.

BASE_DIR = Path(__file__).resolve().parent  # 현재 터미널 위치가 아닌 코드 파일 위치.
DATA_FILE = BASE_DIR / "lab_readings.txt"
OUTPUT_FILE = BASE_DIR / "lab_summary.txt"
conversion_count = 0  # [02] rec_to_pol이 공유하는 모듈 수준의 누적 횟수.

# === A ===
class InvalidReadingError(Exception):  # [03] 이름·필드 구조 오류를 표현하는 사용자 예외.
    pass


def load_readings(filename):
    data = {}
    invalid = 0  # 반복문 밖: 각 줄마다 0으로 초기화하면 안 된다.
    with open(filename, "rt", encoding="utf-8") as file:  # [04] 끝나면 자동 close.
        for line in file:  # [05] readline을 중복 호출하지 않고 매 줄을 한 번씩 읽는다.
            if not line.strip():
                continue  # 빈 줄은 오류로 세지 않고 다음 줄로 넘어간다.
            fields = [field.strip() for field in line.split(",")]  # [06] 문자열 리스트.
            try:  # [07] 이 줄의 검증과 변환이 모두 끝나기 전에는 data를 바꾸지 않는다.
                if not fields[0] or len(fields) < 2:
                    raise InvalidReadingError("missing field")
                values = [float(field) for field in fields[1:]]
            except (InvalidReadingError, ValueError):
                invalid += 1  # 오류 값의 개수가 아니라 잘못된 줄 하나를 센다.
                continue  # Bad,3,hello,4에서 3과 4도 저장하지 않는다.
            if fields[0] in data:  # [08] 기존 이름이면 읽기 목록 뒤에 이어 붙인다.
                data[fields[0]].extend(values)
            else:
                data[fields[0]] = values
    return data, invalid  # [09] 쉼표가 있는 반환값은 두 항목 튜플이다.


def calculate_average(values):
    if not values:
        raise ValueError("empty readings")
    return sum(values) / len(values)


def make_report(data, invalid, filename=OUTPUT_FILE):
    # [10] name: 평균 구조이므로 딕셔너리 컴프리헨션이다.
    means = {name: calculate_average(vals) for name, vals in data.items()}
    # [06] 필터 뒤에 남는 것은 이름만 담은 리스트다.
    selected = [name for name, avg in means.items() if avg >= 15.0]
    # [11] items의 원소는 (이름, 평균). item[1]인 평균을 기준으로 내림차순 정렬.
    ordered = sorted(means.items(), key=lambda item: item[1], reverse=True)
    lines = []
    for number, (name, avg) in enumerate(ordered, start=1):  # [12] 1부터 번호 매김.
        status = "HIGH" if avg >= 20.0 else "LOW"  # [13] 한 줄 조건 표현식.
        lines.append(f"{number}. {name}: count = {len(data[name])}, "
                     f"average = {avg:.2f}, status = {status}")
    lines.append(f"Invalid lines: {invalid}")
    lines.append(f"Sensors with average >= 15.0: {selected}")
    with open(filename, "wt", encoding="utf-8") as file:
        # [01][04] write에는 문자열 하나. 모듈 함수로 줄들을 개행으로 연결한다.
        file.write(lab_strings.str_join(lines, "\n") + "\n")
    return means, selected, ordered

# === B_DEMO ===
def strings_demo():
    assert lab_strings.str_join(["red", "blue"], " / ") == "red / blue"
    assert lab_strings.str_join([]) == ""
    assert lab_strings.str_insert("abcdef", "XYZ", 3) == "abcXYZdef"
    assert lab_strings.str_insert("abcdef", "!", 6) == "abcdef!"
    assert lab_strings.str_insert("abc", "?", -1) is None  # 지정된 오류 메시지도 출력.
    assert lab_strings.is_palindrome("level") is True
    assert lab_strings.is_palindrome(123) is None
    assert lab_strings.is_palindrome("Python") is False
    assert lab_strings.center_with_dots("Data", 9) == "..Data..."
    print("String helpers OK:", lab_strings.center_with_dots("Lab", 9))

# === C ===
class Sensor:
    next_id = 0  # [14] 모든 Sensor·하위 클래스가 사용하는 하나의 공통 카운터.

    def __init__(self, name, readings):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("name must be a nonempty string")
        if not isinstance(readings, list):
            raise TypeError("readings must be a list")
        if not readings:
            raise ValueError("readings must be nonempty")
        for value in readings:
            self._validate_value(value)
        # 모든 검증을 통과한 객체만 ID를 배정하고 카운터를 증가시킨다.
        self.__id = Sensor.next_id
        Sensor.next_id += 1
        self.__name = name
        self.__readings = readings.copy()  # [15] 호출자가 원래 리스트를 바꿔도 보호.

    def _validate_value(self, value):
        # bool은 int의 하위 타입이지만 여기서는 센서 숫자로 허용하지 않는다.
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError("reading must be numeric")
        if value < 0:
            raise ValueError("reading must be nonnegative")

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_values(self):
        return self.__readings.copy()  # [15] 읽어 간 리스트를 수정해도 내부는 보호.

    def add_value(self, value):
        self._validate_value(value)
        self.__readings.append(value)  # 실패한 검증 후에는 이 줄에 도달하지 않는다.

    def get_average(self):
        return sum(self.__readings) / len(self.__readings)

    def __str__(self):
        # self.get_average()는 객체가 하위 클래스라면 재정의한 메서드를 호출한다.
        return (f"Sensor {self.__id} ({self.__name}): "
                f"n={len(self.__readings)}, avg={self.get_average():.2f}")

    @classmethod
    def get_sensor_count(cls):
        return Sensor.next_id  # 하위 클래스별 수가 아니라 전체 생성 수라는 의도.


class CalibratedSensor(Sensor):
    def __init__(self, name, readings, scale, offset):
        # 부모가 ID를 배정하기 전에 하위 클래스 인자도 먼저 검증한다.
        if (isinstance(scale, bool) or isinstance(offset, bool)
                or not isinstance(scale, (int, float))
                or not isinstance(offset, (int, float))):
            raise TypeError("scale and offset must be numeric")
        if scale <= 0:
            raise ValueError("scale must be positive")
        super().__init__(name, readings)  # [14] 복사·기본 검증·ID 배정을 부모에 맡긴다.
        self.__scale = scale
        self.__offset = offset

    def get_average(self):
        return self.__scale * super().get_average() + self.__offset

# === D ===
def roster_demo():
    students = [
        {"name": "Jodie", "grades": ["A", "A-", "B"]},
        {"name": "Paul", "grades": ["C", "B", "B"]},
        {"name": "Krissie", "grades": ["A-", "A", "B", "A+", "A"]},
        {"name": "Peter", "grades": ["D", "XF"]},
    ]
    students[2]["grades"].append("A")  # [08][15] 리스트 -> 딕셔너리 -> 내부 리스트.
    paul = students[1]["grades"]
    paul[0], paul[1] = paul[1], paul[0]  # 오른쪽 값을 먼저 구하므로 안전하게 교환.
    students.insert(2, {"name": "Joel", "grades": ["A", "C", "B", "B"]})
    assert students[2]["name"] == "Joel"  # 삽입 후 Krissie는 index 3이다.
    backup = students.copy()
    print("Before edits, identity/equality:", students is backup, students == backup)
    backup[0]["grades"][0] = "B+"  # 공유하는 안쪽 성적 리스트를 수정한다.
    assert students[0]["grades"][0] == "B+"
    backup[0] = {"name": "Replacement", "grades": []}  # backup의 바깥 칸 하나만 재대입.
    assert students[0]["name"] == "Jodie"
    independent = [{"name": s["name"], "grades": s["grades"].copy()}
                   for s in students]  # 학생마다 새 딕셔너리와 새 성적 리스트를 만든다.
    independent[0]["grades"][0] = "C"
    assert students[0]["grades"][0] == "B+"
    print("Original/independent first grades:", students[0]["grades"][0],
          independent[0]["grades"][0])
    print("After replacement, identity/equality:", students is backup, students == backup)
    accounts = {("joe", 786): 123456, ("jill", 545): 444567,
                ("ted", 346): 578345, ("gwen", 172): 771988}
    assert accounts[("jill", 545)] == 444567
    assert ("joe", 172) not in accounts  # 이름이 같아도 코드를 포함한 튜플 전체가 달라진다.
    accounts[("ted", 346)] = 576644
    accounts[("sasha", 988)] = 111111
    del accounts[("gwen", 172)]
    assert len(accounts) == 4
    products = [("widget", 5.28), ("gadget", 10.44),
                ("widget", 5.55), ("cool stuff", 6.87)]
    products.sort()  # [08] key 없음: 이름을 먼저 비교하고 같으면 가격을 비교한다.
    print("Sorted products:", products)
    return students, backup, independent, accounts, products

# === E ===
def rec_to_pol(z):
    global conversion_count  # [02] 전역 이름에 새 정수 값을 다시 대입하겠다는 선언.
    magnitude = abs(z)
    phase = math.atan2(z.imag, z.real)  # [17] (허수부, 실수부), 각도는 라디안.
    conversion_count += 1  # 계산이 성공한 뒤 집계한다.
    return magnitude, phase


def create_tuple(names, samples, num):
    if len(names) < num or len(samples) < num:
        return None  # zip이 짧은 입력에 맞춰 조용히 줄어들기 전에 거부한다.
    return tuple(zip(names[:num], samples[:num]))  # [12] num=0이면 ().


def apply_gain(z, gain=1.0):
    return z * gain  # [09] 기본 인자. complex는 불변이라 방어적 리스트 복사 불필요.


def apply_function(samples, operation):
    result = []
    for value in samples:
        result.append(operation(value))  # [17] 전달받은 함수 자체를 여기서 호출한다.
    return result


def complex_demo():
    samples = [1 + 1j, 3 + 4j, -1 + 1j]
    labels = ["S1", "S2", "S3", "EXTRA"]
    pairs = create_tuple(labels, samples, 3)
    assert len(pairs) == 3 and create_tuple(labels, samples, 4) is None
    assert create_tuple([], [], 0) == ()
    print("Complex pairs:", pairs)
    print("Default gain:", apply_gain(3 + 4j))
    print("Positional gain:", apply_gain(3 + 4j, 2))
    print("Keyword gain:", apply_gain(3 + 4j, gain=0.5))
    magnitudes = apply_function(samples, abs)  # 함수 전달은 이름만, 괄호 없음.
    before = conversion_count
    polar = apply_function(samples, rec_to_pol)
    assert conversion_count - before == 3  # 앞선 직접 호출이 있더라도 이번 횟수는 3.
    assert magnitudes == [abs(z) for z in samples]
    print("Polar values:", polar)
    print("Batch / total conversions:", conversion_count - before, conversion_count)
    return pairs, magnitudes, polar

# === F ===
class Date:
    DAYS_PER_MONTH = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
    MONTH_NAMES = ("January", "February", "March", "April", "May", "June",
                   "July", "August", "September", "October", "November", "December")

    def __init__(self, year, month, day):
        if not self.__valid_date(year, month, day):
            raise ValueError("Invalid date")
        self.__year, self.__month, self.__day = year, month, day

    def __valid_date(self, year, month, day):  # [14] 생성자·setter에서 공통 사용.
        if type(year) is not int or type(month) is not int or type(day) is not int:
            return False  # 날짜에서 bool은 정수로 허용하지 않는 정책.
        if year < 1 or not 1 <= month <= 12:
            return False  # 월을 인덱스로 쓰기 전에 범위를 먼저 검사한다.
        leap = (year % 4 == 0 and year % 100 != 0) or year % 400 == 0  # [16]
        limit = self.DAYS_PER_MONTH[month - 1]
        if month == 2 and leap:
            limit = 29  # 클래스 조회표는 그대로, 이번 검증의 지역 변수만 변경.
        return 1 <= day <= limit

    def set_date(self, year, month, day):
        if not self.__valid_date(year, month, day):
            print("Invalid date")
            return False
        # 전체 검증 뒤에만 세 값을 저장한다. 실패하면 기존 세 값이 모두 유지된다.
        self.__year, self.__month, self.__day = year, month, day
        return True

    def get_year(self):
        return self.__year

    def get_month(self):
        return self.__month

    def get_day(self):
        return self.__day

    def __str__(self):
        return f"{self.MONTH_NAMES[self.__month - 1]} {self.__day}, {self.__year}"


def dates_demo():
    print("Valid dates:", Date(2000, 2, 29), Date(2024, 2, 29))
    for year, month, day in [(1900, 2, 29), (2023, 2, 29), (2024, 4, 31)]:
        try:
            Date(year, month, day)
        except ValueError as error:
            print("Rejected:", (year, month, day), error)
    meeting = Date(2024, 2, 29)
    before = (meeting.get_year(), meeting.get_month(), meeting.get_day())
    assert meeting.set_date(2023, 2, 29) is False
    assert (meeting.get_year(), meeting.get_month(), meeting.get_day()) == before
    assert meeting.set_date(2023, 3, 1) is True
    print("Updated meeting date:", meeting)
    return meeting

# === G ===
def numerical_demo(show=False, output_dir=BASE_DIR):
    output_dir = Path(output_dir)
    # [18] 각 원소를 반복문으로 계산하지 않고 배열 전체에 연산한다.
    x = np.linspace(0, 10, 500)  # 양 끝 0, 10을 포함해 총 500개.
    f = np.sin(3 * x) * np.exp(-x / 2)
    g = np.cos(2 * x) * np.exp(-x / 2)
    assert f.shape == (500,) and g.shape == (500,)
    print("Curve shape / mean / std:", f.shape, np.mean(f), np.std(f))
    print("Max / index / x:", np.max(f), np.argmax(f), x[np.argmax(f)])
    matrix = f[:12].reshape(3, 4)  # 3*4=12. 이 예제에서는 f의 데이터도 공유한다.
    print("Matrix / transpose shapes:", matrix.shape, matrix.T.shape)
    view = matrix[1:, :2]  # [15][16] 1행 이후, 처음 두 열. 결과 shape (2,2).
    old = matrix[1, 0]
    view[0, 0] = -999
    assert matrix[1, 0] == -999 and f[4] == -999
    copied = matrix[1:, :2].copy()
    copied[0, 0] = -888
    assert matrix[1, 0] == -999
    matrix[1, 0] = old  # 공유된 f도 복구한 뒤 그래프를 그려야 한다.
    step_values = np.arange(0, 10, 2)  # 끝 10은 제외: 0,2,4,6,8.
    points = np.array([[1, 0], [0, 1], [1, 1], [2, 1], [-1, 1]])
    points_float = points.astype(float)  # 원래 정수 배열은 유지한다.
    A = np.array([[2.0, 1.0], [1.0, 2.0]])
    transformed = points_float @ A  # (5,2) @ (2,2) -> (5,2).
    inverse = np.linalg.inv(A)
    determinant = np.linalg.det(A)
    assert np.allclose(A @ inverse, np.eye(2))
    assert np.allclose(transformed @ inverse, points_float)
    b = np.array([7.0, 8.0])
    solution = np.linalg.solve(A, b)  # A @ solution = b를 만족하는 해.
    assert np.allclose(A @ solution, b)
    print("Metadata:", points.ndim, points.size, points.shape, points.dtype)
    print("Converted dtype / arange:", points_float.dtype, step_values)
    print("Determinant / solution:", determinant, solution)
    re = np.random.normal(0, 1 / np.sqrt(2), 10000)  # 두 번째 인자는 분산이 아닌 표준편차.
    im = np.random.normal(0, 1 / np.sqrt(2), 10000)
    z = re + 1j * im
    r = np.abs(z)  # 복소수 배열 전체의 크기. 각 원소 sqrt(re**2+im**2).
    simulation = plt.figure(figsize=(8, 7))
    plt.subplot(2, 1, 1)  # 2행 1열 중 첫 번째. subplot 번호는 1부터.
    plt.plot(x, f, label="f(x) = sin(3x) exp(-x/2)")
    plt.plot(x, g, label="g(x) = cos(2x) exp(-x/2)")
    plt.title("Damped Curves")
    plt.xlabel("x")
    plt.ylabel("Value")
    plt.grid(True)
    plt.legend()
    plt.subplot(2, 1, 2)
    histogram_counts, bin_edges, _ = plt.hist(r, bins=100)
    plt.title("Rayleigh Magnitudes")
    plt.xlabel("Magnitude")
    plt.ylabel("Count")  # density=True를 주지 않았으므로 구간별 개수.
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_dir / "lab_simulation.png", dpi=160)
    scatter = plt.figure(figsize=(6, 5))
    plt.scatter(points_float[:, 0], points_float[:, 1], label="Original", marker="o")
    plt.scatter(transformed[:, 0], transformed[:, 1], label="Transformed", marker="x")
    plt.title("Original and Transformed Points")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_dir / "lab_scatter.png", dpi=160)
    bars = plt.figure(figsize=(6, 4))
    categories = ["Low", "Medium", "High"]
    counts = [12, 7, 15]  # 별도 예제 빈도. 센서 보고서에서 집계한 값은 아니다.
    centers = np.arange(3)
    plt.bar(centers, counts, width=0.35, edgecolor="black")
    plt.xticks(centers, categories)
    plt.title("Reading Categories")
    plt.xlabel("Category")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(output_dir / "lab_bars.png", dpi=160)
    if show:
        plt.show()  # 세 파일의 저장이 모두 끝난 뒤 선택적으로 창을 연다.
    for figure in (simulation, scatter, bars):
        plt.close(figure)  # 그리기 객체 정리이며 원소별 수치 계산 반복문이 아니다.
    return {"x": x, "f": f, "g": g, "matrix": matrix, "points": points,
            "points_float": points_float, "A": A, "transformed": transformed,
            "inverse": inverse, "determinant": determinant, "solution": solution,
            "r": r, "z": z, "histogram_counts": histogram_counts, "bin_edges": bin_edges}

# === H ===
def judge_round(player, computer):
    # [05] 입력과 난수 생성을 분리한 순수 판정. 유효한 0,1,2가 들어온다는 전제.
    if player == computer:
        return "TIE"
    elif ((player == 0 and computer == 2) or
          (player == 1 and computer == 0) or
          (player == 2 and computer == 1)):
        return "WIN"
    else:
        return "LOSS"


def play_training_game():
    names = ["Rock", "Paper", "Scissors"]
    wins = losses = ties = 0  # 반복문 밖에서 한 번만 초기화한다.
    while True:
        raw = input("Gesture (0=Rock, 1=Paper, 2=Scissors, -1=Quit): ")
        try:
            player = int(raw)
        except ValueError:
            print("Invalid integer input.")
            continue  # 아래 난수 생성과 통계 갱신을 실행하지 않는다.
        if player == -1:
            break  # 통계를 출력해야 하므로 여기서 바로 sys.exit하지 않는다.
        if player not in (0, 1, 2):
            print("Invalid gesture.")
            continue
        computer = random.randrange(3)  # 0,1,2 중 하나. 정상 입력에 대해서만 호출.
        outcome = judge_round(player, computer)
        print(f"You: {names[player]}; Computer: {names[computer]}; {outcome}")
        if outcome == "WIN":
            wins += 1
        elif outcome == "LOSS":
            losses += 1
        else:
            ties += 1
    print(f"Wins: {wins}, Losses: {losses}, Ties: {ties}, Total: {wins + losses + ties}")
    sys.exit(0)  # 루프 밖에서 통계 출력 후 프로그램 종료.

# === MAIN ===
def main():
    print("=== ENAI 607 MEGA REVIEW ===")
    if not DATA_FILE.exists():
        raise FileNotFoundError("lab_readings.txt must be beside the script")
    data, invalid = load_readings(DATA_FILE)  # [09] 두 반환값을 따로 받는다.
    means, selected, ordered = make_report(data, invalid)
    assert invalid == 1 and means["Ava"] == 24.0  # 제공된 입력 파일의 예상값.
    assert selected == ["Ava", "Ben"]
    print("Report:", OUTPUT_FILE.name, "Sorted:", ordered)
    strings_demo()
    count_before = Sensor.get_sensor_count()
    original = data["Ava"].copy()
    sensors = [Sensor("Ava", original), CalibratedSensor("Ben", data["Ben"], 1.5, 2.0)]
    assert sensors[0].get_id() != sensors[1].get_id()
    assert Sensor.get_sensor_count() - count_before == 2
    original[0] = -500  # 생성자 입력 목록을 바꿔도 내부 목록은 그대로여야 한다.
    first_copy = sensors[0].get_values()
    first_copy[0] = -900  # getter 반환 목록을 바꿔도 내부 목록은 그대로여야 한다.
    assert sensors[0].get_values()[0] == 10.0
    for bad_value, exception in [(-1, ValueError), ("bad", TypeError)]:
        try:
            sensors[0].add_value(bad_value)
        except exception as error:
            print("Reading rejected:", error)
        else:
            raise AssertionError("invalid reading was accepted")
    assert math.isclose(sensors[1].get_average(), 24.5)
    for sensor in sensors:
        print(sensor)  # __str__ 내부의 self.get_average는 하위 클래스도 구분한다.
    roster_demo()
    complex_demo()
    dates_demo()
    numerical_demo(show="--show" in sys.argv)
    expected = [["TIE", "LOSS", "WIN"], ["WIN", "TIE", "LOSS"], ["LOSS", "WIN", "TIE"]]
    for player in range(3):
        for computer in range(3):
            assert judge_round(player, computer) == expected[player][computer]
    for name in ("lab_summary.txt", "lab_simulation.png", "lab_scatter.png", "lab_bars.png"):
        assert (BASE_DIR / name).is_file()
    print("All checks passed. Optional mode: --game or --show")


if __name__ == "__main__":  # [01] import할 때는 main이 자동으로 실행되지 않는다.
    if "--game" in sys.argv:
        play_training_game()
    else:
        main()
