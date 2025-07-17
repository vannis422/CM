
import streamlit as st
import json
import random

# 載入題庫
with open("C:/Users/user/Desktop/CM/parsed_10_questions.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

# 顯示標題
st.title("🧪 中醫一階模擬測驗")
st.markdown("固定出題：80 題，每題 1.25 分，共 100 分。")

# 初始化 session state
if "used_indices" not in st.session_state:
    st.session_state.used_indices = set()
if "score" not in st.session_state:
    st.session_state.score = 0
if "current_q" not in st.session_state:
    st.session_state.current_q = None
if "submitted" not in st.session_state:
    st.session_state.submitted = False

# 按鈕開始或繼續
if st.button("▶️ 下一題"):
    remaining = list(set(range(len(questions))) - st.session_state.used_indices)
    if remaining:
        idx = random.choice(remaining)
        st.session_state.current_q = questions[idx]
        st.session_state.used_indices.add(idx)
        st.session_state.submitted = False
    else:
        st.session_state.current_q = None
        st.success("✅ 所有題目作答完畢！")

# 顯示題目
q = st.session_state.current_q
if q:
    st.subheader(f"題目：{q['question']}")
    user_ans = st.radio("請選擇你的答案：", list(q["options"].keys()), format_func=lambda k: f"{k}. {q['options'][k]}")
    if st.button("提交答案") and not st.session_state.submitted:
        if user_ans == q["answer"]:
            st.success("✅ 正確！")
            st.session_state.score += 1.25
        else:
            st.error(f"❌ 錯誤，正確答案是 {q['answer']}")
        st.session_state.submitted = True

# 顯示成績
total_done = len(st.session_state.used_indices)
st.info(f"目前得分：{st.session_state.score:.2f} / {total_done * 1.25:.2f} 分，共 {total_done} 題")

# 重新開始
if st.button("🔁 重新開始"):
    st.session_state.clear()
    st.success("✅ 已重設，請點選『下一題』開始測驗。")
