"""세 문제의 정상 입력·경계 조건·복사·수치/그래프 결과를 검증한다."""
from pathlib import Path
import tempfile
import unittest
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from problem_3 import (create_curves, make_slice_examples, solve_system,
                              generate_rayleigh, make_figure)


class SimulationTests(unittest.TestCase):
    def test_grid_endpoints_and_spacing(self):
        x, f, g = create_curves()
        self.assertEqual(x.shape, (500,))
        self.assertEqual(f.shape, x.shape)
        self.assertEqual(g.shape, x.shape)
        self.assertEqual(x[0], 0)
        self.assertEqual(x[-1], 10)
        np.testing.assert_allclose(np.diff(x), 10 / 499)

    def test_functions_and_maximum_coordinate(self):
        x, f, g = create_curves()
        np.testing.assert_allclose(f, np.sin(3 * x) * np.exp(-x / 2))
        np.testing.assert_allclose(g, np.cos(2 * x) * np.exp(-x / 2))
        self.assertEqual(f[np.argmax(f)], f.max())
        self.assertGreater(x[np.argmax(f)], 0)
        self.assertTrue(np.isfinite(f.std()))

    def test_view_copy_and_original_curve(self):
        _, f, _ = create_curves()
        before = f.copy()
        initial, transpose, matrix, view, independent, copied = make_slice_examples(f)
        self.assertEqual(initial.shape, (3, 4))
        self.assertEqual(transpose.shape, (4, 3))
        self.assertEqual(view.shape, (2, 2))
        self.assertTrue(np.shares_memory(matrix, view))
        self.assertEqual(matrix[1, 0], -1)
        self.assertFalse(np.shares_memory(independent, copied))
        np.testing.assert_array_equal(independent, initial)
        np.testing.assert_array_equal(f, before)
        np.testing.assert_array_equal(transpose, initial.T)

    def test_linear_system(self):
        A, b, solution = solve_system()
        np.testing.assert_allclose(solution, [2, 3])
        np.testing.assert_allclose(A @ solution, b)

    def test_complex_magnitudes_and_shapes(self):
        real, imag, z, magnitude = generate_rayleigh()
        self.assertEqual(real.shape, (10_000,))
        self.assertEqual(imag.shape, real.shape)
        self.assertTrue(np.iscomplexobj(z))
        np.testing.assert_array_equal(z.real, real)
        np.testing.assert_array_equal(z.imag, imag)
        np.testing.assert_allclose(magnitude, np.sqrt(real**2 + imag**2))
        self.assertTrue(np.all(magnitude >= 0))

    def test_random_parameters_sanity(self):
        real, imag, _, magnitude = generate_rayleigh(seed=607)
        self.assertLess(abs(real.mean()), 0.03)
        self.assertLess(abs(imag.mean()), 0.03)
        self.assertAlmostEqual(real.std(), 1 / np.sqrt(2), delta=0.03)
        self.assertAlmostEqual(imag.std(), 1 / np.sqrt(2), delta=0.03)
        self.assertLess(abs(np.corrcoef(real, imag)[0, 1]), 0.05)
        self.assertAlmostEqual(np.mean(magnitude**2), 1, delta=0.05)

    def test_histogram_and_saved_figure(self):
        x, f, g = create_curves()
        *_, magnitude = generate_rayleigh()
        fig, axes, counts, edges = make_figure(x, f, g, magnitude)
        try:
            self.assertEqual(len(fig.axes), 2)
            self.assertEqual(len(axes[0].lines), 2)
            self.assertEqual(counts.shape, (100,))
            self.assertEqual(edges.shape, (101,))
            self.assertEqual(counts.sum(), 10_000)
            with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as folder:
                output = Path(folder) / "test.png"
                fig.savefig(output)
                self.assertGreater(output.stat().st_size, 0)
        finally:
            plt.close(fig)

    def test_invalid_sample_count(self):
        with self.assertRaises(ValueError):
            generate_rayleigh(0)
        with self.assertRaises(ValueError):
            generate_rayleigh(-1)



