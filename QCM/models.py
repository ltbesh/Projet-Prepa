import datetime
from django.utils import timezone
from django.db import models

# Create your models here.

from django.db import models

class Question(models.Model):
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    good_answer = models.CharField(max_length=200)
    bad_answer_1 = models.CharField(max_length=200)
    bad_answer_2 = models.CharField(max_length=200)
    bad_answer_3 = models.CharField(max_length=200)

    class_level = models.CharField(max_length=200)

    subject = models.CharField(max_length=200)

    chapter = models.CharField(max_length=200)

