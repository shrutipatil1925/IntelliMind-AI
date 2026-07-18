import streamlit as st 
from langgraph_backend import (chatbot, retrieve_all_threads,
                               thread_document_metadata, ingest_pdf,
                               delete_thread, get_thread_title, 
                               save_thread_title, generate_chat_title)
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
import uuid

from PIL import Image

logo = Image.open("images/chatbot.png")


st.set_page_config(
    page_title="IntelliMind AI",
    page_icon="images/chatbot.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

def load_css():
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        
load_css()

def generate_thread_id():
    return str(uuid.uuid4())

def reset_chat():
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id
    add_thread(st.session_state['thread_id'])
    save_thread_title(thread_id, "New Chat")
    st.session_state['message_history'] = []

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)
        
def load_conversation(thread_id):
    state = chatbot.get_state(config={'configurable':{'thread_id':thread_id}})
    #check if messages key exists in state values, return empty list if not
    return state.values.get('messages',[])
#---------------------------------------session setup---------------------------------
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()
    
if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = retrieve_all_threads()
    
if "ingested_doc" not in st.session_state:
    st.session_state["ingested_doc"] = {}

add_thread(st.session_state['thread_id'])

current_title = get_thread_title(st.session_state["thread_id"])

if current_title == "New Chat":
    save_thread_title(st.session_state["thread_id"], "New Chat")
    
thread_key = str(st.session_state["thread_id"])
thread_docs = st.session_state["ingested_doc"].setdefault(thread_key,{})
threads = st.session_state["chat_threads"][::-1]
selected_thread = None



#------------------------sidebar----------------------------------------------
st.sidebar.image(
    logo, width=80
)

st.sidebar.markdown("""
    <h1 style="text-align:center; font-size:35px;"> IntelliMind AI</h1>
    
    <p style="text-align:center; color:lightgray;">
    Chat • PDF • Search • Tools
    </p>
    """, unsafe_allow_html=True)

st.sidebar.divider()

st.sidebar.markdown(f"### {get_thread_title(thread_key)}")

if st.sidebar.button('➕', use_container_width=True):
    reset_chat()
    st.rerun()
    
uploaded_pdf = st.sidebar.file_uploader("📤Upload PDF ", type=["pdf"])
if uploaded_pdf:
    if uploaded_pdf.name in thread_docs:
        st.sidebar.info(f"`{uploaded_pdf.name}` already processed for this chat.")
    else:
        with st.spinner("Indexing PDF..."):
            
            pdf_bytes = uploaded_pdf.getvalue()

            print("File name:", uploaded_pdf.name)
            print("File size:", uploaded_pdf.size)
            print("Bytes length:", len(pdf_bytes))

            summary = ingest_pdf(
            uploaded_pdf.getvalue(),
            thread_id=thread_key,
            filename = uploaded_pdf.name,
            )
            
            thread_docs[uploaded_pdf.name] = summary
        st.sidebar.success("✅ PDF indexed successfully!")

st.sidebar.subheader(f"Coversations({len(threads)})")
if not threads:
    st.sidebar.write("No past conversations yet.")
else:
    for thread_id in threads:
        icon_col, btn_col, del_col = st.sidebar.columns([1,5,1])
        title = get_thread_title(thread_id)
        if len(title) > 25:
            title = title[:25] + "..."
            
        with icon_col:
            if thread_id == st.session_state["thread_id"]:
                st.image("images/social-media.png", width=18)
            else:
                st.write("")
                
        with btn_col:
            if st.button(title,
                     key=f"side-thread-{thread_id}",
                     use_container_width=True):
                selected_thread = thread_id

        with del_col:
            if st.button("✖️",
                     key=f"delete-{thread_id}",
                     help="Delete chat"):
                delete_thread(thread_id)
                st.session_state["chat_threads"].remove(thread_id)

                if thread_id == st.session_state["thread_id"]:
                    reset_chat()

                st.rerun()
                                    
#--------------------------------loading conversation history------------------------

