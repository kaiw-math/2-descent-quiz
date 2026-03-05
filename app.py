import streamlit as st
import random

# --- 正確なデータセット (LMFDB対応版) ---
curves = {
    # "Label": [a, b, rank, "Equation String"]
    "32.a3": [0, -1, 0, "y^2 = x^3 - x"],
    "64.a4": [0, 1, 0, "y^2 = x^3 + x"],
    "80.a3": [0, -5, 1, "y^2 = x^3 - 5x"],
    "96.b3": [0, -4, 0, "y^2 = x^3 - 4x"],
    "120.a2": [1, -6, 1, "y^2 = x^3 + x^2 - 6x"],
    "128.a1": [0, 2, 0, "y^2 = x^3 + 2x"],
    "144.a2": [0, -9, 0, "y^2 = x^3 - 9x"],
    "192.a3": [0, 3, 0, "y^2 = x^3 + 3x"],
    "242.b3": [11, 22, 0, "y^2 = x^3 + 11x^2 + 22x"],
    "288.d2": [0, -17, 2, "y^2 = x^3 - 17x"],
    "400.d3": [0, -25, 1, "y^2 = x^3 - 25x"],
    "512.i2": [0, -8, 1, "y^2 = x^3 - 8x"],
    "576.c5": [0, 36, 0, "y^2 = x^3 + 36x"],
    "720.j3": [0, -45, 1, "y^2 = x^3 - 45x"],
    "960.d1": [-1, -6, 1, "y^2 = x^3 - x^2 - x"],
}

# --- 補助関数 ---
def get_prime_divisors(n):
    n = abs(int(n))
    primes = set()
    if n == 0: return primes
    d = 2
    temp = n
    while d * d <= temp:
        while temp % d == 0:
            primes.add(d); temp //= d
        d += 1
    if temp > 1: primes.add(temp)
    return primes

def get_bad_primes(a, b):
    primes = {2}
    primes.update(get_prime_divisors(b))
    primes.update(get_prime_divisors(a**2 - 4*b))
    return sorted(list(primes))

# --- UI設定 ---
st.set_page_config(page_title="2-Descent Applet", layout="wide")
st.title("🛡️ Elliptic Curve 2-Descent Trainer")

if 'current_label' not in st.session_state:
    st.session_state.current_label = random.choice(list(curves.keys()))
    st.session_state.answered = False

label = st.session_state.current_label
# ここでリストから4つの要素を順番に取り出しています
a, b, true_rank, eq_text = curves[label]

col1, col2 = st.columns([3, 1])
with col1:
    st.subheader(f"Target: {label}")
    # 方程式はデータに入れた正確な文字列をそのまま表示
    st.latex(eq_text)

with col2:
    st.markdown("##### 🔍 悪い素数 (調査対象)")
    bad_primes = get_bad_primes(a, b)
    primes_str = " ".join([f"`p={p}`" for p in bad_primes] + ["`p=∞`"])
    st.write(primes_str)

st.divider()

user_rank = st.radio("推定ランクを選んでください:", [0, 1, 2], horizontal=True)

if st.button("回答チェック！"):
    st.session_state.answered = True

if st.session_state.answered:
    if user_rank == true_rank:
        st.success(f"正解！ランクは {true_rank} です。素晴らしい洞察力！")
        st.balloons()
    else:
        st.error(f"惜しい！正解は {true_rank} でした。")
    
    if st.button("次の曲線に挑む"):
        st.session_state.current_label = random.choice(list(curves.keys()))
        st.session_state.answered = False
        st.rerun()
