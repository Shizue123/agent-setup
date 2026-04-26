[**English**](./README_en.md) | [**简体中文**](./README.md)

# Agent Setup

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-Enabled-1C3C3C)
![LangGraph](https://img.shields.io/badge/LangGraph-Workflow-blue)
![CrewAI](https://img.shields.io/badge/CrewAI-Multi--Agent-orange)
![AutoGen](https://img.shields.io/badge/AutoGen-AgentChat-6f42c1)
![MCP](https://img.shields.io/badge/MCP-Integrated-0a7ea4)
![License](https://img.shields.io/badge/License-MIT-green)

## 项目概述

Agent Setup 是一个面向 AI Agent 工程学习与实验的渐进式工作区。
仓库围绕从单 Agent 到多 Agent、从基础调用到 Workflow Orchestration 的路线组织，保证每个阶段都可以直接运行、直接复现。

当前代码主线已经覆盖：
- AutoGen Phase 4.3 的 MCP 工作台接入（`workbench=mcp`）。
- LangGraph Phase 5 的 fan-out/fan-in 并发汇聚与 reducer 状态合并。
- 反思式循环路由（quality gate）与模板仓库安全清理。

## 核心特性

- 阶段化学习路径：`exercises/01` 到 `exercises/05` 全链路可运行。
- 多框架协同：LangChain、LangGraph、CrewAI、AutoGen、MCP。
- Windows 友好工程化：`setup.ps1` 自动初始化 venv、安装依赖、生成 `.env`。
- 安全默认配置：通过环境变量注入 API Key，不在业务代码中硬编码敏感凭据。
- 可扩展参考库机制：可按需克隆 `projects/` 下的官方示例仓库。

## 技术栈

- 语言与运行时：Python 3.10+、PowerShell、venv、pip
- Agent 框架：
    - LangChain
    - LangGraph
    - CrewAI / crewai-tools
    - AutoGen (`autogen-agentchat`, `autogen-ext[openai]`)
- 协议与集成：
    - MCP（Model Context Protocol），通过 Node.js stdio server (`@modelcontextprotocol/server-memory`)
- 基础依赖：
    - python-dotenv
    - Pydantic v2

## 快速启动

### 1. 克隆并初始化（推荐）

```powershell
git clone https://github.com/Shizue123/agent-setup.git
cd agent-setup
.\scripts\setup.ps1
```

初始化脚本会自动完成：
- 创建 `.venv`
- 升级 `pip`、`setuptools`、`wheel`
- 安装 `exercises/requirements.txt`
- 若缺失则从 `exercises/.env.example` 生成 `exercises/.env`

### 2. 配置环境变量

编辑 `exercises/.env`，补充你的 API Key（例如 `OPENAI_API_KEY`）。

### 3. 按阶段运行

```powershell
.\.venv\Scripts\python.exe exercises/01-langchain-basics/01_hello_agent.py
.\.venv\Scripts\python.exe exercises/02-langgraph-workflow/01_simple_graph.py
.\.venv\Scripts\python.exe exercises/03-crewai-multiagent/01_research_crew.py
.\.venv\Scripts\python.exe exercises/04-autogen-agents/01_multi_agent_chat.py
.\.venv\Scripts\python.exe exercises/05-advanced-patterns/01_research_pipeline.py
```


