from QCM.models import Question, Answer, Chapter, Subject, Level, Quizz, Guess, News

from django.contrib import admin


class AnswerInline(admin.StackedInline):
	model = Answer
	extra = 4
		
#~ class QuestionInline(admin.StackedInline):
	#~ model = Question
	#~ extra = 1


class QuestionAdmin(admin.ModelAdmin):	
	fieldsets = [
        (None,               {'fields': ['question', 'chapter', 'subject', 'level']}),
    ]
	list_display = ('question', 'get_chapter', 'get_subject', 'get_level')
	inlines = [AnswerInline]


admin.site.register(Question,QuestionAdmin)
admin.site.register(Answer)
admin.site.register(Chapter)
admin.site.register(Subject)
admin.site.register(Level)
admin.site.register(Quizz)
admin.site.register(Guess)
admin.site.register(News)
