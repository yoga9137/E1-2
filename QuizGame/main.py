"""
파이썬 퀴즈 게임 (보너스 기능 추가 버전)
- Quiz 클래스: 퀴즈 1개를 표현
- QuizGame 클래스: 게임 전체를 관리
- state.json에 퀴즈/최고점수 저장 (UTF-8)
"""

import json
import os


# ============================================================
# Quiz 클래스: 퀴즈 1개를 표현.
# ============================================================
class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question
        self.answer = answer


# ============================================================
# QuizGame 클래스: 게임 전체를 관리.
# ============================================================
class QuizGame:
    FILENAME = "state.json"

    def __init__(self):
        self.quizzes = []
        self.high_score = 0
        self.score = 0        

    # ---------------- 메뉴 루프 ----------------
    def run(self):
        pass


# ============================================================
# 프로그램 메인 실행.
# ============================================================
if __name__ == "__main__":
    game = QuizGame()
    game.run()