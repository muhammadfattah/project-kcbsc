from django.db import models
from django.db import connection


class Dataset(models.Model):
    class Meta:
        db_table = 'dataset'
    username = models.CharField(max_length=255)
    ulasan = models.CharField(max_length=2000)
    label = models.CharField(max_length=255)

    def truncate(self):
        cursor = connection.cursor()
        cursor.execute("TRUNCATE TABLE `" + 'dataset' + "`")


class DataTraining(models.Model):
    class Meta:
        db_table = 'data_training'
    username = models.CharField(max_length=255)
    ulasan_sebelum_preprocessing = models.CharField(max_length=2000)
    ulasan_setelah_preprocessing = models.CharField(max_length=2000)
    label = models.CharField(max_length=255)

    def truncate(self):
        cursor = connection.cursor()
        cursor.execute("TRUNCATE TABLE `" + 'data_training' + "`")


class DataTesting(models.Model):
    class Meta:
        db_table = 'data_testing'
    username = models.CharField(max_length=255)
    ulasan_sebelum_preprocessing = models.CharField(max_length=2000)
    ulasan_setelah_preprocessing = models.CharField(max_length=2000)
    label = models.CharField(max_length=255)

    def truncate(self):
        cursor = connection.cursor()
        cursor.execute("TRUNCATE TABLE `" + 'data_testing' + "`")


class HasilKlasifikasi(models.Model):
    class Meta:
        db_table = 'hasil_klasifikasi'
    username = models.CharField(max_length=255)
    ulasan = models.CharField(max_length=2000)
    prediksi = models.CharField(max_length=255)
    label = models.CharField(max_length=255)

    def truncate(self):
        cursor = connection.cursor()
        cursor.execute("TRUNCATE TABLE `" + 'hasil_klasifikasi' + "`")


class DetailKlasifikasi(models.Model):
    class Meta:
        db_table = 'detail_klasifikasi'
    skor_akurasi = models.CharField(max_length=255)

    def truncate(self):
        cursor = connection.cursor()
        cursor.execute("TRUNCATE TABLE `" + 'detail_klasifikasi' + "`")
