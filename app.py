import streamlit as st

from utils.pdf_loader import load_pdf
from utils.text_splitter import split_text
from utils.vector_store import (
    store_embeddings,
    retrieve_chunks,
    clear_database
)
from utils.generator import generate_answer


# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🧠",
    layout="wide"
)


# ---------------- CUSTOM CSS ----------------

st.markdown(
    """
    <style>

    .stApp {
        background-color: #1f1f1f;
        color: #f4efe6;
    }

    h1 {
        text-align: center;
        color: #f4efe6;
        margin-bottom: 30px;
    }

    .stFileUploader {
        background: rgba(244, 239, 230, 0.08);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(244, 239, 230, 0.1);
    }

    .stTextInput > div > div > input {
        background: rgba(244, 239, 230, 0.25);
        color: #f4efe6;
        border-radius: 12px;
        border: 1px solid rgba(244, 239, 230, 0.15);
        padding: 12px;
        width: 60%;
        margin: auto;
        display: block;
        backdrop-filter: blur(10px);
    }

    .answer-box {
        background: rgba(244, 239, 230, 0.08);
        padding: 25px;
        border-radius: 18px;
        border: 1px solid rgba(244, 239, 230, 0.1);
        margin-top: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ---------------- TITLE ----------------

st.title("🧠 AI Research Assistant")


# ---------------- FILE UPLOAD ----------------

uploaded_files = st.file_uploader(
    "Upload PDFs",
    type="pdf",
    accept_multiple_files=True
)


# ---------------- PROCESS PDFs ----------------

if uploaded_files:

    # Clear old database before new upload
    clear_database()

    for uploaded_file in uploaded_files:

        # Save uploaded file
        with open(uploaded_file.name, "wb") as f:
            f.write(uploaded_file.read())

        # Load PDF text
        text = load_pdf(uploaded_file.name)

        # Split text into chunks
        chunks = split_text(text)

        # Skip empty PDFs
        if len(chunks) == 0:
            st.error(f"No text found in {uploaded_file.name}")
            continue

        # Store embeddings
        store_embeddings(
            chunks,
            uploaded_file.name
        )

    st.success("PDFs processed successfully!")


    # ---------------- QUESTION INPUT ----------------

    query = st.text_input(
        "Ask a question"
    )


    # ---------------- QUERY PROCESSING ----------------

    if query:

        documents, metadatas = retrieve_chunks(query)

        answer = generate_answer(
            query,
            documents
        )

        # ---------------- ANSWER ----------------

        st.subheader("Answer")

        st.markdown(
            f"""
            <div class="answer-box">
                {answer}
            </div>
            """,
            unsafe_allow_html=True
        )

        # ---------------- SOURCES ----------------

        st.subheader("Sources")

        for doc, meta in zip(documents, metadatas):

            st.markdown(
                f"""
                **Source:** {meta['source']}

                **Page:** {meta['page']}

                {doc}

                ---
                """
            )