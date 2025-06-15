# kadai6-2.py
# 【使用したオープンデータ】
# 名称：科学技術研究調査（1999年）
# 概要：企業、大学、公的機関などの研究機関が行う研究活動の実態（支出額など）を把握するための統計。
# エンドポイント：https://api.e-stat.go.jp/rest/3.0/app/json/getStatsData
# 機能：統計表IDを指定して、該当するデータセットをJSON形式で取得。
# 使用方法：appidにe-Statで取得したアプリケーションIDを設定し、GETリクエストでデータを取得する。

import requests
import pandas as pd

APP_ID = "06996a9cfc48624133a5cfd17fe89448e6d13f7f"

# 統計表ID（科学技術研究調査）
STATS_DATA_ID = "0000130642"

# API URL 作成
url = (
    f"https://api.e-stat.go.jp/rest/3.0/app/json/getStatsData"
    f"?appId={APP_ID}&lang=J&statsDataId={STATS_DATA_ID}&metaGetFlg=Y&cntGetFlg=N"
)

# APIからデータ取得
response = requests.get(url)
data = response.json()

# データ部を抽出
values = data['GET_STATS_DATA']['STATISTICAL_DATA']['DATA_INF']['VALUE']

# 整形して表示
records = []
for item in values:
    records.append({
        "年次": item.get('@time', ''),
        "分類": item.get('@cat01', ''),
        "組織名": item.get('@area', ''),
        "金額（百万円）": item.get('$', '')
    })

df = pd.DataFrame(records)

# 結果を表示
print("【科学技術研究調査データ】")
print(df.head(20))  # 最初の20件を表示
