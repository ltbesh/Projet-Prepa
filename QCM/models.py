import datetime, random
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
import time
from time import mktime
from datetime import datetime
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse


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
	level = models.ForeignKey(Level, null = True)
	subject = models.ForeignKey(Subject, null = True)
	chapter = models.ForeignKey(Chapter, null = True)
	pub_date = models.DateTimeField('date published', default = datetime.now())
	
	question = models.CharField(max_length = 2000)
	
	def __unicode__ (self):
		return self.question
	def get_chapter(self):
		return self.chapter
	def get_subject(self):
		return self.subject
	def get_level(self):
		return self.level

class Quizz(models.Model):
	user = models.ForeignKey(User)
	date_started = models.DateTimeField('date started', default = datetime.now())
	questions = models.ManyToManyField(Question, through = 'QuestionStatus')
	level = models.ForeignKey(Level, null = True)
	subject = models.ForeignKey(Subject, null = True)
	chapter = models.ForeignKey(Chapter, null = True)
	grade = models.IntegerField(default = 0)
	finished = models.BooleanField(default = False)
		
	def add_question(self, number = 10): #choppe les number questions au hasard dans la bdd question telles que les chapter subjects etc sont ok
		question_list = Question.objects.order_by('?')[0:number]
		for question in question_list:
			question_status = QuestionStatus(question = question, quizz = self)
			question_status.save()

	def get_unanswered_question(self):
		try:
		    question = Question.objects.filter(questionstatus__quizz = self.id, questionstatus__answered = False)[0]
		except:
		    self.finished = True
		    self.save()
		    question = False
		return question
		
	def get_absolute_url(self):
		return reverse('quizz_display', args=[str(self.id)])

	def __unicode__ (self):
			return str(self.user) + "--" + str(self.date_started) + '--' + str(self.level)

class QuestionStatus(models.Model):
	question = models.ForeignKey(Question)
	quizz = models.ForeignKey(Quizz)
	answered = models.BooleanField(default = False)	

	def __unicode__ (self):
		return str(self.question) + " " + str(self.quizz) + " " + str(self.answered)

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

