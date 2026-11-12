"""
파이썬 퀴즈 게임 (보너스 기능 추가 버전)
- Quiz 클래스: 퀴즈 1개를 표현
- QuizGame 클래스: 게임 전체를 관리
- state.json에 퀴즈/최고점수 저장 (UTF-8)
"""

import json
import os


# ============================================================
# 공통 입력 함수
# ============================================================
def input_number(prompt, min_value, max_value):
    """숫자를 입력받아 검증하는 함수 (빈값/문자/범위 검증)"""
    while True:

        # 사용자에게 안내 문구를 보여주고 값을 입력받은 뒤,
        # 앞뒤에 불필요하게 붙은 공백 제거.
        value = input(prompt).strip()
        if value == "":
            print("⚠️  입력이 비어 있습니다. 다시 입력하세요.")
            continue
        
        # 왼쪽(앞부분)에 있는 -(마이너스) 기호를 제거하고 나서 숫자인지 확인
        if not value.lstrip("-").isdigit():
            print("⚠️  숫자만 입력할 수 있습니다. 다시 입력하세요.")
            continue
        number = int(value)
        if number < min_value or number > max_value:
            print(f"⚠️  {min_value}~{max_value} 사이 숫자를 입력하세요.")
            continue
        return number


def input_text(prompt):
    """글자(문자열)를 입력받는 함수 (빈값 검증)"""
    while True:
        text = input(prompt).strip()
        if text == "":
            print("⚠️  빈 값은 입력할 수 없습니다. 다시 입력하세요.")
            continue
        return text


# ============================================================
# Quiz 클래스: 퀴즈 1개를 표현.
# ============================================================
class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = answer

    def show(self):
        """문제와 선택지를 화면에 출력"""
        print(f"\nQ. {self.question}")
        for i, choice in enumerate(self.choices, start=1):
            print(f"   {i}. {choice}")

    def is_correct(self, user_answer):
        """입력한 번호가 정답인지 확인"""
        return user_answer == self.answer

    def to_dict(self):
        """JSON 저장을 위해 딕셔너리로 변환"""
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
        }


