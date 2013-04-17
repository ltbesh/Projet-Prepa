from django.core import validators
from django.contrib.auth.models import User
from QCM.models import Quizz
from django import forms

class QuizzCreateForm(forms.ModelForm):
	class Meta:
		model = Quizz
		fields = ('subject', 'level', 'chapter')