"""Set C의 결과뿐 아니라 공유 관계, 횟수, 실패 시 상태 보존까지 검사한다."""
import contextlib
import io
import math
import unittest
from unittest.mock import patch

import complex_samples as cs
import student_records as sr
from date_validation import Date


class StudentTests(unittest.TestCase):
    def test_record_order_and_nested_updates(self):
        s = sr.create_students()
        self.assertEqual([r["name"] for r in s], ["Jodie", "Paul", "Joel", "Krissie", "Peter"])
        self.assertEqual(s[1]["grades"], ["B", "C", "B"])
        self.assertEqual(s[3]["grades"], ["A-", "A", "B", "A+", "A", "A"])
        self.assertEqual(s[2]["grades"], ["A", "C", "B", "B"])
        self.assertEqual([len(r["grades"]) for r in s], [3, 3, 4, 6, 2])

    def test_shallow_and_independent_copies(self):
        s = sr.create_students()
        with contextlib.redirect_stdout(io.StringIO()):
            backup, independent = sr.demonstrate_copies(s)
        self.assertIsNot(s, backup)
        self.assertEqual(s[0]["name"], "Jodie")
        self.assertEqual(s[0]["grades"][0], "B+")
        self.assertEqual(independent[0]["grades"][0], "A+")
        self.assertIs(backup[1], s[1])  # 교체하지 않은 딕셔너리는 계속 공유한다.
        for original, copied in zip(s, independent):
            self.assertIsNot(original, copied)
            self.assertIsNot(original["grades"], copied["grades"])

    def test_tuple_keys_and_updates(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            a = sr.create_accounts()
        self.assertEqual(len(a), 4)
        self.assertEqual(a[("jill", 545)], 444567)
        self.assertNotIn(("joe", 172), a)
        self.assertNotIn(("gwen", 172), a)
        self.assertEqual(a[("ted", 346)], 576644)
        self.assertEqual(a[("sasha", 988)], 111111)
        self.assertTrue(all(type(k) is tuple and type(v) is int for k, v in a.items()))
        self.assertIn("present: False", out.getvalue())

    def test_default_tuple_order(self):
        self.assertEqual(sr.sort_products(), [("cool stuff", 6.87), ("gadget", 10.44),
                                              ("widget", 5.28), ("widget", 5.55)])


class ComplexTests(unittest.TestCase):
    def setUp(self):
        cs.conversion_count = 0  # 테스트끼리 누적 횟수가 섞이지 않게 초기화한다.

    def test_polar_quadrants_and_axes(self):
        cases = [(1+1j, math.pi/4), (-1+1j, 3*math.pi/4),
                 (-1-1j, -3*math.pi/4), (1-1j, -math.pi/4),
                 (0+2j, math.pi/2), (-2+0j, math.pi), (0j, 0.0)]
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            for x, angle in cases:
                result = cs.rec_to_pol(x)
                self.assertIs(type(result), tuple)
                self.assertAlmostEqual(result[0], abs(x))
                self.assertAlmostEqual(result[1], angle)
        self.assertEqual(out.getvalue(), "")
        self.assertEqual(cs.conversion_count, len(cases))

    def test_failed_conversion_is_not_counted(self):
        with self.assertRaises(TypeError):
            cs.rec_to_pol("not a complex sample")
        self.assertEqual(cs.conversion_count, 0)

    def test_zip_exact_requested_prefix(self):
        names, values = ["S1", "S2", "S3", "EXTRA"], [1+1j, 3+4j, -1+1j]
        result = cs.create_tuple(names, values, 2)
        self.assertEqual(result, (("S1", 1+1j), ("S2", 3+4j)))
        self.assertIs(type(result), tuple)
        self.assertTrue(all(type(item) is tuple for item in result))
        self.assertEqual(len(names), 4)
        self.assertEqual(len(values), 3)

    def test_zip_shortage_on_either_input(self):
        self.assertIsNone(cs.create_tuple(["S1"], [1j, 2j], 2))
        self.assertIsNone(cs.create_tuple(["S1", "S2"], [1j], 2))
        self.assertIsNone(cs.create_tuple([], [], 1))

    def test_zip_zero_is_empty_tuple(self):
        self.assertEqual(cs.create_tuple([], [], 0), ())
        self.assertEqual(cs.create_tuple(["S1"], [1j], 0), ())

    def test_gain_argument_forms_and_original(self):
        x = 3+4j
        self.assertEqual(cs.apply_gain(x), 3+4j)
        self.assertEqual(cs.apply_gain(x, 2), 6+8j)
        self.assertEqual(cs.apply_gain(x, gain=0.5), 1.5+2j)
        self.assertEqual(x, 3+4j)
        self.assertIs(type(cs.apply_gain(x)), complex)

    def test_function_argument_and_counter_delta(self):
        samples = [1+1j, 3+4j, -1+1j]
        original = samples.copy()
        cs.rec_to_pol(3+4j)  # 직접 호출도 전체 카운터에는 포함된다.
        self.assertEqual(cs.apply_function(samples, abs), [math.sqrt(2), 5, math.sqrt(2)])
        self.assertEqual(cs.conversion_count, 1)
        before = cs.conversion_count
        result = cs.apply_function(samples, cs.rec_to_pol)
        self.assertEqual(cs.conversion_count - before, 3)
        self.assertEqual(cs.conversion_count, 4)
        self.assertEqual(len(result), 3)
        self.assertEqual(samples, original)

    def test_generic_operation_and_empty_input(self):
        calls = []
        def operation(x):
            calls.append(x)
            return x * 2
        self.assertEqual(cs.apply_function([1j, 2j], operation), [2j, 4j])
        self.assertEqual(calls, [1j, 2j])
        self.assertEqual(cs.apply_function([], operation), [])


class DateTests(unittest.TestCase):
    @staticmethod
    def fields(date):
        return date.get_year(), date.get_month(), date.get_day()

    def test_leap_centuries_and_ordinary_years(self):
        for year in [1600, 2000, 2024]:
            self.assertEqual(self.fields(Date(year, 2, 29)), (year, 2, 29))
        for year in [1700, 1900, 2023]:
            with self.subTest(year=year), self.assertRaisesRegex(ValueError, "^Invalid date$"):
                Date(year, 2, 29)

    def test_month_end_boundaries(self):
        for month, days in enumerate(Date.DAYS_PER_MONTH, start=1):
            self.assertEqual(Date(2023, month, days).get_day(), days)
            for invalid in [0, days+1]:
                with self.subTest(month=month, day=invalid), self.assertRaises(ValueError):
                    Date(2023, month, invalid)

    def test_bad_types_and_ranges(self):
        for args in [(0,1,1), (-1,1,1), (2024,0,1), (2024,13,1),
                     (2024.0,2,1), (2024,2.0,1), (2024,2,1.0),
                     (True,1,1), (2024,True,1), (2024,1,True), ("2024",2,1)]:
            with self.subTest(args=args), self.assertRaisesRegex(ValueError, "^Invalid date$"):
                Date(*args)

    def test_format_and_lookup_table_unchanged(self):
        before = Date.DAYS_PER_MONTH
        self.assertEqual(str(Date(2000,2,29)), "February 29, 2000")
        self.assertEqual(str(Date(2023,12,31)), "December 31, 2023")
        self.assertEqual(Date.DAYS_PER_MONTH, before)
        self.assertEqual(Date.DAYS_PER_MONTH[1], 28)

    def test_invalid_updates_preserve_all_fields(self):
        date = Date(2024,2,29)
        for proposed in [(2023,2,29), (1900,2,29), (2023,4,31), (2023,13,1), (0,3,1), (2023,3,1.5)]:
            out = io.StringIO()
            with self.subTest(proposed=proposed), contextlib.redirect_stdout(out):
                self.assertIs(date.set_date(*proposed), False)
            self.assertEqual(out.getvalue(), "Invalid date\n")
            self.assertEqual(self.fields(date), (2024,2,29))

    def test_valid_update_changes_all_fields(self):
        date = Date(2024,2,29)
        self.assertIs(date.set_date(2023,3,1), True)
        self.assertEqual(self.fields(date), (2023,3,1))
        self.assertEqual(str(date), "March 1, 2023")

    def test_constructor_and_setter_share_helper(self):
        with patch.object(Date, "_Date__valid_date", return_value=False) as helper:
            with self.assertRaises(ValueError):
                Date(2024,1,1)
            helper.assert_called_once_with(2024,1,1)
        date = Date(2024,1,1)
        with patch.object(Date, "_Date__valid_date", return_value=False) as helper:
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertFalse(date.set_date(2023,3,1))
            helper.assert_called_once_with(2023,3,1)
        self.assertEqual(self.fields(date), (2024,1,1))


if __name__ == "__main__":
    unittest.main(verbosity=2)
