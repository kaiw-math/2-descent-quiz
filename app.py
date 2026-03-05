import streamlit as st
import random
import json
import os

# --- 1. 外部JSONファイルからデータを読み込む ---
def load_data():
    # app.pyと同じ階層にあるcurves.jsonを探す
    json_path = os.path.join(os.path.dirname(__file__), "curves.json")
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)

curves = load_data()

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
    
    # LMFDBへのリンク
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