import unittest
from problem_2 import Sensor, CalibratedSensor


class SensorTests(unittest.TestCase):
    def test_required_examples(self):
        before = Sensor.get_sensor_count()
        s1 = Sensor("Ava", [10, 20, 30])
        s2 = CalibratedSensor("Ben", [4, 6], 1.5, 2.0)
        self.assertEqual(s1.get_average(), 20.0)
        self.assertEqual(s2.get_average(), 9.5)
        s1.add_value(40)
        self.assertEqual(s1.get_average(), 25.0)
        self.assertEqual(Sensor.get_sensor_count(), before + 2)

    def test_private_list_copies(self):
        for factory in (lambda xs: Sensor("A", xs),
                        lambda xs: CalibratedSensor("B", xs, 2, 1)):
            source = [4, 6]
            sensor = factory(source)
            source[0] = 999
            returned = sensor.get_values()
            returned[1] = 999
            self.assertEqual(sensor.get_values(), [4, 6])
            self.assertIsNot(sensor.get_values(), sensor.get_values())

    def test_ids_across_subclasses(self):
        class ExtraSensor(Sensor):
            pass
        start = Sensor.get_sensor_count()
        objects = [Sensor("A", [0]), CalibratedSensor("B", [0], 1, 0),
                   ExtraSensor("C", [0]), Sensor("D", [0])]
        self.assertEqual([s.get_id() for s in objects], list(range(start, start + 4)))
        self.assertEqual(CalibratedSensor.get_sensor_count(), start + 4)
        self.assertIsInstance(Sensor.__dict__["get_sensor_count"], classmethod)

    def test_invalid_readings_and_names(self):
        for name, readings, error in [("", [1], ValueError), ("A", [], ValueError),
                                      ("A", [-1], ValueError), ("A", [1, "2"], TypeError),
                                      ("A", [True], TypeError)]:
            with self.subTest(name=name, readings=readings):
                count = Sensor.get_sensor_count()
                with self.assertRaises(error):
                    Sensor(name, readings)
                self.assertEqual(Sensor.get_sensor_count(), count)

    def test_invalid_calibration_does_not_count(self):
        for scale, offset, error in [(0, 0, ValueError), (-1, 0, ValueError),
                                    ("1", 0, TypeError), (1, "0", TypeError),
                                    (True, 0, TypeError)]:
            with self.subTest(scale=scale, offset=offset):
                count = Sensor.get_sensor_count()
                with self.assertRaises(error):
                    CalibratedSensor("B", [1], scale, offset)
                self.assertEqual(Sensor.get_sensor_count(), count)

    def test_rejected_add_keeps_state(self):
        sensor = Sensor("A", [0, 2])
        for value, error in [(-1, ValueError), ("3", TypeError)]:
            with self.assertRaises(error):
                sensor.add_value(value)
            self.assertEqual(sensor.get_values(), [0, 2])

    def test_child_methods_and_dynamic_string(self):
        sensor = CalibratedSensor("Ben", [4, 6], 1.5, 2)
        sensor.add_value(8)
        self.assertEqual(sensor.get_values(), [4, 6, 8])
        self.assertEqual(sensor.get_average(), 11.0)
        self.assertIn("average = 11.00", str(sensor))
        self.assertIn("Ben", str(sensor))
        self.assertIn(str(sensor.get_id()), str(sensor))
        self.assertIn("count = 3", str(sensor))

    def test_independent_objects_and_negative_offset(self):
        a = Sensor("A", [10, 20])
        b = CalibratedSensor("B", [0], 1, -2)
        self.assertEqual(b.get_average(), -2)
        b.add_value(4)
        self.assertEqual(a.get_values(), [10, 20])
        self.assertEqual(a.get_average(), 15)
        self.assertEqual(b.get_name(), "B")



