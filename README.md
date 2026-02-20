# Modular Agentic Worker Framework

A lightweight, expandable multi-agent framework built using LangGraph for structured task execution, validation, and guardrail-based reasoning.

This system demonstrates:

* Modular agent architecture
* State-driven orchestration
* Conditional routing (dynamic branching)
* Guardrail-based validation loop
* Structured reasoning logging
* Expandable design for future agents

---

## Architecture Overview

The framework consists of three specialized agents:

### 1. Intake Agent

* Receives incoming task
* Classifies and structures input
* Initializes state

### 2. Execution Agent

* Performs rule-based or LLM-assisted reasoning
* Generates structured output
* Updates reasoning trace

### 3. Validation Agent

* Evaluates execution output
* Applies guardrails
* Determines approval or retry
* Controls loop via retry counter

The orchestration layer uses LangGraph with conditional edges to enable dynamic routing:

Validation → (Approved → END)
Validation → (Retry < limit → Execution)

This ensures:

* Controlled feedback loops
* Bounded retries
* Deterministic stopping behavior

---

## Tech Stack

* Python 3.10+
* LangGraph (Agent orchestration)
* LangChain Core
* Ollama (local LLM runtime)
* Gemma 3:4B model
* Structured logging (Python logging module)

---

## Project Structure

```
agents/
    intake_agent.py
    execution_agent.py
    validation_agent.py

orchestrator/
    graph.py

schemas/
    models.py

utils/
    json_parser.py

main.py
requirements.txt
README.md
```

---

## Why LangGraph?

LangGraph provides:

* State-based orchestration
* Conditional routing
* Clean separation of nodes
* Scalable graph expansion
* Deterministic execution paths

This makes it suitable for modular, production-oriented agent systems.

---

## Installation Guide

### 1. Clone Repository

```
git clone <your-repo-url>
cd <project-folder>
```

### 2. Create Virtual Environment

```
python -m venv venv
```

Activate:

Windows:

```
venv\Scripts\activate
```

Mac/Linux:

```
source venv/bin/activate
```

### 3. Install Dependencies

```
pip install -r requirements.txt
```

---

## Install Ollama (Required)

Download and install Ollama from:

https://ollama.com/download

Verify installation:

```
ollama --version
```

---

## Pull Required Model

This project uses:

Gemma 3:4B

Pull the model:

```
ollama pull gemma3:4b
```

---

## Running the System

Start Ollama (if not running):

```
ollama run gemma3:4b
```

Then run the application:

```
uvicorn main:app --reload
```

---

## Guardrail Strategy

* Retry limit enforced via state counter
* Validation approval required to exit loop
* Structured state validation before final output
* Deterministic routing via conditional edges

This prevents infinite loops and ensures bounded execution.

---

## Expandability

New agents can be added by:

1. Creating a new agent file inside `/agents`
2. Registering the node in `graph.py`
3. Defining routing logic if required

The orchestration core does not require structural modification.

---

## Observability

* Structured logging enabled
* Agent-level reasoning trace logged
* State transitions visible per execution cycle

---

## Future Improvements

* Tool integration layer
* Long-term memory storage
* Evaluation harness
* Dockerized deployment
* Metrics instrumentation

---

## Timeline Alignment

Designed to align with a 2-week sprint model:

Week 1:

* Core architecture
* 2 functional agents
* Conditional routing

Week 2:

* Third agent
* Logging & guardrails
* Documentation & refinement

---

## License

MIT
