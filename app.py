import streamlit as st
import json
from docx import Document
from io import BytesIO

# 앱 제목
st.title("🧪 랩 실습 교육 콘텐츠 자동 생성기")
st.markdown("실험을 선택하면 퀴즈와 보고서 템플릿이 자동으로 생성됩니다.")

# 실험 목록
experiment_list = ["STZ 주사액 제조", "PCR", "Cell culture", "Western blot"]
selected_exp = st.selectbox("🔬 실험을 선택하세요", experiment_list)

# 퀴즈 로딩
with open("data/quiz_data.json", "r", encoding="utf-8") as f:
    quiz_data = json.load(f)

st.subheader("📘 퀴즈")
quiz = quiz_data[selected_exp]

score = 0
user_answers = []

for idx, q in enumerate(quiz):
    st.markdown(f"**Q{idx + 1}. {q['question']}**")
    if q["type"] == "mcq":
        answer = st.radio(f"선택하세요", q["options"], key=idx)
    else:
        answer = st.text_input("답을 입력하세요", key=idx)
    user_answers.append(answer)

# 정답 확인
if st.button("✅ 정답 확인"):
    for idx, q in enumerate(quiz):
        if q["type"] == "mcq":
            correct = q["answer"]
            if user_answers[idx] == correct:
                score += 1
                st.success(f"Q{idx + 1} 정답!")
            else:
                st.error(f"Q{idx + 1} 오답 😢 (정답: {correct})")
        else:
            st.info(f"Q{idx + 1}는 주관식입니다. 직접 확인해보세요.")
    st.markdown(f"🎯 총 점수: **{score} / {len(quiz)}**")

# 보고서 다운로드
st.subheader("📄 보고서 템플릿 다운로드")
template_path = f"templates/{selected_exp.replace(' ', '')}_report_template.docx"

def load_docx(path):
    doc = Document(path)
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

docx_file = load_docx(template_path)
st.download_button(
    label="📥 보고서 템플릿 다운로드 (.docx)",
    data=docx_file,
    file_name=f"{selected_exp.replace(' ', '_')}_Report_Template.docx",
    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
)
