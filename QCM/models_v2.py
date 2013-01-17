import datetime
from django.utils import timezone
from django.db import models

# Create your models here.

from django.db import models

class Questions(models.Model):
    reference=models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    creator=models.ForeignKey(Users)
    moderators=models.ForeignKey(Users)
    validator=models.ForeignKey(Admins) #admin qui valide le passage a la bdd live
    
    question = models.CharField(max_length=2000)
    good_answer = models.CharField(max_length=200)
    bad_answers_1 = models.CharField(max_length=200)
    bad_answer_2 = models.CharField(max_length=200)
    bad_answer_3 = models.CharField(max_length=200)
    tags=models.ForeignKey(Tags)
    
    chapitre=models.ForeignKey(Chapitres)
    failed = models.CharField(max_length=200) #pour calculer la difficulté-> à equilibrer avec le niveau de l'user?
    passed = models.CharField(max_length=200)


class Temporary_Questions(models.Model): ##pour stocker les questions qui n'ont pas encore été validées = copie de Questions(models.Model) + flag ={0,1}} 
	

class Chapitres(models.Models):
	matiere=models.CharField(max_length=1000) #Physique, Chime, Histoire ...
	sous_chapitre=models.TextField(null=TRUE, max_length=1000)
	niveau=models.CharField(max_length=1000) #la classe de l'éleve
	name=models.CharField(max_length=1000) #nom du chapitre: thermodynamique, revolution française ...
	

class Users(models.Model):
	alias=models.CharField(max_length=20)
	email=models.CharField(max_length=50)

class Tags(models.Model):
	tag=models.CharField(max_length=15)
	
