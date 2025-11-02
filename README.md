# Math Routing Agent with AI Gateway

An intelligent math problem-solving system that combines AI routing, guardrails, vector knowledge base, and DSPy optimization to deliver accurate, safe, and contextually relevant solutions to students.

## 🎯 Project Overview

This system implements an **AI Gateway** with dual guardrails, intelligent routing between knowledge base and web search, and continuous learning through DSPy optimization and human feedback.

### Key Features

- **🛡️ AI Gateway with Dual Guardrails**
  - Input guardrail: Blocks non-academic queries using keyword filtering
  - Output guardrail: Validates AI responses for safety and relevance

- **🧠 Intelligent Routing Pipeline**
  - Primary: ChromaDB vector search for formula retrieval
  - Fallback: MCP-powered web search when KB confidence is low
  - Semantic understanding of math concepts across classes 9-12

- **📚 Knowledge Base**
  - 500+ curated formulas organized by class and subject
  - Covers Math, Physics, and Chemistry
  - Vector embeddings for semantic search

- **🔄 Continuous Learning**
  - DSPy prompt optimization based on user feedback
  - Human-in-the-loop feedback collection (thumbs up/down)
  - Automated prompt improvement over time

- **📊 Benchmarking**
  - JEE Bench: Custom benchmark dataset for JEE-level problems
  - Performance metrics tracking and analysis
  - JEE Bench: Custom benchmark dataset for JEE-level problems
  - Performance metrics tracking and analysis

## 🏗️ Architecture

┌─────────────────────────────────────────────────────────┐
│ Frontend (HTML/JS) │
└────────────────────┬────────────────────────────────────┘
│
┌────────────────────▼────────────────────────────────────┐
│ FastAPI Backend (main.py) │
├─────────────────────────────────────────────────────────┤
│ Routes │
│ └── math_routes.py (API endpoints) │
├─────────────────────────────────────────────────────────┤
│ Services │
│ ├── guardrail_service.py (Input validation) │
│ ├── output_guardrail_service.py (Output validation) │
│ ├── vector_service.py (ChromaDB search) │
│ ├── mcp_service.py (Web search fallback) │
│ ├── llm_service.py (Groq LLaMA 3.1) │
│ ├── feedback_service.py (User feedback) │
│ ├── dspy_module.py (Prompt optimization) │
│ └── benchmark_service.py (JEE Bench evaluation) │
└─────────────────────────────────────────────────────────┘

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Groq API Key

### Installation

1. **Clone the repository**
git clone https://github.com/mahika29/math-routing-agent.git
cd math-routing-agent

2. **Create virtual environment**
python -m venv venv

Windows
venv\Scripts\activate

Mac/Linux
source venv/bin/activate

3. **Install dependencies**
pip install -r requirements.txt

4. **Set up environment variables**

Create a `.env` file in the project root:
GROQ_API_KEY=your-groq-api-key-here

5. **Run the backend**
cd backend
python main.py

Server will start at `http://localhost:8000`

6. **Open the frontend**

Open `frontend/index.html` in your browser

## 📁 Project Structure

math-routing-agent/
├── backend/
│ ├── routes/
│ │ ├── init.py
│ │ └── math_routes.py
│ ├── services/
│ │ ├── init.py
│ │ ├── benchmark_service.py
│ │ ├── dspy_module.py
│ │ ├── feedback_service.py
│ │ ├── guardrail_service.py
│ │ ├── kb_service.py
│ │ ├── llm_service.py
│ │ ├── mcp_service.py
│ │ ├── output_guardrail_service.py
│ │ ├── vector_service.py
│ │ └── web_search_service.py
│ ├── models/
│ │ └── init.py
│ ├── utils/
│ │ ├── init.py
│ │ └── guardrails.py
│ └── main.py
├── frontend/
│ └── index.html
├── requirements.txt
├── .gitignore
└── README.md

**Key Components:**

