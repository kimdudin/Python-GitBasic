# Python-GitBasic: 터미널 퀴즈 게임

## 1. 프로젝트 개요

Python으로 만든 콘솔 퀴즈 게임입니다. 메뉴에서 번호를 골라 퀴즈를 풀고, 새 퀴즈를 추가하고, 목록과 최고 점수를 확인할 수 있습니다. 퀴즈와 최고 점수는 `state.json`에 저장되어 프로그램을 종료하고 다시 실행해도 유지됩니다. 클래스(객체 지향), 파일 입출력(JSON), 예외 처리, Git 워크플로우를 연습하기 위한 프로젝트입니다.

## 2. 퀴즈 주제와 선정 이유

- **주제:** Git 기초 명령어 (init, add, commit, push, pull, checkout, clone)
- **선정 이유:** 이번 미션에서 직접 사용하는 명령어들이라, 퀴즈를 만들면서 각 명령어의 역할을 복습하고 시험 예상문제로도 나올 수 있을 것 같아 선택했습니다.

## 3. 실행 방법

요구 사항: Python 3.10 이상 (외부 라이브러리 없음)

```bash
git clone https://github.com/kimdudin/Python-GitBasic.git
cd Python-GitBasic
python3 main.py
```

## 4. 기능 목록

| 메뉴 | 기능 | 설명 |
|---|---|---|
| 1 | 퀴즈 풀기 | 문제 수 선택, 랜덤 출제, 힌트(-5점), 100점 만점 환산, 최고 점수 갱신 |
| 2 | 퀴즈 추가 | 문제, 선택지 4개, 정답 번호, 힌트(선택) 입력 후 저장 |
| 3 | 퀴즈 목록 | 등록된 퀴즈를 번호와 함께 출력 |
| 4 | 퀴즈 삭제 | 번호를 골라 삭제 후 저장 |
| 5 | 점수 확인 | 최고 점수 확인 (풀지 않았으면 안내) |
| 6 | 게임 기록 | 최근 10판의 날짜/시간, 문제 수, 점수 확인 |
| 7 | 종료 | 저장 후 종료 |


공통 처리:
- 입력 앞뒤 공백 제거, 빈 입력, 숫자 아님, 범위 밖 입력 시 안내 후 재입력
- Ctrl+C, 입력 종료(EOF) 시 안내 메시지를 출력하고 저장 후 안전하게 종료
- `state.json`이 없으면 기본 퀴즈 사용, 손상되면 안내 후 기본값으로 복구



## 실행 화면

### 개발 환경
![개발 환경](docs/screenshots/dev_env.png)

### 퀴즈 추가
![퀴즈 추가](docs/screenshots/add_quiz.png)

### 퀴즈 목록
![퀴즈 목록](docs/screenshots/quiz_list.png)

### 퀴즈 풀기
![퀴즈 풀기 1](docs/screenshots/play1.png)
![퀴즈 풀기 2](docs/screenshots/play2.png)

### 점수 확인
![점수 확인](docs/screenshots/score.png)

### 재실행 후 데이터 유지
![재실행 후 퀴즈 유지](docs/screenshots/quiz_after_restart.png)
![재실행 후 점수 유지](docs/screenshots/score_after_restart.png)

### Git 이력
![git log](docs/screenshots/git_log.png)


## 5. 파일 구조
Python-GitBasic/
├── main.py
├── README.md
├── .gitignore
├── docs/
│   └── screenshots/          # 실행 화면 스크린샷
│       ├── dev_env.png
│       ├── add_quiz.png
│       ├── quiz_list.png
│       ├── play1.png
│       ├── play2.png
│       ├── score.png
│       ├── quiz_after_restart.png
│       ├── score_after_restart.png
│       └── git_log.png
└── state.json            # 실행 시 생성되는 데이터 파일 (Git 추적 제외)

주요 클래스:
- `Quiz`: 퀴즈 한 문제 (question, choices, answer), 출력/정답 확인/딕셔너리 변환
- `QuizGame`: 게임 전체 관리 (퀴즈 목록, 최고 점수, 메뉴, 저장/불러오기)

## 6. 데이터 파일 (state.json)

- **경로:** 프로젝트 루트의 `state.json` (UTF-8)
- **역할:** 퀴즈 목록, 최고 점수, 게임 기록을 저장해 종료 후에도 유지
- **생성:** 퀴즈 추가/삭제, 퀴즈 풀기, 종료 시 자동 생성/갱신
- **스키마:**

```json
{
  "quizzes": [
    {
      "question": "새 Git 저장소를 만드는 명령어는?",
      "choices": ["add", "commit", "init", "push"],
      "answer": 3,
      "hint": "'시작하다'라는 뜻의 영어 단어와 관련 있어요."
    }
  ],
  "best_score": 80,
  "history": [
    {
      "played_at": "2026-11-12 15:30:00",
      "total": 5,
      "correct": 4,
      "hints_used": 1,
      "score": 80
    }
  ]
}
```

- `quizzes`: 퀴즈 배열 (`answer`는 1~4, `hint`는 없으면 빈 문자열)
- `best_score`: 최고 점수, 100점 만점 (아직 풀지 않았으면 `null`)
- `history`: 게임 기록 배열 (시각, 푼 문제 수, 정답 수, 힌트 사용 횟수, 점수)