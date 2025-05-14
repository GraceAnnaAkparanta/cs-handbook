import streamlit as st
import os
import tempfile
import PyPDF2
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Configure the app
st.set_page_config(page_title="Resume Improver | CS Handbook", page_icon="📒")

# Sidebar navigation
if "page" not in st.session_state:
    st.session_state.page = "Home"

pages = {
    "🏠 Home": "Home",
    "📝 Create Resume": "Create",
    "📄 Improve Resume": "Improve",
    "🎯 Tailor Resume": "Tailor",
    "💬 Chat With AI": "Chat"
}

selected_page = st.sidebar.radio("Choose a section", list(pages.keys()), index=list(pages.values()).index(st.session_state.page))
st.session_state.page = pages[selected_page]

# Common function: extract text from uploaded PDF
def extract_text_from_pdf(file):
    text = ""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(file.getvalue())
        tmp_path = tmp.name

    with open(tmp_path, "rb") as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text

# --- Page Logic ---

# Home
if st.session_state.page == "Home":
    st.title("🏠 Welcome to the CS Handbook Resume Hub")
    st.markdown("""
        This tool helps you build, improve, and tailor resumes for tech jobs.

        **📝 Create Resume** - Start fresh with a guided form  
        **📄 Improve Resume** - Upload your resume and get suggestions  
        **🎯 Tailor Resume** - Align your resume to a specific job  
        **💬 Chat With AI** - Ask questions about anything CS-related
    """)

# Create Resume
elif st.session_state.page == "Create":
    st.title("📝 Create Your Resume")
    st.subheader("Step 1: Basic Information")

    # Personal Info
    first_name = st.text_input("First Name (Preferred)", placeholder="e.g., John")
    last_name = st.text_input("Last Name", placeholder="e.g., Doe")
    email = st.text_input("Email", placeholder="e.g., JohnDoe@example.com")
    phone = st.text_input("Phone Number", placeholder="e.g., (123) 456-7890")
    github = st.text_input("GitHub URL", placeholder="e.g., https://github.com/JohnDoe")

    st.subheader("Step 2: Education")

    school = st.text_input("University/College Name", placeholder="e.g., University of XYZ")
    degree = st.text_input("Degree & Major", placeholder="e.g., B.S. in Computer Science")
    grad_date = st.text_input("Expected Graduation Date", placeholder="e.g., May 2x2x")

    st.subheader("Step 3: Experience")

# Set default values so Pylance knows these variables exist
bullet_1_1 = ""
bullet_1_2 = ""
bullet_1_3 = ""
job_title_1 = ""
company_name_1 = ""
start_date_1 = ""
end_date_1 = ""

# ---- EXPERIENCE ENTRY 1 ----
st.markdown("#### 🔹 Experience 1")
job_title_1 = st.text_input("Job Title (1)", placeholder="e.g., Software Engineer Intern")
company_name_1 = st.text_input("Company Name (1)", placeholder="e.g., Google")
start_date_1 = st.text_input("Start Date (1)", placeholder="e.g., June 2024")
end_date_1 = st.text_input("End Date (1)", placeholder="e.g., August 2024 or Present")
bullet_1_1 = st.text_area("Bullet Point 1 (1)", placeholder="e.g., Developed internal dashboard using Python.")
bullet_1_2 = st.text_area("Bullet Point 2 (1)", placeholder="e.g., Worked on cloud deployment pipelines.")
bullet_1_3 = st.text_area("Bullet Point 3 (1)", placeholder="e.g., Participated in daily agile standups.")


# Set default values so Pylance knows these variables exist
bullet_2_1 = ""
bullet_2_2 = ""
bullet_2_3 = ""
job_title_2 = ""
company_name_2 = ""
start_date_2 = ""
end_date_2 = ""

# ---- EXPERIENCE ENTRY 2 (optional) ----
add_exp2 = st.checkbox("➕ Add Another Experience")

if add_exp2:
    st.markdown("#### 🔹 Experience 2")
    job_title_2 = st.text_input("Job Title (2)", placeholder="e.g., IT Support Specialist")
    company_name_2 = st.text_input("Company Name (2)", placeholder="e.g., Local Tech Co.")
    start_date_2 = st.text_input("Start Date (2)", placeholder="e.g., Jan 2023")
    end_date_2 = st.text_input("End Date (2)", placeholder="e.g., May 2023")
    bullet_2_1 = st.text_area("Bullet Point 1 (2)", placeholder="e.g., Resolved client technical issues quickly.")
    bullet_2_2 = st.text_area("Bullet Point 2 (2)", placeholder="e.g., Managed user accounts and hardware.")
    bullet_2_3 = st.text_area("Bullet Point 3 (2)", placeholder="e.g., Automated common support scripts.")

# Set default values so Pylance knows these variables exist
bullet_3_1 = ""
bullet_3_2 = ""
bullet_3_3 = ""
job_title_3 = ""
company_name_3 = ""
start_date_3 = ""
end_date_3 = ""

# ---- EXPERIENCE ENTRY 3 (optional) ----
add_exp3 = st.checkbox("➕ Add One More Experience")

if add_exp3:
    st.markdown("#### 🔹 Experience 3")
    job_title_3 = st.text_input("Job Title (3)", placeholder="e.g., Web Development Intern")
    company_name_3 = st.text_input("Company Name (3)", placeholder="e.g., Freelance")
    start_date_3 = st.text_input("Start Date (3)", placeholder="e.g., Sept 2022")
    end_date_3 = st.text_input("End Date (3)", placeholder="e.g., Dec 2022")
    bullet_3_1 = st.text_area("Bullet Point 1 (3)", placeholder="e.g., Designed website for a small business.")
    bullet_3_2 = st.text_area("Bullet Point 2 (3)", placeholder="e.g., Maintained client satisfaction and UX.")
    bullet_3_3 = st.text_area("Bullet Point 3 (3)", placeholder="e.g., Optimized website loading time.")

