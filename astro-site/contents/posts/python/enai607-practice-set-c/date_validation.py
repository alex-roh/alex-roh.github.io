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
