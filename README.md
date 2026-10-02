# IntelliMind AI 🤖🧠

> A multi-tool AI assistant that combines conversational AI, document retrieval, web search, calculations, and real-time information through tool calling.

**IntelliMind AI** is an AI-powered assistant designed to go beyond simple chatbot conversations. It can understand user queries, decide when external tools are required, retrieve information from uploaded documents, perform calculations, search the web, and fetch current stock prices.

The project demonstrates how **LLMs, RAG, tool calling, and stateful conversations** can be combined to build a practical AI assistant.

---

## 🚀 Features

### 💬 Conversational AI

IntelliMind AI supports natural-language conversations with an LLM.

Users can ask general questions and continue the conversation using contextual chat history.

---

### 📚 Document Question Answering

Upload documents and ask questions about their content.

The system uses a **Retrieval-Augmented Generation (RAG)** approach:

```text
Document
   ↓
Text Extraction
   ↓
Chunking
   ↓
Embeddings
   ↓
Vector Search
   ↓
Relevant Context
   ↓
LLM
   ↓
Answer
```

This allows the assistant to answer questions using information from the user's documents.

---

### 🔎 Web Search

When a question requires external or current information, IntelliMind AI can use a web-search tool instead of relying only on the LLM's internal knowledge.

Example:

```text
User:
What are the latest developments in artificial intelligence?

        ↓

AI decides that external information is required

        ↓

Web Search Tool

        ↓

Search Results

        ↓

LLM

        ↓

Answer
```

---

### 🧮 Calculator Tool

The assistant can use a calculator tool for mathematical operations.

Example:

```text
User:
What is 125 * 48 + 250?

        ↓

Calculator Tool

        ↓

6250
```

Using a dedicated calculation tool helps avoid relying on the LLM for arithmetic.

---

### 📈 Stock Price Tool

IntelliMind AI can retrieve current stock-price information through a stock-price tool.

Example:

```text
User:
What is the current stock price of Apple?

        ↓

Stock Price Tool

        ↓

Current Market Data

        ↓

AI Response
```

This demonstrates how an AI assistant can connect an LLM with external real-time data sources.

---

### 🧠 Intelligent Tool Selection

One of the main ideas behind IntelliMind AI is allowing the LLM to decide **which tool should be used for a particular query**.

```text
                         User Query
                              │
                              ▼
                         ┌─────────┐
                         │   LLM   │
                         └────┬────┘
                              │
              ┌───────────────┼────────────────┐
              │               │                │
              ▼               ▼                ▼
         Document          Web Search      Calculator
         Retrieval                            │
              │               │                │
              └───────────────┼────────────────┘
                              ▼
                         Tool Result
                              │
                              ▼
                         ┌─────────┐
                         │   LLM   │
                         └────┬────┘
                              │
                              ▼
                           Answer
```

The assistant does not need to use the same workflow for every question.

---

### 🧵 Stateful Conversations

IntelliMind AI maintains conversation state so that users can ask follow-up questions.

For example:

```text
User:
What is Retrieval-Augmented Generation?

AI:
RAG is...

User:
Why is it useful?

AI:
It is useful because...
```

The second question can be interpreted using the previous conversation context.

---

# 🏗️ System Architecture

```text
                         ┌───────────────┐
                         │     User      │
                         └───────┬───────┘
                                 │
                                 ▼
                      ┌────────────────────┐
                      │   IntelliMind AI   │
                      │   AI Assistant     │
                      └─────────┬──────────┘
                                │
                                ▼
                         ┌─────────────┐
                         │     LLM     │
                         └──────┬──────┘
                                │
                 ┌──────────────┼──────────────┐
                 │              │              │
                 ▼              ▼              ▼
          ┌────────────┐ ┌────────────┐ ┌────────────┐
          │    RAG     │ │ Web Search │ │ Calculator │
          │   Tool     │ │    Tool    │ │    Tool    │
          └─────┬──────┘ └──────┬─────┘ └────────────┘
                │               │
                ▼               ▼
          ┌────────────┐  ┌────────────┐
          │ Documents  │  │ Web Data   │
          └────────────┘  └────────────┘

                         ┌──────────────┐
                         │ Stock Price  │
                         │     Tool     │
                         └──────────────┘

                                │
                                ▼
                         ┌─────────────┐
                         │ Tool Result │
                         └──────┬──────┘
                                │
                                ▼
                         ┌─────────────┐
                         │     LLM     │
                         └──────┬──────┘
                                │
                                ▼
                           Final Answer
```

---

# 🔄 How IntelliMind AI Works

## Step 1 — User Query

The user sends a natural-language query.

```text
What is RAG and why is it useful?
```

---

## Step 2 — LLM Understands the Query

The LLM analyzes the request and determines whether it can answer directly or needs an external tool.

---

## Step 3 — Tool Selection

Depending on the query, the assistant can select an appropriate tool.

| Query Type | Tool |
|---|---|
| General question | LLM |
| Document question | RAG |
| Current information | Web Search |
| Mathematical calculation | Calculator |
| Stock information | Stock Price |

---

## Step 4 — Tool Execution

The selected tool is executed and produces an external result.

For example:

```text
User Query
    ↓
LLM
    ↓
Stock Price Tool
    ↓
Market Data
```

---

## Step 5 — Result Returned to LLM

The tool output is provided back to the LLM.

```text
Tool Result
     ↓
     LLM
```

The LLM then uses the result to construct the final response.

---

## Step 6 — Final Response

The assistant returns a natural-language answer to the user.

```text
User
 ↓
LLM
 ↓
Tool
 ↓
Tool Result
 ↓
LLM
 ↓
Final Answer
```

---

# 📚 RAG Pipeline

The document-question-answering component follows a Retrieval-Augmented Generation workflow.

