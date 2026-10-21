"""Lecture 02: Run this file directly; no packages or input files needed.

Input grammar: sensor name, one or more float-convertible readings.
Quoted CSV fields are not supported. Blank lines are skipped.
The sensor name only needs to be nonempty after stripping whitespace.
Like float(), this example accepts nan/inf; add math.isfinite if forbidden.
"""


def parse_reading(line):
    """Return (name, values), return None for blanks, or raise ValueError."""
    if not line.strip():
        return None
    fields = [field.strip() for field in line.split(",")]
    if len(fields) < 2 or not fields[0]:
        raise ValueError("센서 이름과 숫자 한 개 이상이 필요함")
    name = fields[0]
    values = [float(field) for field in fields[1:]]
    return name, values


def format_reading(name, values):
    """Format a parsed record; values must be a nonempty numeric list."""
    average = sum(values) / len(values)
    readings = ", ".join([f"{value:.2f}" for value in values])
    return (f"{name}: count={len(values)}, average={average:.2f}, "
            f"readings=[{readings}]")


def check_examples():
    """Small executable checks for the concepts used in this exercise."""
    assert [0, 1, 2, 3, 4][1:4:2] == [1, 3]
    assert [0, 1, 2, 3, 4][::-1] == [4, 3, 2, 1, 0]
    assert " A B ".strip() == "A B"
    assert "A,,B,".split(",") == ["A", "", "B", ""]
    assert "rAtArthur".lstrip("Art") == "hur"
    assert "rAtArthur".removeprefix("Art") == "rAtArthur"
    assert f"{21764.32:8.1f}" == " 21764.3"
    assert f"{1987:b}" == "11111000011"
    assert parse_reading(" \t\n") is None
    assert parse_reading(" A , 18.5 , 21.0 ") == ("A", [18.5, 21.0])
    assert format_reading("A", [18.5, 21.0]) == (
        "A: count=2, average=19.75, readings=[18.50, 21.00]"
    )
    for invalid in ["A", ",1", "A,", "A,1,,2", "A,wrong"]:
        try:
            parse_reading(invalid)
        except ValueError:
            pass
        else:
            raise AssertionError(f"Expected invalid input: {invalid!r}")


def main():
    check_examples()
    lines = [
        "  sensor_A , 18.5 , 21.0 , 23.5 \n",
        "sensor_B,10,15",
        "   \n",
        ",18.5",
        "sensor_C",
        "sensor_D,wrong",
        "sensor_E,1,,2",
    ]
    for number, line in enumerate(lines, start=1):
        try:
            record = parse_reading(line)
        except ValueError as error:
            print(f"{number}. 오류: {error}")
        else:
            if record is None:
                print(f"{number}. 빈 줄: 건너뜀")
            else:
                name, values = record
                print(f"{number}. {format_reading(name, values)}")


if __name__ == "__main__":
    main()
