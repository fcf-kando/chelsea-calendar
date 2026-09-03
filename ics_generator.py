from datetime import datetime, timedelta, timezone

# ========================================
# ICS用データへ変換
# ========================================

def convert_match_to_event(match):
    """
    football-data.org の試合データを
    ICSイベント用のデータへ変換する
    """

    home_team = match["homeTeam"]["shortName"]
    away_team = match["awayTeam"]["shortName"]

    utc_date = datetime.fromisoformat(
        match["utcDate"].replace("Z", "+00:00")
    )

    # カレンダー上の試合時間は2時間とする
    end_date = utc_date + timedelta(hours=2)

    if match["matchday"] is not None:
        description = (
            f'{match["competition"]["name"]}\n'
            f'Matchday {match["matchday"]}'
        )
    else:
        description = match["competition"]["name"]

    return {
        "uid": f'{match["id"]}@chelsea-calendar',
        "dtstamp": datetime.now(timezone.utc),
        "dtstart": utc_date,
        "dtend": end_date,
        "summary": f"{home_team} vs {away_team}",
        "description": description,
        "status": "CONFIRMED",
        "sequence": 0,
    }


# ========================================
# ICS日時フォーマット
# ========================================

def format_ics_datetime(dt):
    """
    datetimeをICSのUTC日時形式へ変換する

    例:
    2027-05-30 15:00:00+00:00
    ↓
    20270530T150000Z
    """

    return dt.astimezone(timezone.utc).strftime(
        "%Y%m%dT%H%M%SZ"
    )


# ========================================
# ICS文字列エスケープ
# ========================================

def escape_ics_text(text):
    """
    ICSのTEXT値に使用できるようエスケープする
    """

    return (
        str(text)
        .replace("\\", "\\\\")
        .replace(";", "\\;")
        .replace(",", "\\,")
        .replace("\n", "\\n")
    )


# ========================================
# ICS文字列を生成
# ========================================

def create_ics(events):
    """
    ICSカレンダー全体を生成する
    """

    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Chelsea Calendar//EN",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        "X-WR-CALNAME:Chelsea Matches",
        "X-WR-CALDESC:Chelsea FC match schedule",
        "X-WR-TIMEZONE:Asia/Tokyo",
    ]

    for event in events:
        lines.extend([
            "BEGIN:VEVENT",
            f'UID:{escape_ics_text(event["uid"])}',
            f'DTSTAMP:{format_ics_datetime(event["dtstamp"])}',
            f'DTSTART:{format_ics_datetime(event["dtstart"])}',
            f'DTEND:{format_ics_datetime(event["dtend"])}',
            f'SUMMARY:{escape_ics_text(event["summary"])}',
            f'DESCRIPTION:{escape_ics_text(event["description"])}',
            f'STATUS:{event["status"]}',
            f'SEQUENCE:{event["sequence"]}',
            "END:VEVENT",
        ])

    lines.append("END:VCALENDAR")

    return "\r\n".join(lines) + "\r\n"


# ========================================
# ICSファイルを出力
# ========================================

def generate_ics(matches, output_file="chelsea.ics"):
    """
    試合データからICSファイルを生成する
    """

    events = [
        convert_match_to_event(match)
        for match in matches
    ]

    ics_content = create_ics(events)

    with open(
        output_file,
        "w",
        encoding="utf-8",
        newline=""
    ) as f:
        f.write(ics_content)

    print(f"{output_file} を作成しました。")
    print(f"イベント数: {len(events)}")