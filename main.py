import streamlit as st
from processor import get_text
from llm_engine import analyze_resume

st.set_page_config(page_title="AI ATS Optimizer", layout="wide")

st.title("🎯 AI ATS Resume Optimizer")
st.markdown("Optimize your resume for specific Job Descriptions using Google Gemini Pro.")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Enter Groq API Key", type="password")
    if api_key:
        import os
        os.environ["GROQ_API_KEY"] = api_key # Changed variable name

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Upload Documents")
    jd_input = st.text_area("Paste Job Description (JD)", height=300)
    uploaded_file = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"])

if st.button("Analyze Resume") and uploaded_file and jd_input:
    with st.spinner("Analyzing alignment..."):
        resume_text = get_text(uploaded_file)
        result = analyze_resume(resume_text, jd_input)
        
        if "error" in result:
            st.error(result["error"])
        else:
            with col2:
                st.subheader("ATS Analysis Dashboard")
                
                # Metric Score
                score = result.get("score", 0)
                st.gauge = st.metric("Overall Match Score", f"{score}%")
                st.progress(score / 100)
                
                # Dashboard Tabs
                tab1, tab2, tab3 = st.tabs(["✅ Strengths", "🚩 Critical Gaps", "💡 Improvements"])
                
                with tab1:
                    st.success("**Plus Points**")
                    for point in result.get("plus_points", []):
                        st.write(f"- {point}")
                        
                with tab2:
                    st.error("**Non-Negotiables (Missing)**")
                    for gap in result.get("critical_gaps", []):
                        st.write(f"⚠️ {gap}")
                
                with tab3:
                    st.info("**Suggested Additions**")
                    for item in result.get("consider_adding", []):
                        st.write(f"➕ {item}")
                    
                    st.warning("**What to Remove/Clean Up**")
                    for item in result.get("to_remove", []):
                        st.write(f"✂️ {item}")

                st.subheader("Executive Summary")
                st.write(result.get("summary", "No summary provided."))
else:
    with col2:
        st.info("Upload your resume and paste a JD to see the analysis.")