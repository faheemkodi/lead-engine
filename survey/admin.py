from django.contrib import admin

from .models import Lead, Survey, Question, Response, Answer


class ResponseInline(admin.TabularInline):
    model = Response


class AnswerInline(admin.TabularInline):
    model = Answer


class SurveyAdmin(admin.ModelAdmin):
    inlines = [ResponseInline]
    list_display = ("id", "lead", "response_count")

    def response_count(self, object):
        return object.survey_responses.count()

    response_count.short_description = "Response Count"


class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
    list_display = ("number", "type", "text")


admin.site.site_header = "Leads administration"

admin.site.register(Lead)
admin.site.register(Survey, SurveyAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Response)
admin.site.register(Answer)
