import datetime, sha, sys
from xlrd import open_workbook,XL_CELL_TEXT
from random import randint

from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from django.shortcuts import render_to_response, get_object_or_404, render, redirect
from django.db.models import Avg
from django.views.generic import CreateView, DetailView, UpdateView
from django.utils.decorators import method_decorator

from xlrd import open_workbook,XL_CELL_TEXT
from .models import UserProfile, Quizz, Question, Answer, Guess, News, Subject, Chapter, Level
from .forms import QuizzCreateForm

@login_required()
def index(request):
    news = News.objects.all().order_by('date_created')[0:10]
    return render_to_response('QCM/index.html', {'news' : news}, context_instance = RequestContext(request))  

class QuizzCreate(CreateView):
    """
    Creates a new quizz based on which subject / level / chapter the user choose on the form
    """
    model = Quizz        
    form_class = QuizzCreateForm

    def form_valid(self, form):
        quizz = form.save(commit = False)
        quizz.user = self.request.user
        quizz.save()
        quizz.add_question()
        return HttpResponseRedirect(quizz.get_absolute_url())

class QuestionAnswer(UpdateView):
    model = Guess

    def post(self, request, *args, **kwargs):
        guess = Guess.objects.get(pk = request.POST['guess'])
        quizz = guess.quizz
        answer = Answer.objects.get(pk = request.POST['answer'])
        guess.answer = answer
        guess.save()
        return HttpResponseRedirect(quizz.get_absolute_url())

class QuizzDisplay(DetailView):
    """
    Depending on the status of the quizz display an unanswered question or the results of the quizz
    """
    model = Quizz
    context_object_name = "quizz"

    def get(self, request, *args, **kwars):
        self.object = self.get_object()
        quizz = self.object
        if quizz.user != request.user:
            redirect('/')
        if quizz.is_finished():
            self.template_name = 'quizz_results.html'
        else:
            self.template_name = 'question_detail.html'
        context = self.get_context_data(object = self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(QuizzDisplay, self).get_context_data(**kwargs)
        self.object = self.get_object()
        quizz = self.object

        if quizz.finished:
            corrections = []
            guess_list = Guess.objects.filter(quizz = quizz)
            for guess in guess_list:
                corrections.append(guess.correction())
            context['corrections'] = corrections
        else:
            guess = quizz.get_unanswered_question()
            context['guess'] = guess
            question = guess.question
            context['question'] = question
            guess = Guess.objects.get(quizz = quizz, question = question)
            answers = Answer.objects.filter(question = question).order_by('?')
            context['answers'] = answers
        return context   

@login_required
def display_user_profile(request):

    quizz = Quizz.objects.filter(user = request.user).order_by('-date_started')
    form = QuizzCreateForm()

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

def import_questions(request):

    book = open_workbook('QCM/Capitales.xls')
    sheet = book.sheet_by_index(1)

    
    for i in range(sheet.nrows):
        question_cell = sheet.cell(i,0).value
        question = Question(question = question_cell)
        question.save()

        for j in range(4):
            good_answer_cell = sheet.cell(i,j + 1).value
            if j == 0:
                validity = True
            else:
                validity = False
            answer = Answer(answer = good_answer_cell, question = question, validity = validity)
            answer.save()

def geography(request):

    book = open_workbook('QCM/Capitales.xls')
    sheet = book.sheet_by_index(0)

    subject = Subject.objects.get_or_create(name = 'Geographie')[0]
    level = Level.objects.get_or_create(name = 'auto')[0]
    for i in range(sheet.nrows):
        #Capitale ! Pays ? 
        chapter = Chapter.objects.get_or_create(name = 'capitale-pays')[0]
        question_cell = sheet.cell(i,0).value
        question = Question(question = "Quel est le pays dont la capitale est : " + question_cell + " ?", subject = subject, chapter = chapter, level = level)
        question.save()
        good_answer_cell = sheet.cell(i, 1).value
        good_answer = Answer(answer = good_answer_cell, question = question, validity = True)
        good_answer.save()

        #Pays ! CApitale ? 
        chapter = Chapter.objects.get_or_create(name = 'pays-capitale')[0]
        question_cell = sheet.cell(i,1).value
        question1 = Question(question = "Quelle est la capitale de ce pays : " + question_cell + " ?", subject = subject, chapter = chapter, level = level)
        question1.save()
        good_answer_cell = sheet.cell(i, 0).value
        good_answer = Answer(answer = good_answer_cell, question = question1, validity = True)
        good_answer.save()

        #Pays ! Drapeau ? 
        chapter = Chapter.objects.get_or_create(name = 'pays-drapeau')[0]
        question_cell = sheet.cell(i,1).value
        question2 = Question(question = "Quel est le drapeau de ce pays : " + question_cell + " ?", subject = subject, chapter = chapter, level = level)
        question2.save()
        good_answer_cell = sheet.cell(i, 2).value
        good_answer = Answer(answer = good_answer_cell, question = question2, validity = True)
        good_answer.save()

        #Drapeau ! Pays ? 
        chapter = Chapter.objects.get_or_create(name = 'drapeau-pays')[0]
        question_cell = sheet.cell(i,2).value
        question3 = Question(question = "A quel pays appartient ce drapeau : " + question_cell + " ?", subject = subject, chapter = chapter, level = level)
        question3.save()
        good_answer_cell = sheet.cell(i, 1).value
        good_answer = Answer(answer = good_answer_cell, question = question3, validity = True)
        good_answer.save()

        for j in range(3):
            rand = i
            while rand == i:
                rand = randint(0, sheet.nrows - 1)
            bad_answer_cell = sheet.cell(rand, 1).value
            bad_answer = Answer(answer = bad_answer_cell, question = question, validity = False)
            bad_answer.save()

            bad_answer_cell = sheet.cell(rand, 0).value
            bad_answer = Answer(answer = bad_answer_cell, question = question1, validity = False)
            bad_answer.save()

            bad_answer_cell = sheet.cell(rand, 2).value
            bad_answer = Answer(answer = bad_answer_cell, question = question2, validity = False)
            bad_answer.save()

            bad_answer_cell = sheet.cell(rand, 1).value
            bad_answer = Answer(answer = bad_answer_cell, question = question3, validity = False)
            bad_answer.save()
