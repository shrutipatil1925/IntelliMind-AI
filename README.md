# ResearchRAG 🔬📄

> A Retrieval-Augmented Generation (RAG) system for interacting with research papers using semantic search, vector retrieval, and Gemini-powered question answering.

ResearchRAG allows users to upload and work with research papers in PDF format, retrieve the most relevant sections based on a question, and generate context-grounded answers using a Large Language Model.

The project combines **PDF processing, text chunking, Hugging Face embeddings, FAISS vector search, LangChain, and Gemini** into a practical research assistant.

---

## 🚀 Features

- 📄 **PDF Research Paper Processing**
  - Extract text from research papers using PyMuPDF.
  - Process papers into smaller chunks for efficient retrieval.

- ✂️ **Text Chunking**
  - Splits large documents into manageable chunks.
  - Improves semantic retrieval and reduces unnecessary context.

- 🧠 **Semantic Embeddings**
  - Converts document chunks into numerical vector representations.
  - Uses Hugging Face sentence-transformer embeddings.

- 🔎 **FAISS Vector Search**
  - Stores document embeddings in a FAISS index.
  - Retrieves semantically relevant chunks for a user query.

- 🤖 **Gemini-Powered Question Answering**
  - Uses Google's Gemini model to generate answers from retrieved context.
  - Answers are generated using information retrieved from the uploaded research papers.

- 📚 **Research Paper Q&A**
  - Ask natural-language questions about research papers.
  - Retrieve relevant information without manually searching through the entire document.

- 🖼️ **PDF Image Extraction**
  - Extract images from research papers for multimodal processing.
  - Supports research documents containing figures and visual information.

- 💬 **Chat History**
  - Maintains conversation history during interactions.
  - Allows follow-up questions within the research conversation.

---

# 🏗️ System Architecture

```text
                    ┌─────────────────────┐
                    │    Research Paper   │
                    │        PDF          │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    PDF Processing   │
                    │      PyMuPDF        │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Text Extraction   │
                    │    & Chunking       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     Embeddings      │
                    │ Hugging Face Model  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    FAISS Index      │
                    │  Vector Database    │
                    └──────────┬──────────┘
                               │
                       User Question
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Semantic Retrieval  │
                    │ Relevant Chunks     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Gemini LLM        │
                    │ Context + Question  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     Final Answer    │
                    └─────────────────────┘
```

---

# 🔄 RAG Pipeline

ResearchRAG follows a standard Retrieval-Augmented Generation pipeline.

### 1. Document Ingestion

A research paper in PDF format is provided to the system.

```text
Research Paper.pdf
        ↓
    PDF Loader
```

### 2. Text Extraction

The PDF is processed using **PyMuPDF** to extract its textual content.

```text
PDF
 ↓
Pages
 ↓
Extracted Text
```

### 3. Text Chunking

Large text is divided into smaller chunks.

```text
Research Paper
      ↓
Large Text
      ↓
Text Chunks
      ↓
Chunk 1
Chunk 2
Chunk 3
...
```

Chunking makes it possible to retrieve only the relevant portions of a large document instead of passing the complete paper to the LLM.

### 4. Embedding Generation

Each chunk is converted into an embedding vector using a Hugging Face embedding model.

```text
Text Chunk
    ↓
Embedding Model
    ↓
Vector
```

### 5. Vector Storage

The generated embeddings are stored in a **FAISS** index.

```text
Chunk → Embedding → FAISS
```

FAISS enables efficient similarity search over the document vectors.

### 6. Query Processing

When the user asks a question, the question is also converted into an embedding.

```text
User Question
      ↓
Embedding Model
      ↓
Query Vector
```

### 7. Retrieval

FAISS compares the query vector with stored document vectors and retrieves the most relevant chunks.

```text
Query Vector
      ↓
FAISS Similarity Search
      ↓
Relevant Document Chunks
```

### 8. Generation

The retrieved context and user question are passed to Gemini.

```text
Retrieved Context
       +
User Question
       ↓
   Gemini
       ↓
Generated Answer
```

---

# 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| LangChain | RAG workflow and document processing |
| PyMuPDF | PDF text and image extraction |
| Hugging Face | Text embeddings |
| FAISS | Vector similarity search |
| Gemini | Large Language Model |
| PIL | Image processing |
| NumPy | Numerical/vector operations |
| python-dotenv | Environment variable management |

---

# 📁 Project Structure

```text
ResearchRAG/
│
├── data/
│   ├── research.pdf
│   └── second_research.pdf
│
├── faiss_index/
│   ├── index.faiss
│   └── index.pkl
│
├── images/
│   └── extracted_images/
│
├── main.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

> The exact filenames/folders may vary depending on the current version of the project.

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/shrutipatil1925/ResearchRAG.git
```

Move into the project directory:

```bash
cd ResearchRAG
```

---

## 2. Create a Virtual Environment

### Windows

```bash
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

# 🔑 Environment Variables

ResearchRAG uses the Gemini API for answer generation.

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_gemini_api_key
```

Do not commit your `.env` file to GitHub.

Your `.gitignore` should contain:

```text
.env
venv/
__pycache__/
*.pyc
```

---

# ▶️ Running the Project

After activating the virtual environment and configuring the API key:

```bash
python main.py
```

The application will start the ResearchRAG workflow and allow you to interact with the research documents.

---

# 💬 Example Interaction

### User

```text
What is the main objective of this research paper?
```

### ResearchRAG

```text
The main objective of the research is to ...
```

The answer is generated using relevant information retrieved from the research paper.

---

# 🧪 Example Questions

You can ask questions such as:

```text
What is the main objective of the paper?

What methodology does the paper use?

What dataset was used?

What are the main findings?

What are the limitations of the proposed approach?

What models were used in the research?

Explain the methodology in simple terms.

What are the future research directions?
```

---

# 📊 Why RAG?

Large Language Models have a knowledge cutoff and may not have access to information contained in a user's private documents.

RAG solves this problem by combining:

```text
Knowledge Retrieval
        +
Language Generation
        =
Grounded Question Answering
```

Instead of asking the LLM to answer from its general knowledge, ResearchRAG first retrieves relevant information from the research paper and then provides that information as context to the LLM.

This helps the system answer questions based on the actual document.

---

# 🧠 Key Concepts Demonstrated

This project demonstrates practical implementation of several important AI/ML concepts:

### Retrieval-Augmented Generation

Combines information retrieval with LLM-based generation.

### Embeddings

Represents text as numerical vectors that capture semantic meaning.

### Vector Search

Finds documents or text chunks that are semantically similar to a query.

### FAISS

Provides efficient similarity search over high-dimensional vectors.

### Semantic Search

Retrieves information based on meaning rather than exact keyword matching.

### Prompt-Based Generation

Uses retrieved document context to guide Gemini's response.

### Multimodal Document Processing

Research papers can contain both textual and visual information, so the project also explores extracting images from PDF documents.

---

# 📈 Project Workflow

```text
                 USER
                  │
                  ▼
           Upload Research PDF
                  │
                  ▼
          Extract PDF Content
                  │
          ┌───────┴────────┐
          ▼                ▼
        Text             Images
          │
          ▼
       Chunking
          │
          ▼
      Embeddings
          │
          ▼
        FAISS
          │
          │
       User Query
          │
          ▼
       Embedding
          │
          ▼
    Similarity Search
          │
          ▼
  Relevant Text Chunks
          │
          ▼
       Gemini
          │
          ▼
       Answer
```

---

# 🎯 Use Cases

ResearchRAG can be useful for:

- 📚 Research paper analysis
- 🔬 Literature review assistance
- 🎓 Academic learning
- 📄 Document question answering
- 🧑‍🔬 Research exploration
- 🔎 Semantic search across research documents
- 📝 Understanding complex research papers

---

# ⚠️ Limitations

The current implementation has some limitations:

- Answers depend on the quality of the retrieved document chunks.
- OCR may be required for scanned/image-only PDFs.
- Complex tables may not always be represented correctly through text extraction.
- The quality of generated answers depends on the underlying LLM.
- Very large document collections require more scalable indexing and storage.
- Extracted images require additional multimodal processing to fully understand their content.

---

# 🔮 Future Improvements

Possible improvements include:

### 1. Multimodal RAG

Improve understanding of:

- Research figures
- Charts
- Tables
- Diagrams
- Images

### 2. Better Retrieval

Experiment with:

- Hybrid search
- BM25 + vector search
- Re-ranking
- Metadata filtering
- Query expansion

### 3. Advanced RAG

Implement advanced techniques such as:

```text
Basic RAG
   ↓
Advanced Retrieval
   ↓
Re-ranking
   ↓
CRAG / Self-RAG
   ↓
Agentic RAG
```

### 4. Web Interface

Build a user-friendly interface using:

- Django
- Flask
- FastAPI
- Streamlit

### 5. Research Paper Comparison

Allow users to upload multiple papers and ask:

```text
Compare the methodologies used in these papers.

Which datasets are common?

How do their approaches differ?

What are the limitations of each paper?
```

### 6. Citation Support

Return the source paper, page number, and retrieved passage along with the answer.

### 7. Evaluation

Add RAG evaluation metrics for:

- Retrieval accuracy
- Context relevance
- Answer faithfulness
- Answer correctness

---

# 📌 What I Learned From This Project

Building ResearchRAG provided practical experience with:

- Document processing
- PDF parsing
- Text chunking
- Embedding models
- Vector databases
- Semantic search
- Retrieval-Augmented Generation
- LangChain
- Gemini API
- FAISS
- Multimodal document processing
- Environment variable management
- Debugging AI application pipelines

The project demonstrates how an LLM can be connected to an external knowledge source instead of relying only on its pretrained knowledge.

---

# 👩‍💻 Author

**Shruti Patil**

AI/ML Enthusiast

GitHub:  
https://github.com/shrutipatil1925

---

# ⭐ If You Find This Project Useful

If you find ResearchRAG useful or interesting, consider giving the repository a ⭐ on GitHub.

---

## 📄 License

This project is intended for educational and research purposes.