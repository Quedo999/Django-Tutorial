## Part 1: 요청과 응답
> https://docs.djangoproject.com/ko/4.1/intro/tutorial01/
### 1. 장고 버전 확인
- 쉘 프롬프트에서 명령어 실행
```zsh
$ python -m django --version
```
### 2. 프로젝트 만들기
- 터미널에서 프로젝트를 생성할 디렉토리로 이동 후 명령어 실행
```zsh
$ django-admin startproject mysite
```
### 3. 개발 서버
- ex) Django의 사이클
![django-cycle](https://i.stack.imgur.com/rLfSC.jpg)

1. Django 프로젝트가 제대로 동작하는지 확인
   - mysite 디렉토리로 이동해 명령어 실행
    ```
    python manage.py runserver
    ```
   - 이 서버는 개발목적으로만 사용! 개발 후 상용할 때는 실제 서버에 올려야 한다.
  
### 4. 설문조사 앱 만들기
1. 프로젝트와 앱
    1. 프로젝트: 웹 사이트에 대한 구성 및 앱의 모음
    2. 앱: 특정한 기능을 수행하는 어플리케이션

2. 앱을 생성하기
   - manage.py가 존재하는 디렉토리(프로젝트 디렉토리)에서 명령어 실행
   ```
   $ python manage.py startapp polls
   ```
   - 명령어를 실행하면 프로젝트 디렉토리내에 polls 디렉토리가 생성됨.

### 5. 첫 번째 뷰 작성
1. polls/views.py 파일을 열어 파이선 코드를 입력함.
> polls/views.py
~~~python
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
~~~

2. 작성한 뷰를 호출하기 위해 url파일을 작성하고 뷰와 연결해야한다. url파일이 현재 앱 디렉토리 내에 없기 때문에 urls.py파일을 생성하고 코드 작성
> polls/urls.py
~~~python
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
~~~

3. 최상위 URLconf에서 polls.urls 모듈을 바라보게 설정
> mysite/urls.py
~~~python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
]
~~~
  - include()함수는 다른 URLconf들을 참조할 수 있도록 도와준다.
  - 인덱스 뷰가 URLconf에 연결됐으니 작동확인을 위해 서버실행
  - 다른 URL 패턴을 포함할 때 마다 항상 include()를 사용해야하며. admin.site.urls가 유일한 예외.
  - 브라우저에서 해당 주소로 들어가면 뷰에 정의한 “Hello, world. You’re at the polls index."를 확인가능
  > http://localhost:8000/polls/
  - path() 함수에는 2개의 필수인수인 route와 view, 2개의 선택인수인 kwargs와 name까지 모두 4개의 인수가 전달된다.
    1. route: URL 패턴을 가진 문자열.
    2. view: 일치하는 패턴을 찾으면, 해당하는 특정한 view 함수를 호출한다.
    3. kwargs: 임의의 키워드 인수들은 목표한 view에 사전형으로 전달. 튜토리얼에서는 사용 X
    4. name: URL에 이름을 지으면, 템플릿을 포함한 Django 어디에서나 명확히 참조할 수 있다. 이 기능을 이용해 단 하나의 파일만 수정해도 프로젝트 내의 모든 URL 패턴을 변경 가능하도록 도와줌.