# ==========================
# Resume Preview Button
# ==========================
if st.button("📄 Generate Resume Preview"):
    st.markdown("---")
    st.subheader("📄 Resume Preview")

    resume_text = f"""
**{first_name} {last_name}**  
{email} | {phone} | {github}

---

### 🎓 Education
**{school}**  
{degree}  
Expected Graduation: {grad_date}
"""

    if summary != "":
        resume_text += f"""
---

### 💡 Summary
{summary}
"""

    # Add Experience 1 if filled
    if job_title_1 != "" and company_name_1 != "":
        resume_text += f"""
---
### 💼 Experience
**{job_title_1}**, {company_name_1}  
{start_date_1} – {end_date_1}
"""
        if bullet_1_1 != "":
            resume_text += f"- {bullet_1_1}\n"
        if bullet_1_2 != "":
            resume_text += f"- {bullet_1_2}\n"
        if bullet_1_3 != "":
            resume_text += f"- {bullet_1_3}\n"

    # Add Experience 2 if checkbox selected and info provided
    if add_exp2 and job_title_2 != "" and company_name_2 != "":
        resume_text += f"""
**{job_title_2}**, {company_name_2}  
{start_date_2} – {end_date_2}
"""
        if bullet_2_1 != "":
            resume_text += f"- {bullet_2_1}\n"
        if bullet_2_2 != "":
            resume_text += f"- {bullet_2_2}\n"
        if bullet_2_3 != "":
            resume_text += f"- {bullet_2_3}\n"

    # Add Experience 3 if checkbox selected and info provided
    if add_exp3 and job_title_3 != "" and company_name_3 != "":
        resume_text += f"""
**{job_title_3}**, {company_name_3}  
{start_date_3} – {end_date_3}
"""
        if bullet_3_1 != "":
            resume_text += f"- {bullet_3_1}\n"
        if bullet_3_2 != "":
            resume_text += f"- {bullet_3_2}\n"
        if bullet_3_3 != "":
            resume_text += f"- {bullet_3_3}\n"

    # Display the final formatted resume
    st.code(resume_text, language="markdown")
    st.success("✅ This is a preview. Copy or export it in the future!")


    st.subheader("Step 4: Add Summary (Optional)")
    summary = st.text_area("Professional Summary", placeholder="e.g., Passionate CS student with experience in...")

    # Submit and Preview
    if st.button("📄 Generate Resume Preview"):
        st.markdown("---")
        st.subheader("📄 Resume Preview")

        # Start formatting resume output as Markdown
        resume_text = f"""
**{first_name} {last_name}**  
{email} | {phone} | {github}

---

### 🎓 Education
**{school}**  
{degree}  
Expected Graduation: {grad_date}
"""

        # Add Summary if provided
        if summary != "":
            resume_text += f"""
---

### 💡 Summary
{summary}
"""

        # Add Experience if job title and company are provided
        if job_title != "" and company_name != "":
            resume_text += f"""
---

### 💼 Experience
**{job_title}**, {company_name}  
{start_date} – {end_date}
"""

            # Add bullet points if any are written
            if bullet_1 != "":
                resume_text += f"- {bullet_1}\n"
            if bullet_2 != "":
                resume_text += f"- {bullet_2}\n"
            if bullet_3 != "":
                resume_text += f"- {bullet_3}\n"

        # Display the formatted resume
        st.code(resume_text, language="markdown")
        st.success("✅ This is a preview. Copy or export it in the future!")

# Improve Resume
elif st.session_state.page == "Improve":
    st.title("📄 Improve Resume")
    st.subheader("Upload your resume and get better bullet points")

    role = st.text_input("Target Job Title", placeholder="e.g., Software Engineer")
    uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

    if uploaded_file and role:
        resume_text = extract_text_from_pdf(uploaded_file)

        prompt = (
            f"Here's a resume:\n\n{resume_text}\n\n"
            f"Suggest bullet point improvements for the role of '{role}'. "
            f"Use the XYZ format (Accomplished X by doing Y as measured by Z)."
        )

        with st.spinner("Improving your resume..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )
            suggestions = response.choices[0].message.content

        st.success("Suggestions ready!")
        st.markdown(suggestions)

# Tailor Resume
elif st.session_state.page == "Tailor":
    st.title("🎯 Tailor Resume")
    st.subheader("Match your resume with a specific job")

    job_desc = st.text_area("Paste Job Description")
    uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

    if uploaded_file and job_desc:
        resume_text = extract_text_from_pdf(uploaded_file)

        prompt = (
            f"Here is a resume:\n\n{resume_text}\n\n"
            f"And this is a job description:\n\n{job_desc}\n\n"
            f"Suggest edits and new bullet points to match the job. Use XYZ format."
        )

        with st.spinner("Tailoring your resume..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )
            tailored_text = response.choices[0].message.content

        st.success("Tailored suggestions ready!")
        st.markdown(tailored_text)

# Chat With AI
elif st.session_state.page == "Chat":
    st.title("💬 Chat With AI")
    question = st.text_input("Ask a question about CS, resumes, or careers")

    if question:
        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": question}]
            )
            answer = response.choices[0].message.content

        st.success("Answer:")
        st.markdown(answer)

# Footer
st.markdown("---")
st.markdown("🔍 *This tool uses AI. Always double-check results before using.*")
