from django.shortcuts import render
from google_play_scraper import Sort, reviews
import random
import pandas as pd
import numpy as np
from scraping_dataset.forms import ScrapingForm
from io import BytesIO
from django.http import HttpResponse


def index(request):
    df_dataset = ''
    if request.method == 'POST':
        form = ScrapingForm(request.POST)
        if form.is_valid():
            with BytesIO() as b:
                with pd.ExcelWriter(b) as writer:
                    # jumlah data sesuai inputan
                    jumlahData = int(request.POST['jumlah_data'])
                    randomCount = random.randint(
                        jumlahData//3, jumlahData - (jumlahData//3))    # Untuk mengambil jumlah random antara ulasan positif dan negatif

                    resultPositive, continuation_token = reviews(        # Ulasan Positif
                        'id.tix.android',
                        lang='id',
                        country='id',
                        sort=Sort.MOST_RELEVANT,
                        count=randomCount,
                        filter_score_with=5
                    )
                    resultNegative, continuation_token = reviews(       # Ulasan Negatif
                        'id.tix.android',
                        lang='id',
                        country='id',
                        sort=Sort.MOST_RELEVANT,
                        count=jumlahData-randomCount,
                        filter_score_with=1
                    )

                    # Menggabungkan ulasan positif dan negatif
                    result = resultPositive + resultNegative
                    random.shuffle(result)      # Acak data

                    # Membuat dataframe dari variabel result
                    df_dataset = pd.DataFrame(
                        np.array(result), columns=['review'])
                    df_dataset = df_dataset.join(
                        pd.DataFrame(df_dataset.pop('review').tolist()))

                    # Membuat kolom label pada dataframe
                    df_dataset["label"] = ""

                    # Mengambil kolom userName, content, dan label pada dataframe dan export menjadi file excel
                    df_dataset[['userName', 'content', 'label']].to_excel(
                        writer, index=False)

                # Nama file excel
                filename = "dataset.xlsx"

                # Otomatis download file excel
                res = HttpResponse(b.getvalue(),  # Gives the Byte string of the Byte Buffer object
                                   content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                                   )
                res['Content-Disposition'] = f'attachment; filename={filename}'
                return res
    else:
        form = ScrapingForm()
    return render(request, 'scraping_dataset/index.html')
