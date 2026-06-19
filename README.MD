# StackCraft

## Overview

StackCraft is a multi-agent AI application compiler that transforms natural language software requirements into structured engineering artifacts. Instead of relying on a single large language model prompt, StackCraft decomposes the software design process into specialized stages, where each AI agent performs a focused task and passes its output to the next stage in the pipeline.

The system is designed to bridge the gap between high-level product ideas and implementation-ready software specifications by generating:

* Requirement Analysis
* System Design Blueprints
* API Specifications
* Database Schemas
* Authentication Plans
* Validation Reports
* FastAPI Code Scaffolds

The project demonstrates how agentic workflows can be applied to software engineering tasks by introducing modular reasoning, validation, and code generation stages.

---

## Problem Statement

Traditional AI-assisted software generation systems often rely on a single prompt to generate an entire application design. While this approach is fast, it frequently suffers from:

* Inconsistent outputs
* Missing requirements
* Hallucinated components
* Poor schema quality
* Lack of validation
* Limited traceability between decisions

StackCraft addresses these limitations through a multi-agent architecture where each stage focuses on a specific responsibility within the software design lifecycle.

---

## Objectives

The primary objectives of StackCraft are:

* Convert natural language application requirements into structured engineering artifacts.
* Demonstrate multi-agent orchestration for software design tasks.
* Improve output quality through staged reasoning.
* Introduce validation mechanisms before code generation.
* Generate executable backend scaffolding from validated schemas.
* Provide a visual interface for interacting with the AI compiler.

---

## System Architecture

The application follows a sequential multi-agent pipeline.

```text
User Requirement
        │
        ▼
Intent Agent
        │
        ▼
Design Agent
        │
        ▼
Schema Agent
        │
        ▼
Validator
        │
        ▼
Code Generator
        │
        ▼
Generated FastAPI Application
```

Each stage consumes the output of the previous stage and produces structured information for downstream processing.

---

## Pipeline Components

### 1. Intent Agent

The Intent Agent serves as the entry point of the pipeline.

Its responsibility is to analyze the user's natural language prompt and identify:

* Application domain
* User roles
* Functional requirements
* Core features
* Business objectives

Example Input:

```text
Build an online learning platform with authentication, courses, quizzes, and analytics.
```

Example Output:

```json
{
  "application_type": "Online Learning Platform",
  "roles": [
    "Student",
    "Instructor",
    "Administrator"
  ],
  "features": [
    "Authentication",
    "Course Management",
    "Quiz System",
    "Analytics Dashboard"
  ]
}
```

This stage converts unstructured text into machine-readable requirements.

---

### 2. Design Agent

The Design Agent transforms the extracted requirements into a high-level software architecture.

Responsibilities include:

* Identifying application modules
* Defining system entities
* Designing user flows
* Creating page structures
* Planning interactions between components

Example Outputs:

* Dashboard
* Authentication Module
* User Management
* Analytics System
* Course Management

This stage acts as the architectural planning layer of the compiler.

---

### 3. Schema Agent

The Schema Agent converts the architectural design into structured technical specifications.

Generated artifacts include:

#### API Schema

```json
{
  "endpoints": [
    "/login",
    "/courses",
    "/analytics"
  ]
}
```

#### Database Schema

```json
{
  "tables": [
    "users",
    "courses",
    "quizzes"
  ]
}
```

#### UI Schema

```json
{
  "pages": [
    "Login",
    "Dashboard",
    "Courses"
  ]
}
```

#### Authentication Schema

```json
{
  "type": "JWT"
}
```

This stage produces implementation-oriented artifacts.

---

### 4. Validator

Before generating code, StackCraft validates generated schemas.

Validation checks include:

* JSON parsing correctness
* Required section existence
* Structural integrity
* Empty object detection
* Schema completeness

Required sections:

```json
{
  "ui": {},
  "api": {},
  "database": {},
  "auth": {}
}
```

The validator prevents malformed outputs from reaching the code generation stage.

---

### 5. Code Generator

Once validation succeeds, StackCraft generates backend scaffolding.

Current implementation supports:

* FastAPI route generation
* Endpoint scaffolding
* Boilerplate backend structure

Example Output:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/users")
def users():
    return {"message": "ok"}
```

This demonstrates the conversion of AI-generated schemas into executable software artifacts.

---

## Technology Stack

### Artificial Intelligence

* Google Gemini
* Prompt Engineering
* Agent-Based Workflows

### Backend

* Python
* FastAPI

### Frontend

* Streamlit

### Data Processing

* JSON
* Python Standard Library

### Development Tools

* Git
* GitHub
* VS Code

---

## Project Structure

```text
stackcraft/

├── app.py
├── main.py
├── llm.py
├── validator.py
├── codegen.py
│
├── pipeline/
│   ├── intent.py
│   ├── design.py
│   └── schema.py
│
├── prompts/
│   ├── intent.txt
│   ├── design.txt
│   └── schema.txt
│
├── outputs/
│
├── assets/
│   └── logo.png
│
└── requirements.txt
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/harshwt/StackCraft.git
cd StackCraft
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create an environment file:

```env
GEMINI_API_KEY=your_api_key
```

---

## Running the Application

Start the Streamlit interface:

```bash
streamlit run app.py
```

The application will be available locally at:

```text
http://localhost:8501
```

---

## Example Workflow

User Input:

```text
Build a CRM platform with authentication, customer management, analytics, and payment integration.
```

Pipeline Execution:

```text
CRM Requirement
        ↓
Intent Extraction
        ↓
System Design
        ↓
Schema Generation
        ↓
Validation
        ↓
FastAPI Code Generation
```

Generated Deliverables:

* Intent Analysis Report
* Architecture Blueprint
* Database Design
* API Endpoints
* Authentication Plan
* Validation Report
* FastAPI Backend Scaffold

---

## Evaluation and Trade-Offs

StackCraft uses a multi-agent architecture rather than a single-prompt approach.

Advantages:

* Improved output structure
* Better modularity
* Easier debugging
* Increased validation opportunities
* Higher reliability

Trade-Offs:

* Increased latency
* More LLM calls
* Higher token consumption
* Greater orchestration complexity

The project prioritizes correctness and maintainability over minimal inference cost.

---

## Future Work

Planned improvements include:

* Automatic schema repair agents
* React and Next.js code generation
* Docker deployment generation
* Database migration generation
* Agent observability and tracing
* Cost versus quality evaluation dashboards
* Multi-model orchestration
* Security-focused validation layers
* CI/CD pipeline generation
* Infrastructure-as-Code generation

---

## Author

Harshwardhan Tiwari

GitHub: https://github.com/harshwt
