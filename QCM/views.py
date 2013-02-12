from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from QCM.models import Question
from random import randint
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
import datetime, random, sha
from django.shortcuts import render_to_response, get_object_or_404, render
from django.core.mail import send_mail
from QCM.models import UserProfile, Quizz
from QCM.forms import QuestionSelectionForm

@login_required()
def index(request):
	return render_to_response('QCM/index.html',context_instance=RequestContext(request))	

@login_required()
def user_profile(request):
	return render_to_response('QCM/index.html',context_instance=RequestContext(request))	

# Display the form for initializing MCQ so that user create its MCQ based on chosen options
@login_required()
def question_selection(request): 
    if request.method == 'POST': # If the form has been submitted...
        form = QuestionSelectionForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            quizz=Quizz.new(request.user)
            quizz.save()
            quizz.append(request.POST["chapter"],request.POST["subject"],request.POST["level"],2)
            quizz.save()
            return HttpResponseRedirect('question/start') # Redirect after POST
    else:
		form = QuestionSelectionForm()	
		return render_to_response('QCM/questionselection.html',{'form': form},context_instance=RequestContext(request))

    




#Create a quizz and redirect to the first question display view
@login_required()
def start_quizz(request):
	quizz=Quizz.objects.all()
	quizzlist=[]
	for quizzz in quizz:
		quizzlist.append(quizzz)
	quizz=quizzlist[0]
	return render_to_response('QCM/start_quizz.html',{'quizz':quizz},context_instance=RequestContext(request))
# Display one question and its choice so that the user can choose the right answer
@login_required()
def question_display(request):
    return

# Save the answer of the user then redirect to the next answer or to the result page
@login_required()
def question_answer(request):
    # Retrieve the user's answer in the POST array

    # Save the answer in the database

    # Compare the answer with the correct answer
    return

@login_required()
def display_quiz_results(request):
    return
    
@login_required()
def display_user_profile(request):
    return
