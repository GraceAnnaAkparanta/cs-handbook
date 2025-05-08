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
st.set_page_config(page_title="Resume Improver | CS Handbook", page_icon="📒")

# Function to go home
def go_home():
    st.session_state["section"] = "🏠 Home"

# Handle session state for sidebar
if "section" not in st.session_state:
    st.session_state["section"] = "🏠 Home"

section = st.sidebar.radio(
    "Go to",
    ["🏠 Home", "📝 Create Resume", "📄 Improve Resume", "🎯 Tailor Resume", "💬 Chat With AI"],
    index=["🏠 Home", "📝 Create Resume", "📄 Improve Resume", "🎯 Tailor Resume", "💬 Chat With AI"].index(st.session_state["section"]),
    key="section"
)

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

# --- Sections ---
if section == "🏠 Home":
    st.title("🏠 Welcome to the CS Handbook Resume Hub")
    st.markdown("""
        This is your personal toolkit for building strong, job-ready resumes. Whether you’re starting from scratch, refining your resume, or tailoring it for a specific job, this web app has you covered.

        **📝 Create Resume:** Use a guided form to build your resume.  
        **📄 Improve Resume:** Get AI-powered suggestions and a color-coded score to improve your bullet points.  
        **🎯 Tailor Resume:** Match your resume to a job description with smart comparisons.  

        Use the sidebar to explore resume tools and AI-powered support.
    """)

elif section == "📝 Create Resume":
    st.title("📝 Create Resume")
    st.write("🚧 This feature will be available soon!")

elif section == "📄 Improve Resume":
    st.title("📄 Resume Improver")
    st.subheader("Improve your resume bullet points using AI")
    st.markdown("This tool is part of the [CS Handbook Project](https://github.com/GraceAnnaAkparanta/cs-handbook) – powered by OpenAI.")

    desired_role = st.text_input("🎯 Target Role", placeholder="e.g., Software Engineer, Data Analyst")
    uploaded_resume = st.file_uploader("📎 Upload your resume (PDF only)", type=["pdf"])
    resume_text = ""

    if uploaded_resume is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(uploaded_resume.getvalue())
            temp_file_path = temp_file.name

        with open(temp_file_path, "rb") as f:
            pdf_reader = PyPDF2.PdfReader(f)
            for page in pdf_reader.pages:
                resume_text += page.extract_text() or ""

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

elif section == "🎯 Tailor Resume":
    st.title("🎯 Tailor Resume")
    st.subheader("Tailor your resume to match a specific job description")

    uploaded_resume = st.file_uploader("📎 Upload your resume (PDF only)", type=["pdf"])
    job_description = st.text_area("📝 Paste the job description here")

    resume_text = ""
    if uploaded_resume is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(uploaded_resume.getvalue())
            temp_file_path = temp_file.name

        with open(temp_file_path, "rb") as f:
            pdf_reader = PyPDF2.PdfReader(f)
            for page in pdf_reader.pages:
                resume_text += page.extract_text() or ""

    if job_description and resume_text:
        prompt = (
            f"Given the following resume:\n\n{resume_text}\n\n"
            f"And this job description:\n\n{job_description}\n\n"
            f"Suggest personalized bullet points and changes to better align the resume with the job description. "
            f"Use concise language, reflect key responsibilities, and follow the XYZ format."
        )

        with st.spinner("🎯 Tailoring resume..."):
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )
            tailored_response = completion.choices[0].message.content
            st.success("✅ Tailored suggestions ready!")
            st.subheader("🎨 Suggested Customizations")
            st.markdown(tailored_response)

elif section == "💬 Chat With AI":
    st.title("💬 Chat With AI")
    st.markdown("Ask questions about technical concepts, CS topics, job prep, or anything else!")

    user_input = st.text_input("💬 Ask me anything:")

    if user_input:
        with st.spinner("Thinking..."):
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": user_input}]
            )
            answer = completion.choices[0].message.content
            st.success("✅ Response:")
            st.markdown(answer)

# Footer
st.markdown("---")
st.markdown("🔍 *Note: This tool uses AI to provide suggestions. Always review critically and get feedback from peers.*")

if st.button("← Back to CS Handbook Home"):
    go_home()
