# Django-Tutorial

## part 2: 모델과 관리자 페이지
> https://docs.djangoproject.com/ko/4.1/intro/tutorial02/
### 1. 데이터베이스 설치
- mysite/settings.py 파일은 Django 설정을 모듈변수로 표현한 보통의 Python 모듈
- 기본적으로는 SQLite를 사용. 데이터베이스를 처음 경험하거나, Django에서 경험하고 싶다면 가장 간단한 방법. Python에서 기본적으로 제공한다.
- 실제 프로젝트시에는 PostgreSQL과 같이 더 확장성 있는 데이터베이스를 사용하는것이 좋다.
- 다른 데이터베이스 사용시에는 데이터베이스 바인딩을 설치하고, 연결 설정과 맞게끔 DATABASES 'default'의 값을 변경해야한다.
  - ENGINE - 'django.db.backends.sqlite3', 'django.db.backends.postgresql', 'django.db.backends.mysql', 또는 'django.db.backends.oracle'.
  - NAME - 데이터베이스의 이름. SQLite를 사용하는 경우 데이터베이스는 컴퓨터의 파일이 된다.
- SQLite 를 데이터베이스로 사용하지 않는 경우, USER, PASSWORD, HOST 같은 추가 설정이 반드시 필요합니다. 더 자세한 내용은 [DATABASES](https://docs.djangoproject.com/ko/4.1/ref/settings/#std-setting-DATABASES) 문서를 참조.
- mysite/settings.py를 편집할 때, 시간대에 맞춰 TIME_ZONE 값을 설정
- mysite/settings.py의 코드중 INSTALLED_APPS
  - Django 인스턴스에서 활성화된 모든 Django 어플리케이션들의 이름이 담김. 앱들은 다수의 프로젝트에서 사용될 수 있고, 다른 프로젝트에서 사용되기 쉽도록 패키징하여 배포도 가능
  - 기본적으로 다음의 앱들을 포함
    - django.contrib.admin – 관리용 사이트.
    - django.contrib.auth – 인증 시스템.
    - django.contrib.contenttypes – 컨텐츠 타입을 위한 프레임워크.
    - django.contrib.sessions – 세션 프레임워크.
    - django.contrib.messages – 메세징 프레임워크.
    - django.contrib.staticfiles – 정적 파일을 관리하는 프레임워크.
  - 이러한 기본 어플리케이션들 중 몇몇은 최소한 하나 이상의 데이터베이스 테이블을 사용한다. 그러기 위해서는 데이터베이스에서 테이블을 미리 만들 필요가 있음. 다음의 명령어 실행
    ~~~zsh
    $ python manage.py migrate
    ~~~
    - migrate 명령은 INSTALLED_APPS의 설정을 탐색해 mysite/settings.py의 데이터베이스 설정과 app과 함께 제공되는 database migrations에 따라 필요한 데이터베이스 테이블을 생성함.
    - 생성된 내용을 확인하려면 데이터베이스 클라이언트로 접속 후 각 데이터베이스에 맞는 테이블 확인 명령어를 통해 확인가능
    ```
    \dt (PostgreSQL)
    SHOW TABLES; (MariaDB, MySQL)
    .tables (SQLite) 
    SELECT TABLE_NAME FROM USER_TABLES; (Oracle)
    ```
<br/>

### 2. 모델 만들기
- 모델: 부가적인 메타데이터를 가진 데이터베이스의 구조(layout)
- 여론조사 앱에서 Question과 Choice라는 두 가지 모델을 만들 것.
  - Question: 질문과 발행일을 위한 두 개의 필드를 가짐
  - Choice: 선택 텍스트와 투표 집계를 위한 두 개의 필드를 가짐.
- 이러한 개념은 Python 클래스로 표현. polls/models.py 파일을 열어 다음과 같이 수정
> polls/models.py
~~~python
from django.db import models

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
~~~
  - 여기서 각 모델은 django.db.models.Model의 하위 클래스로 표현. 모델마다 여러 클래스 변수가 있고, 각 클래스 변수는 모델에서 데이터베이스 필드를 나타냄.
  - 데이터베이스의 각 필드는 Field클래스의 인스턴스로서 표현.
    - ex) CharField -> 문자필드를 표현
    - ex2) DataTimeField -> 날자와 시간(datetime) 필드를 표현
  - 몇몇 Field 클래스들은 필수 인수가 필요함.
    - ex) CharField의 경우 max_length를 입력해줘야 함.
  - Field 는 다양한 선택적 인수들을 가질 수 있음.
  - Django는 다대일, 다대다, 일대일과 같은 모든 일반 데이터베이스의 관계들을 지원
