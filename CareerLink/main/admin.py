# admin.py

from django.contrib import admin
from .models import *


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]


admin.site.register(Specialization)
admin.site.register(Candidate)
admin.site.register(Question, QuestionAdmin)
admin.site.register(ContactRequest)
