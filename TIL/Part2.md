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
```python
>>> from polls.models import Choice, Question  # Import the model classes we just wrote.

# No questions are in the system yet.
>>> Question.objects.all()
<QuerySet []>

# Create a new Question.
# Support for time zones is enabled in the default settings file, so
# Django expects a datetime with tzinfo for pub_date. Use timezone.now()
# instead of datetime.datetime.now() and it will do the right thing.
>>> from django.utils import timezone
>>> q = Question(question_text="What's new?", pub_date=timezone.now())

# Save the object into the database. You have to call save() explicitly.
>>> q.save()

# Now it has an ID.
>>> q.id
1

# Access model field values via Python attributes.
>>> q.question_text
"What's new?"
>>> q.pub_date
datetime.datetime(2012, 2, 26, 13, 0, 0, 775217, tzinfo=datetime.timezone.utc)

# Change values by changing the attributes, then calling save().
>>> q.question_text = "What's up?"
>>> q.save()

# objects.all() displays all the questions in the database.
>>> Question.objects.all()
<QuerySet [<Question: Question object (1)>]>
```
- <Question: Question object (1)>은 이 객체를 표현하는 데 도움이 되지 않음. (polls/models.py 파일의) Question 모델을 수정하여, __str__() 메소드를 Question과 Choice에 추가해 보자.
> polls/models.py
```python
from django.db import models

class Question(models.Model):
    # ...
    def __str__(self):
        return self.question_text

class Choice(models.Model):
    # ...
    def __str__(self):
        return self.choice_text
```
- 모델에 `__str()__` 메소드를 추가하는건 객체의 표현을 대화식 프롬프트에서 편하게 보려는이유 말고도 Django가 자동으로 생성하는 관리 사이트 에서도 객체의 표현이 사용되기 때문.
- 커스텀 메소드 또한 추가
> polls/models.py
```python
import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    # ...
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
```
- `import datetime`은 Python의 표준 모듈인 datetime 모듈을, `from django.utils import timezone`은 Django의 시간대 관련 유틸리티인 `django.utils.timezone`을 참조하기 위해 추가.
- 변경된 사항을 저장하고, `python manage.py shell`을 다시 실행
```python
>>> from polls.models import Choice, Question

# Make sure our __str__() addition worked.
>>> Question.objects.all()
<QuerySet [<Question: What's up?>]>

# Django provides a rich database lookup API that's entirely driven by
# keyword arguments.
>>> Question.objects.filter(id=1)
<QuerySet [<Question: What's up?>]>
>>> Question.objects.filter(question_text__startswith='What')
<QuerySet [<Question: What's up?>]>

# Get the question that was published this year.
>>> from django.utils import timezone
>>> current_year = timezone.now().year
>>> Question.objects.get(pub_date__year=current_year)
<Question: What's up?>

# Request an ID that doesn't exist, this will raise an exception.
>>> Question.objects.get(id=2)
Traceback (most recent call last):
    ...
DoesNotExist: Question matching query does not exist.

# Lookup by a primary key is the most common case, so Django provides a
# shortcut for primary-key exact lookups.
# The following is identical to Question.objects.get(id=1).
>>> Question.objects.get(pk=1)
<Question: What's up?>

# Make sure our custom method worked.
>>> q = Question.objects.get(pk=1)
>>> q.was_published_recently()
True

# Give the Question a couple of Choices. The create call constructs a new
# Choice object, does the INSERT statement, adds the choice to the set
# of available choices and returns the new Choice object. Django creates
# a set to hold the "other side" of a ForeignKey relation
# (e.g. a question's choice) which can be accessed via the API.
>>> q = Question.objects.get(pk=1)

# Display any choices from the related object set -- none so far.
>>> q.choice_set.all()
<QuerySet []>

# Create three choices.
>>> q.choice_set.create(choice_text='Not much', votes=0)
<Choice: Not much>
>>> q.choice_set.create(choice_text='The sky', votes=0)
<Choice: The sky>
>>> c = q.choice_set.create(choice_text='Just hacking again', votes=0)

# Choice objects have API access to their related Question objects.
>>> c.question
<Question: What's up?>

# And vice versa: Question objects get access to Choice objects.
>>> q.choice_set.all()
<QuerySet [<Choice: Not much>, <Choice: The sky>, <Choice: Just hacking again>]>
>>> q.choice_set.count()
3

# The API automatically follows relationships as far as you need.
# Use double underscores to separate relationships.
# This works as many levels deep as you want; there's no limit.
# Find all Choices for any question whose pub_date is in this year
# (reusing the 'current_year' variable we created above).
>>> Choice.objects.filter(question__pub_date__year=current_year)
<QuerySet [<Choice: Not much>, <Choice: The sky>, <Choice: Just hacking again>]>

# Let's delete one of the choices. Use delete() for that.
>>> c = q.choice_set.filter(choice_text__startswith='Just hacking')
>>> c.delete()
```

<br/>

### 5. Django 관리자 소개
---
1. 관리자 생성하기
     - 관리 사이트에 로그인 할 수 있는 사용자 생성
  ```python
  $ python manage.py createsuperuser
 
  Username: admin
  Email address: admin@example.com
  Password: ********
  Password (again): ********
  superuser created successfully.
  ```
  ---
2. 개발 서버 시작
   - Django의 관리자 사이트는 기본으로 활성화되어 있다. 개발서버를 실행.
    ``` zsh
    $ python manage.py runserver 
    ```
   - 웹 브라우저를 열고 로컬 도메인의 "/admin/"으로 이동하면 관리자의 로그인 화면이 나타남.
    ![관리자로그인](https://docs.djangoproject.com/ko/4.1/_images/admin01.png)
    - translation이 기본적으로 설정되있으므로 LANGUAGE_CODE를 설정하면 지정된 언어로 표시됨.
---
3. 관리자 사이트에 들어가기
   - 슈퍼유저 계정으로 로그인하면 Django 관리 인덱스 페이지가 보임.
    ![관리인덱스페이지](https://docs.djangoproject.com/ko/4.1/_images/admin02.png)
---
4. 관리 사이트에서 poll app 을 변경가능 하도록 변경
     - polls app이 관리 인덱스 페이지에서 보이지 않음
     - 관리 인터페이스가 있으니 polls/admin.py 파일을 열어 편집
     > polls/admin.py
    ```python
    from django.contrib import admin

    from .models import Question

    admin.site.register(Question)
    ```
---
5. 자유로운 관리 기능 탐색
    - Question을 등록시켰으니 Django는 관리 인덱스 페이지에 이를 표시함
    ![관리인덱스페이지](https://docs.djangoproject.com/ko/4.1/_images/admin03t.png)
    - "Question"을 클릭하면 "change list"로 이동. 이 페이지는 데이터 베이스에 저장된 모든 질문들을 보여주고 그 중 하나를 선택해 변경할 수있다.
    ![Question클릭페이지](https://docs.djangoproject.com/ko/4.1/_images/admin04t.png)
    - 해당 서식은 Question 모델에서 자동으로 생성
    - 모델의 각 필드 유형들은 적절한 HTML 입력 위젯으로 표현
