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
from QCM.models import UserProfile, Quizz, Question, Answer, Guess, News
from QCM.forms import QuestionSelectionForm
from django.db.models import Avg
from django.shortcuts import redirect



@login_required()
def index(request):
    news = News.objects.all().order_by('date_created')[0:10]
    return render_to_response('QCM/index.html', {'news' : news}, context_instance=RequestContext(request))  

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
            request.session['quizz'] = quizz
            return redirect('QCM_answer_question') # Redirect after POST
    else:
        form = QuestionSelectionForm()  
        return render_to_response('QCM/questionselection.html',{'form': form},context_instance=RequestContext(request))


@login_required()
def answer_question(request):
    
    quizz = request.session['quizz']

    if request.method == 'POST': 
        answer = get_object_or_404(Answer,answer = request.POST["answer"], question = request.session['question'])
        guess = Guess.new(quizz,answer) 
        guess.save()

    question_request = Question.objects.filter(quizz = quizz)
    guess_request = Guess.objects.filter(quizz = quizz)

    question_list = []
    for q in question_request:
        question_list.append(q)
    
    for g in guess_request:
        question_list.remove(g.answer.question)
    random.shuffle(question_list)

    try: 
        request.session['question'] = question_list[0]
    except:
        return redirect('QCM_end_quizz')

    answer_list = Answer.objects.filter(question = request.session['question']).order_by('?')
    
    return render_to_response('QCM/start_quizz.html',{
        'answers':answer_list, 
        'question':request.session['question']
        },context_instance = RequestContext(request))
            

@login_required()
def end_quizz(request):
    q = request.session['quizz']
    guess_list = []
    guess = Guess.objects.filter(quizz = q)
    
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
        note_finale = round(note_finale, 1)
    except:
        note_finale = 0
    q.grade = note_finale
    q.save()
    return render_to_response('QCM/end_quizz.html',{'note_finale' : note_finale, 'liste' : liste}, context_instance = RequestContext(request))

@login_required
def display_user_profile(request):

    quizz = Quizz.objects.filter(user = request.user).order_by('-date_started')
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


