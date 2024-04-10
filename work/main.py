import featch_api
import store_date
import pandas as pd
import requests

def main():
    #テストデータ
    TEST_LAT = 35.96
    TEST_LNG = 136.185
    TEST_R = 300
    
    #AEDデータ取得
    featch_aed_json = featch_api.FeatchApi(TEST_LAT, TEST_LNG, TEST_R).fetch_aed_date()
    
    #データをDataFrameに変換
    store_aed_pandas = store_date.StoreData(featch_aed_json).aed_data_to_pandas()
    
    print(store_aed_pandas)

if __name__ == "__main__":
    main()
