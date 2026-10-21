"""문제 5: 판정 함수와 입력·통계를 분리한 가위바위보 대회."""
import random
import sys


def judge_round(player, computer):
    # [P5.1-A] main에서 검증한 0, 1, 2를 받는다. 여기서는 출력·난수 생성 금지.
    if player == computer:
        return "TIE"
    elif ((player == 0 and computer == 2)
          or (player == 1 and computer == 0)
          or (player == 2 and computer == 1)):
        return "WIN"
    else:
        return "LOSS"


def main():
    # [P5.2-A] 숫자 인덱스를 표시 이름으로 바꾸는 공통 목록.
    gesture_names = ["Rock", "Paper", "Scissors"]
    # [P5.3-A] 루프 밖에 두어 매 라운드마다 0으로 초기화되지 않게 한다.
    wins = 0
    losses = 0
    ties = 0

    while True:  # [P5.2-B] 종료 요청이 나올 때까지 반복
        try:
            player = int(input("Enter a gesture (0=Rock, 1=Paper, 2=Scissors, -1=Quit): "))
        except ValueError:
            print("Invalid integer input.")
            continue  # 숫자 변환 실패: 아래 난수·판정·카운터 코드는 실행하지 않음

        # [P5.3-B] -1을 먼저 처리해야 잘못된 동작으로 분류하지 않는다.
        if player == -1:
            break
        if player not in (0, 1, 2):
            print("Invalid gesture.")
            continue

        # [P5.2-C] 유효한 입력에만 컴퓨터 선택과 판정을 수행한다.
        computer = random.randrange(3)  # 0, 1, 2 중 하나. 3은 포함하지 않음.
        result = judge_round(player, computer)
        print(f"You: {gesture_names[player]}; Computer: {gesture_names[computer]}; Result: {result}")

        # [P5.3-C] 서로 배타적인 if/elif/else로 카운터 하나만 올린다.
        if result == "WIN":
            wins += 1
        elif result == "LOSS":
            losses += 1
        else:
            ties += 1

    # [P5.3-D] break는 위 while만 끝내므로 최종 통계를 출력할 수 있다.
    total = wins + losses + ties
    print(f"Wins: {wins}, Losses: {losses}, Ties: {ties}, Total: {total}")
    sys.exit()  # 통계 출력 후 프로그램 종료. import할 때는 호출되지 않는다.


if __name__ == "__main__":
    main()
