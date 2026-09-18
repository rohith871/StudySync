# StudySync 📚🤖

**StudySync** is an AI-powered student study companion that combines **Retrieval-Augmented Generation (RAG), multiple LLMs, LangGraph, MCP tools, and spaced repetition** to provide a personalized study experience.

It helps students organize course material, learn from their own notes, test their understanding, revise using flashcards, and maintain a balance between study and leisure.

---

## ✨ Features

### 📖 Course & Topic Management

* Create and manage courses.
* Add topics and study notes to courses.
* Store structured course information in SQLite.
* Index study material in ChromaDB for semantic retrieval.

### 🧠 AI-Powered Teaching

* Retrieves relevant information from the student's course notes using RAG.
* Uses **Google Gemini** to generate topic explanations.
* The generated lesson is grounded in the retrieved study material.

### 📝 AI Quiz Generation

* Generates multiple-choice questions from the generated lesson.
* Uses **Grok** for quiz generation.
* Questions are constrained to information present in the lesson.

### 🔄 Agentic Study Workflow

Study sessions are orchestrated using **LangGraph**:

```text
Topic
  ↓
Teacher Node
  ↓
Quiz Node
  ↓
Life Balance Node
  ↓
Study Session Result
```

The workflow maintains shared state between the different stages.

### 🗂️ Flashcards & Spaced Repetition

* Create and review flashcards.
* Track repetitions and review intervals.
* Uses the **SM-2 spaced-repetition algorithm** to calculate future review schedules.

### ⚖️ Life Balance

* Calculates a recommended leisure budget based on study-related factors.
* Implemented as a deterministic tool rather than relying on an LLM for numerical calculations.

### 🛠️ MCP Tools

The project includes a FastMCP server exposing reusable tools for operations such as:

* Course data access
* Course-note retrieval
* Flashcard access
* SM-2 calculations
* Life-balance calculations

---

# 🏗️ Architecture

```text
                         ┌─────────────────┐
                         │     Student     │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │    Frontend     │
                         │ HTML + JS +     │
                         │ Alpine.js       │
                         └────────┬────────┘
                                  │
                             HTTP / API
                                  │
                                  ▼
                         ┌─────────────────┐
                         │     FastAPI     │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │    LangGraph    │
                         │  Study Workflow │
                         └────────┬────────┘
                                  │
                 ┌────────────────┼────────────────┐
                 │                │                │
                 ▼                ▼                ▼
          ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
          │   Teacher   │  │    Quiz     │  │    Life     │
          │    Node     │  │    Node     │  │   Balance   │
          └──────┬──────┘  └──────┬──────┘  └──────┬──────┘
                 │                │                │
                 ▼                ▼                ▼
             ChromaDB           Grok          MCP Tool
                 │
                 ▼
              Gemini

        ┌────────────────────────────────────────┐
        │               Storage                  │
        │                                        │
        │ SQLite              ChromaDB           │
        │ Courses             Vectorized Notes   │
        │ Topics              Semantic Search    │
        │ Flashcards                              │
        │ Review Data                             │
        └────────────────────────────────────────┘
```

---

# 🔄 Study Session Workflow

When a student starts a study session, the following workflow takes place:

```text
1. Student selects a topic
          ↓
2. Frontend sends request to FastAPI
          ↓
3. Backend retrieves topic information
          ↓
4. LangGraph starts the study workflow
          ↓
5. Teacher Node
      ├── Queries ChromaDB
      ├── Retrieves relevant course notes
      └── Sends context to Gemini
          ↓
6. Gemini generates a lesson
          ↓
7. Quiz Node receives the lesson
          ↓
8. Grok generates MCQs
          ↓
9. Life Balance Node calculates leisure budget
          ↓
10. Final study session result
          ↓
11. FastAPI returns the result to frontend
```

---

# 🧠 Retrieval-Augmented Generation (RAG)

StudySync uses RAG so that explanations can be grounded in the student's own study material.