from problem_1 import load_readings, calculate_average, write_summary


class FileProcessingTests(unittest.TestCase):
    def test_sample_data_and_exact_report(self):
        folder = Path(__file__).parent
        data, errors = load_readings(str(folder / "sensor_data.txt"))
        self.assertEqual(data, {"Ava": [10, 20, 30, 20, 40],
                                "Ben": [5, 15, 25], "Cara": [8, 12, 16]})
        self.assertEqual(errors, 1)
        expected = ("1. Ava: count = 5, average = 24.00, status = HIGH\n"
                    "2. Ben: count = 3, average = 15.00, status = LOW\n"
                    "3. Cara: count = 3, average = 12.00, status = LOW\n"
                    "Invalid lines: 1\n"
                    "Sensors with average >= 15.0: ['Ava', 'Ben']\n")
        with tempfile.TemporaryDirectory(dir=folder) as temp:
            output = Path(temp) / "summary.txt"
            write_summary(data, errors, str(output))
            self.assertEqual(output.read_text(encoding="utf-8"), expected)

    def test_extra_spaces_blank_and_reordered_records(self):
        folder = Path(__file__).parent
        first, e1 = load_readings(str(folder / "sensor_data.txt"))
        second, e2 = load_readings(str(folder / "sensor_data_extra.txt"))
        self.assertEqual(e1, e2)
        self.assertEqual({k: sorted(v) for k, v in first.items()},
                         {k: sorted(v) for k, v in second.items()})
        with tempfile.TemporaryDirectory(dir=folder) as temp:
            a, b = Path(temp) / "a.txt", Path(temp) / "b.txt"
            write_summary(first, e1, str(a))
            write_summary(second, e2, str(b))
            self.assertEqual(a.read_text(encoding="utf-8"), b.read_text(encoding="utf-8"))

    def test_invalid_line_is_atomic(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as temp:
            path = Path(temp) / "input.txt"
            path.write_text("A,1\nA,2,bad,3\nA,4\n", encoding="utf-8")
            data, errors = load_readings(str(path))
            self.assertEqual(data, {"A": [1.0, 4.0]})
            self.assertEqual(errors, 1)

    def test_missing_readings_and_blank_name(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as temp:
            path = Path(temp) / "input.txt"
            path.write_text("\n \t\nSolo\nNo,\nZ,1,wrong,2\n,1\n", encoding="utf-8")
            self.assertEqual(load_readings(str(path)), ({}, 4))

    def test_numeric_zero_negative_and_average(self):
        # 1번에는 측정값 비음수 조건이 없다. 그 조건은 2번에만 있다.
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as temp:
            path = Path(temp) / "input.txt"
            path.write_text("A,0,-2,2\n", encoding="utf-8")
            data, errors = load_readings(str(path))
            self.assertEqual(errors, 0)
            self.assertEqual(calculate_average(data["A"]), 0)

    def test_thresholds_and_tie_break(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as temp:
            output = Path(temp) / "summary.txt"
            write_summary({"Z": [20], "A": [20], "B": [15], "C": [14.99]},
                          0, str(output))
            report = output.read_text(encoding="utf-8")
            self.assertTrue(report.startswith("1. A: count = 1, average = 20.00, status = HIGH"))
            self.assertIn("3. B: count = 1, average = 15.00, status = LOW", report)
            self.assertIn("['A', 'Z', 'B']", report)

    def test_empty_report(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as temp:
            output = Path(temp) / "summary.txt"
            write_summary({}, 0, str(output))
            self.assertEqual(output.read_text(encoding="utf-8"),
                             "Invalid lines: 0\nSensors with average >= 15.0: []\n")

    def test_missing_file_is_not_a_bad_line(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as temp:
            with self.assertRaises(FileNotFoundError):
                load_readings(str(Path(temp) / "missing.txt"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
