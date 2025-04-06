import streamlit as st
from lighthouse_analyzer import run_lighthouse
from website_scraper import get_website_data
from llm_analysis import analyze_website_with_mistral

# Streamlit UI
st.set_page_config(page_title="Feature Flaw Detector", layout="wide")

st.title("🔍 AI-Powered Feature Flaw Detector")
st.write("Analyze websites for flaws and get AI-driven recommendations.")

# User input
url = st.text_input("Enter Website URL", "https://example.com")

if st.button("Analyze Website"):
    with st.spinner("Running analysis..."):
        # Step 1: Scrape website data
        st.subheader("📄 Website Data")
        website_data = get_website_data(url)
        st.json(website_data)

        # Step 2: Run Lighthouse audit
        st.subheader("🚀 Performance & SEO Analysis")
        lighthouse_results = run_lighthouse(url)
        st.json(lighthouse_results)

        # Merge results
        analysis_data = {**website_data, **lighthouse_results}

        # Step 3: AI Analysis
        st.subheader("🧠 AI-Generated Suggestions")
        ai_suggestions = analyze_website_with_mistral(analysis_data)
        st.text(ai_suggestions)

st.write("Powered by Open-Source AI & Lighthouse")
