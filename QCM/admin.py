from QCM.models import Question
from django.contrib import admin


class QuestionAdmin(admin.ModelAdmin):
	fieldsets =  [
		(None, {'fields' : ['question']}),
		('Good Answer',{'fields':['good_answer']}),
		('Bad Answers', {'fields' : ['bad_answer_1','bad_answer_2', 'bad_answer_3']}),
		('Information de date', {'fields' : ['pub_date']}),
		('Information de tag', {'fields' : ['class_level', 'subject', 'chapter']})

	]

	list_display = ('question', 'good_answer', 'bad_answer_1', 'bad_answer_2', 'bad_answer_3', 'pub_date', 'class_level', 'subject', 'chapter')

	list_filter = ['pub_date']

	search_fields = ['question']

	date_hierarchy = 'pub_date'

admin.site.register(Question, QuestionAdmin)

