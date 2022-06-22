"""Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from beranda import views as beranda
from scraping_dataset import views as scraping_dataset
from dataset import views as dataset
from preprocessing import views as preprocessing
from hasil_klasifikasi import views as hasil_klasifikasi

urlpatterns = [
    path('', beranda.index),
    path('scraping-dataset', scraping_dataset.index),
    path('dataset', dataset.index),
    path('data-training', preprocessing.data_training),
    path('data-testing', preprocessing.data_testing),
    path('hasil-klasifikasi', hasil_klasifikasi.index),
]
