from django.core import validators
from django.contrib.auth.models import User
from QCM.models import Subject, Level, Chapter
from django import forms

class QuestionSelectionForm(forms.Form):

	subject = forms.ChoiceField(
		choices = Subject.objects.all().values_list(),
		)
	level = forms.ChoiceField(
		choices = Level.objects.all().values_list(),
		)	
	chapter = forms.ChoiceField(
		choices = Chapter.objects.all().values_list(),
		)
