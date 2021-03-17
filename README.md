# 도서관 대출 서비스

## 목차
- [프로젝트 소개](#프로젝트-소개)
- [주요 사용 기술](#주요-사용-기술)
- [프로젝트 설치 및 실행 방법](#프로젝트-설치-및-실행-방법)
- [디렉토리 구조](#디렉토리-구조)
- [기능 소개](#기능-소개)
- [Reference](#reference)

## 프로젝트 소개
도서 대여, 반납 등의 도서관 기본 기능을 제공하는 반응형 웹 서비스입니다.    
[여기](http://elice-kdt-ai-track-vm-racer-18.koreacentral.cloudapp.azure.com/)에서 자세히 살펴보실 수 있습니다.

## 주요 사용 기술
- Flask
- SQLAlchemy
- PyMySQL
- MySQL
- HTML + Flask Jinja2 + CSS
- Azure VM (OS: ubuntu LTS 18.04)

## 프로젝트 설치 및 실행 방법
### 설치
```bash
# clone the project repository
git clone https://kdt-gitlab.elice.io/001_part2_project-library/team1/library.git
# 프로젝트 디렉토리로 이동
cd library
```

### 가상 환경 구축
```bash
# 가상 환경 폴더 생성
python -m venv python-env
# 가상 환경 접속
source python-env/bin/activate
# 패키지 설치
pip install -r requirements.txt
```

### 데이터베이스 설정
```bash
# library/config.py 생성하고 아래 내용 작성
# 실제 정보를 <>, []에 기입해주세요.

SQLALCHEMY_DATABASE_URI = "mysql+pymysql://<username>:<password>@<hostname>:3306/<database_name>?charset=utf8mb4"
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = [secret_key]
```

### 마이그레이션 및 데이터 초기화
```bash
# migrations directory 생성
flask db init
flask db migrate
flask db upgrade

# 초기 데이터 로드
python load_data.py
```

### 실행
```bash
python run.py
```

## 디렉토리 구조
```
library                 # root
├─ data
|   └─ books.csv                # 초기 데이터
├─ launcher
|   ├─ static                   # css, image
|   ├─ templates                # html files
|   ├─ views
|   |   ├─ auth_views.py            # 회원가입, 로그인, 로그아웃 view
|   |   ├─ board_views.py           # 게시판 view
|   |   ├─ book_views.py            # 책 상세 view
|   |   └─ main_views.py            # 메인, 대여, 반납 view
|   ├─ __init__.py
|   ├─ forms.py                 # 회원가입, 로그인 form 정의
|   └─ models.py                # User, Book, BookRental, Comment, Article Model 정의
├─ migrations
├─ python-env               # python 가상 환경
├─ .gitignore
├─ config.py
├─ load_data.py             # 초기 데이터 로드 파일
├─ README.md
├─ requirements.txt
└─ run.py                   # launcher 실행 파일
```

## 기능 소개
### 로그인
- 사용자로부터 아이디(이메일)와 비밀번호 정보를 입력받아 로그인합니다.
- 아이디와 비밀번호는 필수 입력 사항입니다.
- 아이디는 이메일 형식으로만 입력해야 합니다.
- 비밀번호는 최소 8자리 이상의 길이로 입력해야 합니다.
- 로그인한 유저에 대해 session으로 관리합니다.

### 로그아웃
- 현재 로그인한 사용자에 대해 로그아웃합니다.
- 로그아웃한 사용자를 현재 session에서 제거합니다. 

### 회원가입
- 사용자로부터 이름, 아이디(이메일), 비밀번호 정보를 입력받아 회원가입합니다.
- 이름은 한글, 영문으로만 입력해야 합니다.
- 아이디는 이메일 형식으로만 입력해야 합니다. 
- 비밀번호와 비밀번호 확인의 값이 일치해야 합니다.
- 비밀번호는 영문, 숫자, 특수문자를 각 하나 이상 조합하여 최소 8자리 이상의 길이로 구성합니다.

### 메인
- 현재 DB 상에 존재하는 모든 책 정보를 가져옵니다.
- 현재 DB 상에 존재하는 남은 책의 수를 표기합니다. 
- 책 이름을 클릭 시 책 소개 페이지로 이동합니다.
- 책의 평점은 현재 DB 상에 담겨있는 모든 평점의 평균입니다. 숫자 한자리수로 반올림하여 표기합니다.
- 한 페이지 당 8권의 책만을 표기하도록 페이지네이션 기능을 추가하였습니다.

### 대여하기
- 메인 페이지의 대여하기 버튼을 클릭하여 실행합니다.
- 현재 DB 상에 책이 존재하지 않는 경우, 대여되지 않습니다.
- 현재 DB 상에 책이 존재하지 않는 경우, 사용자에게 대여가 불가능하다는 메세지를 반환합니다.
- 현재 DB 상에 책이 존재하지만 사용자가 이미 대여 중인 경우, 대여가 불가능하다는 메세지를 반환합니다.
- 현재 DB 상에 책이 존재하고 대여한 적이 없거나 반납 완료한 경우, 책을 대여하고 책의 권수를 -1 합니다.
- 대여기록 : 로그인한 사용자가 대여한 모든 책에 대한 정보를 출력합니다.

### 반납하기
- 로그인한 사용자가 대여한 책 중 반납하지 않은 책을 모두 보여줍니다.
- 반납하기 버튼을 통해 책을 반납합니다. 책을 반납한 후 DB 상에 책의 권수를 +1 합니다.

### 책 소개
- 책 이름을 클릭하여 접근합니다.
- 책에 대한 소개를 출력합니다.
- 댓글
    - 총 댓글수를 보여줍니다.
    - 가장 최신의 댓글이 위에 위치하도록 sorting하여 보여줍니다.
    - 댓글을 작성함으로써 책에 대한 평가 점수를 기입합니다.
    - 댓글 내용과 평가 점수는 모두 필수 입력 사항입니다.
    - 댓글은 대여한 책에 대해서만 한 번 입력 가능합니다.

### 입고 게시판
- 원하는 책이 없을 경우, 사용자는 책 이름과 저자를 입력하여 입고 요청 게시글을 작성할 수 있습니다.
- 모든 게시글에 대한 정보(게시글 번호, 작성자, 책 이름, 저자, 작성일, 입고 현황)를 출력합니다.
- 가장 오래된 게시글부터 차례로 번호가 매겨지며, 최신의 게시글이 상단에 위치합니다.

## Reference
- [Flask 공식 문서](https://flask.palletsprojects.com/en/1.1.x/)
- [점프 투 플라스크](https://wikidocs.net/book/4542)
- 엘리스 AI 트랙 [05-01] Flask 웹 프로그래밍
- 엘리스 AI 트랙 [01-02] HTML/CSS
