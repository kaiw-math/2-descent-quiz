import streamlit as st
import requests
import random

# --- LMFDBから条件に合う曲線をランダムに取得する関数 ---
def get_random_curve():
    # 検索条件: 
    # rank: 0, 1, 2
    # torsion_structure: [2] または [2, 2] (2次ねじれを持つもの)
    # conductor: 1000以下 (計算が重くなりすぎないように)
    # random=true: ランダムに1件取得
    url = "https://www.lmfdb.org/api/ec_curves/?rank=0,1,2&torsion_structure=[2]&conductor=1-1000&_format=json&_sample=1"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data['data']:
                item = data['data'][0]
                return {
                    "label": item['label'],
                    "eq": item['equation'],
                    "rank": item['rank'],
                    "url": f"https://www.lmfdb.org/EllipticCurve/Q/{item['label'].replace('.','/')}"
                }
    except Exception as e:
        st.error(f"APIエラー: {e}")
    return None

st.set_page_config(page_title="2-Descent Random Challenge", page_icon="🎲")

st.title("🎲 2-Descent Random Challenge")
st.write("LMFDBからランク2以下の曲線をランダムに取得します。")

# セッション状態で問題を管理
if 'current_curve' not in st.session_state:
    st.session_state.current_curve = None
    st.session_state.answered = False

# 「新しい問題を出す」ボタン
if st.button("新しい問題を生成") or st.session_state.current_curve is None:
    with st.spinner("LMFDBから抽出中..."):
        st.session_state.current_curve = get_random_curve()
        st.session_state.answered = False

if st.session_state.current_curve:
    curve = st.session_state.current_curve
    
    st.info(f"**Cremona Label: {curve['label']}**")
    st.latex(curve['eq'])
    
    st.divider()
    
    # 回答エリア
    user_rank = st.radio("この曲線のランク $r$ は？", [0, 1, 2], horizontal=True)
    
    if st.button("回答をチェック"):
        st.session_state.answered = True
        
    if st.session_state.answered:
        if user_rank == curve['rank']:
            st.success(f"正解！ ランクは **{curve['rank']}** です。")
            st.balloons()
        else:
            st.error(f"残念！ 正解は **{curve['rank']}** でした。")
        
        st.markdown(f"[LMFDBで詳細な計算結果を見る]({curve['url']})")
