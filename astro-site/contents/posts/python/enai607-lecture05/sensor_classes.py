"""Lecture 05: Sensor and CalibratedSensor, runnable Problem 2 solution."""


class Sensor:
    next_id = 0

    def __init__(self, name, readings):
        if not name:
            raise ValueError("name must not be empty")
        if not readings:
            raise ValueError("readings must not be empty")

        for value in readings:
            self._validate_value(value)

        self.__name = name
        self.__values = readings.copy()
        self.__id = Sensor.next_id
        Sensor.next_id += 1

    def _validate_value(self, value):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError("reading must be numeric")
        if not value >= 0:
            raise ValueError("reading must be nonnegative")

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_values(self):
        return self.__values.copy()

    def add_value(self, value):
        self._validate_value(value)
        self.__values.append(value)

    def get_average(self):
        return sum(self.__values) / len(self.__values)

    def __str__(self):
        return (
            f"Sensor {self.get_id()} ({self.get_name()}): "
            f"count = {len(self.__values)}, "
            f"average = {self.get_average():.2f}"
        )

    @classmethod
    def get_sensor_count(cls):
        return Sensor.next_id


class CalibratedSensor(Sensor):
    def __init__(self, name, readings, scale, offset):
        if isinstance(scale, bool) or not isinstance(scale, (int, float)):
            raise TypeError("scale must be numeric")
        if not scale > 0:
            raise ValueError("scale must be positive")
        if isinstance(offset, bool) or not isinstance(offset, (int, float)):
            raise TypeError("offset must be numeric")

        super().__init__(name, readings)
        self.__scale = scale
        self.__offset = offset

    def get_average(self):
        original_average = super().get_average()
        return self.__scale * original_average + self.__offset


def main():
    source = [10, 20, 30]
    s1 = Sensor("Ava", source)
    s2 = CalibratedSensor("Ben", [4, 6], 1.5, 2.0)

    print(s1.get_average())
    print(s2.get_average())
    s1.add_value(40)
    print(s1.get_average())
    print(Sensor.get_sensor_count())

    print("IDs:", s1.get_id(), s2.get_id())
    print("Names:", s1.get_name(), s2.get_name())

    source[0] = 999
    print("After changing input:", s1.get_values())
    exported = s1.get_values()
    exported[0] = -999
    print("After changing returned list:", s1.get_values())

    s2.add_value(8)
    print("Child readings:", s2.get_values())
    print("Child average:", s2.get_average())
    print(s1)
    print(s2)
    print("Count through child:", CalibratedSensor.get_sensor_count())

    try:
        s1.add_value(-5)
    except ValueError as exc:
        print(f"ValueError: {exc}")
    print("After failed add:", s1.get_values())


if __name__ == "__main__":
    main()
