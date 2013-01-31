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
from QCM.forms import QuestionSelectionForm

@login_required()
def index(request):
    return render_to_response('QCM/index.html',context_instance=RequestContext(request))

# Display the form for initializing MCQ so that user create its MCQ based on chosen options
@login_required()
def question_selection(request): 
    form = QuestionSelectionForm()
    return render_to_response('QCM/questionselection.html',{'form': form})

#Create a quizz and redirect to the first question display view
@login_required()
def start_quiz(request):
    return
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
