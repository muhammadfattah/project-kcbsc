from django.shortcuts import render
from django.http import HttpResponseRedirect
from dataset.forms import DatasetFileForm
from dataset.models import DataTesting, DataTraining, Dataset, DetailKlasifikasi, HasilKlasifikasi

from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import model_selection
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import pandas as pd
import re
import string


def index(request):
    if request.method == 'POST':
        form = DatasetFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file_dataset'])
            return HttpResponseRedirect("dataset")
    else:
        form = DatasetFileForm()
    return render(request, 'dataset/index.html', {
        'dataset': Dataset.objects.all()
    })


def handle_uploaded_file(f):    # Fungsi handle upload file
    fileName = 'static/upload/'+f.name          # Nama file excel yang diupload

    # Membaca file excel dan dimasukkan ke dalam variabel df
    with open(fileName, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    # Sesuai nama file dan nama sheet
    df = pd.read_excel(fileName, 'Sheet1')

    # Mengosongkan semua table yang ada di database
    Dataset().truncate()
    DataTraining().truncate()
    DataTesting().truncate()
    HasilKlasifikasi().truncate()
    DetailKlasifikasi().truncate()

    # Menyimpan dataset sebelum preprocessing ke database
    for index in df['content'].keys():
        username = df['userName'].get(index)
        ulasan = df['content'].get(index)
        label = df['label'].get(index)
        Dataset(username=username, ulasan=ulasan, label=label).save()

    df_sebelum_preprocessing = df

    # Memanggil fungsi preprocessing untuk kolom ulasan di variabel df
    df['content'] = df['content'].apply(preprocess)

    # Memanggil fungsi modelling untuk membuat model
    Train_X, Test_X, SVM, Tfidf_vect, skor_akurasi = modelling(
        df)

    # Memasukkan data training ke database
    for index in Train_X.keys():
        username = df['userName'].get(index)
        ulasan_sebelum_preprocessing = df_sebelum_preprocessing['content'].get(
            index)
        ulasan_setelah_preprocessing = df['content'].get(index)
        label = df['label'].get(index)
        DataTraining(
            username=username,
            ulasan_sebelum_preprocessing=ulasan_sebelum_preprocessing, ulasan_setelah_preprocessing=ulasan_setelah_preprocessing,
            label=label).save()

    # Memasukkan data testing ke database
    for index in Test_X.keys():
        username = df['userName'].get(index)
        ulasan_sebelum_preprocessing = df_sebelum_preprocessing['content'].get(
            index)
        ulasan_setelah_preprocessing = df['content'].get(index)
        label = df['label'].get(index)
        DataTesting(
            username=username,
            ulasan_sebelum_preprocessing=ulasan_sebelum_preprocessing, ulasan_setelah_preprocessing=ulasan_setelah_preprocessing,
            label=label).save()

    # Memasukkan data hasil klasifikasi ke database
    for index in Test_X.keys():
        username = df['userName'].get(index)
        ulasan = df['content'].get(index)
        prediksi = classify(df['content'].get(index), SVM, Tfidf_vect)
        label = df['label'].get(index)
        HasilKlasifikasi(username=username, ulasan=ulasan,
                         prediksi=prediksi, label=label).save()

    # Memasukkan skor hasil klasifikasi ke database
    DetailKlasifikasi(skor_akurasi=skor_akurasi).save()


def preprocess(text):  # Fungsi text preprocessing
    # Membuat class untuk fungsi stemming
    stemFactory = StemmerFactory()
    stemmer = stemFactory.create_stemmer()

    # Membuat class untuk fungsi remove stopword
    stopwordFactory = StopWordRemoverFactory()
    stopword = stopwordFactory.create_stop_word_remover()

    teks = text.lower()   # Mengubah seluruh huruf menjadi huruf kecil

    teks = re.sub("\n", " ", teks)    # Menghapus \n

    # Menghapus url
    teks = re.sub(
        "((www\.[^\s]+)|(https?://[^\s]+)|(http?://[^\s]+))", " ", teks)

    teks = re.sub("\d+", " ", teks)   # Menghapus semua angka

    # Menghapus semua tanda baca
    for punc in string.punctuation:
        if punc in teks:
            teks.replace(punc, " ")

    teks = re.sub(" +", " ", teks)  # Menghapus spasi berlebih

    teks = teks.strip()  # Menghapus karakter kosong

    # Stemming (mengubah ke dalam bentuk kata dasar)
    teks = stemmer.stem(teks)

    teks = stopword.remove(teks)    # Remove Stopwords

    return teks


def modelling(df_dataset):  # Fungsi modelling
    # Membagi data menjadi data training dan data testing
    Train_X, Test_X, Train_Y, Test_Y = model_selection.train_test_split(
        df_dataset['content'], df_dataset['label'], test_size=0.2)

    Encoder = LabelEncoder()
    Train_Y_Encoded = Encoder.fit_transform(Train_Y)
    Test_Y_Encoded = Encoder.fit_transform(Test_Y)

    Tfidf_vect = TfidfVectorizer()
    Tfidf_vect.fit(df_dataset['content'])
    Train_X_Tfidf = Tfidf_vect.transform(Train_X)
    Test_X_Tfidf = Tfidf_vect.transform(Test_X)

    SVM = SVC()
    SVM.fit(Train_X_Tfidf, Train_Y_Encoded)
    prediction_SVM = SVM.predict(Test_X_Tfidf)
    skor_akurasi = accuracy_score(prediction_SVM, Test_Y_Encoded)*100

    return Train_X, Test_X, SVM, Tfidf_vect, skor_akurasi


def classify(text, SVM, Tfidf_vect):
    pred = SVM.predict(Tfidf_vect.transform([text]))
    if pred == 1:
        return "positif"
    else:
        return "negatif"
