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
from QCM.models import UserProfile, Quizz, Question, Answer, Guess, News, QuestionStatus
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
            return redirect('QCM_quizz', quizz.id) # Redirect after POST
    else:
        form = QuestionSelectionForm()  
        return render_to_response('QCM/questionselection.html',{'form': form},context_instance=RequestContext(request))


@login_required()
def display_quizz(request, id):

    quizz = get_object_or_404(Quizz, pk = id)

    # If user does not own quizz
    if quizz.user != request.user:
        # Mettre un redirect a la place
        return redirect('index')

    if request.method == 'POST':
        # We store the guess and redirect to the same view
        question = get_object_or_404(Question, pk = request.POST['question'])
        answer = get_object_or_404(Answer,answer = request.POST["answer"], question = question)
        guess = Guess.new(quizz,answer) 
        guess.save()

        question_status = QuestionStatus.objects.get(question = question.id, quizz = quizz.id)
        question_status.answered = True
        question_status.save()
        return redirect('QCM_quizz', quizz.id)

    else:
    # Test wether or not the quizz is finished
        if quizz.finished:
        # Compute the grade and save it, send question, guess and correct answers to the template
            guess_request = Guess.objects.filter(quizz = quizz)
            question_list = []
            nb_correct_answer = 0

            for guess in guess_request:
                if guess.answer.validity:
                    nb_correct_answer += 1
                    correct_answer = guess.answer
                else:
                    try:
                        correct_answer = Answer.objects.get(question = guess.answer.question, validity = 1)
                    except:
                        correct_answer = "Il n'y avait pas de bonne reponse"
                question_list.append((guess.answer.question, guess.answer, correct_answer))

            try:
                grade = round((nb_correct_answer / float(len(guess_request))) * 20.0)
            except:
                grade = 0
            quizz.grade = grade
            quizz.save()
            return render_to_response('QCM/end_quizz.html',{
                'grade' : grade, 
                'question_list' : question_list
                }, context_instance = RequestContext(request))
        else:
        # Retrieve a question that has not been answered yet and send it to the template
            try:
                question = Question.objects.filter(questionstatus__quizz = quizz.id, questionstatus__answered = False)[0]
            except:
                quizz.finished = True
                quizz.save()
                return redirect('QCM_quizz', quizz.id)

            answer_list = Answer.objects.filter(question = question).order_by('?')
            
            return render_to_response('QCM/start_quizz.html',{
                'answers':answer_list, 
                'question':question,
                'quizz':quizz
                },context_instance = RequestContext(request))
                
@login_required
def display_user_profile(request):

    quizz = Quizz.objects.filter(user = request.user).order_by('-date_started')
    form = QuestionSelectionForm()

    if request.method == 'POST':
        if 'quizz_id' in request.POST:
            return redirect('QCM_quizz', request.POST['quizz_id'])

        quizz = quizz.filter(
            level = request.POST['level'], 
            subject = request.POST['subject'], 
            chapter = request.POST['chapter'])
        form = QuestionSelectionForm(request.POST)
    try:
        grade = round (quizz.aggregate(Avg('grade'))["grade__avg"],1)
    except:
        grade = 0

    return render_to_response('QCM/user_profile.html', {
        'form' : form,
        'quizz' : quizz,
        'grade' : grade
    }, context_instance = RequestContext(request))