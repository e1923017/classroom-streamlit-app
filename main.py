
import streamlit as st
import pandas as pd
import datetime
import random

# 追加　スプレッドシート参照
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRmjJQCY8tTaIYkXaK90sgZCnaZE-vvsfGEfg4_o1VFl1dpnSp3yl5g1z2-PCfqzk6vNm6tzYen3fC4/pub?output=csv"

st.set_page_config(page_title="空き状況確認", layout="wide")

st.title("空き状況確認アプリ")

#def load_data():
#    now = datetime.datetime.now()
#    data = {
#        "time": [now - datetime.timedelta(minutes=5*i) for i in range(10)][::-1],
#        "people": [random.randint(0, 30) for _ in range(10)]
#    }
#    return pd.DataFrame(data)

#df = load_data()

# スプレッドシート参照
df = pd.read_csv(CSV_URL)

# 人数取得（スプレッドシート参照）
count = df[df["教室"] == room]["人数"].values[0]

st.metric("現在の人数", {count}.iloc[-1])



st.subheader("過去の人数推移")
st.line_chart(df.set_index("time")["people"])

st.subheader("ログ")
st.dataframe(df)
