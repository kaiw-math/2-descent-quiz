import streamlit as st
import random

# --- 1. 正確なデータセット (LMFDB対応版・定数項0) ---
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

# --- 2. 補助関数 (素因数分解と悪い素数の抽出) ---
def get_prime_divisors(n):
    n = abs(int(n))
    primes = set()
    if n == 0: return primes
    d = 2
    temp = n
    while d * d <= temp:
        while temp % d == 0:
            primes.add(d)
            temp //= d
        d += 1
    if temp > 1:
        primes.add(temp)
    return primes

def get_bad_primes(a, b):
    primes = {2}
    primes.update(get_prime_divisors(b))
    primes.update(get_prime_divisors(a**2 - 4*b))
    return sorted(list(primes))

# --- 3. UI構築 ---
st.set_page_config(page_title="2-Descent Trainer", layout="wide")
st.title("🛡️ Elliptic Curve 2-Descent Trainer")

# セッション状態の保持
if 'current_label' not in st.session_state:
    st.session_state.current_label = random.choice(list(curves.keys()))
    st.session_state.answered = False

label = st.session_state.current_label
a, b, true_rank, eq_text = curves[label]

# 上部表示エリア
col1, col2 = st.columns([3, 1])
with col1:
    st.subheader(f"Target Curve: {label}")
    st.latex(eq_text)

with col2:
    st.markdown("##### 🔍 悪い素数 (要調査)")
    bad_primes = get_bad_primes(a, b)
    primes_str = " ".join([f"`p={p}`" for p in bad_primes] + ["`p=∞`"])
    st.write(primes_str)
    st.caption("※これら以外の素数では局所障害は起きません")

st.divider()

# 回答入力エリア
user_rank = st.radio("この曲線のランク r は？", [0, 1, 2], horizontal=True)

if st.button("回答チェック！"):
    st.session_state.answered = True

# 結果表示
if st.session_state.answered:
    if user_rank == true_rank:
        st.success(f"正解！ランクは {true_rank} です。")
        st.balloons()
    else:
        st.error(f"残念！正解は {true_rank} でした。")
    
    # LMFDBへのリンク（ベタ打ち対応）
    lmfdb_url = f"https://www.lmfdb.org/EllipticCurve/Q/{label.replace('.', '/')}"
    st.markdown(f"🔗 [LMFDBで詳細を確認する]({lmfdb_url})")
    
    st.write("---")
    if st.button("次の問題へ"):
        st.session_state.current_label = random.choice(list(curves.keys()))
        st.session_state.answered = False
        st.rerun()

# サイドバーのヒント
with st.sidebar:
    st.header("📖 2-Descent Mini Guide")
    st.write("2-isogeny降下法の基本公式:")
    st.latex(r"\bar{a} = -2a")
    st.latex(r"\bar{b} = a^2 - 4b")
    st.write("ランク計算式:")
    st.latex(r"2^{r+2} = |Im(\delta)| \cdot |Im(\bar{\delta})|")
