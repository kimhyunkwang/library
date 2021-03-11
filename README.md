# 도서관 대출 서비스

## 프로젝트 소개
도서 대여, 반납 등의 도서관 기본 기능을 제공하는 웹 서비스입니다.

## 주요 사용 기술
- Flask
- SQLAlchemy
- PyMySQL
- MySQL
- HTML + Flask Jinja2 + CSS
- Azure

## Directory 구조
```
library
├─ data
|   └─ books.csv
├─ launcher
|   ├─ static : css, image
|   ├─ templates : html files
|   ├─ views
|   |   ├─ auth_views.py : 회원가입, 로그인, 로그아웃
|   |   ├─ board_views.py : 게시판
|   |   ├─ book_views.py : 책 상세
|   |   └─ main_views.py : 메인, 대여, 반납
|   ├─ __init__.py
|   ├─ forms.py : 회원가입, 로그인 form 정의
|   └─ models.py : User, Book, BookRental, Comment, Article Model 정의
├─ migrations
├─ python-env
├─ .gitignore
├─ config.py
├─ load_data.py
├─ README.md
├─ requirements.txt
└─ run.py
```

## Reference
- Flask 공식 문서
- [점프 투 플라스크](https://wikidocs.net/book/4542)
- 엘리스 AI 트랙 [05-01] Flask 웹 프로그래밍
- 엘리스 AI 트랙 [01-02] HTML/CSS