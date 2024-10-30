import streamlit as st
from getRAG import user_input
import asyncio

async def getRag(text, database):
    return await user_input(text, database)

if 'page' not in st.session_state:
    st.session_state.page = "Home"

# Function to display chat interface
def chat_interface(surgeryBook, database):
    chat = []
    # Accept user input
    prompt = st.chat_input("Ask your question")

    if prompt:
        # Add user message to chat history
        chat.append({"role": "user", "content": prompt})

        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(f"**You:** {prompt}")

        # Display loading message
        loading_message_placeholder = st.empty()
        loading_message_placeholder.markdown("**Loading...**")

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            response = loop.run_until_complete(getRag(prompt, database))
            st.markdown(f"**Assistant:** {response}")

        # Clear loading message and display response
        loading_message_placeholder.empty()
        chat.append({"role": "assistant", "content": response})

    # Book view button to display the uploaded file's content
    # if st.button("📖 View Book"):
    #     st.text_area("Book Content", surgeryBook, height=400, disabled=True)
    st.download_button(label="📖 Download Book", data=surgeryBook, file_name=surgeryBook, mime="application/pdf")

# Main application
st.set_page_config(page_title="Doctor's Study Assistant", layout="wide")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Go to", ["Home", "Surgery Book"])

# Page navigation logic
if page == "Home":
    st.title("Welcome to Medi-Help")
    st.write("Medi-Help is an AI-driven solution designed to assist doctors with their studies. It provides an easy way to ask questions and receive answers based on their medical book content.")
    st.write("""
        - **Study Assistant:** Read the medical books or start asking questions.
        - **Interactive QA Chat:** Interact with the content through a question-answering chat interface.
             


                        ---BY HP21
    """)

elif page == "Surgery Book":
    st.title("Surgery Chat")
    st.session_state.page = "Rag"
    chat_interface("Books\\SRB's Manual of Surgery 5th Edition.pdf", "SurgeryBook")
