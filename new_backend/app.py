import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
import os
import PyPDF2
import tempfile

# Load env vars
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Page config
st.set_page_config(page_title="Resume Improver | CS Handbook", page_icon="📄")

# Custom CSS
st.markdown("""
    <style>
    html, body, [class*="css"]  {
        font-family: 'Segoe UI', sans-serif;
        background-color: #f9f9fb;
    }
    .stButton>button {
        background-color: #4a90e2;
        color: white;
        padding: 0.6em 1.2em;
        border: none;
        border-radius: 8px;
        transition: all 0.2s;
    }
    .stButton>button:hover {
        background-color: #357ABD;
        transform: scale(1.02);
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.title("📄 Resume Improver")
st.subheader("Improve your resume bullet points using AI")
st.markdown("This tool is part of the [CS Handbook Project](#) – powered by OpenAI.")

# Input fields
desired_role = st.text_input("🎯 Target Role", placeholder="e.g., Software Engineer, Data Analyst")

uploaded_resume = st.file_uploader("📎 Upload your resume (PDF only)", type=["pdf"])
resume_text = ""

# Extract text from PDF
if uploaded_resume is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(uploaded_resume.getvalue())
        temp_file_path = temp_file.name

    with open(temp_file_path, "rb") as f:
        pdf_reader = PyPDF2.PdfReader(f)
        for page in pdf_reader.pages:
            resume_text += page.extract_text() or ""

# Generate improvements
if desired_role and resume_text:
    prompt = (
        f"Here is a resume:\n\n{resume_text}\n\n"
        f"Suggest improvements for someone applying to a '{desired_role}' role. "
        f"Use the XYZ format (Accomplished X by doing Y as measured by Z). "
        f"Only list improved bullet points."
    )

    with st.spinner("✨ Improving your resume..."):
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        response = completion.choices[0].message.content
        st.success("✅ Suggestions ready!")
        st.subheader("💡 Improved Bullet Points")
        st.markdown(response)

# Optional: Back link
st.markdown("---")
st.markdown("[← Back to CS Handbook Home](#)")
