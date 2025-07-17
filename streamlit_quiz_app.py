
import streamlit as st
import json
import random
import os
from collections import defaultdict

# 選擇考科
subject = st.selectbox("請選擇考科別：", ["中醫基礎一", "中醫基礎二"])

# 題目數設定
category_config = {
    "中醫基礎一": {
        "file": "CM-1.json",
        "title": "🧪 中醫一階模擬測驗-1",
        "categories": {
            "中藥學": 40,
            "方劑學": 40
        }
    },
    "中醫基礎二": {
        "file": "CM-2.json",
        "title": "🧪 中醫一階模擬測驗-2",
        "categories": {
            "內經": 40,
            "難經": 20,
            "中醫基礎理論": 10,
            "中醫醫學史": 10
        }
    }
}

st.title(category_config[subject]["title"])

# 載入題庫並依分類抽題
@st.cache_data
def load_questions_by_category(file_path, category_rule):
    with open(file_path, "r", encoding="utf-8") as f:
        all_questions = json.load(f)

    categorized = defaultdict(list)
    for q in all_questions:
        categorized[q["category"]].append(q)

    selected = []
    for cat, count in category_rule.items():
        questions = categorized.get(cat, [])
        if len(questions) < count:
            st.warning(f"⚠️ 類別「{cat}」題數不足，只抽到 {len(questions)} 題")
            count = len(questions)
        selected += random.sample(questions, count)
    
    random.shuffle(selected)
    return selected

# 初始化 session_state
if "questions" not in st.session_state:
    file_path = category_config[subject]["file"]
    category_rule = category_config[subject]["categories"]
    st.session_state.questions = load_questions_by_category(file_path, category_rule)
    st.session_state.used_indices = set()
    st.session_state.score = 0
    st.session_state.current_q = None
    st.session_state.submitted = False

# 顯示下一題
if st.button("▶️ 下一題"):
    remaining = list(set(range(len(st.session_state.questions))) - st.session_state.used_indices)
    if remaining:
        idx = random.choice(remaining)
        st.session_state.current_q = st.session_state.questions[idx]
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

# 顯示分數
total_done = len(st.session_state.used_indices)
st.info(f"目前得分：{st.session_state.score:.2f} / {total_done * 1.25:.2f} 分，共 {total_done} 題")

# 重設
if st.button("🔁 重新開始"):
    st.session_state.clear()
    st.success("✅ 已重設，請點選『下一題』開始測驗。")
