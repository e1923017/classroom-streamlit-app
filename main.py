
import streamlit as st
import pandas as pd

CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRmjJQCY8tTaIYkXaK90sgZCnaZE-vvsfGEfg4_o1VFl1dpnSp3yl5g1z2-PCfqzk6vNm6tzYen3fC4/pub?output=csv"

st.set_page_config(page_title="空き状況確認", layout="wide")
st.title("空き状況確認アプリ")

if "history" not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=["時間", "人数"])

df = pd.read_csv(CSV_URL)

# B列 → 人数
latest_people = pd.to_numeric(df.iloc[0, 1], errors="coerce")

# C列 → 時間
latest_time = pd.to_datetime(df.iloc[0, 2], errors="coerce")

if pd.isna(latest_time):
    latest_time = pd.Timestamp.now()

history = st.session_state.history

if len(history) == 0 or history.iloc[-1]["時間"] != latest_time:
    history.loc[len(history)] = [latest_time, latest_people]

st.session_state.history = history.tail(10).reset_index(drop=True)

st.metric("現在の人数", latest_people)

st.subheader("人数の推移")
st.line_chart(st.session_state.history.set_index("時間")["人数"])

st.subheader("ログ")
st.dataframe(st.session_state.history)
