import streamlit as st
import PyPDF2


# ---------- Extract text from PDF ----------
def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""

    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()

    return text


# ---------- Calculate Resume Score ----------
def calculate_score(text):
    score = 0
    text = text.lower()

    keywords = ["education", "skills", "project", "internship", "experience"]

    for word in keywords:
        if word in text:
            score += 20

    if len(text) > 1000:
        score += 10

    return min(score, 100)


# ---------- Suggestions ----------
def suggest_improvements(text):
    suggestions = []
    text = text.lower()

    if "objective" not in text:
        suggestions.append("Add career objective section")

    if "project" not in text:
        suggestions.append("Add at least one project")

    if "skills" not in text:
        suggestions.append("Mention technical skills clearly")

    if len(text) < 800:
        suggestions.append("Resume content is too short")

    return suggestions


# ---------- Rewrite bullet points ----------
def rewrite_bullets(text):
    lines = text.split("\n")
    improved = []

    for line in lines:
        if len(line.strip()) > 20:
            improved.append("✔ Successfully worked on: " + line.strip())

    return improved[:5]


# ---------- STREAMLIT UI ----------

st.title("Resume Analyzer & Improver")

uploaded_file = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])

if uploaded_file is not None:

    text = extract_text_from_pdf(uploaded_file)

    st.subheader("Resume Score")
    score = calculate_score(text)
    st.write(score, "/ 100")

    st.subheader("Suggestions")

    suggestions = suggest_improvements(text)

    if suggestions:
        for s in suggestions:
            st.write("•", s)
    else:
        st.write("Your resume looks good!")

    st.subheader("Improved Bullet Points")

    bullets = rewrite_bullets(text)

    for b in bullets:
        st.write(b)