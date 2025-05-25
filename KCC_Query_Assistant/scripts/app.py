import streamlit as st
from rag_pipeline import handle_query
from PIL import Image

st.set_page_config(
    page_title="Kisan Query Assistant",
    layout="centered",
    page_icon="🌾"
)

st.markdown("""
    <style>
    .main-title {
        font-size: 2.2em;
        font-weight: 700;
        color: #1e4d2b;
        text-align: center;
        margin-bottom: 0.5em;
    }
    .sub-title {
        font-size: 1.1em;
        color: #4a7c59;
        text-align: center;
        margin-top: -0.5em;
        margin-bottom: 2em;
    }
    .response-box {
        background-color: #e6ffe6;
        padding: 1.2em;
        border-left: 5px solid #1e4d2b;
        border-radius: 5px;
    }
    </style>
    <div class="main-title">🌾 Kisan Query Assistant</div>
    <div class="sub-title">Get agricultural advice from KCC dataset, the web, or AI</div>
""", unsafe_allow_html=True)

user_input = st.text_input("\U0001F4DD Ask your agricultural question:", "", placeholder="e.g., How to protect cotton crops from whitefly?")

if st.button("Get Answer") and user_input.strip():
    with st.spinner("Generating your answer..."):
        result = handle_query(user_input)

        st.markdown("""
        <div class="response-box">
        <b>Source:</b> <span style='color:#1e4d2b;'>%s</span><br><br>
        %s
        </div>
    """ % (result['source'], result['answer']), unsafe_allow_html=True)

        if result['context']:
            with st.expander("\U0001F4DA Show KCC Context Used"):
                for i, c in enumerate(result['context'], 1):
                    st.markdown(f"**{i}.** {c}")

st.markdown("""
    <hr style='margin-top:3em;'>
    <div style='text-align:center;'>
        <small>Built with ❤️ for Farmers.</small>
    </div>
""", unsafe_allow_html=True)
