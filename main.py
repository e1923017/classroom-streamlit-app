import streamlit as st
import pandas as pd

st.title("教室人数表示Webアプリ")

CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRmjJQCY8tTaIYkXaK90sgZCnaZE-vvsfGEfg4_o1VFl1dpnSp3yl5g1z2-PCfqzk6vNm6tzYen3fC4/pub?output=csv"

# スプレッドシート参照
df = pd.read_csv(CSV_URL)

# 教室選択（Webアプリ上）
room = st.selectbox("教室を選択してください", df["教室"])

# 人数取得（スプレッドシート参照）
count = df[df["教室"] == room]["人数"].values[0]

# Webアプリ上で表示
st.write(f"{room} の人数は {count} 人です")
