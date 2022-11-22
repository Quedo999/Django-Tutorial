import datetime
from django.db import models
from django.utils import timezone
from django.contrib import admin

# Create your models here.
class Question(models.Model):
    def __str__(self):
        return self.question_text


    @admin.display(
            boolean=True,
            ordering='pub_date',
            description='Published recently?',
        )
    def was_published_recently(self):
        # 미래의 데이터가 들어갈 경우 False를 반환해야함. 에러코드가 된다.
        # return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

class Choice(models.Model):
    def __str__(self):
        return self.choice_text
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)