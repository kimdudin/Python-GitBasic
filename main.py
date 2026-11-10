class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question    # 문제 (str)
        self.choices = choices      # 선택지 4개 (list)
        self.answer = answer        # 정답 번호 1~4 (int)

    def display(self):
        print(self.question)
        for number, choice in enumerate(self.choices, start=1):
            print(f"{number}. {choice}")

    def is_correct(self, user_answer):
        return user_answer == self.answer

def get_default_quizzes():
    return [
        Quiz("새 Git 저장소를 만드는 명령어는?", ["add", "commit", "init", "push"], 3),
        Quiz("변경한 파일을 커밋 대상에 올리는 명령어는?", ["commit", "clone", "pull", "add"], 4),
        Quiz("원격 변경사항을 가져와 합치는 명령어는?", ["commit", "clone", "pull", "add"], 3),
        Quiz("브랜치를 바꾸는 명령어는?", ["checkout", "clone", "pull", "add"], 1),
        Quiz("원격 저장소를 통째로 복제하는 명령어는?", ["checkout", "clone", "pull", "add"], 2),
    ]

def get_number_input(prompt, min_value, max_value):
    while True:
        text = input(prompt).strip()

        if text == "":
            print("입력이 비어 있습니다.")
            continue

        try:
            number = int(text)
        except ValueError:
            print("숫자만 입력할 수 있습니다.")
            continue

        if number < min_value or number > max_value:
            print(f"{min_value}~{max_value} 사이의 번호를 입력하세요.")
            continue

        return number
    # 공백 제거, 빈 입력, 숫자 변환 실패, 범위 밖을 처리하고 숫자를 return

def play_quiz(quizzes):
    if not quizzes:
        print("등록된 퀴즈가 없습니다.")
        return 0, 0

    score = 0
    for quiz in quizzes:
        print()
        quiz.display()
        answer = get_number_input("정답 번호 (1~4): ", 1, 4)
        if quiz.is_correct(answer):
            print("정답입니다!")
            score += 1
        else:
            print(f"오답입니다. 정답은 {quiz.answer}번입니다.")

    print(f"\n결과: {len(quizzes)}문제 중 {score}문제 정답")
    return score, len(quizzes)

def show_menu():
    print("========== 퀴즈 게임 ==========")
    print("1. 퀴즈 풀기")
    print("2. 퀴즈 추가")
    print("3. 퀴즈 목록")
    print("4. 점수 확인")
    print("5. 종료")
    print("================================")

def get_menu_choice():
    while True:
        text = input("번호를 선택하세요: ").strip()
        # 1) 빈 입력이면
        if text =="":
            print("입력이 비어있습니다. 1~5 사이의 숫자를 입력하세요.")
            continue #안내 출력 후 continue
        # 2) 숫자변환 
        try:
            choice = int(text)
        except ValueError: 
            print("숫자만 입력할 수 있습니다.")
            continue #안내 출력 후 continue
        # 3) 범위확인
        if choice< 1 or choice > 5: #1~5 범위 밖이면 
            print("1~5 사이의 번호를 선택하세요.") #안내 출력 후 
            continue

        # 4) 통과하면 
        return choice

def main():
    while True:
        show_menu()
        choice = get_menu_choice()

        if choice == 1:
            play_quiz(get_default_quizzes())
        elif choice == 5:
            print("프로그램을 종료합니다.")
            break
        else:
            print("준비 중입니다.")

main()   # 정의가 다 끝난 맨 아래에서 호출