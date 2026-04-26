[**English**](./README_en.md) | [**简体中文**](./README.md)

# Agent Setup

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-Enabled-1C3C3C)
![LangGraph](https://img.shields.io/badge/LangGraph-Workflow-blue)
![CrewAI](https://img.shields.io/badge/CrewAI-Multi--Agent-orange)
![AutoGen](https://img.shields.io/badge/AutoGen-AgentChat-6f42c1)
![MCP](https://img.shields.io/badge/MCP-Integrated-0a7ea4)
![License](https://img.shields.io/badge/License-MIT-green)

## Project Overview

Agent Setup is a staged engineering workspace for AI Agent development, designed to keep runnable examples, environment automation, and framework comparisons in one repository.
It addresses three practical pain points: fragmented learning paths, non-reproducible local setup, and migration friction between Agent frameworks.
The current implementation forms an end-to-end evolution path from single-agent tool calling to workflow orchestration and multi-agent MCP integration.

## Core Features

- Explicit tool-calling lifecycle: `exercises/01-langchain-basics/01_hello_agent.py` demonstrates `tool_calls -> ToolMessage feedback -> final response` as a complete loop.
- Observable graph control flow: `exercises/02-langgraph-workflow/01_simple_graph.py` covers sequential graphs, conditional routing (`add_conditional_edges`), and agent-tool loop patterns.
- Multi-agent orchestration variants: `exercises/03-crewai-multiagent/01_research_crew.py` includes sequential, hierarchical, and event-driven flow/router modes.
- Stable MCP bridging in AutoGen: `exercises/04-autogen-agents/01_multi_agent_chat.py` uses `workbench=mcp` and defensive `getattr` extraction for message compatibility.
- Concurrent state safety in LangGraph: `exercises/05-advanced-patterns/01_research_pipeline.py` uses `Annotated + merge_dicts` to resolve fan-out write conflicts on shared state keys.

## Architecture & Tech Stack

### Data Flow

1. User input enters one of the staged exercise scripts (`exercises/01`~`05`).
2. Execution is delegated to the phase-specific runtime:
   - LangChain for model + tool feedback loops.
   - LangGraph for stateful node execution and conditional routing.
   - CrewAI for role/task-based multi-agent coordination.
   - AutoGen for message-driven agent chat and MCP tool workbench integration.
3. Results are emitted as structured console traces so learners can inspect decision paths and state transitions.

### Module Dependency Map

- `scripts/setup.ps1`: environment bootstrap (`venv`, pip toolchain, dependency install, `.env` initialization).
- `exercises/requirements.txt`: unified dependency baseline.
- `exercises/01`~`05`: staged implementation tracks for horizontal framework comparison and vertical capability growth.
- `scripts/clone-reference-repos.ps1`: optional sync of upstream reference repositories into `projects/` for source-level study.

### Stack Details

- Language/runtime: Python 3.10+, PowerShell, venv, pip
- Agent frameworks: LangChain, LangGraph, CrewAI, AutoGen
- Protocol layer: MCP (Model Context Protocol)
- Typing/configuration: TypedDict, Annotated, python-dotenv, Pydantic v2
- Platform: Windows/macOS/Linux (PowerShell scripts primarily target Windows)

## Getting Started

### Prerequisites

- Python 3.10+
- Git
- Node.js 18+ (required for MCP examples using `npx`)

### 1. Clone repository

```powershell
git clone https://github.com/Shizue123/agent-setup.git
cd agent-setup
```

### 2. Option A: one-command bootstrap (recommended)

```powershell
.\scripts\setup.ps1
```

### 3. Option B: manual setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r exercises/requirements.txt
Copy-Item exercises/.env.example exercises/.env
```

### 4. Configure environment variables

Edit `exercises/.env` and provide your API keys (for example `OPENAI_API_KEY`).

### 5. Run phase by phase

```powershell
.\.venv\Scripts\python.exe exercises/01-langchain-basics/01_hello_agent.py
.\.venv\Scripts\python.exe exercises/02-langgraph-workflow/01_simple_graph.py
.\.venv\Scripts\python.exe exercises/03-crewai-multiagent/01_research_crew.py
.\.venv\Scripts\python.exe exercises/04-autogen-agents/01_multi_agent_chat.py
.\.venv\Scripts\python.exe exercises/05-advanced-patterns/01_research_pipeline.py
```

### 6. Optional: clone upstream references

```powershell
.\scripts\clone-reference-repos.ps1
```

This pulls official repositories into `projects/` for local comparison.
