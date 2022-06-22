from django import forms


class ScrapingForm(forms.Form):
    jumlah_data = forms.CharField()
