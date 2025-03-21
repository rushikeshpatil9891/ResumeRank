# %%
import streamlit as st
from PyPDF2 import PdfReader
import pandas as pd
import altair as alt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# %%
# Function to extract text from PDF
def extract_text_from_pdf(file):
    pdf = PdfReader(file)
    text = ""
    for page in pdf.pages:
        text += page.extract_text()
    return text

# %%
# Function to rank resumes based on job description
def rank_resumes(job_description, resumes):
    documents = [job_description] + resumes
    vectorizer = TfidfVectorizer().fit_transform(documents)
    vectors = vectorizer.toarray()
    job_description_vector = vectors[0]
    resume_vectors = vectors[1:]
    cosine_similarities = cosine_similarity([job_description_vector], resume_vectors).flatten()
    return cosine_similarities

# %%
# Streamlit app
st.set_page_config(page_title="AI Resume Screening & Candidate Ranking System", layout="wide")

# Header and navigation bar
st.markdown("""
    <style>
        .header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 10px 0;
            color: black;
        }
        .header img {
            height: 50px;
        }
        .header h1 {
            margin: 0;
            padding-left: 10px;
        }
        .footer {
            text-align: center;
            padding: 10px 0;
            margin-top: 20px;
            border-top: 1px solid #eaeaea;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="header">
        <img src="https://cdn.shopify.com/s/files/1/0558/6413/1764/files/Rainbow_Logo_Design_29_1024x1024.jpg?v=1680141974" alt="Logo">
        <h1>AI Resume Screening & Candidate Ranking System</h1>
    </div>
""", unsafe_allow_html=True)

# Job description input
st.sidebar.header("Job Description")
job_description = st.sidebar.text_area("Enter the job description")

# File uploader
st.sidebar.header("Upload Resumes")
uploaded_files = st.sidebar.file_uploader("Upload PDF files", type=["pdf"], accept_multiple_files=True)

# Main content
if uploaded_files and job_description:
    st.header("Ranking Resumes")
    
    resumes = []
    progress_bar = st.progress(0)
    for i, file in enumerate(uploaded_files):
        text = extract_text_from_pdf(file)
        resumes.append(text)
        progress_bar.progress((i + 1) / len(uploaded_files))
    
    # Rank resumes
    scores = rank_resumes(job_description, resumes)
    
    # Display scores
    results = pd.DataFrame({"Resume": [file.name for file in uploaded_files], "Score": scores})
    results = results.sort_values(by="Score", ascending=False)
    
    st.subheader("Results")
    st.dataframe(results)

    # Display chart
    chart = alt.Chart(results).mark_bar().encode(
        x='Score',
        y=alt.Y('Resume', sort='-x')
    ).properties(
        title='Resume Ranking Scores'
    )
    st.altair_chart(chart, use_container_width=True)

    # Download results
    csv = results.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download results as CSV",
        data=csv,
        file_name='resume_ranking_results.csv',
        mime='text/csv',
    )
else:
    st.info("Please enter the job description and upload resumes to rank.")

# Footer
st.markdown("""
    <div class="footer">
        <p>&copy; 2025 AI Resume Screening & Candidate Ranking System. All rights reserved.</p>
    </div>
""", unsafe_allow_html=True)