| Directory/File | Purpose |
|---------------|---------|
| `backend/routes/` | API endpoint definitions |
| `backend/services/` | Core business logic and AI services |
| `backend/models/` | Data models |
| `backend/utils/` | Helper functions and utilities |
| `backend/main.py` | FastAPI application entry point |
| `frontend/` | User interface (HTML/CSS/JS) |
| `requirements.txt` | Python dependencies |

## 🔌 API Endpoints

### POST `/api/ask`
Solve a math problem with AI routing

**Request Body:**
{
"question": "What is the quadratic formula?",
"class_level": "10"
}


**Response:**
{
"answer": "The quadratic formula is x = (-b ± √(b²-4ac)) / 2a...",
"source": "knowledge_base",
"confidence": 0.95,
"formulas_used": ["quadratic_formula"]
}

### POST `/api/feedback`
Submit user feedback for continuous learning

**Request Body:**
{
"question_id": "uuid-here",
"rating": "thumbs_up",
"comment": "Great explanation!"
}

### GET `/api/benchmark`
Run JEE Bench evaluation

**Response:**
{
"accuracy": 0.87,
"total_questions": 100,
"correct": 87,
"metrics": {...}
}

## 🛠️ Technologies Used

| Component | Technology |
|-----------|-----------|
| **Backend Framework** | FastAPI 0.109.0 |
| **LLM Provider** | Groq (LLaMA 3.1 70B) |
| **Vector Database** | ChromaDB 0.4.22 |
| **Prompt Optimization** | DSPy 2.4.0 |
| **Embeddings** | Sentence Transformers 2.3.1 |
| **Frontend** | Vanilla HTML/CSS/JavaScript |
| **Data Processing** | Pandas 2.1.4, NumPy 1.26.3 |

## 🧪 Testing

Run the benchmarking suite:

python backend/services/benchmark_service.py

This evaluates the system on JEE-level problems and outputs performance metrics.

## 📊 System Flow

1. **User submits question** via frontend
2. **Input Guardrail** validates academic relevance
3. **Vector Search** queries ChromaDB for relevant formulas
4. **Routing Decision:**
   - High confidence (>0.7) → Use KB results
   - Low confidence → Fallback to MCP web search
5. **LLM Service** generates answer using Groq
6. **Output Guardrail** validates response safety
7. **Response delivered** to user
8. **Feedback collected** for DSPy optimization

## 🎓 Supported Subjects

This system is **primarily focused on Mathematics** for competitive exam preparation.

### **Mathematics (Classes 9-12 + JEE)**
- **Core Topics:**
  - Algebra (Equations, Inequalities, Functions)
  - Trigonometry (Identities, Equations, Inverse Functions)
  - Calculus (Limits, Derivatives, Integration, Differential Equations)
  - Coordinate Geometry (Lines, Circles, Conic Sections)
  - Vectors & 3D Geometry
  - Probability & Statistics
  - Number Theory & Combinatorics

- **JEE-Specific Coverage:**
  - Advanced problem-solving techniques
  - Multiple-choice question patterns
  - Time-efficient solving strategies
  - Formula derivations and applications

### **Note:**
While the architecture supports Physics and Chemistry formulas, the current implementation is **optimized for Mathematics** with a focus on JEE preparation.


## 🔒 Security Features

- ✅ Input validation and sanitization
- ✅ Academic keyword filtering
- ✅ Output content moderation
- ✅ No storage of sensitive user data
- ✅ API key protection via environment variables

## 📈 Future Enhancements

- [ ] Multi-language support
- [ ] Image-based problem solving
- [ ] Step-by-step solution breakdown
- [ ] Collaborative problem-solving sessions
- [ ] Mobile app integration

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is created for educational purposes as part of a Generative AI assignment.

## 👤 Author

**Mahika Harikumar**
- GitHub: [@mahika29](https://github.com/mahika29)

## 🙏 Acknowledgments

- Groq for providing fast LLM inference
- ChromaDB for vector search capabilities
- DSPy team for prompt optimization framework
- JEE Bench dataset contributors

---

**Built with ❤️ for students preparing for competitive exams**

