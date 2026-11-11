import json
import os
import random                                  # 보너스 1: 랜덤 출제
from datetime import datetime                  # 보너스 5: 기록 시각

# state.json은 프로젝트 루트(이 파일과 같은 폴더)에 저장
STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "state.json")

POINT_PER_QUIZ = 10     # 문제당 기본 점수
HINT_PENALTY = 5        # 보너스 3: 힌트를 쓴 문제의 감점


# =====================================================
# 1단계: Quiz 클래스 - 퀴즈 한 문제를 표현
# =====================================================
class Quiz:
    def __init__(self, question, choices, answer, hint=""):
        self.question = question    # 문제 (str)
        self.choices = choices      # 선택지 4개 (list)
        self.answer = answer        # 정답 번호 1~4 (int)
        self.hint = hint            # 보너스 3: 힌트 (str, 없으면 "")

    def display(self):
        # 문제와 선택지를 1~4 번호와 함께 출력
        print(self.question)
        for number, choice in enumerate(self.choices, start=1):
            print(f"{number}. {choice}")

    def is_correct(self, user_answer):
        # 입력한 번호가 정답이면 True, 아니면 False
        return user_answer == self.answer

    def to_dict(self):
        # JSON으로 저장하기 위해 딕셔너리로 변환
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
            "hint": self.hint,
        }

    @staticmethod
    def from_dict(data):
        # 딕셔너리에서 Quiz 객체로 복원 (형식이 틀리면 예외 발생)
        question = data["question"]
        choices = data["choices"]
        answer = data["answer"]
        hint = data.get("hint", "")           # 옛 state.json(힌트 없음)도 읽을 수 있게 기본값 사용
        if not isinstance(question, str) or not question.strip():
            raise ValueError("question 형식 오류")
        if not isinstance(choices, list) or len(choices) != 4:
            raise ValueError("choices 형식 오류")
        if not isinstance(answer, int) or isinstance(answer, bool) or not 1 <= answer <= 4:
            raise ValueError("answer 형식 오류")
        if not isinstance(hint, str):
            raise ValueError("hint 형식 오류")
        return Quiz(question, choices, answer, hint)


# =====================================================
# 2단계: 기본 퀴즈 데이터 (Git 기초 명령어 주제)
# =====================================================
def get_default_quizzes():
    return [
        Quiz("새 Git 저장소를 만드는 명령어는?", ["add", "commit", "init", "push"], 3,
             "'시작하다'라는 뜻의 영어 단어와 관련 있어요."),
        Quiz("변경한 파일을 커밋 대상에 올리는 명령어는?", ["commit", "clone", "pull", "add"], 4,
             "'추가하다'라는 뜻이에요."),
        Quiz("원격 변경사항을 가져와 합치는 명령어는?", ["commit", "clone", "pull", "add"], 3,
             "push의 반대 방향이에요."),
        Quiz("브랜치를 바꾸는 명령어는?", ["checkout", "clone", "pull", "add"], 1,
             "'계산대에서 확인하다'라는 뜻으로도 쓰는 단어예요."),
        Quiz("원격 저장소를 통째로 복제하는 명령어는?", ["checkout", "clone", "pull", "add"], 2,
             "'복제'를 뜻하는 영어 단어예요."),
    ]


# =====================================================
# 3단계: 입력 도우미 함수 (self가 필요 없어 클래스 밖에 둠)
# =====================================================
def get_text_input(prompt):
    # 문자열 입력: 공백 제거 후, 비어 있으면 다시 입력
    while True:
        text = input(prompt).strip()
        if text == "":
            print("입력이 비어 있습니다. 다시 입력하세요.")
            continue
        return text


def get_number_input(prompt, min_value, max_value):
    # 숫자 입력: min_value~max_value 범위의 숫자를 받을 때까지 반복
    while True:
        text = input(prompt).strip()          # 1) 공백 제거

        if text == "":                        # 2) 빈 입력
            print("입력이 비어 있습니다.")
            continue

        try:                                  # 3) 숫자 변환
            number = int(text)
        except ValueError:
            print("숫자만 입력할 수 있습니다.")
            continue

        if number < min_value or number > max_value:   # 4) 범위 확인
            print(f"{min_value}~{max_value} 사이의 번호를 입력하세요.")
            continue

        return number                         # 5) 통과하면 반환


