from django.contrib import admin
from .models import Question, Answer, Branch


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'stream', 'created_at')
    list_filter = ('stream', 'created_at')
    search_fields = ('title', 'user__email', 'stream')
    date_hierarchy = 'created_at'
    readonly_fields = ('view_count',)
    filter_horizontal = ('answers',)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__email', 'question__title')
    date_hierarchy = 'created_at'


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_form')
    search_fields = ('name', 'short_form')
