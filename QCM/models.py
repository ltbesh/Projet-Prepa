import datetime
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

from django.db import models


class Chapter(models.Model):
	subject = models.CharField(max_length = 200) #Physique, Chime, Histoire ...
	level = models.CharField(max_length = 200) # Student class level 
	name = models.CharField(max_length = 200) # name of the chapter : calculus, probability ...
	

class Question(models.Model):
    pub_date = models.DateTimeField('date published')
    #creator = models.ForeignKey(User)
    #moderators = models.ForeignKey(User) # We need to be able to assign several moderators
    #validator = models.ForeignKey(User) #admin qui valide le passage a la bdd live
    
    question = models.CharField(max_length = 2000)
    
    # tags = models.ForeignKey(Tags) # Used for classifying question (course question, order of magnitude ...)

    #chapter = models.ForeignKey(Chapter)

class Answer(models.Model):
	question = models.ForeignKey(Question)
	answer = models.CharField(max_length = 200)
	validity = models.BooleanField()

class Guess(models.Model):
	user = models.ForeignKey(User)
	answer = models.ForeignKey(Answer)
	answer_date = models.DateTimeField('date answered')


#class Temporary_Questions(models.Model): # inherit from question, has comments from admin and moderators in addition to questions fields
	


#class Tags(models.Model):
#	tag = models.CharField(max_length=15)
	