```text
                DOCUMENT INGESTION

                  PDF / Document
                        │
                        ▼
                Text Extraction
                        │
                        ▼
                   Chunking
                        │
                        ▼
                   Embeddings
                        │
                        ▼
                 Vector Storage
                        │
                        ▼
                   Vector Search
                        │
                        │
                  USER QUERY
                        │
                        ▼
                    Retrieval
                        │
                        ▼
                Relevant Context
                        │
                        ▼
                       LLM
                        │
                        ▼
                     Answer
```

The retrieved document content provides additional context to the LLM before generating the answer.

---

# 🧠 Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core development |
| LLM | Natural-language understanding and generation |
| LangChain | LLM application and tool integration |
| RAG | Document-based question answering |
| Embeddings | Semantic representation of documents |
| Vector Search | Relevant document retrieval |
| Gemini API | AI model / language generation |
| Web Search | External information retrieval |
| Calculator Tool | Mathematical operations |
| Stock Price Tool | Market information |
| `.env` | API key management |

---

# 📂 Project Structure

```text
IntelliMind-AI/
│
├── app/
│   ├── agents/
│   ├── tools/
│   ├── rag/
│   └── ...
│
├── data/
│   └── documents/
│
├── vectorstore/
│
├── main.py
│
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

> Adjust the folder names above if your current repository structure differs.

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/shrutipatil1925/IntelliMind-AI.git
```

Move into the project:

```bash
cd IntelliMind-AI
```

---

## 2. Create a Virtual Environment

### Windows

```powershell
python -m venv venv
```

Activate it:

```powershell
venv\Scripts\activate
```

### Linux / macOS

```bash
python -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔐 Environment Variables

Create a `.env` file in the project root.

```env
GOOGLE_API_KEY=your_gemini_api_key
```

If your current implementation uses additional API keys for external tools, add them according to the tool configuration.

### Important

Never commit API keys to GitHub.

Add the following to `.gitignore`:

```text
.env
venv/
__pycache__/
*.pyc
```

---

# ▶️ Running the Application

After activating the virtual environment and configuring the required API keys:

```bash
python main.py
```

The application will start the IntelliMind AI assistant.

---

# 💡 Example Queries

### General AI

```text
Explain what an embedding is.
```

### Document RAG

```text
What is the main conclusion of this research paper?
```

### Web Search

```text
What are the latest developments in AI?
```

### Calculator

```text
Calculate 25% of 8400.
```

### Stock Information

```text
What is the current stock price of Apple?
```

### Follow-up Question

```text
User:
What is RAG?

AI:
RAG combines retrieval with language generation...

User:
How does retrieval work?

AI:
Retrieval finds relevant information from...
```

---

# 🔥 Why This Project Is Different From a Basic Chatbot

A traditional chatbot:

```text
User
 ↓
LLM
 ↓
Answer
```

IntelliMind AI:

```text
                         ┌── RAG
                         │
User → LLM → Tool ───────┼── Web Search
                         │
                         ├── Calculator
                         │
                         └── Stock Price
                              ↓
                         Tool Result
                              ↓
                             LLM
                              ↓
                           Answer
```

The assistant can therefore interact with **external tools and knowledge sources** instead of depending only on the model's internal knowledge.

---

# 🎯 Use Cases

IntelliMind AI can be used as a foundation for:

- 📚 Document research
- 🔎 Information retrieval
- 📄 Research paper Q&A
- 🧮 Mathematical assistance
- 📈 Financial information lookup
- 🌐 Current-information search
- 🤖 General AI assistance
- 🧠 Tool-using AI agents

---

# 🧪 Key AI Concepts Demonstrated

This project provides practical experience with:

### 1. Large Language Models

Using an LLM to understand user queries and generate natural-language responses.

### 2. Retrieval-Augmented Generation

Connecting an LLM to external document knowledge.

### 3. Tool Calling

Allowing an LLM to select and invoke external tools.

### 4. Semantic Search

Finding relevant information based on semantic similarity.

### 5. Conversation State

Maintaining context across multiple messages.

### 6. Agentic Workflows

Moving beyond a fixed chatbot pipeline toward an assistant capable of selecting different tools based on the user's request.

---

# 🔮 Future Improvements

Possible improvements for IntelliMind AI include:

## Multi-Agent Architecture

Separate specialized agents could handle different tasks:

```text
                 IntelliMind
                     │
       ┌─────────────┼─────────────┐
       ▼             ▼             ▼
  Research Agent  Data Agent   Web Agent
       │             │             │
       ▼             ▼             ▼
     RAG          SQL/Data       Search
```

---

## Advanced RAG

Improve document retrieval using:

- Hybrid Search
- Re-ranking
- Metadata filtering
- Query rewriting
- CRAG
- Self-RAG

---

## Long-Term Memory

Add persistent user memory so the assistant can retain useful information across sessions.

---

## More Tools

Additional tools could include:

- SQL database querying
- Email integration
- Calendar integration
- Code execution
- File analysis
- Data visualization

---

## Web Interface

The current assistant can be extended into a full web application using:

- Django
- FastAPI
- React

---

# 📈 Learning Outcomes

Through IntelliMind AI, the project demonstrates practical experience with:

- Python
- LLM application development
- RAG
- Embeddings
- Vector databases
- LangChain
- Gemini API
- Tool calling
- Agentic AI concepts
- Conversation state
- API integration
- Document processing
- Debugging AI workflows

---

# 👩‍💻 Author

**Shruti Patil**

AI/ML Enthusiast

GitHub:  
https://github.com/shrutipatil1925

---

# ⭐ Support

If you find this project useful or interesting, consider giving the repository a ⭐ on GitHub.

---

## 📄 License

This project is intended for educational and research purposes.