def is_valid_history_item(item):
    # 보너스 5: 기록 한 건의 형식 검사
    if not isinstance(item, dict):
        return False
    if not isinstance(item.get("played_at"), str):
        return False
    for key in ("total", "correct", "hints_used", "score"):
        value = item.get(key)
        if not isinstance(value, int) or isinstance(value, bool):
            return False
    return True


# =====================================================
# QuizGame 클래스 - 게임 전체를 관리
#   - 속성: quizzes(퀴즈 목록), best_score(최고 점수), history(게임 기록)
# =====================================================
class QuizGame:
    def __init__(self):
        self.quizzes = []
        self.best_score = None
        self.history = []                     # 보너스 5: 모든 게임 기록
        self.load_state()

    # =================================================
    # 10단계: 파일 저장/불러오기 (state.json)
    # =================================================
    def save_state(self):
        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
            "history": self.history,
        }
        try:
            with open(STATE_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except OSError:
            print("저장에 실패했습니다. 파일 권한이나 경로를 확인하세요.")

    def load_state(self):
        if not os.path.exists(STATE_FILE):    # 첫 실행: 파일 없음
            self.quizzes = get_default_quizzes()
            self.best_score = None
            self.history = []
            return

        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            quizzes = [Quiz.from_dict(item) for item in data["quizzes"]]
            best_score = data["best_score"]
            if best_score is not None and (
                not isinstance(best_score, int) or isinstance(best_score, bool)
            ):
                raise ValueError("best_score 형식 오류")
            history = data.get("history", [])  # 옛 파일에는 history가 없을 수 있음
            if not isinstance(history, list) or not all(is_valid_history_item(h) for h in history):
                raise ValueError("history 형식 오류")
            self.quizzes = quizzes
            self.best_score = best_score
            self.history = history
        except (OSError, ValueError, KeyError, TypeError):
            print("데이터 파일이 손상되어 기본 퀴즈로 초기화합니다.")
            self.quizzes = get_default_quizzes()
            self.best_score = None
            self.history = []
            self.save_state()

    # =================================================
    # 4단계: 퀴즈 추가 기능 (힌트 입력 포함)
    # =================================================
    def add_quiz(self):
        question = get_text_input("문제: ")
        choices = []
        for i in range(1, 5):
            choices.append(get_text_input(f"선택지 {i}: "))
        answer = get_number_input("정답 번호 (1~4): ", 1, 4)
        hint = input("힌트 (없으면 Enter): ").strip()    # 힌트는 비워도 됨
        self.quizzes.append(Quiz(question, choices, answer, hint))
        self.save_state()
        print(f"퀴즈가 추가되었습니다. (현재 {len(self.quizzes)}개)")

    # =================================================
    # 5단계: 퀴즈 풀기 기능 (랜덤 출제 + 문제 수 선택 + 힌트)
    # =================================================
    def play_quiz(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        # 보너스 2: 풀 문제 수 선택
        total = get_number_input(f"풀 문제 수 (1~{len(self.quizzes)}): ", 1, len(self.quizzes))
        # 보너스 1: 전체 중 total개를 무작위 순서로 뽑기
        selected = random.sample(self.quizzes, total)

        points = 0                            # 얻은 점수 합계
        correct_count = 0
        hints_used = 0
        for quiz in selected:
            print()
            quiz.display()

            hint_used = False
            while True:
                if quiz.hint:                 # 힌트가 있는 문제만 0번으로 힌트 보기
                    answer = get_number_input(
                        f"정답 번호 (1~4, 힌트 보기: 0 / -{HINT_PENALTY}점): ", 0, 4)
                else:
                    answer = get_number_input("정답 번호 (1~4): ", 1, 4)

                if answer == 0:               # 보너스 3: 힌트 요청
                    if not hint_used:
                        hint_used = True
                        hints_used += 1
                    print(f"힌트: {quiz.hint}")
                    continue                  # 힌트를 보고 다시 입력
                break

            if quiz.is_correct(answer):
                gained = POINT_PER_QUIZ - (HINT_PENALTY if hint_used else 0)
                points += gained
                correct_count += 1
                print(f"정답입니다! (+{gained}점)")
            else:
                print(f"오답입니다. 정답은 {quiz.answer}번입니다.")

        # 100점 만점으로 환산: 문제 수가 달라도 점수를 공정하게 비교
        score = round(points * 100 / (POINT_PER_QUIZ * total))
        print(f"\n결과: {total}문제 중 {correct_count}문제 정답 (힌트 {hints_used}회) → {score}점")

        self.update_best_score(score)
        self.add_history(total, correct_count, hints_used, score)
        self.save_state()

    # =================================================
    # 6단계: 퀴즈 목록 기능
    # =================================================
    def list_quizzes(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        print("\n===== 퀴즈 목록 =====")
        for number, quiz in enumerate(self.quizzes, start=1):
            mark = " (힌트 있음)" if quiz.hint else ""
            print(f"{number}. {quiz.question}{mark}")
        print(f"총 {len(self.quizzes)}개")

    # =================================================
    # 보너스 4: 퀴즈 삭제 기능
    # =================================================
    def delete_quiz(self):
        if not self.quizzes:
            print("삭제할 퀴즈가 없습니다.")
            return

        self.list_quizzes()
        number = get_number_input(f"삭제할 번호 (1~{len(self.quizzes)}, 취소: 0): ", 0, len(self.quizzes))
        if number == 0:
            print("삭제를 취소했습니다.")
            return

        removed = self.quizzes.pop(number - 1)    # 번호는 1부터, 리스트 인덱스는 0부터
        self.save_state()                         # 삭제 후 파일에 반영
        print(f"삭제되었습니다: {removed.question}")

    # =================================================
    # 7단계: 점수 확인 기능 + 보너스 5: 기록 히스토리
    # =================================================
    def update_best_score(self, score):
        if self.best_score is None or score > self.best_score:
            self.best_score = score

    def show_best_score(self):
        if self.best_score is None:
            print("아직 퀴즈를 풀지 않았습니다.")
        else:
            print(f"최고 점수: {self.best_score}점 (100점 만점)")

    def add_history(self, total, correct, hints_used, score):
        # 한 판이 끝날 때마다 날짜/시간, 푼 문제 수, 점수를 기록
        self.history.append({
            "played_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total": total,
            "correct": correct,
            "hints_used": hints_used,
            "score": score,
        })

    def show_history(self):
        if not self.history:
            print("아직 게임 기록이 없습니다.")
            return

        print("\n===== 게임 기록 (최근 10개) =====")
        for item in self.history[-10:]:
            print(f"{item['played_at']} | {item['total']}문제 중 {item['correct']}개 정답 "
                  f"| 힌트 {item['hints_used']}회 | {item['score']}점")
        print(f"총 {len(self.history)}판")

    # =================================================
    # 8단계: 메뉴
    # =================================================
    def show_menu(self):
        print("========== 퀴즈 게임 ==========")
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 퀴즈 삭제")
        print("5. 점수 확인")
        print("6. 게임 기록")
        print("7. 종료")
        print("================================")

    def get_menu_choice(self):
        return get_number_input("번호를 선택하세요: ", 1, 7)

    # =================================================
    # 9단계: 프로그램 흐름
    # =================================================
    def run(self):
        while True:
            self.show_menu()
            choice = self.get_menu_choice()

            if choice == 1:
                self.play_quiz()
            elif choice == 2:
                self.add_quiz()
            elif choice == 3:
                self.list_quizzes()
            elif choice == 4:
                self.delete_quiz()
            elif choice == 5:
                self.show_best_score()
            elif choice == 6:
                self.show_history()
            elif choice == 7:
                self.save_state()
                print("프로그램을 종료합니다.")
                break


# =====================================================
# 프로그램 시작 (Ctrl+C / EOF 안전 종료)
# =====================================================
def main():
    game = QuizGame()
    try:
        game.run()
    except (KeyboardInterrupt, EOFError):
        print("\n입력이 중단되었습니다. 저장 후 안전하게 종료합니다.")
        game.save_state()


main()