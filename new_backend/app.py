import streamlit as st
import os
import tempfile
import PyPDF2
from dotenv import load_dotenv
from openai import OpenAI
# Adding to enable downloading pdfs
from fpdf import FPDF
import io

def create_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    lines = text.split('\n')
    for line in lines:
        pdf.multi_cell(0, 10, line)

    # Get PDF content as bytes
    pdf_output = pdf.output(dest='S').encode('latin-1')

    # Save to BytesIO buffer
    pdf_buffer = io.BytesIO(pdf_output)
    return pdf_buffer
# Adding to enable downloading pdfs

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Configure the app
st.set_page_config(page_title="Resume Improver | CS Handbook", page_icon="📒")


# # ========== Define Shared Variables ==========
# # Resume-related
# first_name = last_name = email = phone = github = ""
# school = degree = grad_date = ""
# job_title_1 = company_name_1 = start_date_1 = end_date_1 = ""
# bullet_1_1 = bullet_1_2 = bullet_1_3 = ""
# job_title_2 = company_name_2 = start_date_2 = end_date_2 = ""
# bullet_2_1 = bullet_2_2 = bullet_2_3 = ""
# job_title_3 = company_name_3 = start_date_3 = end_date_3 = ""
# bullet_3_1 = bullet_3_2 = bullet_3_3 = ""
# summary = ""

# # Project-related
# project_name_1 = project_desc_1 = project_tech_1 = ""
# project_name_2 = project_desc_2 = project_tech_2 = ""
# project_name_3 = project_desc_3 = project_tech_3 = ""

