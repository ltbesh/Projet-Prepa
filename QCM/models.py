import datetime, random
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
	user = models.OneToOneField(User)
	activation_key = models.CharField(max_length = 40)
	key_expires = models.DateTimeField()

# Example : Mathematique, Physics, Chemistry ...
class Subject(models.Model):
	name = models.CharField(max_length = 200)

	def __unicode__ (self):
		return self.name

# Example : MPSI, PCSI ...
class Level(models.Model):
	name = models.CharField(max_length = 200)

	def __unicode__ (self):
		return self.name

# Example : Calculus, algebra ...
class Chapter(models.Model):
	name = models.CharField(max_length = 200) # name of the chapter : calculus, probability ...
	
	def __unicode__ (self):
		return self.name

# Questions that are to be answered by the students


#FIX ME
#FIX ME : Should we put the id of the correct answer instead of the boolean fiels validity in the answer model ???
#FIX ME
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
	questions=models.ManyToManyField(Question)
	
	@classmethod
	def new(self,chap,subj,lev,number=10): #choppe les number questions au hasard dans la bdd question telles que les chapter subjects etc sont ok
		question_list = Question.objects.all().filter(chapter=chap,subject=subj,level=lev)
		new_list=[]
		for question in question_list:
			new_list.append	(question)
		random.shuffle(new_list)
		new_list = new_list[1:number]
		self.save()
		for question in new_list:
			self.questions.add(question)
		self.save()
		
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



#class Temporary_Questions(models.Model): # inherit from question, has comments from admin and moderators in addition to questions fields
	


#class Tags(models.Model):
#	tag = models.CharField(max_length=15)
	
