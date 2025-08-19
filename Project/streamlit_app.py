import streamlit as st
import uuid
import os
import shutil
import tempfile
from datetime import datetime

# Import required functions
from database_connection import create_application_logs, insert_application_logs
from prompt_defination import regular_assistant, context_aware_assistant
from sql_agent import sql_query
from rag_loaders import file_to_vector_store, folder_creation

# Initialize database
create_application_logs()

def initialize_session():
    """Initialize session state variables"""
    if 'session_id' not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
        folder_creation(st.session_state.session_id)
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

def save_uploaded_file(uploaded_file, session_id):
    """Save uploaded file to session folder"""
    session_folder = f"Files/{session_id}"
    if not os.path.exists(session_folder):
        os.makedirs(session_folder)
    
    file_path = os.path.join(session_folder, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    return uploaded_file.name

def main():
    st.set_page_config(page_title="Mentora - University Assistant", page_icon="🎓", layout="wide")
    
    # Initialize session
    initialize_session()
    
    # Header with styling
    st.markdown("""
    <div style="text-align: center; padding: 1rem; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); border-radius: 10px; margin-bottom: 2rem;">
        <h1 style="color: white; margin: 0;">🎓 Mentora</h1>
        <p style="color: white; margin: 0;">University Students Helper - Academic & Administrative Queries</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write(f"📱 Session ID: `{st.session_state.session_id[:8]}...`")
    
    # Set default mode
    if 'current_mode' not in st.session_state:
        st.session_state.current_mode = "General"
    
    # Mode selection with colored buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        general_mode = st.button("🧠 General", use_container_width=True, 
                                type="primary" if st.session_state.current_mode == "General" else "secondary")
    with col2:
        query_mode = st.button("🗄️ Query", use_container_width=True,
                              type="primary" if st.session_state.current_mode == "Query" else "secondary")
    with col3:
        rag_mode = st.button("📚 RAG", use_container_width=True,
                            type="primary" if st.session_state.current_mode == "RAG" else "secondary")
    
    # Update mode based on button clicks
    if general_mode:
        st.session_state.current_mode = "General"
        st.rerun()
    elif query_mode:
        st.session_state.current_mode = "Query"
        st.rerun()
    elif rag_mode:
        st.session_state.current_mode = "RAG"
        st.rerun()
    
    # Display current mode with styling
    mode_color = {"General": "🧠", "Query": "🗄️", "RAG": "📚"}
    st.markdown(f"""
    <div style="text-align: center; padding: 0.5rem; background-color: #f0f2f6; border-radius: 5px; margin: 1rem 0;">
        <h3 style="margin: 0;">{mode_color[st.session_state.current_mode]} Current Mode: {st.session_state.current_mode}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Mode-specific UI
    if st.session_state.current_mode == "General":
        st.info("**🧠 General AI Mode** - Ask any general questions using AI's built-in knowledge")
        
    elif st.session_state.current_mode == "Query":
        st.info("**🗄️ Database Query Mode** - Ask questions about student database")
        
    elif st.session_state.current_mode == "RAG":
        st.info("**📚 RAG Mode** - Upload documents and ask questions with context memory")
        
        # File upload section
        st.markdown("### 📁 Upload Documents")
        uploaded_files = st.file_uploader(
            "Choose files", 
            accept_multiple_files=True,
            type=['pdf', 'docx', 'txt'],
            help="Upload documents to create a knowledge base"
        )
        
        if uploaded_files:
            if st.button("🔄 Process Files", type="primary"):
                with st.spinner("Processing files..."):
                    processed_files = []
                    for uploaded_file in uploaded_files:
                        try:
                            # Save file
                            filename = save_uploaded_file(uploaded_file, st.session_state.session_id)
                            
                            # Add to vector store
                            result = file_to_vector_store(filename, st.session_state.session_id)
                            processed_files.append(filename)
                            
                        except Exception as e:
                            st.error(f"Error processing {uploaded_file.name}: {str(e)}")
                    
                    if processed_files:
                        st.success(f"✅ Successfully processed: {', '.join(processed_files)}")
    
    # Chat interface with styling
    st.markdown("### 💬 Chat with Mentora")
    
    # Create a container for chat messages
    chat_container = st.container()
    
    with chat_container:
        # Display chat history
        for chat in st.session_state.chat_history:
            with st.chat_message("user"):
                st.write(chat["question"])
            with st.chat_message("assistant"):
                st.write(chat["answer"])
    
    # Chat input with custom styling
    user_input = st.chat_input("💬 Ask Mentora anything...")
    
    if user_input:
        # Add user message to chat
        with st.chat_message("user"):
            st.write(user_input)
        
        # Process based on current mode
        with st.chat_message("assistant"):
            with st.spinner("🤔 Mentora is thinking..."):
                try:
                    if st.session_state.current_mode == "General":
                        # General AI response
                        answer = regular_assistant(user_input)
                        model_used = "gemma3:270m"
                        
                    elif st.session_state.current_mode == "Query":
                        # Database query
                        answer = sql_query(user_input)
                        model_used = "gemma2:2b"
                        
                    elif st.session_state.current_mode == "RAG":
                        # RAG response
                        answer = context_aware_assistant(user_input, st.session_state.session_id)
                        model_used = "llama3.2:latest"
                    
                    # Display answer with formatting
                    st.markdown(f"**Mentora:** {answer}")
                    
                    # Log to database
                    insert_application_logs(st.session_state.session_id, user_input, answer, model_used)
                    
                    # Add to chat history
                    st.session_state.chat_history.append({
                        "question": user_input,
                        "answer": answer,
                        "mode": st.session_state.current_mode
                    })
                    
                except Exception as e:
                    error_msg = f"❌ Sorry, I encountered an error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.chat_history.append({
                        "question": user_input,
                        "answer": error_msg,
                        "mode": st.session_state.current_mode
                    })
    
    # Sidebar with session info and mode-specific notes
    with st.sidebar:
        st.markdown("### 📊 Session Info")
        st.write(f"**Session ID:** {st.session_state.session_id[:8]}...")
        st.write(f"**Current Mode:** {st.session_state.current_mode}")
        st.write(f"**Messages:** {len(st.session_state.chat_history)}")
        
        st.markdown("---")
        
        # Mode-specific sidebar notes
        if st.session_state.current_mode == "General":
            st.markdown("### 🧠 General Mode Notes")
            st.info("""
            **Memory:** No context memory - each question is independent
            
            **Usage:** Ask any general questions about academics, university life, or any topic
            """)
            
        elif st.session_state.current_mode == "Query":
            st.markdown("### 🗄️ Query Mode Notes")
            st.warning("""
            **Memory:** No context memory - each query is independent
            
            **Database Access:** Multiple student and academic tables
            
            **Available Tables & Fields:**
            
            **📚 Student Sessions (2021-2023):**
            - student_id
            - student_name  
            - student_cgpa
            - student_hall_allotment
            
            **🏆 CSE Results (Previous 10 years):**
            - id
            - session_name
            - student_id
            - student_name
            - student_cgpa
            - is_topper
            - result
            
            **💰 Semester Fee Catalog:**
            - fee_id
            - category
            - amount
            
            **Example Queries:**
            - "Students with CGPA > 3.5 in 2021"
            - "All CSE toppers from last 10 years"
            - "Fee structure for different categories"
            - "CSE results for session 2020"
            """)
            
        elif st.session_state.current_mode == "RAG":
            st.markdown("### 📚 RAG Mode Notes")
            st.success("""
            **Memory:** Full context memory - remembers previous conversations
            
            **AI Behavior:** Mentora will mix answers from:
            - Uploaded documents
            - Built-in AI knowledge
            - Previous conversation context
            
            **Best For:** Document analysis, research questions, detailed academic discussions
            """)
        
        st.markdown("---")
        
        # Session controls
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 New Session", use_container_width=True):
                # Clear session state
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
        
        with col2:
            if st.button("🗑️ Clear Chat", use_container_width=True):
                st.session_state.chat_history = []
                st.rerun()

if __name__ == "__main__":
    main()
