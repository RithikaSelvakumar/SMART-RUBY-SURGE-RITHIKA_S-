import streamlit as st
import tempfile
from lgout import (
    extract_text_from_image,
    extract_text_from_pdf,
    extract_text_from_docx,
    generate_answer,
    vector_store,
)

# Streamlit App Configuration
st.set_page_config(
    page_title="Document & Image Query Retrieval System",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📄 Document & Image Query Retrieval System")
st.write("Extract text from various file formats, store it in a vector store, and query it for relevant answers.")

# -------------------- Extract Text Section -------------------- #
st.header("📝 Extract Text")

file_type = st.selectbox("Select file type:", ["Image", "PDF", "DOCX"])
uploaded_file = st.file_uploader(f"Upload a {file_type} file:", type=["jpg", "jpeg", "png", "pdf", "docx"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_type.lower()}") as temp_file:
        temp_file.write(uploaded_file.read())
        temp_file_path = temp_file.name

    # Extract text based on file type
    extracted_text = None
    if file_type == "Image":
        extracted_text = extract_text_from_image(temp_file_path)
    elif file_type == "PDF":
        extracted_text = extract_text_from_pdf(temp_file_path)
    elif file_type == "DOCX":
        extracted_text = extract_text_from_docx(temp_file_path)

    # If text is extracted, show the "Add to Vector Store" button
    if extracted_text:
        st.text_area("Extracted Text:", extracted_text, height=150)
        if st.button("Add to Vector Store"):
            if vector_store:
                vector_store.add_documents([extracted_text])
                st.success("Text added to vector store!")
            else:
                st.error("Vector store is not initialized.")
    else:
        st.error("Unable to extract text. Please try again.")

# -------------------- Query Text Section -------------------- #
st.header("🔍 Query Text")
query = st.text_input(
    "Ask me anything! 🎙️",
    placeholder="E.g., 'Summarize the document' or 'Find key points from the text'"
)

if query and st.button("Get Answer"):
    with st.spinner("Generating response..."):
        response = generate_answer(query)
    st.subheader("Response:")
    st.write(response)

st.markdown(
    """
    <style>
        footer {visibility: hidden;}
        .stApp {background-color: #171717;}
        
        /* Make text elements white */
        h1, h2, h3, h4, h5, h6, .stTextInput, .stTextArea, .stMarkdown, 
        .stSubheader, .stWrite, .stTitle, .stHeader {
            color: white !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)