# add_exp2 = False
# add_exp3 = False
# add_proj2 = False
# add_proj3 = False


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
    bullet_1_1 = bullet_1_2 = bullet_1_3 = ""
    job_title_1 = company_name_1 = start_date_1 = end_date_1 = ""

    # Set default values for project variables
    project_name_1 = project_desc_1 = project_tech_1 = ""
    project_name_2 = project_desc_2 = project_tech_2 = ""
    project_name_3 = project_desc_3 = project_tech_3 = ""
    add_proj2 = False
    add_proj3 = False


    # ---- EXPERIENCE ENTRY 1 ----
    st.markdown("#### 🔹 Experience 1")
    job_title_1 = st.text_input("Job Title (1)", placeholder="e.g., Software Engineer Intern")
    company_name_1 = st.text_input("Company Name (1)", placeholder="e.g., Google")
    start_date_1 = st.text_input("Start Date (1)", placeholder="e.g., June 2024")
    end_date_1 = st.text_input("End Date (1)", placeholder="e.g., August 2024 or Present")
    bullet_1_1 = st.text_area("Bullet Point 1 (1)", placeholder="e.g., Developed internal dashboard using Python.")
    bullet_1_2 = st.text_area("Bullet Point 2 (1)", placeholder="e.g., Worked on cloud deployment pipelines.")
    bullet_1_3 = st.text_area("Bullet Point 3 (1)", placeholder="e.g., Participated in daily agile standups.")

    # Optional Experience 2
    bullet_2_1 = bullet_2_2 = bullet_2_3 = ""
    job_title_2 = company_name_2 = start_date_2 = end_date_2 = ""
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

    # Optional Experience 3
    bullet_3_1 = bullet_3_2 = bullet_3_3 = ""
    job_title_3 = company_name_3 = start_date_3 = end_date_3 = ""
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

    st.subheader("Step 4: Projects")

    # Set default values for Pylance/type hints
    project_name_1 = project_desc_1 = project_tech_1 = ""
    project_name_2 = project_desc_2 = project_tech_2 = ""
    project_name_3 = project_desc_3 = project_tech_3 = ""

    # ---- PROJECT 1 ----
    st.markdown("#### 🔸 Project 1")
    project_name_1 = st.text_input("Project Name (1)", placeholder="e.g., Smart Parking App")
    project_desc_1 = st.text_area("Description (1)", placeholder="e.g., A web app that helps users find real-time parking spots.")
    project_tech_1 = st.text_input("Technologies Used (1)", placeholder="e.g., React, Node.js, Firebase")

    # Optional Project 2
    add_proj2 = st.checkbox("➕ Add Another Project")
    if add_proj2:
        st.markdown("#### 🔸 Project 2")
        project_name_2 = st.text_input("Project Name (2)", placeholder="e.g., Resume Builder Tool")
        project_desc_2 = st.text_area("Description (2)", placeholder="e.g., A Python-based CLI tool for creating resumes.")
        project_tech_2 = st.text_input("Technologies Used (2)", placeholder="e.g., Python, Rich Library")

    # Optional Project 3
    add_proj3 = st.checkbox("➕ Add One More Project")
    if add_proj3:
        st.markdown("#### 🔸 Project 3")
        project_name_3 = st.text_input("Project Name (3)", placeholder="e.g., AI Chatbot")
        project_desc_3 = st.text_area("Description (3)", placeholder="e.g., A chatbot using OpenAI GPT for mental health check-ins.")
        project_tech_3 = st.text_input("Technologies Used (3)", placeholder="e.g., Python, Streamlit, OpenAI API")


    def generate_resume_preview():
        preview = ""

        # === Header Info ===
        if first_name and last_name:
            preview += f"**{first_name} {last_name}**  \n"
        if email or phone or github:
            contact_info = " | ".join(filter(None, [email, phone, github]))
            preview += f"{contact_info}\n"

        preview += "\n---\n\n"

        # === Education ===
        preview += "### 🎓 Education  \n"
        if school:
            preview += f"**{school}**  \n"
        if degree:
            preview += f"{degree}  \n"
        if grad_date:
            preview += f"Expected Graduation: {grad_date}\n"

        # === Projects ===
        if project_name_1:
            preview += "\n\n---\n\n### 🛠️ Projects\n"
            preview += f"**{project_name_1}**  \n{project_desc_1}  \n_Tech Used: {project_tech_1}_\n"
        if add_proj2 and project_name_2:
            preview += f"\n**{project_name_2}**  \n{project_desc_2}  \n_Tech Used: {project_tech_2}_\n"
        if add_proj3 and project_name_3:
            preview += f"\n**{project_name_3}**  \n{project_desc_3}  \n_Tech Used: {project_tech_3}_\n"

        # === Experience ===
        if job_title_1 and company_name_1:
            preview += "\n\n---\n\n### 💼 Experience\n"
            preview += f"**{job_title_1}**, {company_name_1}  \n{start_date_1} – {end_date_1}\n"
            for bullet in [bullet_1_1, bullet_1_2, bullet_1_3]:
                if bullet:
                    preview += f"- {bullet}\n"

        if add_exp2 and job_title_2 and company_name_2:
            preview += f"\n**{job_title_2}**, {company_name_2}  \n{start_date_2} – {end_date_2}\n"
            for bullet in [bullet_2_1, bullet_2_2, bullet_2_3]:
                if bullet:
                    preview += f"- {bullet}\n"

        if add_exp3 and job_title_3 and company_name_3:
            preview += f"\n**{job_title_3}**, {company_name_3}  \n{start_date_3} – {end_date_3}\n"
            for bullet in [bullet_3_1, bullet_3_2, bullet_3_3]:
                if bullet:
                    preview += f"- {bullet}\n"

        return preview

    
    # ==========================
    # Resume Preview Button
    # ==========================
    if st.button("📄 Generate Resume Preview"):
        st.markdown("---")
        st.subheader("📄 Resume Preview")

        preview = generate_resume_preview()
        st.markdown(preview)

        # Only generate PDF after preview is created
        if preview.strip():
            pdf_bytes = create_pdf(preview)
            st.download_button(
                label="📥 Download Resume as PDF",
                data=pdf_bytes,
                file_name="resume.pdf",
                mime="application/pdf"
            )

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

