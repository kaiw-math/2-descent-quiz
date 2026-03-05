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
    except Exception as e:
        st.error(f"JSON読み込みエラー: {e}")
        st.stop()

# --- 数式を美しく整形する関数 ---
def format_equation(a, b):
    # y^2 = x^3 からスタート
    eq = "y^2 = x^3"
    
    # x^2 の項 (a)
    if a != 0:
        sign = "+" if a > 0 else "-"
        val = abs(a)
        coeff = "" if val == 1 else val
        eq += f" {sign} {coeff}x^2"
    
    # x の項 (b)
    if b != 0:
        sign = "+" if b > 0 else "-"
        val = abs(b)
        coeff = "" if val == 1 else val
        eq += f" {sign} {coeff}x"
        
    return eq

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

# --- アプリ起動 ---
curves = load_data()

st.set_page_config(page_title="2-Descent Trainer", layout="wide")
st.title("🛡️ Elliptic Curve 2-Descent Trainer")

if 'current_label' not in st.session_state:
    st.session_state.current_label = random.choice(list(curves.keys()))
    st.session_state.answered = False

label = st.session_state.current_label
# a, b, rank の3つだけを取り出す
a, b, true_rank = curves[label]

# 数式を整形
pretty_eq = format_equation(a, b)

col1, col2 = st.columns([3, 1])
with col1:
    st.subheader(f"Target Curve: {label}")
    st.latex(pretty_eq) # ここで整形された数式を表示

with col2:
    st.markdown("##### 🔍 悪い素数 (要調査)")
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
    
    # LMFDBリンクの生成
    lmfdb_url = f"https://www.lmfdb.org/EllipticCurve/Q/{label.replace('a', '/a/').replace('b', '/b/').replace('c', '/c/').replace('d', '/d/').replace('t', '/t/').replace('v', '/v/').replace('o', '/o/').replace('h', '/h/').replace('i', '/i/').replace('f', '/f/')}"
    st.markdown(f"🔗 [LMFDBで詳細を確認する]({lmfdb_url})")
    
    if st.button("次の問題へ"):
        st.session_state.current_label = random.choice(list(curves.keys()))
        st.session_state.answered = False
        st.rerun()
