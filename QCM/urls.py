from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'selection/$', 'QCM.views.question_selection', name = 'selection'),
    url(r'start/$', 'QCM.views.start_quiz', name = 'start_quiz'),
    url(r'(?P<pk>\d+)$', 'QCM.views.question_display', name = 'question_display'),
    url(r'answer/(?P<pk>\d+)$', 'QCM.views.question_answer', name = 'question_answer'),
    url(r'quiz/results$', 'QCM.views.display_quiz_results', name = 'quiz_results'),

    #FIX ME : User profil can not be in the question app
    url(r'account/$', 'QCM.views.question_selection', name = 'user_profile'),

)
