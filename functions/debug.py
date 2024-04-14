
import store_aed_data

def main():
    #テストデータ
    TEST_LAT = 35.96
    TEST_LNG = 136.185
    TEST_R = 300
    
    #AEDデータ取得
    featch_aed_json = store_aed_data.fetch_aed_data(TEST_LAT, TEST_LNG, TEST_R)
    
    #データをDataFrameに変換
    store_aed_pandas = store_aed_data.aed_data_to_pandas(featch_aed_json)
    
    print(store_aed_pandas)

if __name__ == "__main__":
    main()