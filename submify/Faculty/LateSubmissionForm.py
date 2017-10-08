from django import forms
from Faculty.models import Submission


class LateSubmissionForm(forms.ModelForm):

    class Meta:
        model = Submission
        exclude = ['startDate', 'hashString']

    class Media:
        js = ('late-submission-field.js', )
