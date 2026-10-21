"""예상문제 2: Sensor와 CalibratedSensor의 상속·복사·검증."""


class Sensor:
    # 부모·자식 전체가 함께 사용하는 '다음 ID'. 성공한 생성 수와 같다.
    next_id = 0

    def __init__(self, name, readings):
        # name과 readings의 컨테이너 타입은 문제의 전제를 따른다.
        if not name:
            raise ValueError("센서 이름은 비어 있으면 안 됨")
        if not readings:
            raise ValueError("측정값 리스트는 비어 있으면 안 됨")
        for value in readings:
            self._validate_value(value)

        # 두 개의 밑줄: private 인스턴스 필드(name mangling).
        # 원본을 복사해야 호출자가 입력 리스트를 바꿔도 저장값은 유지된다.
        self.__name = name
        self.__values = readings.copy()

        # 모든 검증이 끝난 뒤 ID를 부여하여 실패한 생성은 세지 않는다.
        # self.next_id 또는 type(self).next_id로 증가시키지 않는다.
        self.__id = Sensor.next_id
        Sensor.next_id += 1

    def _validate_value(self, value):
        # bool은 int의 하위 타입이지만 측정값으로는 받지 않는 정책이다.
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError("측정값은 int 또는 float이어야 함")
        if not value >= 0:
            raise ValueError("측정값은 0 이상이어야 함")

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_values(self):
        # getter에서도 복사해야 외부에서 private 리스트를 변경할 수 없다.
        return self.__values.copy()

    def add_value(self, value):
        self._validate_value(value)  # 검사 실패 시 append까지 도달하지 않음
        self.__values.append(value)

    def get_average(self):
        return sum(self.__values) / len(self.__values)

    def __str__(self):
        # self.get_average()는 자식 객체에서 재정의한 메서드를 호출한다.
        return (
            f"Sensor {self.get_id()} ({self.get_name()}): "
            f"count = {len(self.__values)}, average = {self.get_average():.2f}"
        )

    @classmethod
    def get_sensor_count(cls):
        # cls 인자는 클래스 메서드 규약에 따라 받는다.
        # 반환할 값은 계층 전체의 공유 카운터이므로 부모 이름을 명시한다.
        return Sensor.next_id


class CalibratedSensor(Sensor):
    def __init__(self, name, readings, scale, offset):
        # 부모 생성자가 ID를 증가시키기 전에 보정 인자부터 검사한다.
        if isinstance(scale, bool) or not isinstance(scale, (int, float)):
            raise TypeError("scale은 숫자여야 함")
        if not scale > 0:
            raise ValueError("scale은 0보다 커야 함")
        if isinstance(offset, bool) or not isinstance(offset, (int, float)):
            raise TypeError("offset은 숫자여야 함")

        # 부모가 이름·측정값·ID를 초기화한다. 부모 로직을 중복 작성하지 않음.
        super().__init__(name, readings)
        self.__scale = scale
        self.__offset = offset

    def get_average(self):
        # 자기 자신을 다시 호출하면 재귀가 되므로 super()로 원래 평균을 구함.
        original_average = super().get_average()
        return self.__scale * original_average + self.__offset


def main():
    source = [10, 20, 30]
    s1 = Sensor("Ava", source)
    s2 = CalibratedSensor("Ben", [4, 6], 1.5, 2.0)
    print(s1.get_average())            # 20.0
    print(s2.get_average())            # 9.5
    s1.add_value(40)
    print(s1.get_average())            # 25.0
    print(Sensor.get_sensor_count())   # 2: 이 스크립트를 새로 실행했을 때

    print("IDs:", s1.get_id(), s2.get_id())
    print("Names:", s1.get_name(), s2.get_name())

    # 생성자 입력 리스트를 나중에 바꿔도 객체가 바뀌지 않는지 확인.
    source[0] = 999
    print("입력 리스트 변경 후:", s1.get_values())
    # getter 결과를 바꿔도 객체가 바뀌지 않는지 별도로 확인.
    exported = s1.get_values()
    exported[0] = -999
    print("반환 리스트 변경 후:", s1.get_values())

    s2.add_value(8)  # 부모의 add_value를 상속받아 그대로 사용한다.
    print("자식 측정값:", s2.get_values())
    print("자식 보정 평균:", s2.get_average())
    print(s1)  # __str__ 자동 호출
    print(s2)  # 부모 __str__ 안에서 자식의 get_average 호출
    print("자식 클래스로 조회한 전체 수:", CalibratedSensor.get_sensor_count())

    try:
        s1.add_value(-5)
    except ValueError as error:
        print(f"ValueError: {error}")
    print("추가 실패 후 원본:", s1.get_values())

    # 현재 객체 둘의 ID가 중복되지 않는지, 값이 유지되는지 실제 검증.
    assert s1.get_id() != s2.get_id()
    assert s1.get_values() == [10, 20, 30, 40]
    assert s2.get_values() == [4, 6, 8]
    assert s2.get_average() == 11.0


if __name__ == "__main__":
    main()
