import streamlit as st

from utils.pdf_loader import load_pdf
from utils.text_splitter import split_text
from utils.embeddings import create_embeddings, create_query_embedding
from utils.retriever import retrieve_chunks
from utils.generator import generate_answer

st.title("AI Research Assistant")

uploaded_file = st.file_uploader(
    "Upload a PDF",
    type="pdf"
)

if uploaded_file:

    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.read())

    text = load_pdf("temp.pdf")

    chunks = split_text(text)

    embeddings = create_embeddings(chunks)

    query = st.text_input("Ask a question")

    if query:

        query_embedding = create_query_embedding(query)

        relevant_chunks = retrieve_chunks(
            query_embedding,
            embeddings,
            chunks
        )

        answer = generate_answer(
            query,
            relevant_chunks
        )

        st.subheader("Answer")

        st.write(answer)