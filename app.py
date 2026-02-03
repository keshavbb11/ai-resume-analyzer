import streamlit as st
import tempfile
import pandas as pd
import json
import re


from resume_loader import load_resume, sanitize_text
from vector_store import chunk_documents, build_vectorstore
from analysis_engine import analysis_chain
from scoring_engine import compute_score
from recommendation_engine import recommendation_chain
from pdf_report import generate_pdf


def extract_json(text: str):
    match = re.search(r"\{[\s\S]*\}", text)
    if not match:
        raise ValueError("No JSON found")
    return json.loads(match.group())


st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f172a, #020617);
}

h1, h2, h3 {
    color: #e5e7eb;
}

p, li, span, div {
    color: #cbd5f5;
}

.metric-card {
    background: #020617;
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 0 15px rgba(99,102,241,0.15);
}

.stButton>button {
    background: linear-gradient(90deg, #6366f1, #22d3ee);
    color: white;
    border-radius: 14px;
    font-weight: 600;
    padding: 0.6em 1.4em;
}

.stDownloadButton>button {
    background: linear-gradient(90deg, #22c55e, #4ade80);
    color: black;
    border-radius: 12px;
}

[data-testid="stExpander"] {
    background: #020617;
    border-radius: 14px;
    border: 1px solid #1e293b;
}
</style>
""", unsafe_allow_html=True)


st.markdown("## 📄 AI Resume Analyzer")
st.caption("Bias-aware • GenAI-powered • ATS-style resume evaluation")


with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    role = st.selectbox(
        "Job Role",
        ["Backend Developer", "GenAI Engineer"]
    )
    top_k = st.slider(
        "Context depth (Top-K chunks)",
        2, 6, 4
    )
    st.markdown("---")
    st.caption("Runs locally with Ollama")


col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 📤 Upload Resumes")
    uploaded_resumes = st.file_uploader(
        "PDF resumes",
        type="pdf",
        accept_multiple_files=True
    )

with col2:
    st.markdown("### 🧾 Job Description")
    job_description = st.text_area(
        "Paste the JD here",
        height=220
    )


st.markdown("")
analyze = st.button("🚀 Analyze Resumes", use_container_width=True)


if analyze:

    if not uploaded_resumes or not job_description:
        st.error("Please upload resumes and provide a job description.")
        st.stop()

    results = []

    with st.spinner("Analyzing resumes with GenAI…"):
        for resume in uploaded_resumes:

            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(resume.read())
                path = tmp.name

            docs = load_resume(path)
            for d in docs:
                d.page_content = sanitize_text(d.page_content)

            chunks = chunk_documents(docs)
            vectorstore = build_vectorstore(chunks)
            retriever = vectorstore.as_retriever(search_kwargs={"k": top_k})

            context_docs = retriever.invoke("Extract skills, experience, projects")

            raw_analysis = analysis_chain.invoke({
                "context": context_docs,
                "job_description": job_description
            })

            try:
                analysis = extract_json(raw_analysis)
            except Exception:
                st.error("LLM returned invalid JSON")
                st.text(raw_analysis)
                st.stop()

            final_score = compute_score(analysis, role)

            recommendations = recommendation_chain.invoke({
                "context": context_docs,
                "job_description": job_description
            })

            results.append({
                "Resume": resume.name,
                "Score": final_score,
                "Analysis": analysis,
                "Recommendations": recommendations
            })

    
    results.sort(key=lambda x: x["Score"], reverse=True)

    st.markdown("## 📊 Overview")

    m1, m2, m3 = st.columns(3)
    m1.metric("Total Resumes", len(results))
    m2.metric("Top Score", results[0]["Score"])
    m3.metric("Role Evaluated", role)

    
    st.markdown("## 🏆 Resume Ranking")
    st.dataframe(
        pd.DataFrame(
            [{"Resume": r["Resume"], "Score": r["Score"]} for r in results]
        ),
        use_container_width=True
    )

    
    st.markdown("## 📄 Detailed Analysis")

    for idx, r in enumerate(results):

        with st.expander(f"{idx+1}. {r['Resume']} — Score {r['Score']}"):

            t1, t2, t3 = st.tabs(["🔍 Analysis", "📈 Scores", "🎯 Recommendations"])

            with t1:
                st.markdown("**Skills Found**")
                st.write(", ".join(r["Analysis"]["skills_found"]))

                st.markdown("**Missing Skills**")
                st.write(", ".join(r["Analysis"]["missing_skills"]))

            with t2:
                st.progress(r["Analysis"]["skills_score"] / 100)
                st.caption(f"Skills: {r['Analysis']['skills_score']}")

                st.progress(r["Analysis"]["experience_score"] / 100)
                st.caption(f"Experience: {r['Analysis']['experience_score']}")

                st.progress(r["Analysis"]["projects_score"] / 100)
                st.caption(f"Projects: {r['Analysis']['projects_score']}")

                st.progress(r["Analysis"]["clarity_score"] / 100)
                st.caption(f"Clarity: {r['Analysis']['clarity_score']}")

            with t3:
                st.write(r["Recommendations"])

            pdf_path = generate_pdf(r)
            with open(pdf_path, "rb") as f:
                st.download_button(
                    "📥 Download PDF Report",
                    f,
                    file_name=pdf_path,
                    mime="application/pdf"
                )


st.markdown("---")
st.caption("Built with Streamlit • LangChain • FAISS • Ollama")
