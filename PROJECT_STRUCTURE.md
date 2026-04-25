[🇨🇳 简体中文](https://github.com/Shizue123/agent-setup/tree/main) | [🇺🇸 English](https://github.com/Shizue123/agent-setup/tree/En)

# Agent-Setup 项目结构与代码导读

本项目是一个由浅入深、循序渐进的 AI Agent 学习与开发脚手架。从基础的 LangChain 到复杂的 AutoGen 多智能体以及 MCP（Model Context Protocol）协议挂载，项目代码按照架构难度和商业落地逻辑进行了切割。

目前的工程目录结构已经非常合理（按照“脚本配置” -> “阶段练习” -> “外部参考”的逻辑组织），因此不需要进行大的文件夹合并或移动代码，以保持学习路径的连贯性。

以下是对当前项目根目录下各个文件夹及核心代码的详细说明：

## 根目录核心文件
- `README.md`: 项目的主说明文件，快速指引。
- `LICENSE`: 开源授权协议。
- `gemini-tutor-prompt.md`: 用于设定 AI 导师（如我）的 Prompt，确保能以“先架构职责、后代码映射”的资深开发者视角为你提供教学辅助。

---

## 📂 exercises / (核心实战演练场)
这是你学习和敲代码的主战场，按照 01 到 05 的阶段逐步深入：

### `01-langchain-basics/` (第一阶段：基础概念)
- **`01_hello_agent.py`**: 介绍基础模型调用、Prompt 模板、以及最简单的单 Agent 流程。
- **`phase1_review.txt`**: 第一阶段的学习和架构复盘笔记。

### `02-langgraph-workflow/` (第二阶段：图与状态机)
- **`01_simple_graph.py`**: 引入状态机概念，通过节点 (Nodes) 和边 (Edges) 构建具有流转逻辑和循环的工作流底座，这是复杂 Agent 编排的最重要基础。

### `03-crewai-multiagent/` (第三阶段：声明式多 Agent)
- **`01_research_crew.py`**: 使用 CrewAI 框架，以“声明式”的方法建立员工（Agent）、任务（Task）和团队（Crew），实现基于角色的顺序/层级流水线。
- **`phase3_summary.md`**: 总结 CrewAI 的核心（角色扮演、硬编码业务逻辑等）。

### `04-autogen-agents/` (第四阶段：Actor 异步多 Agent 与 MCP)
- **`01_multi_agent_chat.py`**: 通过微软 AutoGen 实现无严格图连线的异步多体对话路由。包含了 `4.1基础Agent`、`4.2多Agent作为工具(AgentTool)`，以及最具商业潜力的 `4.3 MCP Agent`（通过 Node.js 本地服务挂载工具箱）。
- **`phase4_summary.md`**: 涵盖了 AutoGen 与 MCP 的填坑总结和架构流转思想。
- *备注：此部分代码克服了 0.7+ 版本的 MCP 工具绑定限制。*

### `05-advanced-patterns/` (第五阶段：高级系统编排)
- **`01_research_pipeline.py`**: 将 1~4 阶段的思想融合，回归 LangGraph 构建高度可控的工业级管线。实现了扇出（并发搜索）、扇入（归纳）、Reducer（状态防冲突）以及带打分机制的质量反思循环（Reflection Loop）。
- **`phase5_summary.md`**: 总结阶段 5 并发处理与状态控制模式文档。

### 其他
- `requirements.txt`: 演练场需要的 Python 依赖包。
- `并发文本同步练习.txt`: 相关的测试临时文本。

---

## 📂 projects / (外部优秀开源参考项目)
使用脚本全局克隆下来的业界顶级参考项目，用于查阅底层源码或官方高级示例。
- **`crewai-examples/`**: 官方提供的各行业 CrewAI 商业落地 Demo（如求职、营销、股票分析等）。
- **`langgraph/`**: Langchain 官方的图框架源码及大量优秀的设计模式模板（如 reflexions, plan-and-execute 等）。

---

## 📂 scripts / (环境与依赖自动化配置)
用于快速部署开发环境的 PowerShell 脚本。
- **`clone-reference-repos.ps1`**: 自动化获取外部参考源码（即克隆 `projects/` 下的内容）的脚本。
- **`setup.ps1`**: 自动配置 Python 虚拟环境（.venv）、安装依赖包、甚至初始化全局配置的脚本。

