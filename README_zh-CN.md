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

Agent Setup 是一个面向 AI Agent 工程学习的渐进式工作区，目标是把可运行示例、环境自动化和阶段化练习组织到同一仓库中，让学习者可以从单 Agent 基础逐步走向多 Agent 编排与 MCP 集成。

结合当前代码与最近变更，项目重点已覆盖：
- Phase 4.3 中 AutoGen + MCP 的稳定接入，采用 `workbench=mcp` 并兼容消息对象差异。
- Phase 5 中 LangGraph 高级模式落地，包括 fan-out/fan-in、并发状态 reducer 合并、反思式循环路由。
- 模板仓库清理和安全加固，保证公开分享时不携带敏感信息与临时测试文件。

## Core Features

- 分阶段学习路径：从 Prompt 与单 Agent 到复杂工作流与多智能体协作。
- `exercises/01` 到 `exercises/05` 全部可直接运行。
- 覆盖主流框架：LangChain、LangGraph、CrewAI、AutoGen、MCP。
- 提供 Windows 友好的自动化脚本（`venv` 初始化、依赖安装、`.env` 模板生成）。
- 默认采用安全实践：通过环境变量注入密钥，不在代码中硬编码凭据。

## Tech Stack

- 语言：Python 3.10+
- 运行与工具：PowerShell、venv、pip
- Agent 框架：
  - LangChain
  - LangGraph
  - CrewAI / crewai-tools
  - AutoGen (`autogen-agentchat`, `autogen-ext[openai]`)
- 协议与集成：
  - MCP (Model Context Protocol)，通过 Node.js stdio server (`@modelcontextprotocol/server-memory`)
- 配置与类型：
  - python-dotenv
  - Pydantic v2

## Getting Started

### 1. 克隆并初始化（推荐）

```powershell
git clone https://github.com/Shizue123/agent-setup.git
cd agent-setup
.\scripts\setup.ps1
```

该脚本会自动：
- 创建 `.venv`
- 升级 `pip`、`setuptools`、`wheel`
- 安装 `exercises/requirements.txt` 依赖
- 若缺失则从 `exercises/.env.example` 生成 `exercises/.env`

### 2. 配置环境变量

编辑 `exercises/.env` 并填写你的 API Key（如 `OPENAI_API_KEY`）。

### 3. 按阶段运行示例

```powershell
.\.venv\Scripts\python.exe exercises/01-langchain-basics/01_hello_agent.py
.\.venv\Scripts\python.exe exercises/02-langgraph-workflow/01_simple_graph.py
.\.venv\Scripts\python.exe exercises/03-crewai-multiagent/01_research_crew.py
.\.venv\Scripts\python.exe exercises/04-autogen-agents/01_multi_agent_chat.py
.\.venv\Scripts\python.exe exercises/05-advanced-patterns/01_research_pipeline.py
```

### 4. 可选参考仓库

```powershell
.\scripts\clone-reference-repos.ps1
```

该命令会把官方参考仓库拉取到 `projects/`，仅用于本地学习，不参与本仓库版本管理。
