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

Agent Setup is a progressive workspace for AI Agent engineering and experimentation.
The repository is organized as a staged path from single-agent fundamentals to multi-agent orchestration, with runnable code in every phase.

Current code evolution includes:
- Stable AutoGen Phase 4.3 MCP integration via `workbench=mcp`.
- Advanced LangGraph Phase 5 patterns: fan-out/fan-in concurrency and reducer-based state merge.
- Reflection loop routing with quality gating, plus repository hygiene hardening for public use.

## Core Features

- Phase-based curriculum: fully runnable tracks from `exercises/01` to `exercises/05`.
- Multi-framework coverage: LangChain, LangGraph, CrewAI, AutoGen, and MCP.
- Windows-friendly engineering workflow: `setup.ps1` bootstraps venv, installs dependencies, and generates `.env`.
- Security-first defaults: API keys are read from environment variables, not hardcoded in exercise logic.
- Optional reference repository sync under `projects/` for local comparison and study.

## Tech Stack

- Language and runtime: Python 3.10+, PowerShell, venv, pip
- Agent frameworks:
  - LangChain
  - LangGraph
  - CrewAI / crewai-tools
  - AutoGen (`autogen-agentchat`, `autogen-ext[openai]`)
- Protocol and integration:
  - MCP (Model Context Protocol) via Node.js stdio server (`@modelcontextprotocol/server-memory`)
- Core dependencies:
  - python-dotenv
  - Pydantic v2

## Getting Started

### 1. Clone and bootstrap (recommended)

```powershell
git clone https://github.com/Shizue123/agent-setup.git
cd agent-setup
.\scripts\setup.ps1
```

The setup script will:
- create `.venv`
- upgrade `pip`, `setuptools`, and `wheel`
- install dependencies from `exercises/requirements.txt`
- generate `exercises/.env` from `exercises/.env.example` if missing

### 2. Configure environment variables

Edit `exercises/.env` and provide your API keys (for example `OPENAI_API_KEY`).

### 3. Run phase by phase

```powershell
.\.venv\Scripts\python.exe exercises/01-langchain-basics/01_hello_agent.py
.\.venv\Scripts\python.exe exercises/02-langgraph-workflow/01_simple_graph.py
.\.venv\Scripts\python.exe exercises/03-crewai-multiagent/01_research_crew.py
.\.venv\Scripts\python.exe exercises/04-autogen-agents/01_multi_agent_chat.py
.\.venv\Scripts\python.exe exercises/05-advanced-patterns/01_research_pipeline.py
```
