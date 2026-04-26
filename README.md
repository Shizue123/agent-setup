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

Agent Setup 是一个面向 AI Agent 工程实践的分阶段训练仓库，核心目标是把“可运行示例 + 工程化脚手架 + 多框架对照学习”落到同一工作区。
它解决了学习路径碎片化、环境复现不稳定、跨框架迁移成本高这三类常见痛点，并面向个人开发者、小团队内部培训和 PoC 原型验证场景。
当前主线已形成从单 Agent Tool Calling，到 Workflow Orchestration，再到多 Agent + MCP 集成的闭环演进链路。

## 核心特性

- Tool Calling 闭环实现清晰：`exercises/01-langchain-basics/01_hello_agent.py` 中完整演示了 `tool_calls -> ToolMessage 回填 -> 最终回答` 的三段式执行链。
- Graph 路由与循环模式可观测：`exercises/02-langgraph-workflow/01_simple_graph.py` 覆盖顺序图、条件路由（`add_conditional_edges`）和 ReAct 循环（agent-tool-agent）。
- 多 Agent 分工策略对照充分：`exercises/03-crewai-multiagent/01_research_crew.py` 同时提供 sequential、hierarchical 与 flow/router 三种编排形态。
- MCP 工具工作台接入稳定：`exercises/04-autogen-agents/01_multi_agent_chat.py` 使用 `workbench=mcp`，并通过 `getattr` 兼容消息对象差异，降低 SDK 版本漂移风险。
- 并发状态冲突处理到位：`exercises/05-advanced-patterns/01_research_pipeline.py` 通过 `Annotated + merge_dicts` 处理 fan-out 并行写入同一 state key 的竞争问题。

## 架构与技术栈

### 数据流转路径

1. 用户输入进入阶段脚本（`exercises/01`~`05`）。
2. 根据阶段模式触发不同执行内核：
     - LangChain: 模型调用与工具回填。
     - LangGraph: StateGraph 节点执行、条件边路由、循环迭代。
     - CrewAI: Agent/Task/Crew 或 Flow 事件监听链。
     - AutoGen: AgentChat 消息驱动与 MCP 工具桥接。
3. 输出统一回落到控制台日志，便于学习者观察状态变化与调用顺序。

### 模块依赖关系

- `scripts/setup.ps1` 负责环境初始化（venv、pip 工具链、依赖安装、`.env` 模板落盘）。
- `exercises/requirements.txt` 提供统一依赖基线。
- `exercises/01`~`05` 提供逐级增强的编排样例，形成横向框架对照与纵向能力递进。
- `scripts/clone-reference-repos.ps1` 可选拉取 `projects/` 参考实现，用于源码级对照学习。

### 具体技术栈

- 语言与运行时：Python 3.10+、PowerShell、venv、pip
- Agent 框架：LangChain、LangGraph、CrewAI、AutoGen
- 协议层：MCP（Model Context Protocol）
- 配置与数据模型：python-dotenv、Pydantic v2、TypedDict / Annotated
- 平台要求：Windows / macOS / Linux（PowerShell 脚本主要面向 Windows）

## 快速启动

### 前置依赖

- Python 3.10+
- Git
- Node.js 18+（用于 MCP 相关示例中的 `npx`）

### 1. 克隆仓库

```powershell
git clone https://github.com/Shizue123/agent-setup.git
cd agent-setup
```

### 2. 方式 A：一键初始化（推荐）

```powershell
.\scripts\setup.ps1
```

### 3. 方式 B：手动初始化

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r exercises/requirements.txt
Copy-Item exercises/.env.example exercises/.env
```

### 4. 配置环境变量

编辑 `exercises/.env`，补充你的 API Key（例如 `OPENAI_API_KEY`）。

### 5. 按阶段运行

```powershell
.\.venv\Scripts\python.exe exercises/01-langchain-basics/01_hello_agent.py
.\.venv\Scripts\python.exe exercises/02-langgraph-workflow/01_simple_graph.py
.\.venv\Scripts\python.exe exercises/03-crewai-multiagent/01_research_crew.py
.\.venv\Scripts\python.exe exercises/04-autogen-agents/01_multi_agent_chat.py
.\.venv\Scripts\python.exe exercises/05-advanced-patterns/01_research_pipeline.py
```

### 6. 可选：拉取官方参考仓库

```powershell
.\scripts\clone-reference-repos.ps1
```

用于将 LangGraph / CrewAI 等官方仓库拉取到 `projects/` 做本地对照学习。


