import streamlit as st
import random

# --- 2次ねじれを持つ曲線の厳選リスト ---
# [Label, Equation, Rank]
CURVE_LIST = [
    ["32.a3", "y^2 = x^3 - x", 0],
    ["64.a4", "y^2 = x^3 + x", 0],
    ["80.a3", "y^2 = x^3 - 5x", 1],
    ["288.d2", "y^2 = x^3 - 17x", 2],
    ["120.a2", "y^2 = x^3 + x^2 - 6x", 1],
    ["96.a1", "y^2 = x^3 + x^2 - 2x", 1],
    ["225.e1", "y^2 = x^3 - 25x", 0],
    ["100.a1", "y^2 = x^3 + x^2 - x", 0],
    ["196.a1", "y^2 = x^3 - 7x^2", 0],
    ["338.b1", "y^2 = x^3 + x^2 - 10x - 12", 1],
    ["400.c1", "y^2 = x^3 - x^2 - 4x + 4", 0],
    ["576.h1", "y^2 = x^3 - 6x^2 + 9x", 0],
    ["700.i1", "y^2 = x^3 + x^2 - 16x - 20", 1],
    ["841.a1", "y^2 + y = x^3 - x^2 - x", 1],
    ["900.g1", "y^2 = x^3 - 13x + 12", 1]
]

st.set_page_config(page_title="2-Descent Challenge", page_icon="🎲")

st.title("🎲 2-Descent Random Challenge")
st.write("2次ねじれを持つ曲線のランクを推定しましょう。")

# セッション状態で問題を管理
if 'curve' not in st.session_state:
    st.session_state.curve = random.choice(CURVE_LIST)
    st.session_state.answered = False

# 新しい問題ボタン
if st.button("新しい問題を生成"):
    st.session_state.curve = random.choice(CURVE_LIST)
    st.session_state.answered = False
    st.rerun()

curve = st.session_state.curve

# 表示
st.info(f"**Cremona Label: {curve[0]}**")
st.latex(curve[1])

st.divider()

# 回答
user_rank = st.radio("この曲線のランク $r$ は？", [0, 1, 2], horizontal=True)

if st.button("回答をチェック"):
    st.session_state.answered = True

if st.session_state.answered:
    # 修正箇所: user_rank と curve[2] を正しく比較
    if user_rank == curve[2]:
        st.success(f"正解！ ランクは **{curve[2]}** です。")
        st.balloons()
    else:
        st.error(f"残念！ 正解は **{curve[2]}** でした。")
    
    # LMFDBへのリンク
    url_label = curve[0].replace('.', '/')
    st.markdown(f"### [LMFDBで詳細を確認](https://www.lmfdb.org/EllipticCurve/Q/{url_label})")
    
    st.write("---")
    st.write("💡 **2-descentのヒント:**")
    st.write("この曲線の 2-torsion が $(0,0)$ にあると仮定して、双対曲線の係数 $\\bar{b} = a^2 - 4b$ を計算してみましょう。")
