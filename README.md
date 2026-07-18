# IntelliMind AI

IntelliMind AI is an intelligent AI-powered chatbot built using **LangGraph**, **LangChain**, **Google Gemini**, and **Streamlit**. It provides conversational AI along with Retrieval-Augmented Generation (RAG) for PDFs, web search, stock price lookup, calculator functionality, and persistent conversation history.

##  Features

-  AI Chat Assistant
-  Chat with PDF Documents (RAG)
-  Web Search
-  Calculator Tool
-  Stock Price Lookup
-  Chat History
-  Automatic Conversation Titles
-  Beautiful Streamlit Interface
-  Real-time Streaming Responses

## Tech Stack

### Frontend
- Streamlit
- HTML
- CSS

### Backend
- Python
- LangGraph
- LangChain
- Google Gemini API

### Vector Database
- FAISS

### Embeddings
- Gemini Embedding Model

### Tools
- DuckDuckGo Search
- Alpha Vantage Stock API

### Database
- SQLite

---

## 📂 Project Structure

```
IntelliMind-AI/
│
├── images/
│
├── langgraph_backend.py
├── langgraph_frontend.py
├── chatbot.db
├── style.css
├── requirements.txt
├── .env
├── README.md
└── .gitignore
```

---

##  Installation

### Clone Repository

```bash
git clone https://github.com/shrutipatil1925/IntelliMind-AI.git

cd IntelliMind-AI
```

---

### Create Virtual Environment

Windows

```bash
python -m venv venv
```

Activate

```bash
venv\Scripts\activate
```

---

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Environment Variables

Create a `.env` file.

```
GOOGLE_API_KEY=YOUR_GEMINI_API_KEY
```

---

### Run Application

```bash
streamlit run langgraph_frontend.py
```

## Future Improvements

- Voice Assistant
- Image Understanding
- Authentication
- Multi-PDF Support
- Cloud Deployment
- Docker Support
- Dark / Light Themes

---

## Author

Shruti Patil