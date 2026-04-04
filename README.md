# 🤖 AI Agent 学习路径

## 目录
- [工程目录结构](#工程目录结构)
- [文件位置索引](#文件位置索引)
- [环境准备](#环境准备)
- [学习路线图](#学习路线图)
- [阶段一：基础概念](#阶段一基础概念--agent-原理与-llm-基础)
- [阶段二：核心框架](#阶段二核心框架--agent-开发框架)
- [阶段三：工作流编排](#阶段三工作流编排--agent-workflow-orchestration)
- [阶段四：多智能体系统](#阶段四多智能体系统--multi-agent-systems)
- [阶段五：生产部署](#阶段五生产部署--production-deployment)
- [推荐项目](#推荐学习项目)
- [学习资源](#学习资源)

---

## 工程目录结构

当前工作区的实际目录层级如下：

```text
agent-setup/
├── .venv/
├── README.md
├── gemini-tutor-prompt.md
├── exercises/
│   ├── .env
│   ├── .env.example
│   ├── requirements.txt
│   ├── 01-langchain-basics/
│   │   └── 01_hello_agent.py
│   ├── 02-langgraph-workflow/
│   │   └── 01_simple_graph.py
│   ├── 03-crewai-multiagent/
│   │   └── 01_research_crew.py
│   ├── 04-autogen-agents/
│   │   └── 01_multi_agent_chat.py
│   └── 05-advanced-patterns/
│       └── 01_research_pipeline.py
└── projects/
    ├── crewai-examples/
    ├── deepagents/
    └── langgraph/
```

## 文件位置索引

### 根目录
- 学习总览文档：README.md
- Gemini 辅导设定：gemini-tutor-prompt.md
- Python 虚拟环境：.venv/

### 环境与依赖
- 本地环境变量文件：exercises/.env
- 环境变量模板：exercises/.env.example
- 练习依赖清单：exercises/requirements.txt

### 练习代码
- LangChain 基础练习：exercises/01-langchain-basics/01_hello_agent.py
- LangGraph 工作流练习：exercises/02-langgraph-workflow/01_simple_graph.py
- CrewAI 多智能体练习：exercises/03-crewai-multiagent/01_research_crew.py
- AutoGen 多 Agent 练习：exercises/04-autogen-agents/01_multi_agent_chat.py
- 高级编排综合练习：exercises/05-advanced-patterns/01_research_pipeline.py

### 已克隆的参考项目
- LangGraph 源码仓库：projects/langgraph/
- CrewAI 示例仓库：projects/crewai-examples/
- Deep Agents 示例仓库：projects/deepagents/

### 推荐查看顺序
1. 先看 README.md 了解总体路线
2. 先创建并激活 .venv 虚拟环境
3. 再安装 exercises/requirements.txt 中的依赖并配置 exercises/.env
4. 按顺序完成 exercises/01-langchain-basics/01_hello_agent.py
5. 然后进入 exercises/02-langgraph-workflow/01_simple_graph.py
6. 再看 CrewAI、AutoGen 和高级模式几个练习文件
7. 遇到实现细节不清楚时，去 projects/ 下面对应仓库查源码和示例

## 环境准备

开始练习前，建议始终先在项目根目录使用虚拟环境，避免全局 Python 包冲突。

### 1. 创建虚拟环境

如果还没有创建，可以在项目根目录执行：

```powershell
python -m venv .venv
```

### 2. 激活虚拟环境

Windows PowerShell：

```powershell
.\.venv\Scripts\Activate.ps1
```

激活后，后续安装依赖和运行练习都应在这个环境里完成。

### 3. 安装依赖

```powershell
pip install -r exercises/requirements.txt
```

如果在 Windows 下安装过程中遇到下载超时、SSL 波动、或 `WinError 32`（临时文件被占用）等问题，建议使用下面这套更稳的安装方式。

#### Windows 稳定安装方案

先在项目根目录创建专用临时目录和缓存目录：

```powershell
New-Item -ItemType Directory -Force .pip-tmp, .pip-cache
```

然后在当前 PowerShell 会话里指定 pip 使用这些目录：

```powershell
$env:TMP = 'D:\agent-setup\.pip-tmp'
$env:TEMP = 'D:\agent-setup\.pip-tmp'
$env:PIP_CACHE_DIR = 'D:\agent-setup\.pip-cache'
```

最后再执行安装：

```powershell
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r exercises/requirements.txt --retries 10 --timeout 120 --disable-pip-version-check
```

这样做的好处：
- 避免系统临时目录中的文件被其他程序占用
- 降低大包下载时因网络慢导致的失败概率
- 在同一项目内保留缓存，后续重装更快

#### 安装后建议检查

```powershell
python -m pip check
python -c "import chromadb, langgraph, crewai_tools, autogen_ext; print('imports-ok')"
```

如果输出 `imports-ok`，说明关键依赖已经可用。

#### VS Code 解释器选择

安装完成后，建议确认 VS Code 当前工作区使用的是 `.venv` 里的解释器，而不是 Conda 或系统 Python。

应选择：

```text
d:\agent-setup\.venv\Scripts\python.exe
```

否则即使依赖已经装好，Pylance 也仍然可能提示无法解析导入。

### 4. 配置环境变量

先复制模板，再填入你的 API Key：

```powershell
Copy-Item exercises/.env.example exercises/.env
```

### 5. 验证环境是否就绪

可以先运行第一节练习，确认解释器和依赖都正常：

```powershell
python exercises/01-langchain-basics/01_hello_agent.py
```

## 学习路线图

```
基础概念 → 核心框架 → 工作流编排 → 多智能体 → 生产部署
  (1周)      (2周)       (2周)       (2周)      (1周)
```

---

## 阶段一：基础概念 — Agent 原理与 LLM 基础

### 学习目标
- 理解什么是 AI Agent（智能体）
- 掌握 LLM 的基础调用（OpenAI API / 其他模型）
- 理解 Prompt Engineering 基础
- 了解 Function Calling / Tool Use 机制

### 核心概念
| 概念 | 说明 |
|------|------|
| **Agent** | 能感知环境、做出决策、执行动作的自主系统 |
| **LLM** | 大语言模型，Agent 的"大脑" |
| **Tool Use** | Agent 调用外部工具（搜索、代码执行、API 等） |
| **Memory** | 短期记忆（对话上下文）和长期记忆（向量数据库） |
| **Planning** | Agent 将复杂任务分解为子任务的能力 |
| **ReAct** | Reasoning + Acting 范式，推理与行动交替 |

### 实践练习
1. 使用 OpenAI API 完成基础对话
2. 实现一个带 Function Calling 的简单 Agent
3. 构建一个能使用搜索工具的 ReAct Agent

### 推荐阅读
- [Lilian Weng: LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/)
- [OpenAI Function Calling Guide](https://platform.openai.com/docs/guides/function-calling)
- [Andrew Ng: Agentic Design Patterns](https://www.deeplearning.ai/the-batch/how-agents-can-improve-llm-performance/)

---

## 阶段二：核心框架 — Agent 开发框架

### 2.1 LangChain（基础框架）
> ⭐ 132k Stars | 构建 LLM 应用的标准框架

**学习内容：**
- LangChain 核心概念：Chain、Agent、Tool、Memory
- LCEL (LangChain Expression Language)
- 集成各种模型和工具
- RAG (Retrieval Augmented Generation)

**本地练习：** `exercises/01-langchain-basics/01_hello_agent.py`

```bash
pip install langchain langchain-openai
```

**文档：** https://docs.langchain.com/

### 2.2 LangGraph（工作流编排 ⭐重点）
> ⭐ 28.2k Stars | 低级别的有状态 Agent 编排框架

**学习内容：**
- 图结构编排（StateGraph）
- 节点（Node）和边（Edge）的定义
- 状态管理（State）
- 条件路由和循环
- Human-in-the-loop
- 持久化和检查点

**本地练习：** `exercises/02-langgraph-workflow/01_simple_graph.py`

**参考源码：** `projects/langgraph/`

```bash
pip install langgraph
```

**文档：** https://docs.langchain.com/oss/python/langgraph/overview

### 2.3 学习路径
```
LangChain 基础 → LCEL → LangGraph 图编排 → 状态管理 → 高级模式
```

---

## 阶段三：工作流编排 — Agent Workflow Orchestration

### 3.1 LangGraph 工作流模式

#### 模式一：顺序执行 (Sequential)
```python
from langgraph.graph import StateGraph

graph = StateGraph(State)
graph.add_node("step1", step1_func)
graph.add_node("step2", step2_func)
graph.add_edge("step1", "step2")
```

#### 模式二：条件路由 (Conditional Routing)
```python
graph.add_conditional_edges(
    "classifier",
    route_function,
    {"path_a": "node_a", "path_b": "node_b"}
)
```

#### 模式三：循环 (Loop / ReAct)
```python
graph.add_conditional_edges(
    "agent",
    should_continue,
    {"continue": "tool", "end": END}
)
graph.add_edge("tool", "agent")  # 循环回 agent
```

#### 模式四：并行执行 (Parallel Fan-out/Fan-in)
```python
graph.add_edge("start", ["branch_a", "branch_b"])
graph.add_edge(["branch_a", "branch_b"], "merge")
```

#### 模式五：子图 (Subgraph)
```python
subgraph = StateGraph(SubState)
# ... 定义子图
main_graph.add_node("sub_process", subgraph.compile())
```

### 3.2 CrewAI Flows（事件驱动编排）
> ⭐ 47.8k Stars | 快速灵活的多 Agent 自动化框架

```python
from crewai.flow.flow import Flow, listen, start, router

class MyFlow(Flow):
    @start()
    def fetch_data(self):
        return {"data": "..."}

    @listen(fetch_data)
    def process_data(self, data):
        return analyze(data)

    @router(process_data)
    def route_result(self):
        if self.state.confidence > 0.8:
            return "high_confidence"
        return "low_confidence"
```

### 3.3 实践项目
1. **研究助手**：搜索 → 筛选 → 总结 → 输出报告
2. **客服系统**：分类 → 路由 → 处理 → 反馈
3. **数据管道**：获取 → 清洗 → 分析 → 可视化

**对应练习文件：**
- LangGraph 基础与循环：`exercises/02-langgraph-workflow/01_simple_graph.py`
- 高级研究管道：`exercises/05-advanced-patterns/01_research_pipeline.py`
- CrewAI Flow 思路：`exercises/03-crewai-multiagent/01_research_crew.py`

---

## 阶段四：多智能体系统 — Multi-Agent Systems

### 4.1 Microsoft AutoGen
> ⭐ 56.6k Stars | 微软的多 Agent AI 框架

**核心概念：**
- AssistantAgent / UserProxyAgent
- 多 Agent 对话和协作
- AgentTool（Agent 作为工具）
- MCP Server 集成
- AutoGen Studio（无代码 GUI）

```bash
pip install autogen-agentchat autogen-ext[openai]
```

**文档：** https://microsoft.github.io/autogen/

**本地练习：** `exercises/04-autogen-agents/01_multi_agent_chat.py`

### 4.2 CrewAI Crews
**核心概念：**
- Agent（角色、目标、背景故事）
- Task（描述、预期输出）
- Crew（Agent 团队 + 流程）
- Process（sequential / hierarchical）

```bash
pip install crewai
```

**文档：** https://docs.crewai.com/

**本地练习：** `exercises/03-crewai-multiagent/01_research_crew.py`

**参考示例：** `projects/crewai-examples/`

### 4.3 多 Agent 协作模式

| 模式 | 说明 | 适用场景 |
|------|------|----------|
| **顺序协作** | Agent A → Agent B → Agent C | 流水线任务 |
| **层级协作** | Manager 分配任务给 Workers | 复杂项目管理 |
| **对话协作** | Agents 之间自由讨论 | 头脑风暴/辩论 |
| **专家路由** | Router 将问题分发给专家 | 客服/知识问答 |
| **竞争协作** | 多 Agent 独立完成，选最优 | 代码生成/方案比较 |

### 4.4 实践项目
1. **写作团队**：研究员 + 作家 + 编辑 协作写文章
2. **代码审查**：Coder + Reviewer + Tester 协作
3. **投资分析**：市场分析师 + 风控专家 + 策略师

---

## 阶段五：生产部署 — Production Deployment

### 学习内容
- Agent 评估和测试（LangSmith）
- 可观测性和追踪
- 错误处理和重试机制
- 安全性考虑（Prompt Injection 防护等）
- 成本优化
- 部署方案（API 服务、Docker、云平台）

### 工具链
| 工具 | 用途 |
|------|------|
| **LangSmith** | 追踪、调试、评估 |
| **LangFuse** | 开源的可观测性平台 |
| **Guardrails AI** | 输出验证和安全防护 |
| **Docker** | 容器化部署 |

---

## 推荐学习项目

### 已克隆到本地（`projects/` 目录）

| # | 项目 | 用途 | 难度 |
|---|------|------|------|
| 1 | `langgraph` | LangGraph 框架源码与官方示例 | ⭐⭐ |
| 2 | `crewai-examples` | CrewAI 官方示例集合 | ⭐⭐ |
| 3 | `deepagents` | 深度 Agent / 子 Agent 设计参考 | ⭐⭐⭐ |

### 本地练习文件（`exercises/` 目录）

| # | 文件 | 用途 | 难度 |
|---|------|------|------|
| 1 | `01-langchain-basics/01_hello_agent.py` | LangChain 基础、Tool Use、ReAct | ⭐ |
| 2 | `02-langgraph-workflow/01_simple_graph.py` | LangGraph 顺序图、条件路由、循环 | ⭐⭐ |
| 3 | `03-crewai-multiagent/01_research_crew.py` | CrewAI Crew 与 Flow 基础 | ⭐⭐ |
| 4 | `04-autogen-agents/01_multi_agent_chat.py` | AutoGen 单 Agent 与多 Agent | ⭐⭐ |
| 5 | `05-advanced-patterns/01_research_pipeline.py` | 综合编排项目 | ⭐⭐⭐ |

### GitHub 推荐仓库

| 仓库 | Stars | 说明 |
|------|-------|------|
| [langchain-ai/langgraph](https://github.com/langchain-ai/langgraph) | 28.2k | 工作流编排核心框架 |
| [microsoft/autogen](https://github.com/microsoft/autogen) | 56.6k | 微软多 Agent 框架 |
| [crewAIInc/crewAI](https://github.com/crewAIInc/crewAI) | 47.8k | 多 Agent 自动化框架 |
| [crewAIInc/crewAI-examples](https://github.com/crewAIInc/crewAI-examples) | - | CrewAI 实战示例集 |
| [langchain-ai/langchain](https://github.com/langchain-ai/langchain) | 132k | LLM 应用基础框架 |
| [langchain-ai/deepagents](https://github.com/langchain-ai/deepagents) | - | 深度 Agent（计划/子Agent） |

---

## 学习资源

### 免费课程
- [DeepLearning.AI: Multi AI Agent Systems with CrewAI](https://www.deeplearning.ai/short-courses/multi-ai-agent-systems-with-crewai/)
- [DeepLearning.AI: AI Agents in LangGraph](https://www.deeplearning.ai/short-courses/ai-agents-in-langgraph/)
- [LangChain Academy](https://academy.langchain.com/courses/intro-to-langgraph)（免费 LangGraph 课程）
- [learn.crewai.com](https://learn.crewai.com/)（CrewAI 官方课程）

### 官方文档
- LangGraph: https://docs.langchain.com/oss/python/langgraph/overview
- CrewAI: https://docs.crewai.com/
- AutoGen: https://microsoft.github.io/autogen/
- LangChain: https://docs.langchain.com/

### 社区
- LangChain Forum: https://forum.langchain.com/
- AutoGen Discord: https://aka.ms/autogen-discord
- CrewAI Community: https://community.crewai.com/
