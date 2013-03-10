from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'selection/$', 'QCM.views.question_selection', name = 'QCM_selection'),
    url(r'start/$', 'QCM.views.start_quizz', name = 'QCM_start_quizz'),
    url(r'end/$', 'QCM.views.end_quizz', name = 'QCM_end_quizz'),

    #FIX ME : User profile can not be in the question app
    url(r'account/$', 'QCM.views.display_user_profile', name = 'user_profile'),

)