```text
Student Notes
      ↓
   ChromaDB
      ↓
Semantic Retrieval
      ↓
Relevant Context
      ↓
Gemini
      ↓
AI Explanation
```

Instead of asking the LLM to explain a topic using only its general knowledge, the system first retrieves relevant content from the student's stored notes.

This allows the generated lesson to be based on the course material available in StudySync.

---

# 🤖 LangGraph Workflow

LangGraph is used to orchestrate the different stages of a study session.

The shared state contains information such as:

```text
topic_id
topic_title
retrieved_context
teacher_explanation
quiz_questions
quiz_score
life_balance_output
```

The workflow can be represented as:

```text
                 START
                   │
                   ▼
              ┌─────────┐
              │ Teacher │
              └────┬────┘
                   │
                   ▼
              ┌─────────┐
              │  Quiz   │
              └────┬────┘
                   │
                   ▼
           ┌──────────────┐
           │ Life Balance │
           └──────┬───────┘
                  │
                  ▼
                 END
```

### Teacher Node

The teacher node:

1. Receives the selected topic.
2. Retrieves relevant notes from ChromaDB.
3. Provides the retrieved context to Gemini.
4. Generates a structured lesson.
5. Stores the lesson in the LangGraph state.

### Quiz Node

The quiz node:

1. Receives the generated lesson.
2. Sends the lesson to Grok.
3. Requests multiple-choice questions.
4. Parses the generated quiz.
5. Stores the questions in the shared state.

### Life Balance Node

The life-balance stage uses a deterministic calculation tool to estimate a recommended leisure budget based on study-related information.

---

# 🛠️ MCP Architecture

StudySync includes a **FastMCP server** that exposes reusable application tools.

```text
                 MCP Server
                     │
       ┌─────────────┼─────────────┐
       │             │             │
       ▼             ▼             ▼
   RAG Tools     DB Tools      SM-2 Tools
       │             │             │
       ▼             ▼             ▼
   ChromaDB       SQLite      Flashcards
```

Example tool categories include:

```text
Course / database tools
RAG / note retrieval tools
SM-2 calculation tools
Life-balance tools
```

MCP provides a standardized interface for exposing these capabilities as tools.

> Note: The current implementation does not route every backend operation through an MCP client. Some components directly call the underlying Python functions while the MCP server exposes the reusable tool layer.

---

# 🗃️ Data Storage

StudySync uses two types of storage.

## SQLite

SQLite stores structured application data such as:

* Courses
* Topics
* Flashcards
* Flashcard review information
* Life-balance records

## ChromaDB

ChromaDB is used as the vector store for course notes.

It enables semantic retrieval during AI-powered study sessions.

```text
                 Study Material
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
       SQLite                  ChromaDB
   Structured Data          Vector Search
          │                       │
          ▼                       ▼
  Course / Topic Data       Relevant Notes
                                  │
                                  ▼
                                Gemini
```

---

# 🗂️ Project Structure

```text
StudySync/
│
├── backend/
│   │
│   ├── app/
│   │   │
│   │   ├── api/
│   │   │   ├── courses.py
│   │   │   ├── flashcards.py
│   │   │   ├── life_balance.py
│   │   │   └── sessions.py
│   │   │
│   │   ├── graph/
│   │   │   ├── state.py
│   │   │   ├── orchestrator.py
│   │   │   └── nodes/
│   │   │       ├── teacher.py
│   │   │       ├── quiz.py
│   │   │       └── life_balance.py
│   │   │
│   │   ├── mcp_server/
│   │   │   ├── server.py
│   │   │   └── tools/
│   │   │       ├── db_tools.py
│   │   │       ├── rag_tools.py
│   │   │       └── sm2_tools.py
│   │   │
│   │   ├── store/
│   │   │   ├── db.py
│   │   │   ├── models.py
│   │   │   └── chroma.py
│   │   │
│   │   ├── config.py
│   │   └── main.py
│   │
│   └── seed.py
│
├── frontend/
│   ├── index.html
│   ├── css/
│   │   └── custom.css
│   └── js/
│       └── app.js
│
└── README.md
```

