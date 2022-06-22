from django.shortcuts import render

from dataset.models import DetailKlasifikasi, HasilKlasifikasi


def index(request):
    return render(request, 'hasil_klasifikasi/index.html', {
        'hasilKlasifikasi': HasilKlasifikasi.objects.all(),
        'akurasi': DetailKlasifikasi.objects.first()
    })
