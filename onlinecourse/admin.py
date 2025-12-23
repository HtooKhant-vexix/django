from django.contrib import admin
from .models import OnlineCourse, Lesson, Enrollment, Question, Choice, Submission

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 5

class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 5

class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 5

class OnlineCourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline, QuestionInline]
    list_display = ('title', 'pub_date')
    list_filter = ['pub_date']
    search_fields = ['title', 'description']

class LessonAdmin(admin.ModelAdmin):
    list_display = ['title']

class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ['content', 'course', 'grade']

admin.site.register(OnlineCourse, OnlineCourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Enrollment)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission)
