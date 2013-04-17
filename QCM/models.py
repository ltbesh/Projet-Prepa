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
	level = models.ForeignKey(Level, null = True)
	subject = models.ForeignKey(Subject, null = True)
	chapter = models.ForeignKey(Chapter, null = True)
	grade = models.IntegerField(default = 0)
	finished = models.BooleanField(default = False)
	

	def is_finished(self):
		try:
			guess = Guess.objects.filter(quizz = self, answer = None)[0]
		except:
			self.finished = True
			self.compute_grade()
			self.save()
		return self.finished

	def compute_grade(self):
		"""
		Calculates the grade for a quizz and return it (the grade is /20)
		"""
		guess_list = Guess.objects.filter(quizz = self)
		nb_correct_answer = 0
		for guess in guess_list:
			if guess.answer.validity:
				nb_correct_answer += 1
		self.grade = round((nb_correct_answer / float(len(guess_list))) * 20.0)
		self.save()
		return self.grade

	def add_question(self, number = 10): 
		"""
		Adds number question to the quizz with corresponding subject, level and chapter
		"""
		question_list = Question.objects.filter(level = self.level, subject = self.subject, chapter = self.chapter).order_by('?')[0:number]
		for question in question_list:
			guess = Guess(question = question, quizz = self)
			guess.save()

	def get_unanswered_question(self):
		"""
		Returns a question of the current quizz that has not been answered yet
		"""
		if self.is_finished():
			return None
		else:
			return Guess.objects.filter(quizz = self, answer = None)[0]
		
	def get_absolute_url(self):
		return reverse('quizz_display', args=[str(self.id)])

	def __unicode__ (self):
			return str(self.user) + "--" + str(self.date_started) + '--' + str(self.level)

class Answer(models.Model):
	answer = models.CharField(max_length = 200)
	question = models.ForeignKey(Question)
	validity = models.BooleanField()

	def __unicode__ (self):
		return self.answer

class Guess(models.Model):
	quizz = models.ForeignKey(Quizz)
	question = models.ForeignKey(Question)
	answer = models.ForeignKey(Answer, blank = True, null = True)
	answer_date = models.DateTimeField('date answered', default = datetime.now())

	def get_correct_answer(self):
		try :
			correct_answer = Answer.objects.get(question = self.question, validity = True)
		except:
			correct_answer = "Il n'y avait pas de bonne reponse"
		return correct_answer

	def correction(self):
		return (self.question, self.answer, self.get_correct_answer())

	def __unicode__ (self):
			return str(self.quizz.id) + "--" + str(self.question.id) + '--' + str(self.answer)


class News(models.Model):
	author  = models.ForeignKey(User)
	date_created = models.DateTimeField()
	title = models.CharField(max_length = 200)
	content = models.TextField()