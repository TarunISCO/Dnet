from django import forms


class TitleFormatForm(forms.ModelForm):
    class Media:
        js = ('title-format-field.js', )
