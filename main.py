
import streamlit as st
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
from datetime import datetime

# =====================
# Google Sheets 接続
# =====================
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

creds = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=SCOPES
)

client = gspread.authorize(creds)
sheet = client.open("PeopleLog").sheet1

# =====================
# Streamlit 設定
# =====================
st.set_page_config(page_title="空き状況確認", layout="wide")
st.title("空き状況確認アプリ")

# =====================
# Sheets から取得
# =====================
latest_people = sheet.acell("B2").value
latest_time = sheet.acell("C2").value

logs = sheet.get("B4:C13")  # 過去10件

# DataFrame化
log_df = pd.DataFrame(logs, columns=["人数", "時間"])

# =====================
# 表示
# =====================
st.subheader("最新情報")
st.metric("現在の人数", latest_people)
st.write(f"更新時刻：{latest_time}")

st.subheader("過去10件ログ")
st.dataframe(log_df)

st.subheader("人数推移")
st.line_chart(
    log_df.set_index("時間")["人数"].astype(float)
)

# =====================
# 更新処理
# =====================
def update_sheets(new_people):
    now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

    # 最新値を上書き
    sheet.update("B2", new_people)
    sheet.update("C2", now)

    # 既存ログ（9件）取得
    old_logs = sheet.get("B4:C12")

    # 新ログを先頭に追加
    new_logs = [[new_people, now]] + old_logs

    # 10件分書き戻し
    sheet.update("B4:C13", new_logs)

# =====================
# 更新UI
# =====================
st.subheader("人数更新")

new_people = st.number_input(
    "現在の人数を入力",
    min_value=0,
    step=1
)

if st.button("更新"):
    update_sheets(new_people)
    st.success("Google Sheets を更新しました")
    st.experimental_rerun()
