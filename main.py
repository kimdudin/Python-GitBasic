import json
import os

# state.json은 프로젝트 루트(이 파일과 같은 폴더)에 저장
STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "state.json")


# =====================================================
# 1단계: Quiz 클래스 - 퀴즈 한 문제를 표현
# =====================================================
class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question    # 문제 (str)
        self.choices = choices      # 선택지 4개 (list)
        self.answer = answer        # 정답 번호 1~4 (int)

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
        }

    @staticmethod
    def from_dict(data):
        # 딕셔너리에서 Quiz 객체로 복원 (형식이 틀리면 예외 발생)
        question = data["question"]
        choices = data["choices"]
        answer = data["answer"]
        if not isinstance(question, str) or not question.strip():
            raise ValueError("question 형식 오류")
        if not isinstance(choices, list) or len(choices) != 4:
            raise ValueError("choices 형식 오류")
        if not isinstance(answer, int) or isinstance(answer, bool) or not 1 <= answer <= 4:
            raise ValueError("answer 형식 오류")
        return Quiz(question, choices, answer)


# =====================================================
# 2단계: 기본 퀴즈 데이터 (Git 기초 명령어 주제)
# =====================================================
def get_default_quizzes():
    return [
        Quiz("새 Git 저장소를 만드는 명령어는?", ["add", "commit", "init", "push"], 3),
        Quiz("변경한 파일을 커밋 대상에 올리는 명령어는?", ["commit", "clone", "pull", "add"], 4),
        Quiz("원격 변경사항을 가져와 합치는 명령어는?", ["commit", "clone", "pull", "add"], 3),
        Quiz("브랜치를 바꾸는 명령어는?", ["checkout", "clone", "pull", "add"], 1),
        Quiz("원격 저장소를 통째로 복제하는 명령어는?", ["checkout", "clone", "pull", "add"], 2),
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


# =====================================================
# QuizGame 클래스 - 게임 전체를 관리
#   - 속성: self.quizzes(퀴즈 목록), self.best_score(최고 점수)
# =====================================================
class QuizGame:
    def __init__(self):
        self.quizzes = []
        self.best_score = None
        self.load_state()                     # 시작할 때 파일에서 불러오기

    # =================================================
    # 10단계: 파일 저장/불러오기 (state.json)
    # =================================================
    def save_state(self):
        # 퀴즈 목록과 최고 점수를 JSON 파일에 저장
        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
        }
        try:
            with open(STATE_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except OSError:
            print("저장에 실패했습니다. 파일 권한이나 경로를 확인하세요.")

    def load_state(self):
        # 파일에서 불러오기. 없으면 기본값, 손상됐으면 안내 후 기본값으로 복구
        if not os.path.exists(STATE_FILE):    # 첫 실행: 파일 없음
            self.quizzes = get_default_quizzes()
            self.best_score = None
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
            self.quizzes = quizzes
            self.best_score = best_score
        except (OSError, ValueError, KeyError, TypeError):
            # json.JSONDecodeError는 ValueError의 하위 클래스
            print("데이터 파일이 손상되어 기본 퀴즈로 초기화합니다.")
            self.quizzes = get_default_quizzes()
            self.best_score = None
            self.save_state()                 # 기본값으로 복구해 다시 저장

    # =================================================
    # 4단계: 퀴즈 추가 기능
    # =================================================
    def add_quiz(self):
        question = get_text_input("문제: ")
        choices = []
        for i in range(1, 5):                 # 선택지 4개 입력
            choices.append(get_text_input(f"선택지 {i}: "))
        answer = get_number_input("정답 번호 (1~4): ", 1, 4)
        self.quizzes.append(Quiz(question, choices, answer))   # 리스트에 추가
        self.save_state()                     # 추가 즉시 저장
        print(f"퀴즈가 추가되었습니다. (현재 {len(self.quizzes)}개)")

    # =================================================
    # 5단계: 퀴즈 풀기 기능
    # =================================================
    def play_quiz(self):
        if not self.quizzes:                  # 퀴즈가 없는 경우
            print("등록된 퀴즈가 없습니다.")
            return

        score = 0
        for quiz in self.quizzes:
            print()
            quiz.display()
            answer = get_number_input("정답 번호 (1~4): ", 1, 4)
            if quiz.is_correct(answer):
                print("정답입니다!")
                score += 1
            else:
                print(f"오답입니다. 정답은 {quiz.answer}번입니다.")

        print(f"\n결과: {len(self.quizzes)}문제 중 {score}문제 정답")
        self.update_best_score(score)         # 풀 때마다 최고 점수와 비교
        self.save_state()                     # 갱신된 최고 점수 저장

    # =================================================
    # 6단계: 퀴즈 목록 기능
    # =================================================
    def list_quizzes(self):
        if not self.quizzes:                  # 퀴즈가 없는 경우
            print("등록된 퀴즈가 없습니다.")
            return

        print("\n===== 퀴즈 목록 =====")
        for number, quiz in enumerate(self.quizzes, start=1):   # 번호는 1부터
            print(f"{number}. {quiz.question}")                 # 목록에서는 문제만 출력
        print(f"총 {len(self.quizzes)}개")

    # =================================================
    # 7단계: 점수 확인 기능
    # =================================================
    def update_best_score(self, score):
        # 처음 푼 경우(None)이거나 이번 점수가 더 높으면 갱신
        if self.best_score is None or score > self.best_score:
            self.best_score = score

    def show_best_score(self):
        if self.best_score is None:           # 아직 퀴즈를 풀지 않은 경우
            print("아직 퀴즈를 풀지 않았습니다.")
        else:
            print(f"최고 점수: {self.best_score}점")

    # =================================================
    # 8단계: 메뉴
    # =================================================
    def show_menu(self):
        print("========== 퀴즈 게임 ==========")
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")
        print("================================")

    def get_menu_choice(self):
        # 메뉴 번호(1~5) 입력. 검증은 get_number_input 재사용
        return get_number_input("번호를 선택하세요: ", 1, 5)

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
                self.show_best_score()
            elif choice == 5:
                self.save_state()             # 종료 전 저장
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
        # Ctrl+C 또는 입력 스트림 종료: 안내 후 저장하고 정상 종료
        print("\n입력이 중단되었습니다. 저장 후 안전하게 종료합니다.")
        game.save_state()


main()