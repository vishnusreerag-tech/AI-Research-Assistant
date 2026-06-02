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


# ---------------- SESSION STATE ----------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pdf_processed" not in st.session_state:
    st.session_state.pdf_processed = False


# ---------------- CUSTOM CSS ----------------

st.markdown(
    """
    <style>

    :root {
        --accent: #8b5cf6;
    }

    .stApp {
        background-color: #1f1f1f;
        color: #f4efe6;
    }

    /* Sidebar */

    section[data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #181818 0%,
            #121212 100%
        );
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    /* Main Title */

    .main-title {
        font-size: 42px;
        font-weight: 700;
        color: #f4efe6;
        margin-bottom: 8px;
        text-align: center;
    }

    .subtitle {
        color: #9ca3af;
        margin-bottom: 35px;
        text-align: center;
        font-size: 16px;
    }

    .chat-container {
        max-width: 750px;
        margin: auto;
    }

    /* Chat Messages */

    div[data-testid="stChatMessage"] {

        background: rgba(255,255,255,0.05);

        backdrop-filter: blur(14px);

        border: 1px solid rgba(255,255,255,0.08);

        border-radius: 20px;

        padding: 18px;

        margin-bottom: 16px;

        box-shadow:
            0 4px 20px rgba(0,0,0,0.15);

        transition: all 0.2s ease;
    }

    div[data-testid="stChatMessage"]:hover {

        border: 1px solid rgba(139,92,246,0.35);

        box-shadow:
            0 0 20px rgba(139,92,246,0.12);
    }

    /* Chat Input */

    .stChatInputContainer {

        background-color: #1f1f1f;

        border-top: 1px solid rgba(255,255,255,0.08);
    }

    textarea {

        background: rgba(255,255,255,0.06) !important;

        border: 1px solid rgba(255,255,255,0.10) !important;

        border-radius: 18px !important;

        color: #f4efe6 !important;

        backdrop-filter: blur(10px);
    }

    textarea:focus {

        border: 1px solid var(--accent) !important;

        box-shadow:
            0 0 12px rgba(139,92,246,0.25) !important;
    }

    /* Buttons */

    .stButton > button {

        background: rgba(139,92,246,0.15);

        color: white;

        border: 1px solid rgba(139,92,246,0.35);

        border-radius: 12px;

        transition: 0.2s;
    }

    .stButton > button:hover {

        background: rgba(139,92,246,0.25);

        border-color: rgba(139,92,246,0.6);
    }

    /* File uploader */

    .stFileUploader {

        background: rgba(255,255,255,0.03);

        border-radius: 16px;

        padding: 10px;

        border: 1px solid rgba(255,255,255,0.08);
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.title("🧠 AI Research")

    uploaded_files = st.file_uploader(
        "Upload PDFs",
        type="pdf",
        accept_multiple_files=True
    )

    if uploaded_files:

        clear_database()

        for uploaded_file in uploaded_files:

            with open(uploaded_file.name, "wb") as f:
                f.write(uploaded_file.read())

            text = load_pdf(uploaded_file.name)

            if "pdfs" not in st.session_state:
                st.session_state["pdfs"] = {}

            st.session_state["pdfs"][uploaded_file.name] = text

            chunks = split_text(text)
            if len(chunks) == 0:
                st.error(f"No text found in {uploaded_file.name}")
                continue

            store_embeddings(
                chunks,
                uploaded_file.name
            )

        st.session_state.pdf_processed = True

        st.success("PDFs processed successfully!")

    st.divider()
    # ---------------- AI TOOLS ----------------

    st.subheader("✨ AI Tools")

if st.button("📄 Summarize PDF"):

    if "pdfs" not in st.session_state or len(st.session_state["pdfs"]) == 0:

        st.warning("Upload a PDF first")

    else:

        for filename, text in st.session_state["pdfs"].items():

            summary_prompt = f"""
            Summarize the following document.

            Include:
            - Main topic
            - Key concepts
            - Important points
            - Conclusion

            Document:

            {text[:4000]}
            """

            summary = generate_answer(
                summary_prompt,
                [text[:4000]]
            )

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content":
                    f"## 📄 {filename}\n\n{summary}"
                }
            )

        st.rerun()
if st.button("📝 Generate Notes", key="notes_btn"):

    if "pdfs" not in st.session_state or len(st.session_state["pdfs"]) == 0:

        st.warning("Upload a PDF first")

    else:

        for filename, text in st.session_state["pdfs"].items():

            notes_prompt = f"""
            Create well-structured study notes from this document.

            Format:

            # Title

            ## Main Topics

            ### Key Concepts

            - Important points
            - Definitions
            - Explanations

            ### Summary

            Keep the notes concise and student-friendly.

            Document:

            {text[:4000]}
            """

            notes = generate_answer(
                notes_prompt,
                [text[:4000]]
            )

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": f"## 📝 Notes for {filename}\n\n{notes}"
                }
            )

        st.rerun()
    ...

if st.button("🎯 Generate Quiz", key="quiz_btn"):

    if "pdfs" not in st.session_state or len(st.session_state["pdfs"]) == 0:

        st.warning("Upload a PDF first")

    else:

        for filename, text in st.session_state["pdfs"].items():

            quiz_prompt = f"""
            Create a multiple choice quiz from this document.

            Requirements:
            - Generate 5 MCQs
            - Each question should have 4 options
            - Mention the correct answer
            - Questions should test understanding
            - Keep formatting clean

            Format:

            1. Question

            - A)

            - B)
            
            - C)
            
            - D)

            Answer: B

            Document:

            {text[:3000]}
            """

            quiz = generate_answer(
                quiz_prompt,
                [text[:3000]]
            )

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content":
                    f"## 🎯 Quiz for {filename}\n\n{quiz}"
                }
            )

if st.button("🧠 Create Flashcards", key="flashcards_btn"):

    if "pdfs" not in st.session_state or len(st.session_state["pdfs"]) == 0:

        st.warning("Upload a PDF first")

    else:

        for filename, text in st.session_state["pdfs"].items():

            flashcard_prompt = f"""
            Create study flashcards from this document.

            Requirements:
            - Generate 5 flashcards
            - Each flashcard should contain:
                Question
                Answer
            - Keep answers concise
            - Focus on important concepts

            Format EXACTLY like this in Markdown:

            ### Flashcard 1

            **Q:** What is Artificial Intelligence?

            **A:** Artificial Intelligence is the simulation of human intelligence in machines.

            ### Flashcard 2

            **Q:** What is Machine Learning?

            **A:** Machine Learning is a subset of AI that enables systems to learn from data.

            Document:

            {text[:3000]}
            """

            flashcards = generate_answer(
                flashcard_prompt,
                [text[:3000]]
            )

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content":
                    f"## 🧠 Flashcards for {filename}\n\n{flashcards}"
                }
            )
    ...

if st.button("🗑️ Clear Chat", key="clear_chat_btn"):

    # Clear chat messages
    st.session_state.messages = []

    # Clear uploaded PDFs
    if "pdfs" in st.session_state:
        del st.session_state["pdfs"]

    # Reset PDF processed state
    st.session_state.pdf_processed = False

    # Clear vector database
    clear_database()

    st.rerun()
    ...


# ---------------- MAIN UI ----------------

st.markdown(
    """
    <div class="chat-container">

    <div class="main-title">
    AI Research Assistant
    </div>

    <div class="subtitle">
    Upload PDFs and chat with your documents
    </div>

    </div>
    """,
    unsafe_allow_html=True
)

# ---------------- WELCOME SCREEN ----------------

if (
    len(st.session_state.messages) == 0
    and st.session_state.pdf_processed
):

    st.markdown(
        """
        <div style="text-align:center;padding:40px;">

        <h2>🧠 Welcome to AI Research Assistant</h2>

        <p style="color:#9ca3af;">
        Upload PDFs and ask questions about:
        </p>

        <p>
        📚 Research Papers<br>
        📝 Study Notes<br>
        📖 Books<br>
        📄 Documentation
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

# ---------------- DISPLAY CHAT ----------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# ---------------- CHAT INPUT ----------------

if st.session_state.pdf_processed:

    prompt = st.chat_input(
        "Ask anything about your PDFs..."
    )

    if prompt:

        # User message
        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        with st.chat_message(
        "user",
        avatar="👨‍💻"
    ):
            st.markdown(prompt)

        # Retrieve documents
        documents, metadatas = retrieve_chunks(prompt)

        # Generate answer
        answer = generate_answer(
            prompt,
            documents
        )

        # Assistant message
        with st.chat_message(
    "assistant",
    avatar="🧠"
):

            st.markdown(answer)

            with st.expander("Sources"):

                for doc, meta in zip(documents, metadatas):

                    st.markdown(
                        f"""
                        **Source:** {meta['source']}

                        **Page:** {meta['page']}

                        {doc}

                        ---
                        """
                    )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

else:

    st.info("Upload PDFs from the sidebar to begin.")