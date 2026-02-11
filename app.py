"""
RAG Pipeline - Streamlit Application
Multi-language document Q&A system
"""

import warnings
warnings.filterwarnings('ignore')

import streamlit as st
from pathlib import Path

from src.document_processor import DocumentProcessor
from src.embeddings_hf import EmbeddingGenerator
from src.vector_store import VectorStore
from src.generator import ResponseGenerator

# Page config
st.set_page_config(
    page_title="RAG Document Q&A",
    page_icon="📚",
    layout="wide"
)

# Add CSS for proper Arabic text rendering
st.markdown("""
<style>
    /* Force RTL for Arabic content */
    .stMarkdown p, .stMarkdown div, .stMarkdown ul, .stMarkdown ol {
        direction: rtl;
        text-align: right;
        unicode-bidi: embed;
    }
    
    /* Keep English LTR when detected */
    .stMarkdown p:has(> :first-child:not([lang="ar"])) {
        direction: ltr;
        text-align: left;
    }
    
    /* Fix list formatting for Arabic */
    .stMarkdown ul, .stMarkdown ol {
        padding-right: 2rem;
        padding-left: 0;
    }
    
    /* Better Arabic font rendering */
    * {
        font-family: 'SF Pro', 'Segoe UI', 'Tahoma', 'Arial', sans-serif;
        text-rendering: optimizeLegibility;
        -webkit-font-smoothing: antialiased;
    }
    
    /* Fix expander text */
    .streamlit-expanderHeader, .streamlit-expanderContent {
        direction: rtl;
        text-align: right;
    }
    
    /* Keep code blocks LTR */
    code, pre {
        direction: ltr !important;
        text-align: left !important;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("📚 RAG ststem")
st.markdown("Upload documents and ask questions in English or Arabic")

# Initialize session state
if 'vector_store' not in st.session_state:
    st.session_state.vector_store = None
if 'embedder' not in st.session_state:
    st.session_state.embedder = None
if 'generator' not in st.session_state:
    st.session_state.generator = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'documents_loaded' not in st.session_state:
    st.session_state.documents_loaded = False

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Load existing database option
    if Path("vector_store").exists():
        if st.button("📂 Load Existing Database"):
            with st.spinner("Loading vector database..."):
                st.session_state.vector_store = VectorStore(dimension=1024)
                st.session_state.vector_store.load("vector_store")
                st.session_state.embedder = EmbeddingGenerator(model_name="intfloat/multilingual-e5-large")
                st.session_state.generator = ResponseGenerator()
                st.session_state.documents_loaded = True
                st.success(f"✅ Loaded {len(st.session_state.vector_store.texts)} documents")
    
    st.markdown("---")
    
    # File upload
    st.header("Upload Documents")
    uploaded_files = st.file_uploader(
        "Choose PDF, DOCX, or TXT files",
        type=['pdf', 'docx', 'txt'],
        accept_multiple_files=True
    )
    
    if uploaded_files and st.button("Process Documents"):
        with st.spinner("Processing documents..."):
            # Save uploaded files
            upload_dir = Path("temp_uploads")
            upload_dir.mkdir(exist_ok=True)
            
            file_paths = []
            for uploaded_file in uploaded_files:
                file_path = upload_dir / uploaded_file.name
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                file_paths.append(str(file_path))
            
            # Process documents
            processor = DocumentProcessor()
            chunks = processor.load_documents(file_paths)
            
            # Generate embeddings
            st.info("Generating embeddings...")
            embedder = EmbeddingGenerator(model_name="intfloat/multilingual-e5-large")
            texts, embeddings, metadatas = embedder.embed_documents(chunks)
            
            # Build vector store
            st.info("Building vector store...")
            vector_store = VectorStore(dimension=1024)
            vector_store.add_documents(texts, embeddings, metadatas)
            
            # Save
            vector_store.save("vector_store")
            
            # Store in session
            st.session_state.vector_store = vector_store
            st.session_state.embedder = embedder
            st.session_state.generator = ResponseGenerator()
            st.session_state.documents_loaded = True
            
            st.success(f"✅ Processed {len(chunks)} chunks from {len(uploaded_files)} documents")
    
    st.markdown("---")
    
    # Settings
    st.header("🔧 Settings")
    top_k = st.slider("Number of relevant chunks", 1, 10, 3)
    
    if st.button("🗑️ Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()

# Main area
if not st.session_state.documents_loaded:
    st.info("👆 Upload documents or load existing database from the sidebar to get started")
else:
    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "sources" in message:
                with st.expander("📄 View Sources"):
                    for i, source in enumerate(message["sources"], 1):
                        st.markdown(f"**Source {i}:** {source['file']} (Page {source['page']})")
                        st.caption(f"Distance: {source['distance']:.4f}")
                        st.text(source['text'][:200] + "...")
                        st.markdown("---")
    
    # Query input
    query = st.chat_input("Ask a question about your documents...")
    
    if query:
        # Add user message
        st.session_state.chat_history.append({"role": "user", "content": query})
        
        with st.chat_message("user"):
            st.markdown(query)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Searching documents..."):
                # Retrieve
                query_emb = st.session_state.embedder.generate_embedding(query)
                results = st.session_state.vector_store.search(query_emb, k=top_k)
                
            # Generate with streaming
            response_placeholder = st.empty()
            full_response = ""
            
            # Stream the response
            for chunk in st.session_state.generator.generate_stream(
                query, 
                results, 
                chat_history=st.session_state.chat_history[:-1]  # Exclude current question
            ):
                full_response += chunk
                response_placeholder.markdown(full_response + "▌")
            
            # Final response without cursor
            response_placeholder.markdown(full_response)
            
            # Show sources
            sources = []
            for result in results:
                sources.append({
                    'file': result['metadata']['source_file'],
                    'page': result['metadata']['page'],
                    'distance': result['distance'],
                    'text': result['text']
                })
            
            with st.expander("📄 View Sources"):
                for i, source in enumerate(sources, 1):
                    st.markdown(f"**Source {i}:** {source['file']} (Page {source['page']})")
                    st.caption(f"Distance: {source['distance']:.4f}")
                    #st.text(source['text'][:200] + "...")
                    st.markdown("---")
        
        # Add assistant message
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": full_response,
            "sources": sources
        })