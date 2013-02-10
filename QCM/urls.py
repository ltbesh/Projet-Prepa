from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'selection/$', 'QCM.views.question_selection', name = 'QCM_selection'),
    url(r'start/$', 'QCM.views.start_quiz', name = 'QCM_start_quiz'),
    url(r'(?P<pk>\d+)$', 'QCM.views.question_display', name = 'QCM_question_display'),
    url(r'answer/(?P<pk>\d+)$', 'QCM.views.question_answer', name = 'QCM_question_answer'),
    url(r'quiz/results$', 'QCM.views.display_quiz_results', name = 'QCM_quiz_results'),

    #FIX ME : User profil can not be in the question app
    url(r'account/$', 'QCM.views.user_profile', name = 'user_profile'),

)

