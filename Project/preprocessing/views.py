from django.shortcuts import render

from dataset.models import DataTesting, DataTraining


def data_training(request):
    return render(request, 'preprocessing/data_training.html', {
        'dataTraining': DataTraining.objects.all()
    })


def data_testing(request):
    return render(request, 'preprocessing/data_testing.html', {
        'dataTesting': DataTesting.objects.all()
    })
