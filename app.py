import streamlit as st
from openai import OpenAI
import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

st.set_page_config(page_title="AI Smart Roadmap", page_icon="🚀")

# --------- CUSTOM CSS ---------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f172a, #1e293b);
}
.hero {
    text-align: center;
    padding: 60px;
    background: linear-gradient(135deg, #2563eb, #1e3a8a);
    border-radius: 20px;
    color: white;
}
.feature-card {
    background: rgba(255,255,255,0.08);
    padding: 20px;
    border-radius: 15px;
    margin-top: 20px;
    color: white;
}
.result-box {
    background: rgba(255,255,255,0.1);
    padding: 25px;
    border-radius: 15px;
    margin-top: 20px;
    color: white;
}
.stButton>button {
    background-color: #2563eb;
    color: white;
    width: 100%;
    height: 45px;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# --------- HERO SECTION ---------
st.markdown("""
<div class="hero">
    <h1>🚀 AI Smart Roadmap Generator</h1>
    <p>Generate personalized career roadmaps powered by AI</p>
</div>
""", unsafe_allow_html=True)

# --------- FEATURES SECTION ---------
st.markdown("""
<div class="feature-card">
    <h3>✨ Features</h3>
    <ul>
        <li>AI Generated Learning Path</li>
        <li>Structured Timeline</li>
        <li>Project Suggestions</li>
        <li>Downloadable PDF</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# --------- INPUT SECTION ---------
st.markdown("## 🎯 Generate Your Roadmap")

goal = st.text_input("Enter Your Career Goal")
level = st.selectbox("Select Your Level", ["Beginner", "Intermediate", "Advanced"])
duration = st.selectbox("Select Duration", ["3 Months", "6 Months", "1 Year"])

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

roadmap_text = ""

if st.button("Generate Roadmap"):

    if goal == "":
        st.warning("Please enter your goal")
    else:
        with st.spinner("Generating AI Roadmap..."):

            prompt = f"""
            Create a detailed roadmap to become {goal}.
            Level: {level}
            Duration: {duration}.
            Include tools, projects, and timeline.
            """

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a professional career roadmap generator."},
                    {"role": "user", "content": prompt}
                ]
            )

            roadmap_text = response.choices[0].message.content

            st.markdown(
                f'<div class="result-box">{roadmap_text}</div>',
                unsafe_allow_html=True
            )

            # --------- PDF GENERATION ---------
            pdf_file = "roadmap.pdf"
            doc = SimpleDocTemplate(pdf_file)
            styles = getSampleStyleSheet()
            story = []

            story.append(Paragraph("AI Smart Roadmap", styles["Heading1"]))
            story.append(Spacer(1, 0.3 * inch))
            story.append(Paragraph(roadmap_text, styles["Normal"]))

            doc.build(story)

            with open(pdf_file, "rb") as f:
                st.download_button("📥 Download PDF", f, file_name="Roadmap.pdf")

# --------- FOOTER ---------
st.markdown("""
<hr>
<center style='color:white'>
Built with ❤️ using Streamlit & OpenAI
</center>
""", unsafe_allow_html=True)
