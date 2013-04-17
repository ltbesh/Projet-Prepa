from django.conf.urls import patterns, include, url
from views import QuizzCreate, QuestionAnswer, QuizzDisplay
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'quizz/create/$', QuizzCreate.as_view(), name = 'quizz_create'),
    url(r'quizz/(?P<pk>\d+)/$', QuizzDisplay.as_view(), name = 'quizz_display'),
    url(r'guess/update/$', QuestionAnswer.as_view(), name = 'question_answer'),

    url(r'import', 'QCM.views.geography'),
    #FIX ME : User profile can not be in the question app
    url(r'account/$', 'QCM.views.display_user_profile', name = 'user_profile'),
)

