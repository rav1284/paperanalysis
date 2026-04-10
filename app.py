import streamlit as st
from utils.pdf_reader import extract_text
from utils.preprocess import preprocess
from utils.summarizer import summarize
from utils.qa_engine import answer_question
from utils.plagiarism import check_plagiarism
from utils.word2vec_engine import train_word2vec
from utils.ppt_generator import create_ppt
from utils.section_extractor import extract_sections
from utils.summarizer import summarize_text

st.set_page_config(page_title="Research Paper Assistant", layout="wide")

st.title("📚 Intelligent Research Paper Chatbot")

uploaded_file = st.file_uploader("Upload Research Paper (PDF)", type="pdf")

if uploaded_file:
    text = extract_text(uploaded_file)
    sentences, cleaned_sentences = preprocess(text)

    model = train_word2vec(sentences)

    st.success("PDF processed successfully!")

    if st.button("📄 Generate Summary"):
        sections = extract_sections(text)

        if not sections["abstract"]:
            st.warning("Abstract not found or empty")

        st.subheader("📌 Title")
        st.write(sections["title"])

        st.subheader("📄 Abstract Summary")
        st.write(summarize_text(sections.get("abstract", "")))

        st.subheader("📘 Introduction Summary")
        st.write(summarize_text(sections.get("introduction", "")))        

        st.subheader("✅ Conclusion")
        st.write(summarize_text(sections.get("conclusion", "")))        

        st.session_state["summary"] = {
            "title": sections["title"],
            "abstract": sections["abstract"],
            "introduction": sections["introduction"],
            "conclusion": sections["conclusion"]
        }
    question = st.text_input("❓ Ask a question from paper")

    if question:
        with st.spinner("Thinking... 🤔"):
            result = answer_question(question, sentences, model)

        st.subheader("💬 Answer")
        st.success(result)

    st.subheader("🔍 Plagiarism Check")
    text1 = st.text_area("Text 1")
    text2 = st.text_area("Text 2")

    if st.button("Check Similarity"):
        score = check_plagiarism(text1, text2, model)        

        percentage = score * 100

        if percentage > 80:
            st.error(f"Similarity Score: {percentage:.2f}% (High Plagiarism 🚨)")
        elif percentage > 50:
            st.warning(f"Similarity Score: {percentage:.2f}% (Moderate ⚠️)")
        else:
            st.success(f"Similarity Score: {percentage:.2f}% (Low ✅)")

    if st.button("📊 Generate PPT"):
        if "summary" in st.session_state:
            create_ppt(st.session_state["summary"])
            st.success("PPT Generated: output.pptx")
        else:
            st.warning("Generate summary first!")
