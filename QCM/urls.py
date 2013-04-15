from django.conf.urls import patterns, include, url
from views import QuizzCreate, QuestionDisplay, QuizzDisplay
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'quizz/create/$', QuizzCreate.as_view(), name = 'quizz_create'),
    url(r'question/(?P<pk>\w+)/$', QuestionDisplay.as_view(), name = 'question_display'),
    url(r'quizz/(?P<pk>\w+)/$', QuizzDisplay.as_view(), name = 'quizz_display'),

    url(r'import', 'QCM.views.geography'),
    #FIX ME : User profile can not be in the question app
    url(r'account/$', 'QCM.views.display_user_profile', name = 'user_profile'),
)

