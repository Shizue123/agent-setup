"""
练习 2: LangGraph 工作流编排
==============================
目标: 掌握 LangGraph 的核心概念 — StateGraph, Node, Edge

前置条件:
    pip install langgraph langchain-openai python-dotenv
"""

import os
from typing import TypedDict, Annotated
from dotenv import load_dotenv

load_dotenv()

# ============================================
# 练习 2.1: 最简单的图
# ============================================

class SimpleState(TypedDict):
    """定义图的状态"""
    messages: list[str]
    current_step: str

def exercise_1_simple_graph():
    """
    任务: 创建一个简单的 3 节点顺序图
    
    流程: start → process → summarize → END
    
    步骤:
    1. 导入 StateGraph, START, END
    2. 定义状态 TypedDict
    3. 创建三个节点函数
    4. 添加边连接节点
    5. 编译并运行
    
    提示:
        from langgraph.graph import StateGraph, START, END
        
        graph = StateGraph(SimpleState)
        graph.add_node("process", process_func)
        graph.add_edge(START, "process")
        graph.add_edge("process", END)
        
        app = graph.compile()
        result = app.invoke({"messages": [], "current_step": ""})
    """
    from langgraph.graph import StateGraph, START, END
    
    def start_node(state: SimpleState) -> dict:
        """起始节点：初始化"""
        # TODO: 向 messages 添加一条消息
        return {"messages": state["messages"] + ["开始处理"], "current_step": "start"}
    
    def process_node(state: SimpleState) -> dict:
        """处理节点：处理数据"""
        # TODO: 处理消息
        return {"messages": state["messages"] + ["处理中..."], "current_step": "process"}
    
    def summarize_node(state: SimpleState) -> dict:
        """总结节点：生成总结"""
        # TODO: 总结所有消息
        return {"messages": state["messages"] + ["总结完成"], "current_step": "summarize"}
    
    # TODO: 创建图，添加节点和边，编译运行
    pass


# ============================================
# 练习 2.2: 条件路由
# ============================================

class RouterState(TypedDict):
    """带路由的状态"""
    query: str
    category: str
    response: str

def exercise_2_conditional_routing():
    """
    任务: 创建一个带条件路由的图
    
    流程:
        classify → (技术问题) → tech_support
                 → (一般问题) → general_support
                 → (投诉) → complaint_handler
        → END
    
    步骤:
    1. 创建分类节点
    2. 创建路由函数
    3. 使用 add_conditional_edges 添加条件边
    
    提示:
        graph.add_conditional_edges(
            "classify",
            route_function,  # 返回下一个节点的名称
            {
                "tech": "tech_support",
                "general": "general_support",
                "complaint": "complaint_handler"
            }
        )
    """
    from langgraph.graph import StateGraph, START, END
    
    # TODO: 实现分类器和各处理节点
    # TODO: 创建图并添加条件路由
    pass


# ============================================
# 练习 2.3: 循环（ReAct 模式）
# ============================================

class AgentState(TypedDict):
    """Agent 状态"""
    messages: list
    tool_calls: list
    iteration: int
    max_iterations: int
    final_answer: str

def exercise_3_loop_pattern():
    """
    任务: 实现一个带循环的 Agent 图（ReAct 模式）
    
    流程:
        agent → should_continue? → (yes) → tool → agent (循环)
                                 → (no)  → END
    
    步骤:
    1. 创建 agent 节点（模拟 LLM 决策）
    2. 创建 tool 节点（模拟工具执行）
    3. 创建 should_continue 函数（决定是否继续循环）
    4. 连接为循环图
    
    这是 Agent 最核心的设计模式！
    
    提示:
        graph.add_conditional_edges(
            "agent",
            should_continue,
            {"continue": "tool", "end": END}
        )
        graph.add_edge("tool", "agent")  # 形成循环
    """
    from langgraph.graph import StateGraph, START, END
    
    # TODO: 实现 agent 节点、tool 节点、should_continue 路由
    # TODO: 创建循环图
    pass


# ============================================
# 练习 2.4: 带 LLM 的完整 Agent
# ============================================

def exercise_4_llm_agent():
    """
    任务: 创建一个使用真实 LLM 的 Agent
    
    步骤:
    1. 定义工具（搜索、计算等）
    2. 创建带工具绑定的 LLM
    3. 构建 Agent 图
    4. 运行并观察 Agent 的推理过程
    
    提示:
        from langchain_openai import ChatOpenAI
        from langchain_core.tools import tool
        from langgraph.prebuilt import create_react_agent
        
        # 最简单的方式：使用预构建的 ReAct Agent
        agent = create_react_agent(model, tools)
        result = agent.invoke({"messages": [("user", "你的问题")]})
    """
    # TODO: 创建完整的 LLM Agent
    pass


if __name__ == "__main__":
    print("=" * 50)
    print("练习 2: LangGraph 工作流编排")
    print("=" * 50)
    
    print("\n--- 2.1 简单的顺序图 ---")
    exercise_1_simple_graph()
    
    print("\n--- 2.2 条件路由 ---")
    exercise_2_conditional_routing()
    
    print("\n--- 2.3 循环模式 ---")
    exercise_3_loop_pattern()
    
    print("\n--- 2.4 带 LLM 的 Agent ---")
    exercise_4_llm_agent()
