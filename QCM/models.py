import datetime, random
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
import time
from time import mktime
from datetime import datetime
from django.shortcuts import get_object_or_404

class UserProfile(models.Model): #Used for registration
	user = models.OneToOneField(User)
	activation_key = models.CharField(max_length = 40)
	key_expires = models.DateTimeField()
	
class Subject(models.Model):# Example : Mathematique, Physics, Chemistry ...
	name = models.CharField(max_length = 200)

	def __unicode__ (self):
		return self.name

class Level(models.Model):# Example : MPSI, PCSI ...
	name = models.CharField(max_length = 200)

	def __unicode__ (self):
		return self.name


class Chapter(models.Model):# Example : Calculus, algebra ...
	name = models.CharField(max_length = 200) # name of the chapter : calculus, probability ...
	
	def __unicode__ (self):
		return self.name

class Question(models.Model):
	level = models.ManyToManyField(Level)
	subject = models.ManyToManyField(Subject)
	chapter = models.ManyToManyField(Chapter)
	pub_date = models.DateTimeField('date published', default = datetime.now())
	
	question = models.CharField(max_length = 2000)
	
	def __unicode__ (self):
		return self.question
	def get_chapter(self):
		return self.chapter.all()
	def get_subject(self):
		return self.subject.all()
	def get_level(self):
		return self.clevel.all()

class Quizz(models.Model):

	user = models.ForeignKey(User)
	date_started = models.DateTimeField('date started')
	questions = models.ManyToManyField(Question)
	level = models.ForeignKey(Level, null = True)
	subject = models.ForeignKey(Subject, null = True)
	chapter = models.ForeignKey(Chapter, null = True)
	grade = models.IntegerField(default = 0)

	@classmethod
	def new(cls,user, chapter, subject, level):
		struct=time.localtime()
		level = get_object_or_404(Level, pk = level)
		subject = get_object_or_404(Subject, pk = subject)
		chapter = get_object_or_404(Chapter, pk = chapter)
		quizz=cls(user = user, level = level, subject = subject, chapter = chapter, date_started = datetime.fromtimestamp(mktime(struct)))
		return quizz
		
	def append(self, number = 10): #choppe les number questions au hasard dans la bdd question telles que les chapter subjects etc sont ok
		question_list = Question.objects.filter(chapter = self.chapter, subject = self.subject,level = self.level).order_by('?')[0:number]
		for question in question_list:
			self.questions.add(question)

	def __unicode__ (self):
			return str(self.user) + "--" + str(self.date_started)
			
		
class Answer(models.Model):
	question = models.ForeignKey(Question)
	answer = models.CharField(max_length = 200)
	validity = models.BooleanField()

	def __unicode__ (self):
		return self.answer

class Guess(models.Model):
	quizz = models.ForeignKey(Quizz)
	answer = models.ForeignKey(Answer)
	answer_date = models.DateTimeField('date answered')

	@classmethod
	def new(cls,use,ans):
		struct=time.localtime()
		quizz=cls(quizz=use,answer=ans,answer_date=datetime.fromtimestamp(mktime(struct)))
		return quizz

class News(models.Model):
	author  = models.ForeignKey(User)
	date_created = models.DateTimeField()
	title = models.CharField(max_length = 200)
	content = models.TextField()

#class Temporary_Questions(models.Model): # inherit from question, has comments from admin and moderators in addition to questions fields
	


#class Tags(models.Model):
#	tag = models.CharField(max_length=15)
	
