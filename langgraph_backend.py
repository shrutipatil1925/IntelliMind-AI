from __future__ import annotations

from langgraph.graph import START, END, StateGraph
from typing import TypedDict, Annotated, Dict, Optional, Any
from langchain_core.messages import BaseMessage,SystemMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
import sqlite3
import requests
import os
import tempfile

load_dotenv()

llm = ChatGoogleGenerativeAI(model = "gemini-3.1-flash-lite")
embedding = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2")

#---------PDF retriever store (per thread)-------------

_THREAD_RETRIEVERS: Dict[str, Any] = {}
_THREAD_METADATA: Dict[str, dict] = {}

def _get_retriever(thread_id: Optional[str]):
    """Fetch the retriever for a thread if available."""
    if thread_id and thread_id in _THREAD_RETRIEVERS:
        return _THREAD_RETRIEVERS[thread_id]
    return None

def ingest_pdf(file_bytes:bytes, thread_id:str, filename: Optional[str] = None) -> dict:
    print("Received bytes:", len(file_bytes))
    
    """Build a FAISS retriever for the uploaded PDF and store it for the thread.
    Returns a summary dict that can be surface in the UI.
    """
    
    if not file_bytes:
        raise ValueError("No bytes recieved for ingestion.")
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(file_bytes)
        temp_file.flush()
        temp_path = temp_file.name
        
        print("Temp file:", temp_path)
        print("Temp size:", os.path.getsize(temp_path))
        
        try:
            loader = PyPDFLoader(temp_path)
            docs = loader.load()
            
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000, chunk_overlap=200, separators=["\n\n","\n"," ",""]
            )
            chunks = splitter.split_documents(docs)
            
            vector_store = FAISS.from_documents(chunks, embedding)
            retriever = vector_store.as_retriever(
                search_type='similarity', search_kwargs={"k":4}
            )
            
            _THREAD_RETRIEVERS[str(thread_id)] = retriever
            _THREAD_METADATA[str(thread_id)] = {
                "filename":filename or os.path.basename(temp_path),
                "documents":len(docs),
                "chunks": len(chunks),
            }
            return{
                "filename": filename or os.path.basename(temp_path),
                "documents": len(docs),
                "chunks": len(chunks),
            }
            
        finally:
            try:
                os.remove(temp_path)
            except OSError:
                pass

#-----------------------Tools-------------------------------------------
search_tool = DuckDuckGoSearchRun(region="us-en")

@tool
def calculator(first_num:float, second_num: float, operation:str) -> dict:
    """
    Perform  a basic arithmatic operation on two numbers.
    Supported opeartion: add, sub, mul , div
    """
    
    try:
        if operation == "add":
            result = first_num + second_num
        elif operation == "sub":
            result = first_num - second_num
        elif operation == "mul":
            result = first_num * second_num
        elif operation == "div":
            if second_num == 0:
                return {"error": "Division by zero is not allowed"}
            result = first_num / second_num
        else:
            return {"error": f"Unsupported operation '{operation}'"}
        
        return {"first_num": first_num, "second_num": second_num, "operation": operation, "result": result}
    except Exception as e:
        return {"error": str(e)}
    
@tool
def get_stock_price(symbol:str) -> dict:
    """
    Fetch latest stock price for a given symbol (e.g. 'AAPL', 'TSLA') 
    using Alpha Vantage with API key in the URL.
    """
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey=C9PE94QUEW9VWGFM"
    r = requests.get(url)
    return r.json()

@tool
def rag_tool(query:str, thread_id:Optional[str] = None) -> dict:
    """
    Retrieve relevant information from the uploaded PDF for this chat thread.
    Always include the thread_id when calling this tool.
    """
    retriever = _get_retriever(thread_id)
    
    if retriever is None:
        return{
            "error":"No document indexed for this chat. Upload a PDF first.",
            "query":query,
        }
        
    result = retriever.invoke(query)
    context = [doc.page_content for doc in result]
    metadata = [doc.metadata for doc in result]
    
    return {
        "query": query,
        "context": context,
        "metadata": metadata,
        "source_file": _THREAD_METADATA.get(str(thread_id), {}).get("filename"),
    }

    
tools = [search_tool, calculator, get_stock_price, rag_tool]
llm_with_tools = llm.bind_tools(tools)

#--------------generate thread title-----------------------
def generate_chat_title(first_message: str) -> str:
    prompt = f"""
    Generate a concise conversation title.

    Rules:
    - Maximum 3 words
    - No punctuation
    - No quotes
    - Title Case
    - Return ONLY the title

    User message:
    {first_message}
    """
    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        if isinstance(response.content, list):
            title = "".join(
                part.get("text","")
                for part in response.content
                if isinstance(part, dict)
            )
        else:
            title = response.content
        return title.strip()
    
    except Exception:
        words = first_message.split()
        return " ".join(words[:3]).title()

#--------------------state---------------------------------
class chatState(TypedDict):
    messages : Annotated[list[BaseMessage], add_messages]
  
#---------------------node--------------------------------  
def chat_node(state: chatState, config=None):
    """LLM node that may answer or request a tool call."""
    thread_id = None
    if config and isinstance(config,dict):
        thread_id=config.get("configurable",{}).get("thread_id")
        
    system_message = SystemMessage(
        content=(
            "You are a helpful assistant.For questions about the uploaded PDF, call"
            "The `rag_tool` and include the thread_id"
            f"`{thread_id}`. you can also use the web search, stock proce and calculator tool when helpful"
            "If no document is available, ask the user to upload a PDF"
            "Generate a answer in bullet form, heading form "
            "Use emojis in answer"  
        )
    )
    messages = [system_message,*state['messages']]
    response = llm_with_tools.invoke(messages, config=config)
    return {'messages':[response]}

conn = sqlite3.connect(database='chatbot.db', check_same_thread=False)

cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS thread_titles (
        thread_id TEXT PRIMARY KEY, title TEXT
    )  """)

conn.commit()

checkpointer = SqliteSaver(conn=conn)

#---------------------------graph----------------------------
graph = StateGraph(chatState)

tool_node = ToolNode(tools)

graph.add_node("chat_node", chat_node)
graph.add_node("tools",tool_node)
graph.add_edge(START, "chat_node")
graph.add_conditional_edges("chat_node", tools_condition)
graph.add_edge("tools","chat_node")

chatbot = graph.compile(checkpointer=checkpointer)

def retrieve_all_threads():
    all_threads = set()
    
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config['configurable']['thread_id'])
        
    return list(all_threads)

def thread_has_document(thread_id:str) -> bool:
    return str(thread_id) in _THREAD_RETRIEVERS

def thread_document_metadata(thread_id:str) -> dict:
    return _THREAD_METADATA.get(str(thread_id),{})

#delete thread
def delete_thread(thread_id):
    cursor = conn.cursor()
    
    cursor.execute(
        "DELETE FROM checkpoints WHERE thread_id = ?",
        (thread_id,)
    )
    
    cursor.execute(
        "DELETE FROM writes WHERE thread_id=?",
        (thread_id,)
    )
    
    cursor.execute(
        "DELETE FROM thread_titles WHERE thread_id=?",
        (thread_id,)
        )
    conn.commit()
    
#Save title    
def save_thread_title(thread_id:str, title:str):
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT OR REPLACE INTO thread_titles(thread_id, title)
        VALUES(?,?)
        """, (thread_id, title))
    
    conn.commit()
    
#Get title
def get_thread_title(thread_id: str):
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT title FROM thread_titles WHERE thread_id = ?
        """,(thread_id,))
    
    row = cursor.fetchone()
    
    if row:
        return row[0]
    return "New Chat"