for message in st.session_state["message_history"]:
    avatar = "images/user.png" if message["role"] == "user" else "images/ai.png"
    
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# -------- Welcome Screen --------
if len(st.session_state["message_history"]) == 0:

    # Center the entire content
    left, center, right = st.columns([2, 4, 2])

    with center:

        # ---------- Logo + Title ----------
        logo_col, title_col = st.columns([1, 6], vertical_alignment="center")

        with logo_col:
            st.image("images/chatbot.png", width=70)

        with title_col:
            st.markdown("""
            <h1 style="
                margin:0;
                font-size:52px;
                color:white;
                line-height:1.2;
            ">
                IntelliMind AI
            </h1>
            """, unsafe_allow_html=True)

        # ---------- Tagline ----------
        st.markdown("""
        <p style="
            text-align:center;
            color:#9CA3AF;
            font-size:20px;
            margin-top:8px;
            margin-bottom:40px;
        ">
            Your Smart AI Assistant
        </p>
        """, unsafe_allow_html=True)

        # ---------- Features ----------
        col1, col2 = st.columns(2, gap="large")

        # LEFT SIDE
        with col1:

            icon, text = st.columns([1,5], vertical_alignment="center")

            with icon:
                st.image("images/file.png", width=28)

            with text:
                st.markdown("**Chat with PDFs**")

            st.divider()

            icon, text = st.columns([1,5], vertical_alignment="center")

            with icon:
                st.image("images/search.png", width=28)

            with text:
                st.markdown("**Search the Web**")

        # RIGHT SIDE
        with col2:

            icon, text = st.columns([1,5], vertical_alignment="center")

            with icon:
                st.image("images/calculator.png", width=28)

            with text:
                st.markdown("**Calculator**")

            st.divider()

            icon, text = st.columns([1,5], vertical_alignment="center")

            with icon:
                st.image("images/graph.png", width=28)

            with text:
                st.markdown("**Stock Prices**")
    
user_input = st.chat_input('Type here')

if user_input:
    
    thread_id = st.session_state["thread_id"]
     
    if get_thread_title(thread_id) == "New Chat":
        # save_thread_title(thread_id, user_input[:20])
        title = generate_chat_title(user_input)
        save_thread_title(thread_id, title)
    
    #add msg to history 
    st.session_state['message_history'].append({'role':'user','content':user_input})   
    # st.rerun()
    
    with st.chat_message('user', avatar="images/user.png"):
        st.markdown(user_input)
        
    CONFIG = {
        "configurable":{"thread_id":st.session_state["thread_id"]},
        "metadata":{
            "thread_id":st.session_state["thread_id"]
        },
        "run_name": "chat_turn"
    }
    #------------------------------Assistant streaming block------------------------------
    with st.chat_message('assistant', avatar="images/ai.png"):
            
        thinking = st.empty()
        thinking.info(" Thinking...")
        
        def ai_only_stream():
            
            first_chunk = True
            
            for message_chunk, metadata in chatbot.stream(
                {'messages':[HumanMessage(content=user_input)]},
                    config = CONFIG,
                    stream_mode = 'messages',
            ):
                    
                if isinstance(message_chunk, AIMessage):
                    
                    if first_chunk:
                        thinking.empty()
                        first_chunk = False
                        
                    if isinstance(message_chunk.content, list):
                        for item in message_chunk.content:
                            if isinstance(item,dict) and item.get("type") == "text":
                                yield item["text"]
                    elif isinstance(message_chunk.content, str):
                        yield message_chunk.content
                        
        ai_message = st.write_stream(ai_only_stream())

#----------debug 2---------------------------------
        state = chatbot.get_state(CONFIG)

        #add msg to history
        st.session_state['message_history'].append({'role':'assistant','content':ai_message})
        
st.divider()

if selected_thread:
    st.session_state["thread_id"] = selected_thread
    messages = load_conversation(selected_thread)
    
    temp_messages = []  
    for msg in messages:
        if isinstance(msg, HumanMessage):
            temp_messages.append({
                "role":"user",
                "content":msg.text
            })
        elif isinstance(msg, AIMessage):
            
            if msg.tool_calls:
                continue
            
            content = msg.content
            
            if isinstance(content, list):
                text = ""
                
                for item in content:
                    if isinstance(item,dict) and item.get("type") == "text":
                        text += item.get("text","")
                        
            else:
                text = content
            
            temp_messages.append({
                "role":"assistant",
                "content":text
            })
            
        elif isinstance(msg, ToolMessage):
            continue
        
    st.session_state["message_history"] = temp_messages
    st.session_state["ingested_doc"].setdefault(str(selected_thread),{})
    st.rerun()