import streamlit as st
import random
import json
import os

# --- データの読み込み ---
def load_data():
    json_path = os.path.join(os.path.dirname(__file__), "curves.json")
    if not os.path.exists(json_path):
        st.error(f"ファイルが見つかりません: {json_path}")
        st.stop()
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        st.error(f"JSONの形式が正しくありません。curves.jsonを確認してください。\nエラー内容: {e}")
        st.stop()

curves = load_data()

# --- 数論的な補助関数 ---
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

# --- アプリの表示 ---
st.set_page_config(page_title="2-Descent Trainer", layout="wide")
st.title("🛡️ Elliptic Curve 2-Descent Trainer")

if 'current_label' not in st.session_state:
    st.session_state.current_label = random.choice(list(curves.keys()))
    st.session_state.answered = False

label = st.session_state.current_label
a, b, true_rank, eq_text = curves[label]

col1, col2 = st.columns([3, 1])
with col1:
    st.subheader(f"Target Curve: {label}")
    st.latex(eq_text)

with col2:
    st.markdown("##### 🔍 悪い素数 (調査対象)")
    bad_primes = get_bad_primes(a, b)
    primes_str = " ".join([f"`p={p}`" for p in bad_primes] + ["`p=∞`"])
    st.write(primes_str)

st.divider()

user_rank = st.radio("この曲線のランク r は？", [0, 1, 2], horizontal=True)

if st.button("回答チェック！"):
    st.session_state.answered = True

if st.session_state.answered:
    if user_rank == true_rank:
        st.success(f"正解！ランクは {true_rank} です。")
        st.balloons()
    else:
        st.error(f"残念！正解は {true_rank} でした。")
    
    lmfdb_url = f"https://www.lmfdb.org/EllipticCurve/Q/{label.replace('a', '/a/').replace('b', '/b/').replace('c', '/c/').replace('d', '/d/').replace('t', '/t/').replace('v', '/v/').replace('o', '/o/').replace('h', '/h/').replace('i', '/i/').replace('f', '/f/')}"
    st.markdown(f"🔗 [LMFDBで詳細を確認する]({lmfdb_url})")
    
    if st.button("次の問題へ"):
        st.session_state.current_label = random.choice(list(curves.keys()))
        st.session_state.answered = False
        st.rerun()
