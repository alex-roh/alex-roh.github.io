"""입력과 난수만 고정해 실제 main의 반복·통계·종료를 확인한다."""
import contextlib
import io
import unittest
from unittest.mock import patch
import tournament


def run_interaction(entries, computer_choices):
    remaining = iter(entries)
    output = io.StringIO()

    def fake_input(prompt):
        entry = next(remaining)
        print(prompt + entry)  # 실제 입력 화면처럼 사용자 입력도 기록한다.
        return entry

    with contextlib.redirect_stdout(output), patch("builtins.input", side_effect=fake_input), \
            patch("tournament.random.randrange", side_effect=computer_choices) as random_choice:
        try:
            tournament.main()
        except SystemExit as error:
            # 종료를 확인한 뒤 테스트 프로세스 자체는 계속 실행한다.
            assert error.code is None or error.code == 0
        else:
            raise AssertionError("main이 sys.exit()로 종료하지 않았음")
    return output.getvalue(), random_choice.call_count


class TournamentTests(unittest.TestCase):
    def test_all_nine_outcomes_and_no_output(self):
        expected = [["TIE", "LOSS", "WIN"], ["WIN", "TIE", "LOSS"], ["LOSS", "WIN", "TIE"]]
        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch("tournament.random.randrange") as random_choice:
            for player in range(3):
                for computer in range(3):
                    self.assertEqual(tournament.judge_round(player, computer), expected[player][computer])
        self.assertEqual(output.getvalue(), "")
        random_choice.assert_not_called()

    def test_required_sample_and_invalid_inputs_do_not_play(self):
        text, calls = run_interaction(["hello", "7", "0", "-1"], [2])
        self.assertIn("Invalid integer input.\n", text)
        self.assertIn("Invalid gesture.\n", text)
        self.assertIn("You: Rock; Computer: Scissors; Result: WIN", text)
        self.assertTrue(text.endswith("Wins: 1, Losses: 0, Ties: 0, Total: 1\n"))
        self.assertEqual(calls, 1)

    def test_multiple_rounds_increment_exactly_one_counter(self):
        text, calls = run_interaction(["0", "1", "2", "-1"], [2, 2, 2])
        self.assertTrue(text.endswith("Wins: 1, Losses: 1, Ties: 1, Total: 3\n"))
        self.assertEqual(calls, 3)

    def test_immediate_quit_has_zero_rounds(self):
        text, calls = run_interaction(["-1"], [])
        self.assertIn("Wins: 0, Losses: 0, Ties: 0, Total: 0", text)
        self.assertEqual(calls, 0)

    def test_invalid_integer_and_negative_gesture(self):
        text, calls = run_interaction(["3.5", "-2", "-1"], [])
        self.assertEqual(text.count("Invalid integer input."), 1)
        self.assertEqual(text.count("Invalid gesture."), 1)
        self.assertEqual(calls, 0)


if __name__ == "__main__":
    # 원문의 네 직접 호출을 먼저 확인하고, 실제 main의 상호작용도 재현한다.
    print(tournament.judge_round(0, 2))
    print(tournament.judge_round(1, 2))
    print(tournament.judge_round(2, 2))
    print(tournament.judge_round(2, 1))
    print(run_interaction(["hello", "7", "0", "-1"], [2])[0], end="")
    unittest.main(verbosity=2)
