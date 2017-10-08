# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from Faculty.models import *

from Faculty.TitleFormatForm import TitleFormatForm
from Faculty.LateSubmissionForm import LateSubmissionForm


admin.site.register(FacultyModel)
admin.site.register(Course)


class TitleFormatAdmin(admin.ModelAdmin):
    form = TitleFormatForm


admin.site.register(TitleFormat, TitleFormatAdmin)


class LateSubmissionAdmin(admin.ModelAdmin):
    form = LateSubmissionForm


admin.site.register(Submission, LateSubmissionAdmin)

admin.site.register(Submit)