<br/>

### 3. 모델의 활성화
- 모델에 대한 작은 코드들이 Django에게 상당한 양의 정보를 전달함.
- Django는 해당 정보들을 가지고 다음과 같은 일을 할 수 있다.
  - 이 앱을 위한 데이터베이스 스키마 생성 (CREATE TABLE 문)
  - Question과 Choice 객체에 접근하기 위한 Python 데이터베이스 접근 API를 생성
- 가장 먼저 현재 프로젝트에 polls앱이 설치되어 있다는 것을 알려야 한다.
- 앱을 현재의 프로젝트에 포함시키기 위해서 앱의 구성 클래스에 대한 참조를 INSTALLD_APPS 설정에 추가해야함.
- PillsConfig 클래스는 polls/apps.py 파일내에 존재함. 따라서 경로는 `polls.apps.PollsConfig`가 된다. 해당 경롤를 mysite/settings.py 내부에 있는 INSTALLD_APPS 설정에 추가
> mysite/settings.py
```python
INSTALLED_APPS = [
    'polls.apps.PollsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```
- makemigrations명령어를 실행시켜 모델을 변경시킨 사실과(이 경우 새로운 모델을 만듬) 변경사항들을 migration으로 저장시키고 싶다는 것을 Django에게 알려줌.
~~~zsh
$ python manage.py makemigrations polls
~~~
- migration은 Djago가 모델의 변경사항을 디스크에 저장하는 방법.
- sqlmigrate 명령은 migration 이름을 인수로 받아 실행하는 SQL문장을 보여줌
```zsh
$ python manage.py sqlmigrate polls 0001
```
- 해당 명령어로 나오는 출력이 migration 할때 사용되는 SQL문장
- 참고
  - 사용하는 데이터베이스에 따라 출력결과는 다를 수 있음.
  - 테이블 이름은 앱의 이름과 모델의 이름이 조합돼 자동으로 생성. 튜토리얼의 경우 polls와 question, choice가 합쳐짐.(동작 재지정 가능)
  - 기본 키(id)가 자동으로 추가된다.(동작 재지정 가능)
  - 관례에 따라 Django는 외래 키 필드명에 "_id"이름을 자동으로 추가(동작 재지정 가능)
  - 외래키 관계는 FOREIGN KEY 라는 제약에 의해 명시.
  - sqlmigrate 명령은 실제로 마이그레이션을 실행하는게 아닌 화면에 출력해 필요한 SQL Django를 확인할 수 있도록 함.
- migrate를 실행해 데이터베이스에 모델과 관련된 테이블을 생성.
```zsh
$ python manage.py migrate
```
- migrate 명령은 아직 적용되지 않은 마이그레이션을 모두 수집해 이를 실행하며(Django는 django_migrations 테이블을 두어 마이그레이션 적용 여부를 추적) 이 과정을 통해 모델에서의 변경 사항들과 데이터베이스의 스키마의 동기화가 이루어짐.
- 마이그레이션은 프로젝트 개발때처럼 데이터베이스나 테이블에 손대지 않고 모델의 반복적인 변경을 가능하게 함. 동작 중인 데이터베이스를 자료 손실 없이 업그레이드 하는 데 최적화 됨.
- 모델의 변경을 만드는 세단계 지침
  1. models.py 에서 모델을 변경
  2. python manage.py makemigrations 명령을 통해 변경사항에 대한 마이그레이선 생성
  3. python manage.py migrate 명령을 통해 변경 사항을 데이터베이스에 적용
<br/>

### 4. API 가지고 놀기
- 대화식 Python 쉘에서 Django API를 사용해보기.
- manage.py에 설정된 DJANGO_SETTINGS_MODULE 환경변수를 사용하기 위해 해당 명령어 사용
```zsh
$ python manage.py shell
```
- DJANGO_SETTINGS_MODULE 은 Django에게 mysite/settings.py의 Python 가져오기 경로를 제공
- 