# ============================================================
# QuizGame 클래스: 게임 전체를 관리.
# ============================================================
class QuizGame:
    FILENAME = "state.json"

    def __init__(self):
        self.quizzes = []
        self.high_score = 0
        self.score = 0  

    # ---------------- 기본 퀴즈 데이터 ----------------
    def load_default(self):
        """파일이 없거나 손상됐을 때 사용할 기본 퀴즈 5개"""
        default_data = [
            ("대한민국의 수도는?",
             ["부산", "서울", "대구", "인천"], 2),
            ("태양계에서 가장 큰 행성은?",
             ["지구", "화성", "목성", "토성"], 3),
            ("물의 화학 기호는?",
             ["H2O", "CO2", "O2", "NaCl"], 1),
            ("1년은 며칠일까요? (평년 기준)",
             ["364일", "365일", "366일", "367일"], 2),
            ("무지개의 색은 보통 몇 가지로 표현할까요?",
             ["5가지", "6가지", "7가지", "8가지"], 3),
        ]
        self.quizzes = [Quiz(q, c, a) for q, c, a in default_data]
        self.high_score = 0     

    # ---------- JSON 파일(state.json) 불러오기 ----------
    def load(self):
        """state.json에서 파일 데이터를 불러온다."""
        try:
            with open(self.FILENAME, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.quizzes = [
                Quiz(q["question"], q["choices"], q["answer"])
                for q in data["quizzes"]
            ]
            self.high_score = data["high_score"]
        except FileNotFoundError:
            print("💡 저장 파일이 없어 기본 퀴즈로 시작합니다.")
            self.load_default()
        except (json.JSONDecodeError, KeyError, TypeError):
            print("⚠️  파일이 손상되어 기본 퀴즈로 복구합니다.")
            self.load_default()

    # ---------- JSON 파일(state.json) 저장하기 ----------
    def save(self):
        """현재 데이터를 state.json 파일에 저장한다."""
        data = {
            "quizzes": [q.to_dict() for q in self.quizzes],
            "high_score": self.high_score,
        }
        try:
            with open(self.FILENAME, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except OSError:
            print("⚠️  저장 중 오류가 발생했습니다.")

    # ---------------- 메뉴 출력 ----------------
    def show_menu(self):
        print("\n" + "=" * 30)
        print("      🎯 파이썬 퀴즈 게임")
        print("=" * 30)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 퀴즈 삭제")       # 🆕 삭제 메뉴 추가(보너스)
        print("6. 종료")            # 🆕 종료 번호 6으로 이동
        print("=" * 30)

    # ---------------- 1. 퀴즈 풀기 (보너스 과제: 문제 수 선택) ----------------
    def play(self):
        """저장된 퀴즈 중 원하는 개수만큼 출제한다."""
        if not self.quizzes:
            print("\n📭 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가하세요.")
            return

        total = len(self.quizzes)  # 전체 퀴즈 개수

        # 🆕 몇 문제를 풀지 선택 (1 ~ 전체 개수)(보너스 문제)
        print(f"\n현재 등록된 퀴즈는 총 {total}개입니다.")
        count = input_number(
            f"몇 문제를 풀까요? (1~{total}): ", 1, total
        )

        # 🆕 선택한 개수만큼 앞에서부터 출제
        # (랜덤 출제는 또 다른 보너스 과제이므로 여기서는 순서대로 출제)
        selected = self.quizzes[:count]

        score = 0
        print(f"\n총 {count}개의 문제를 풉니다!")

        for index, quiz in enumerate(selected, start=1):
            print(f"\n----- {index}번 문제 -----")
            quiz.show()
            user_answer = input_number("정답 번호(1~4): ", 1, 4)

            if quiz.is_correct(user_answer):
                print("✅ 정답입니다!")
                score += 1
            else:
                print(f"❌ 오답입니다. 정답은 {quiz.answer}번입니다.")

        # 결과 표시
        print("\n" + "=" * 30)
        print(f"🎉 결과: {count}문제 중 {score}문제 정답!")

        # 최고 점수 갱신
        self.score_recorded = True
        if score > self.high_score:
            self.high_score = score
            print(f"🏆 최고 점수를 갱신했습니다! ({score}점)")
        else:
            print(f"현재 최고 점수: {self.high_score}점")
        print("=" * 30)

        self.save()

    # ---------------- 2. 퀴즈 추가 ----------------
    def add_quiz(self):
        """새 퀴즈를 입력받아 추가한다."""
        print("\n----- 퀴즈 추가 -----")
        question = input_text("문제를 입력하세요: ")

        choices = []
        for i in range(1, 5):
            choice = input_text(f"선택지 {i}번: ")
            choices.append(choice)

        answer = input_number("정답 번호(1~4): ", 1, 4)

        new_quiz = Quiz(question, choices, answer)
        self.quizzes.append(new_quiz)
        self.save()
        print("✅ 퀴즈가 추가되었습니다!")

    # ---------------- 3. 퀴즈 목록 ----------------
    def show_list(self):
        """저장된 퀴즈 목록을 출력한다."""
        if not self.quizzes:
            print("\n📭 등록된 퀴즈가 없습니다.")
            return

        print(f"\n----- 퀴즈 목록 (총 {len(self.quizzes)}개) -----")
        for index, quiz in enumerate(self.quizzes, start=1):
            print(f"{index}. {quiz.question}")

    # ---------------- 4. 최고 점수 확인 ----------------
    def show_score(self):
        """최고 점수를 출력한다."""
        if not self.score_recorded:
            print("\n📊 아직 퀴즈를 풀지 않았습니다.")
            return
        print(f"\n🏆 최고 점수: {self.best_score}점")

    # ---------------- 5. 퀴즈 삭제 (보너스 과제: 퀴즈삭제 기능) ----------------
    def delete_quiz(self):
        """목록에서 번호를 선택해 퀴즈를 삭제한다."""
        if not self.quizzes:
            print("\n📭 삭제할 퀴즈가 없습니다.")
            return

        # 현재 목록을 먼저 보여주기
        print(f"\n----- 퀴즈 삭제 (총 {len(self.quizzes)}개) -----")
        for index, quiz in enumerate(self.quizzes, start=1):
            print(f"{index}. {quiz.question}")
        print("0. 취소")  # 🆕 실수로 들어왔을 때 빠져나갈 수 있는 취소 옵션

        # 삭제할 번호 입력 (0 = 취소)
        choice = input_number(
            f"삭제할 퀴즈 번호(0~{len(self.quizzes)}): ",
            0, len(self.quizzes)
        )

        if choice == 0:
            print("↩️  삭제를 취소했습니다.")
            return

        # 🆕 리스트는 0부터 시작하므로 입력 번호에서 1을 뺀다
        removed = self.quizzes.pop(choice - 1)
        self.save()  # 🆕 삭제 결과를 파일에 바로 반영
        print(f"🗑️  '{removed.question}' 퀴즈를 삭제했습니다.")

    # ---------------- 메뉴 루프 ----------------
    def run(self):
        self.load()
        try:
            while True:
                self.show_menu()
                choice = input_number("메뉴 선택(1~6): ", 1, 6)  # 🆕 범위 1~6

                if choice == 1:
                    # 퀴즈 풀기 기능
                    self.play()
                elif choice == 2:
                    # 퀴즈 추가 기능
                    self.add_quiz()
                    pass
                elif choice == 3:
                    # 퀴즈 목록 기능
                    self.show_list()
                elif choice == 4:
                    # 최고점수 확인 기능
                    self.show_score()
                elif choice == 5:          # 🆕 퀴즈 삭제(보너스 문제)
                    self.delete_quiz()
                elif choice == 6:
                    # 프로그램 종료
                    self.save()
                    print("\n👋 프로그램을 종료합니다. 안녕히 가세요!")
                    break
        except (KeyboardInterrupt, EOFError):
            # Ctrl+C 또는 입력 종료 시에도 안전하게 저장 후 종료
            print("\n\n💾 저장 후 안전하게 종료합니다.")
            self.save()


# ============================================================
# 프로그램 메인 실행.
# ============================================================
if __name__ == "__main__":
    game = QuizGame()
    game.run()