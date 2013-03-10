from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from QCM.models import Question
from random import randint
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
import datetime, random, sha, sys
from django.shortcuts import render_to_response, get_object_or_404, render
from django.core.mail import send_mail
from QCM.models import UserProfile, Quizz, Question, Answer, Guess
from QCM.forms import QuestionSelectionForm
from django.db.models import Avg
from django.shortcuts import redirect



@login_required()
def index(request):
	return render_to_response('QCM/index.html', context_instance=RequestContext(request))	

# Display the form for initializing MCQ so that user create its MCQ based on chosen options
@login_required()
def question_selection(request): 
    if request.method == 'POST': # If the form has been submitted...
        form = QuestionSelectionForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            quizz = Quizz.new(request.user,request.POST["chapter"],request.POST["subject"],request.POST["level"])
            quizz.save()
            quizz.append()
            quizz.save()
            request.session['quizz']=quizz
            return HttpResponseRedirect('question/start') # Redirect after POST
    else:

		form = QuestionSelectionForm()	
		return render_to_response('QCM/questionselection.html',{'form': form},context_instance=RequestContext(request))


@login_required()
def start_quizz(request):
		
	if request.method == 'POST': 
	
		quizz = request.session['quizz']
		ans = request.POST["answer"]
		
		ans = Answer.objects.all().filter(answer=ans, question=request.session['question'])
		ans = ans[0]
		
		guess = Guess.new(quizz,ans) 
		guess.save()
		question_list=Question.objects.filter(quizz=quizz)
		guess_list=Guess.objects.filter(quizz=quizz)
		
		q_l=[]
		for q in question_list:
			q_l.append(q)
		question_list=q_l
		
		for g in guess_list:
			question_list.remove(g.answer.question)
		random.shuffle(question_list)
		
		try: 
			request.session['question']=question_list[0]
			answerlist=[]
			for answer in Answer.objects.filter(question = request.session['question']):
				answerlist.append(answer)
			random.shuffle(answerlist)
			return render_to_response('QCM/start_quizz.html',{'answers':answerlist, 'question':request.session['question']},context_instance = RequestContext(request))
			
		except:
			
			return HttpResponseRedirect('question/end')

	else:
		
		quizz = request.session['quizz']
		
		question_list=Question.objects.filter(quizz=quizz)
		guess_list=Guess.objects.filter(quizz=quizz)
		
		q_l=[]
		for q in question_list:
			q_l.append(q)
		question_list=q_l
		
		for g in guess_list:
			question_list.remove(g.answer.question)
		random.shuffle(question_list)
		
		try: 
			request.session['question']=question_list[0]
			answerlist=[]
			for answer in Answer.objects.filter(question = request.session['question']):
				answerlist.append(answer)
			random.shuffle(answerlist)
			return render_to_response('QCM/start_quizz.html',{'answers':answerlist, 'question':request.session['question']},context_instance = RequestContext(request))
			
		except:
			print sys.exc_info()
			return HttpResponseRedirect('question/end')

@login_required()
def end_quizz(request):
	q = request.session['quizz']
	guess_list = []
	guess = Guess.objects.filter(quizz = q)
	
	print guess
	note = 0
	liste = []
	
	for g in guess:
		liste2 = []
		guess_list.append(g)
		liste2.append(g.answer.question)
		liste2.append(g.answer)
		if g.answer.validity:
			note = note + 1
			liste2.append(g.answer)
		else:
			plop = Answer.objects.filter(question = g.answer.question, validity = 1)
			try:
				liste2.append(plop[0])
			except IndexError , e:
				liste2.append("Il n'y avait pas de bonne reponse")
				
		liste.append(liste2)

	try:
		note_finale = (note / float(len(guess_list))) * 20.0
		note_finale=round(note_finale, 1)
	except:
		pass
	q.grade = note_finale
	q.save()
	return render_to_response('QCM/end_quizz.html',{'note_finale' : note_finale, 'liste' : liste}, context_instance = RequestContext(request))

@login_required
def display_user_profile(request):

	quizz = Quizz.objects.filter(user = request.user)
	form = QuestionSelectionForm()

	if request.method == 'POST':
		if 'quizz_id' in request.POST:
			quizz = get_object_or_404(Quizz, pk = request.POST['quizz_id'])
			request.session['quizz'] = quizz
			return redirect('QCM_end_quizz')

		quizz = quizz.filter(
			level = request.POST['level'], 
			subject = request.POST['subject'], 
			chapter = request.POST['chapter'])
		form = QuestionSelectionForm(request.POST)

	grade = quizz.aggregate(Avg('grade'))["grade__avg"]

	return render_to_response('QCM/user_profile.html', {
		'form' : form,
		'quizz' : quizz,
		'grade' : grade
	}, context_instance = RequestContext(request))


