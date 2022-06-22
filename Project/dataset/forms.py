from django import forms


class DatasetFileForm(forms.Form):
    file_dataset = forms.FileField()
