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

        if choice == 5: # 5번이면 
            print("프로그램을 종료합니다.")#종료 메시지 출력 후 
            break
        else:
            print("준비 중입니다.") # 나머지는 "준비 중입니다" 출력

main()   # 정의가 다 끝난 맨 아래에서 호출