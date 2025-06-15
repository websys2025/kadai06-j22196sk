import requests
import pandas as pd

APP_ID = "06996a9cfc48624133a5cfd17fe89448e6d13f7f"
API_URL = "http://api.e-stat.go.jp/rest/3.0/app/json/getStatsData"

# データの種類：家計調査（家計収支編 二人以上の世帯 詳細結果表）
# 統計表ID：0003213667
# カテゴリコード：0600（通信費）
# エンドポイント：https://api.e-stat.go.jp/rest/3.0/app/json/getStats
# このプログラムは、全国の通信費に関する統計データを取得し、
# pandasのDataFrameに変換して整形後、コンソールに出力する

params = {
    "appId": APP_ID,
    "statsDataId": "0003109558",
    "lang": "J"  # 日本語を指定
}

response = requests.get(API_URL, params=params)
data = response.json()

# 統計データからデータ部取得
values = data['GET_STATS_DATA']['STATISTICAL_DATA']['DATA_INF']['VALUE']

# JSONからDataFrameを作成
df = pd.DataFrame(values)

# メタ情報取得
meta_info = data['GET_STATS_DATA']['STATISTICAL_DATA']['CLASS_INF']['CLASS_OBJ']

# 統計データのカテゴリ要素をID(数字の羅列)から、意味のある名称に変更する
for class_obj in meta_info:

    # メタ情報の「@id」の先頭に'@'を付与した文字列が、統計データの列名と対応している
    column_name = '@' + class_obj['@id']

    # 統計データの列名を「@code」から「@name」に置換するディクショナリを作成
    id_to_name_dict = {}
    if isinstance(class_obj['CLASS'], list):
        for obj in class_obj['CLASS']:
            id_to_name_dict[obj['@code']] = obj['@name']
    else:
        id_to_name_dict[class_obj['CLASS']['@code']] = class_obj['CLASS']['@name']

    # ディクショナリを用いて、指定した列の要素を置換
    df[column_name] = df[column_name].replace(id_to_name_dict)

# 統計データの列名を変換するためのディクショナリを作成
col_replace_dict = {'@unit': '単位', '$': '値'}
for class_obj in meta_info:
    org_col = '@' + class_obj['@id']
    new_col = class_obj['@name']
    col_replace_dict[org_col] = new_col

# ディクショナリに従って、列名を置換する
new_columns = []
for col in df.columns:
    if col in col_replace_dict:
        new_columns.append(col_replace_dict[col])
    else:
        new_columns.append(col)

df.columns = new_columns
print(df)