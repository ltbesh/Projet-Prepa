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
from QCM.forms import QuizzCreateForm
from django.db.models import Avg
from django.shortcuts import redirect
from django.views.generic import CreateView, DetailView, FormView
from django.utils.decorators import method_decorator

# Import excel
from xlrd import open_workbook,XL_CELL_TEXT

@login_required()
def index(request):
    news = News.objects.all().order_by('date_created')[0:10]
    return render_to_response('QCM/index.html', {'news' : news}, context_instance = RequestContext(request))  

# Create new quizz based on which subject / level / chapter the user choose
class QuizzCreate(CreateView):
    model = Quizz        
    form_class = QuizzCreateForm

    def form_valid(self, form):
        quizz = form.save(commit = False)
        quizz.user = self.request.user
        quizz.save()
        quizz.add_question()
        return HttpResponseRedirect(quizz.get_absolute_url())

class QuestionDisplay(DetailView):
    model = Question
    context_object_name = "question"

    def form_valid(self, form):
        # We store the guess and redirect to the same view
        print "form"
        question = get_object_or_404(Question, pk = request.POST['question'])
        answer = get_object_or_404(Answer,answer = request.POST['answer'], question = question)
        quizz = get_object_or_404(Quizz, pk = request.POST['quizz'])
        guess = Guess.new(quizz,answer) 
        guess.save()

        question_status = QuestionStatus.objects.get(question = question.id, quizz = quizz.id)
        question_status.answered = True
        question_status.save()
        return redirect('quizz_display', quizz.id)

    def get_context_data(self, **kwargs):
        print 'context'
        context = super(QuestionDisplay, self).get_context_data(**kwargs)
        context['answers'] = Answer.objects.filter(question = self.get_object()).order_by('?')
        return context

class QuizzDisplay(DetailView):
    """
    If the quizz is not finished, display an question not answered yet,
    otherwise display the results of the quizz
    """
    model = Quizz
    context_object_name = "quizz"

    def get_context_data(self, **kwargs):
        quizz = self.get_object()
        context = super(QuizzDisplay, self).get_context_data(**kwargs)
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

        context['question_list'] = question_list

        self.compute_grade(nb_correct_answer, float(len(guess_request)))

        return context

    def compute_grade(self, nb_correct_answer, nb_questions):
        quizz = self.get_object()
        try:
            grade = round((nb_correct_answer / nb_questions)) * 20.0
        except:
            grade = 0
        quizz.grade = grade
        quizz.save()     

    def get(self, request, *args, **kwargs):
        quizz = self.get_object()
        # If user does not own quizz
        if quizz.user != request.user:
            return redirect('index')
        if quizz.finished:
            return super(QuizzDisplay, self).get(self, request, *args, **kwargs)
        else:
            question = quizz.get_unanswered_question()
            if question :
                return redirect('question_display', question.pk)
            else :
                return redirect('quizz_display', quizz.id)
                
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

def geography(request, question_wording = 'De quel pays cette vile est elle la capitale : ', question_wording_backward = 'Quelle est la capitale  de ce pays : ', first_column = 0, second_column = 1):

    book = open_workbook('QCM/Capitales.xls')
    sheet = book.sheet_by_index(0)

    for i in range(sheet.nrows):
        question_cell = sheet.cell(i,first_column).value
        question = Question(question = question_wording + " " + question_cell + " ?")
        question.save()
        good_answer_cell = sheet.cell(i, second_column).value
        good_answer = Answer(answer = good_answer_cell, question = question, validity = True)
        good_answer.save()

        question_cell = sheet.cell(i,second_column).value
        question1 = Question(question = question_wording_backward + " " + question_cell + " ?")
        question1.save()
        good_answer_cell = sheet.cell(i, first_column).value
        good_answer = Answer(answer = good_answer_cell, question = question1, validity = True)
        good_answer.save()

        for j in range(3):
            rand = i
            while rand == i:
                rand = randint(0, sheet.nrows - 1)
            bad_answer_cell = sheet.cell(rand, second_column).value
            bad_answer = Answer(answer = bad_answer_cell, question = question, validity = False)
            bad_answer.save()

            bad_answer_cell = sheet.cell(rand, first_column).value
            bad_answer = Answer(answer = bad_answer_cell, question = question1, validity = False)
            bad_answer.save()




