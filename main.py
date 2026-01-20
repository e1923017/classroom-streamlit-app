
import streamlit as st
import pandas as pd

CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRmjJQCY8tTaIYkXaK90sgZCnaZE-vvsfGEfg4_o1VFl1dpnSp3yl5g1z2-PCfqzk6vNm6tzYen3fC4/pub?output=csv"

st.set_page_config(page_title="空き状況確認", layout="wide")
st.title("空き状況確認アプリ")

# 10秒ごとに更新
st.autorefresh(interval=10 * 1000, key="refresh")

# 履歴保存用（Streamlit側）
if "history" not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=["時間", "人数"])

# 最新データ取得
df = pd.read_csv(CSV_URL)

latest_people = df.loc[0, "人数"]
latest_time = pd.to_datetime(df.loc[0, "時間"])

# 履歴に追加（同じ時刻は重複防止）
if (
    len(st.session_state.history) == 0
    or st.session_state.history.iloc[-1]["時間"] != latest_time
):
    st.session_state.history.loc[len(st.session_state.history)] = [
        latest_time,
        latest_people,
    ]

# ===== 表示 =====

st.metric("現在の人数", latest_people)

st.subheader("過去の人数推移")
st.line_chart(
    st.session_state.history.set_index("時間")["人数"]
)

st.subheader("ログ")
st.dataframe(st.session_state.history)
