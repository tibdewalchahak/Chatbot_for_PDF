import os
os.environ['STREAMLIT_SERVER_FILE_WATCHER_TYPE'] = 'none'

import streamlit as st
import tempfile
from pdf_utils import extract_text_from_pdf, chunk_text
from rag_utils import build_faiss_index, search, generate_answer_with_groq

st.set_page_config(page_title="PDF Chatbot")

# Suppress torch watcher warnings
os.environ['STREAMLIT_SERVER_FILE_WATCHER_TYPE'] = 'none'

# Initialize session state
if 'processed' not in st.session_state:
    st.session_state.processed = False
if 'temp_files' not in st.session_state:
    st.session_state.temp_files = []
if 'file_names' not in st.session_state:
    st.session_state.file_names = []
if 'messages' not in st.session_state:
    st.session_state.messages = []

uploaded_files = st.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True)

if uploaded_files and not st.session_state.processed:
    with st.spinner("Processing PDFs..."):
        all_text = ""
        temp_files = []
        file_names = []
        
        for uploaded_file in uploaded_files:
            # Save each uploaded file to a temporary location
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            temp_file.write(uploaded_file.read())
            temp_file.close()
            
            pdf_path = temp_file.name
            temp_files.append(pdf_path)
            file_names.append(uploaded_file.name)
            
            # Extract text from this PDF
            text = extract_text_from_pdf(pdf_path)
            all_text += f"\n\n--- Document: {uploaded_file.name} ---\n{text}"
        
        st.session_state.temp_files = temp_files
        st.session_state.file_names = file_names
        
        # Chunk the combined text and build index
        chunks = chunk_text(all_text)
        build_faiss_index(chunks)
        
        st.session_state.processed = True
        st.success(f"Processed {len(uploaded_files)} PDF(s) successfully! You can now start chatting.")
        
        # Display uploaded files
        st.subheader("Uploaded Documents:")
        for name in st.session_state.file_names:
            st.write(f"- {name}")

if st.session_state.processed:
    st.subheader("Chat with your PDF")
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask a question about the PDF..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                top_chunks = search(prompt)
                answer = generate_answer_with_groq(prompt, top_chunks)
                if answer:
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    error_msg = "Sorry, I couldn't generate an answer. Please try again."
                    st.markdown(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

# Cleanup on rerun or close
for temp_file in st.session_state.temp_files:
    if temp_file and os.path.exists(temp_file):
        try:
            os.unlink(temp_file)
        except:
            pass