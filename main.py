
import streamlit as st
import pandas as pd
import datetime
import random

# 追加　スプレッドシート
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRmjJQCY8tTaIYkXaK90sgZCnaZE-vvsfGEfg4_o1VFl1dpnSp3yl5g1z2-PCfqzk6vNm6tzYen3fC4/pub?output=csv"

st.set_page_config(page_title="空き状況確認", layout="wide")

st.title("空き状況確認アプリ")

# スプレッドシート参照
df = pd.read_csv(CSV_URL)

# 人数列取得空白除外
counts = df["人数"].dropna()

latest = counts.iloc[-1]

st.metric("現在の人数",latest)

time = df["時間"].dropna()



st.subheader("過去の人数推移")
st.line_chart(df.set_index("時間")["人数"])

st.subheader("ログ")
st.dataframe(df)