---

# 💻 Technology Stack

| Technology        | Purpose                   |
| ----------------- | ------------------------- |
| **Python**        | Backend development       |
| **FastAPI**       | REST API framework        |
| **Uvicorn**       | ASGI server               |
| **SQLAlchemy**    | Database ORM              |
| **SQLite**        | Structured data storage   |
| **ChromaDB**      | Vector database           |
| **LangChain**     | LLM integration           |
| **LangGraph**     | AI workflow orchestration |
| **Google Gemini** | AI teaching / explanation |
| **Grok**          | AI quiz generation        |
| **FastMCP**       | Tool server               |
| **SM-2**          | Spaced repetition         |
| **HTML/CSS**      | Frontend                  |
| **JavaScript**    | Frontend logic            |
| **Alpine.js**     | Frontend state management |
| **Pico CSS**      | UI styling                |

---

# ⚙️ Installation

## 1. Clone the repository

```bash
git clone https://github.com/rohith871/StudySync.git
cd StudySync
```

## 2. Create a virtual environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

---

## 3. Install backend dependencies

```bash
cd backend
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

StudySync requires API credentials for the LLM services.

Create a `.env` file in the backend directory and configure the required API keys used by the application.

Example:

```env
GOOGLE_API_KEY=your_google_api_key
XAI_API_KEY=your_xai_api_key
```

**Never commit real API keys to GitHub.**

---

# ▶️ Running the Backend

From the `backend` directory:

```bash
uvicorn app.main:app --reload
```

The FastAPI application will start on:

```text
http://127.0.0.1:8000
```

FastAPI's interactive API documentation can be accessed through:

```text
http://127.0.0.1:8000/docs
```

---

# 🌐 Running the Frontend

The frontend is contained in:

```text
frontend/
```

Open `index.html` using a local web server.

For example, using Python:

```bash
cd frontend
python -m http.server 5500
```

Then open:

```text
http://127.0.0.1:5500
```

---

# 📚 Flashcard System

StudySync implements the **SM-2 spaced-repetition algorithm**.

The review process is:

```text
Flashcard
    ↓
Student recalls answer
    ↓
Student provides rating
    ↓
SM-2 calculation
    ↓
Update:
  • Easiness Factor
  • Repetition count
  • Interval
  • Next review date
```

This allows cards that are difficult to be reviewed more frequently while well-known cards can be reviewed at longer intervals.

---

# 🔐 Security

API keys should be provided through environment variables.

The `.env` file should not be committed to the repository.

Add it to `.gitignore`:

```gitignore
.env
venv/
__pycache__/
*.pyc
```

---

# 🚀 Future Improvements

Potential extensions include:

* User authentication and individual study profiles
* Persistent cloud database
* More sophisticated learner personalization
* Adaptive quiz difficulty
* Progress analytics and dashboards
* Additional LLM providers
* More MCP-based tools
* Calendar integration
* Automated study-plan generation
* Deployment using Docker
* Cloud-hosted vector database
* Improved evaluation of generated lessons and quizzes

---

# 🎯 Project Highlights

StudySync demonstrates the integration of several modern AI application concepts:

```text
              StudySync
                  │
       ┌──────────┼───────────┐
       │          │           │
       ▼          ▼           ▼
      RAG     Multi-LLM    Tool Use
       │          │           │
       ▼          ▼           ▼
   ChromaDB   Gemini/Grok    MCP
                  │
                  ▼
              LangGraph
                  │
                  ▼
          AI Study Workflow
```

The project combines:

* **RAG** for grounding AI responses in student notes
* **LLMs** for teaching and quiz generation
* **LangGraph** for workflow orchestration
* **MCP** for reusable tools
* **SM-2** for spaced repetition
* **FastAPI** for backend APIs
* **SQLite + ChromaDB** for complementary data storage



