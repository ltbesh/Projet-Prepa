import datetime, random
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
import time
from time import mktime
from datetime import datetime

class UserProfile(models.Model): #Used for registration
	user = models.OneToOneField(User)
	activation_key = models.CharField(max_length = 40)
	key_expires = models.DateTimeField()
	
#FIXME:MK: can we merge UserProfile & PlayerProfile?

#~ class PlayerProfile(models.Model): #Our custom User. OneToOneField/ForeignKey relationship with User
	#~ user = models.OneToOneField(User) #Or ForeignKey ?
	#~ current_quizz = models.OneToOneField(Quizz) #Can be empty: to retrieve un-finished quizz
	#~ #level = models.CharField() #Player Level (Terminale S, MPSI, MedecineP1...)
	#~ #school = models.CharField() #OneToOne avec Lycee? 
	#~ #contributor = models.BooleanField() #0=NO 1=YES
	#~ # stats = ???
	#~ quizz = models.ManyToManyField(Quizz) #list of requested quizz : FIXME: MK: Not needed?


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

#FIX ME
#FIX ME LTB: Should we put the id of the correct answer instead of the boolean fiels validity in the answer model ??? 
#FIX ME MK: Nope? It is easier to do tests with booleans?

class Question(models.Model):
	level = models.ForeignKey(Level)
	subject = models.ForeignKey(Subject)
	chapter = models.ForeignKey(Chapter)
	pub_date = models.DateTimeField('date published')
	
	question = models.CharField(max_length = 2000)
	
	def __unicode__ (self):
		return self.question

class Quizz(models.Model):
	user = models.ForeignKey(User)
	date_started = models.DateTimeField('date started')
	questions = models.ManyToManyField(Question)
	level = models.ForeignKey(Level, null = True)
	subject = models.ForeignKey(Subject, null = True)
	chapter = models.ForeignKey(Chapter, null = True)
	grade = models.IntegerField(default = 0)

	@classmethod
	def new(cls,use, chap, subj, lev, number = 10):
		struct=time.localtime()
		level = Level.objects.filter(pk = lev)[0]
		subject = Subject.objects.filter(pk = subj)[0]
		chapter = Chapter.objects.filter(pk = chap)[0]
		quizz=cls(user = use, level = level, subject = subject, chapter = chapter, date_started = datetime.fromtimestamp(mktime(struct)))
		return quizz
		
	def append(self, number = 10): #choppe les number questions au hasard dans la bdd question telles que les chapter subjects etc sont ok
		question_list = Question.objects.all().filter(chapter = self.chapter, subject = self.subject,level = self.level)
		newlist = []
		for question in question_list:
			newlist.append(question)
		random.shuffle(newlist)
		newlist = newlist[0:int(number)]
		for question in newlist:
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
	