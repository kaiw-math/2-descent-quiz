import streamlit as st
import random

# データセットにLMFDBの詳細情報を追加
curves = {
    "32.a3": {"eq": "y^2 = x^3 - x", "rank": 0, "url": "https://www.lmfdb.org/EllipticCurve/Q/32/a/3"},
    "64.a4": {"eq": "y^2 = x^3 + x", "rank": 0, "url": "https://www.lmfdb.org/EllipticCurve/Q/64/a/4"},
    "80.a3": {"eq": "y^2 = x^3 - 5x", "rank": 1, "url": "https://www.lmfdb.org/EllipticCurve/Q/80/a/3"},
    "288.d2": {"eq": "y^2 = x^3 - 17x", "rank": 2, "url": "https://www.lmfdb.org/EllipticCurve/Q/288/d/2"},
}

st.set_page_config(page_title="2-Descent Trainer", layout="centered")

st.title("📈 2-Descent Training App")

if 'label' not in st.session_state:
    st.session_state.label = random.choice(list(curves.keys()))
    st.session_state.answered = False

label = st.session_state.label
data = curves[label]

# メイン表示
st.markdown(f"### Target Curve: `{label}`")
st.latex(data['eq'])

# ユーザー回答
st.write("この曲線のランク $r$ を予測してください。")
cols = st.columns(3)
choices = [0, 1, 2]
user_choice = st.radio("選択してください:", choices, horizontal=True, label_visibility="collapsed")

if st.button("Check Answer", use_container_width=True):
    st.session_state.answered = True

if st.session_state.answered:
    if user_choice == data['rank']:
        st.success(f"正解！ ランクは {data['rank']} です。")
        st.balloons()
    else:
        st.error(f"残念。 正解は {data['rank']} でした。")
    
    # LMFDBへのリンク
    st.markdown(f"[LMFDBで詳細を確認する]({data['url']})")
    
    if st.button("Next Curve"):
        st.session_state.label = random.choice(list(curves.keys()))
        st.session_state.answered = False
        st.rerun()

st.sidebar.header("Help & Theory")
st.sidebar.markdown("""
2-降下法の手順:
1. $E$ の有理2次ねじれ点を $(0,0)$ へ移動
2. 双対曲線 $\\bar{E}$ を構成
3. $\\text{Im}(\\delta)$ と $\\text{Im}(\\bar{\\delta})$ のサイズを判定
""")