from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse
from QCM.models import Question
from random import randint
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm


@login_required()
def index(request):
    return render_to_response('QCM/index.html',context_instance=RequestContext(request))

@login_required()
def qcm(request):
    questions = Question.objects.filter(subject = 'mathematique')
    number = randint(0,len(questions)-1)
    question = questions[number]
    return render_to_response('QCM/qcm.html', {'question' : question})

def register(request):
    if request.method =='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(form.cleaned_data['username'], None, form.cleaned_data['password1'])
            user.save()
            return render_to_response('QCM/index.html') # Redirect after POST
    else:
        form = UserCreationForm() # An unbound form

    return render_to_response('register.html', {
        'form': form,
    },context_instance=RequestContext(request))

