
import streamlit as st
import pandas as pd

CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRmjJQCY8tTaIYkXaK90sgZCnaZE-vvsfGEfg4_o1VFl1dpnSp3yl5g1z2-PCfqzk6vNm6tzYen3fC4/pub?output=csv"

st.set_page_config(page_title="空き状況確認", layout="wide")
st.title("空き状況確認アプリ")

# =====================
# 履歴（最大10件）
# =====================
if "history" not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=["時間", "人数"])

# =====================
# 最新データ取得
# =====================
df = pd.read_csv(CSV_URL)

latest_people = pd.to_numeric(df.loc[0, "人数"], errors="coerce")

latest_time = pd.to_datetime(
    df.loc[0, "時間"],
    errors="coerce"
)

# 時刻が取れない場合は現在時刻
if pd.isna(latest_time):
    latest_time = pd.Timestamp.now()

# =====================
# 履歴に追加（重複防止）
# =====================
history = st.session_state.history

if (
    len(history) == 0
    or history.iloc[-1]["時間"] != latest_time
):
    history.loc[len(history)] = [latest_time, latest_people]

# 直近10件に制限
st.session_state.history = history.tail(10).reset_index(drop=True)

# =====================
# 表示
# =====================
st.metric("現在の人数", latest_people)

st.subheader("人数の推移")
st.line_chart(
    st.session_state.history.set_index("時間")["人数"]
)

st.subheader("ログ")
st.dataframe(st.session_state.history)
