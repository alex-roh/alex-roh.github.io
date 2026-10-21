"""문제 4.4: 모듈 이름을 통해 함수를 호출하고 독립적으로 검증한다."""
import contextlib
import io
import unittest
import my_strings  # [P4.4-A] 구현을 복사하거나 from ... import로 가져오지 않는다.


def demonstrate():
    print(my_strings.str_join(["red", "blue", "green"]))
    print(my_strings.str_join(["red", "blue", "green"], " / "))
    print(repr(my_strings.str_join([], ":")))  # ''를 보여 빈 문자열임을 확인
    print(my_strings.str_insert("abcdef", "!", 0))
    print(my_strings.str_insert("abcdef", "XYZ", 3))
    print(my_strings.str_insert("abcdef", "!", 6))
    print(my_strings.str_insert("abcdef", "?", -1))
    print(my_strings.is_palindrome("level"))
    print(my_strings.is_palindrome("Python"))
    print(my_strings.is_palindrome(123))
    print(my_strings.center_with_dots("Data", 9))
    original = "abc"
    returned = my_strings.str_insert(original, "X", 1)
    returned = returned + "!"
    # [P4.4-B] 문자열은 불변이다. 반환값을 재대입해도 original 객체는 안 바뀐다.
    print("원본:", original, "/ 새 결과:", returned)


class StringTests(unittest.TestCase):
    def test_join_default_separator_and_order(self):
        self.assertEqual(my_strings.str_join(["red", "blue", "green"]), "redbluegreen")

    def test_join_separator_empty_and_single(self):
        self.assertEqual(my_strings.str_join(["a", "b"], sep=" / "), "a / b")
        self.assertEqual(my_strings.str_join([], ":"), "")
        self.assertEqual(my_strings.str_join(["only"], ":"), "only")
        self.assertEqual(my_strings.str_join(["", ""], ":"), ":")

    def test_join_does_not_modify_list(self):
        values = ["a", "b"]
        my_strings.str_join(values, "-")
        self.assertEqual(values, ["a", "b"])

    def test_insert_endpoints_middle_and_empty(self):
        self.assertEqual(my_strings.str_insert("abc", "X", 0), "Xabc")
        self.assertEqual(my_strings.str_insert("abc", "X", 1), "aXbc")
        self.assertEqual(my_strings.str_insert("abc", "X", 3), "abcX")
        self.assertEqual(my_strings.str_insert("", "X", 0), "X")

    def test_invalid_insert_message_and_none(self):
        for position in [-1, 4, 1.5]:
            with self.subTest(position=position):
                output = io.StringIO()
                with contextlib.redirect_stdout(output):
                    result = my_strings.str_insert("abc", "X", position)
                self.assertIsNone(result)
                self.assertEqual(output.getvalue(), "str_insert(): position input parameter out of range.\n")

    def test_insert_uses_own_join(self):
        from unittest.mock import patch
        with patch.object(my_strings, "str_join", wraps=my_strings.str_join) as joined:
            self.assertEqual(my_strings.str_insert("abc", "X", 1), "aXbc")
            joined.assert_called_once_with(["a", "X", "bc"])

    def test_palindrome_exact_case_and_punctuation(self):
        for text, expected in [("level", True), ("Python", False), ("Level", False),
                               ("", True), ("a", True), ("A,a", False)]:
            with self.subTest(text=text):
                self.assertEqual(my_strings.is_palindrome(text), expected)

    def test_palindrome_invalid_type(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertIsNone(my_strings.is_palindrome(123))
        self.assertEqual(output.getvalue(), "is_palindrome(): the input parameter must be a string.\n")

    def test_center_even_odd_zero_padding(self):
        for text, width, expected in [("Data", 9, "..Data..."), ("Data", 8, "..Data.."),
                                       ("Data", 4, "Data"), ("", 3, "...")]:
            with self.subTest(text=text, width=width):
                result = my_strings.center_with_dots(text, width)
                self.assertEqual(result, expected)
                self.assertEqual(len(result), width)


if __name__ == "__main__":
    demonstrate()
    unittest.main(verbosity=2)
