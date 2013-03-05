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
from QCM.models import UserProfile, Quizz, Question, Answer, Guess
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
            quizz.append(request.POST["chapter"],request.POST["subject"],request.POST["level"],request.POST["number"])
            quizz.save()
            return HttpResponseRedirect('question/start') # Redirect after POST
    else:

		form = QuestionSelectionForm()	
		return render_to_response('QCM/questionselection.html',{'form': form},context_instance=RequestContext(request))

question_list=[]
i=0
quizz=0

@login_required()
def start_quizz(request):

	def make_quizz():
		global i
		global question_list
		global quizz
		i=0
		quizz=Quizz.objects.all()
		quizzlist=[]
		for quizzz in quizz:
			quizzlist.append(quizzz)
		global quizz
		quizz=quizzlist[-1] # load the last quizz #FIXME: make the question_selection view pass the quizz instead of retrieving it this way to avoid DB mayhem?
		questions=quizz.questions.all()
		global question_list
		question_list=[]
		for question in questions:
			global question_list
			question_list.append(question)
		return question_list
		
	if request.method == 'POST': 
	
		ans=request.POST["answer"]		
		ans=Answer.objects.all().filter(question=question_list[i].id, answer=ans)
		ans = ans[0]

		guess=Guess.new(quizz,ans) #quizz & answer sont des foreignkey
		guess.save()
		
		global question_list
		global i
		if i<len(question_list)-1:
			global i
			i=i+1
			quest=question_list[i]
			answerlist=[]
			for answer in Answer.objects.all().filter(question=quest.id):
				answerlist.append(answer)
			random.shuffle(answerlist)
			
			return render_to_response('QCM/start_quizz.html',{'answers':answerlist, 'question':quest},context_instance=RequestContext(request))
			
		else:
			return HttpResponseRedirect('question/end')

	else:
		
		question_list=make_quizz()
		quest=question_list[0]
		answerlist=[]
		for answer in Answer.objects.all().filter(question=quest.id):
			answerlist.append(answer)
		
		random.shuffle(answerlist)
		
		return render_to_response('QCM/start_quizz.html',{'answers':answerlist, 'question':quest},context_instance=RequestContext(request))

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
def end_quizz(request):
	return render_to_response('QCM/end_quizz.html',context_instance=RequestContext(request))

@login_required()
def display_quiz_results(request):
    return
    
@login_required()
def display_user_profile(request):
    return
