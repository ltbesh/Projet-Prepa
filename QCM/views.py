from django.template import RequestContext
from django.http import HttpResponse
from QCM.models import Question
from random import randint
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
import datetime, random, sha
from django.shortcuts import render_to_response, get_object_or_404
from django.core.mail import send_mail
from QCM.models import UserProfile
#from QCM.forms import RegistrationForm

@login_required()
def index(request):
	return render_to_response('QCM/index.html',context_instance=RequestContext(request))

@login_required()
def qcm(request):
	questions = Question.objects.filter(subject = 'mathematique')
	number = randint(0,len(questions)-1)
	question = questions[number]
	return render_to_response('QCM/qcm.html', {'question' : question})

