import os
import requests
from ics_generator import generate_ics

# ========================================
# 設定
# ========================================


# 環境変数からAPIキーを取得
API_KEY = os.getenv("FOOTBALL_DATA_API_KEY")

if not API_KEY:
    raise ValueError(
        "環境変数 FOOTBALL_DATA_API_KEY が設定されていません。"
    )
TEAM_ID = 61
SEASON = 2502

# ========================================
# APIリクエスト
# ========================================

API_URL = f"https://api.football-data.org/v4/teams/{TEAM_ID}/matches"
headers = {
    "X-Auth-Token": API_KEY
}

params = {
    "season": SEASON
}

response = requests.get(
    API_URL,
    headers=headers,
    params=params
)

# HTTPエラーが発生した場合は例外を発生させる
response.raise_for_status()

# JSONをPythonの辞書として取得
data = response.json()

# # ========================================
# # 試合データを表示
# # ========================================

# for match in data["matches"]:
#     competition_code = match["competition"]["code"]
#     utc_date = match["utcDate"]

#     home_team = match["homeTeam"]["name"]
#     away_team = match["awayTeam"]["name"]

#     print(
#         f"{utc_date} | "
#         f"{competition_code} | "
#         f"{home_team} vs {away_team}"
#     )
#     from pprint import pprint
#     pprint(match)

# ========================================
# ICSを生成
# ========================================

generate_ics(data["matches"])