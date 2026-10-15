# Chelsea Calendar

Chelsea FCの試合予定を取得し、カレンダーアプリで購読できるICSファイルを生成します。GitHub Actionsで毎時更新し、GitHub Pagesで公開する構成です。

## カレンダーを購読する

カレンダーアプリの「URLで追加」「照会カレンダー」などの機能に、公開先のICS URLを登録してください。このリポジトリを標準のGitHub Pages URLで公開した場合、URLは次のとおりです。

```text
https://fcf-kando.github.io/chelsea-calendar/chelsea.ics
```

実際の公開先は、GitHub Actionsのデプロイ結果またはリポジトリの **Settings → Pages** で確認できます。

継続して予定を反映するには、ファイルの一度きりのインポートではなくURLで購読してください。反映のタイミングは、利用するカレンダーアプリの更新間隔に依存します。

## 登録される試合情報

- 対戦カード：`⚽ ホームチーム vs アウェイチーム`
- 開始日時と、開始から2時間後の終了日時
- 大会名と節番号（節番号がある場合）
- 会場（取得できる場合）

Premier Leagueの現在のシーズンから開始年を取得し、その年を指定してfootball-data.orgのChelsea（チームID: `61`）の試合一覧を取得します。対象はAPIから返される試合で、大会や試合ステータスによる絞り込みは行いません。

日時はUTCで出力し、カレンダーのタイムゾーン情報は`Asia/Tokyo`に設定しています。表示時刻はカレンダーアプリの設定に従います。会場がないPremier Leagueの試合は、ホームチームの本拠地で補完します。他大会では、中立地開催を誤って補完しないよう、この処理を行いません。

## ローカルでICSを生成する

Python 3.11以降と、football-data.orgのAPIキーを用意してください。依存ライブラリは`requests`です。

リポジトリのルートで、次のコマンドを実行します。

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
$env:FOOTBALL_DATA_API_KEY = "YOUR_API_KEY"
.\.venv\Scripts\python.exe main.py
```

macOS / Linuxの場合：

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
export FOOTBALL_DATA_API_KEY="YOUR_API_KEY"
.venv/bin/python main.py
```

実行すると、カレントディレクトリの`chelsea.ics`を生成・上書きし、イベント数を表示します。APIキーが未設定の場合や、APIへのリクエストがHTTPエラーになった場合は処理を終了します。

## GitHub Actionsで自動更新する

1. リポジトリの **Settings → Secrets and variables → Actions** に、`FOOTBALL_DATA_API_KEY`という名前でAPIキーを登録します。
2. **Settings → Pages → Build and deployment → Source** で **GitHub Actions** を選びます。
3. **Actions → Update Chelsea Calendar → Run workflow** から手動実行し、デプロイ結果を確認します。

以後は[更新ワークフロー](.github/workflows/update.yml)が毎時20分（UTC）に実行されます。日本時間でも毎時20分です。スケジュール実行はGitHub Actionsの状況により遅れる場合があります。

ワークフローはICSを生成し、GitHub Pagesへデプロイします。生成ファイルをリポジトリへコミットする処理はありません。フォークして利用する場合は、自分の公開先に合わせて購読URLを変更してください。

## ファイル構成

| ファイル | 役割 |
| --- | --- |
| [main.py](main.py) | APIからシーズン・試合・会場情報を取得し、ICS生成を呼び出す |
| [ics_generator.py](ics_generator.py) | 試合データをイベントへ変換し、ICS形式で出力する |
| [requirements.txt](requirements.txt) | Pythonの依存ライブラリ |
| [.github/workflows/update.yml](.github/workflows/update.yml) | 定期実行とGitHub Pagesへのデプロイ |

チームを変更する場合は`main.py`の`TEAM_ID`、シーズンの取得元を変更する場合は`COMPETITION_CODE`を編集します。`COMPETITION_CODE`は試合一覧の大会を絞り込む設定ではありません。
