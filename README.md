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

## 🏗️ Architecture

