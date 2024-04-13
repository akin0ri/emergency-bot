from django.shortcuts import render
from django.http import HttpResponse

import featch_api
import store_date
import pandas as pd

def index(request):
    return HttpResponse("Hello World")

def test(request):
    # テストデータ
    TEST_LAT = 35.96
    TEST_LNG = 136.185
    TEST_R = 300

    # JSON形式でAED APIデータの情報を取得
    featch_aed_json = featch_api.FeatchApi(TEST_LAT, TEST_LNG, TEST_R).fetch_aed_date()

    # 取得したJSONデータをPandasのデータフレームに保存
    store_aed_pandas = store_date.StoreData(featch_aed_json).aed_data_to_pandas()
    
    # pandasのデータをテキストに変換
    text = ""
    for index, item in store_aed_pandas.iterrows():
        text = f"{text} {item['LocationName']}にAEDがあります。距離は{item['DIST']}Mです。https://maps.google.com/maps?ll={item['Lat']},{item['Lng']}"

    # リクエストメソッドがPOSTならばTEXTを返却しGETならHTMLを返す
    if request.method == "POST":
        # ここにLINE APIの処理を追記する

        return HttpResponse(f"OK {text}")
    else:
        return render(request, "index.html", {"text": text})
