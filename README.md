[**简体中文**](./README_zh-CN.md) | [**English**](./README.md)

# Agent Setup

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-Enabled-1C3C3C)
![LangGraph](https://img.shields.io/badge/LangGraph-Workflow-blue)
![CrewAI](https://img.shields.io/badge/CrewAI-Multi--Agent-orange)
![AutoGen](https://img.shields.io/badge/AutoGen-AgentChat-6f42c1)
![MCP](https://img.shields.io/badge/MCP-Integrated-0a7ea4)
![License](https://img.shields.io/badge/License-MIT-green)

## Overview

Agent Setup is a progressive learning workspace for modern AI Agent engineering.
It organizes runnable examples, environment automation, and phase-based exercises in one repository so learners can move from single-agent basics to multi-agent orchestration and MCP tool integration.

Recent code evolution in this workspace includes:
- Stabilized AutoGen 4.3 MCP integration using `workbench=mcp` and safe message content extraction.
- Completed advanced LangGraph pipeline patterns in Phase 5, including fan-out/fan-in, reducer-based concurrent state merge, and reflection loop routing.
- Repository hygiene cleanup to keep the template safe for public sharing.

## Core Features

- Progressive curriculum from foundational prompting to production-oriented orchestration.
- Phase-based runnable scripts under `exercises/01` to `exercises/05`.
- Multi-framework coverage: LangChain, LangGraph, CrewAI, AutoGen, and MCP.
- Windows-friendly setup scripts with virtual environment bootstrap and dependency installation.
- Security-friendly defaults (`.env.example` template, env var based keys, no hardcoded credentials).

## Tech Stack

- Language: Python 3.10+
- Runtime and tooling: PowerShell, venv, pip
- Agent frameworks:
    - LangChain
    - LangGraph
    - CrewAI and crewai-tools
    - AutoGen (`autogen-agentchat`, `autogen-ext[openai]`)
- Integration protocol:
    - MCP (Model Context Protocol) via Node.js stdio server (`@modelcontextprotocol/server-memory`)
- Config and typing:
    - python-dotenv
    - Pydantic v2

## Getting Started

### 1. Clone and bootstrap (recommended)

```powershell
git clone https://github.com/Shizue123/agent-setup.git
cd agent-setup
.\scripts\setup.ps1
```

This script will:
- create `.venv`
- upgrade `pip`, `setuptools`, `wheel`
- install dependencies from `exercises/requirements.txt`
- create `exercises/.env` from `exercises/.env.example` when missing

### 2. Configure environment variables

Edit `exercises/.env` and add your keys (for example `OPENAI_API_KEY`).

### 3. Run by phase

```powershell
.\.venv\Scripts\python.exe exercises/01-langchain-basics/01_hello_agent.py
.\.venv\Scripts\python.exe exercises/02-langgraph-workflow/01_simple_graph.py
.\.venv\Scripts\python.exe exercises/03-crewai-multiagent/01_research_crew.py
.\.venv\Scripts\python.exe exercises/04-autogen-agents/01_multi_agent_chat.py
.\.venv\Scripts\python.exe exercises/05-advanced-patterns/01_research_pipeline.py
```

### 4. Optional reference repositories

```powershell
.\scripts\clone-reference-repos.ps1
```

This downloads selected upstream references into `projects/` for local study only.

