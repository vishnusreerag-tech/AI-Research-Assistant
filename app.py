import streamlit as st

from utils.pdf_loader import load_pdf
from utils.text_splitter import split_text
from utils.vector_store import (
    store_embeddings,
    retrieve_chunks
)
from utils.generator import generate_answer


# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🧠",
    layout="wide"
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

        # ---------------- ANSWER ----------------

        st.subheader("Answer")

        st.write(answer)