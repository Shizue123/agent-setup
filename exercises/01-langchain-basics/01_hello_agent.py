"""
练习 1: LangChain 基础 — Hello Agent
=====================================
目标: 理解 LangChain 的基本组件和 Agent 概念

前置条件:
    pip install langchain langchain-openai python-dotenv

设置环境变量:
    创建 .env 文件，添加: OPENAI_API_KEY=sk-xxx
    或者使用其他模型提供商的 API Key
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ============================================
# 练习 1.1: 基础模型调用
# ============================================
# TODO: 使用 ChatOpenAI 或其他模型进行基础对话
# 提示: from langchain_openai import ChatOpenAI

def exercise_1_basic_chat():
    """
    任务: 创建一个 ChatOpenAI 实例并调用它
    
    步骤:
    1. 导入 ChatOpenAI
    2. 创建模型实例
    3. 调用 model.invoke("你好，介绍一下你自己")
    4. 打印结果
    """
    # 你的代码写在这里
    pass


# ============================================
# 练习 1.2: Function Calling / Tool Use
# ============================================
# TODO: 定义一个工具，让模型能够调用它

def exercise_2_tool_use():
    """
    任务: 创建工具并让 Agent 使用
    
    步骤:
    1. 使用 @tool 装饰器定义一个搜索工具（模拟）
    2. 将工具绑定到模型
    3. 调用模型并处理工具调用
    
    提示:
        from langchain_core.tools import tool
        
        @tool
        def search(query: str) -> str:
            '''搜索互联网上的信息'''
            return f"搜索结果: {query} 的相关信息..."
    """
    # 你的代码写在这里
    pass


# ============================================
# 练习 1.3: ReAct Agent
# ============================================
# TODO: 创建一个完整的 ReAct Agent

def exercise_3_react_agent():
    """
    任务: 构建一个 ReAct Agent
    
    步骤:
    1. 定义工具集（搜索、计算器等）
    2. 创建 Agent（使用 create_react_agent）
    3. 运行 Agent 完成一个任务
    
    提示:
        from langchain.agents import create_react_agent, AgentExecutor
        from langchain import hub
        
        prompt = hub.pull("hwchase17/react")
        agent = create_react_agent(llm, tools, prompt)
        executor = AgentExecutor(agent=agent, tools=tools)
    """
    # 你的代码写在这里
    pass


if __name__ == "__main__":
    print("=" * 50)
    print("练习 1: LangChain 基础")
    print("=" * 50)
    
    print("\n--- 1.1 基础模型调用 ---")
    exercise_1_basic_chat()
    
    print("\n--- 1.2 Tool Use ---")
    exercise_2_tool_use()
    
    print("\n--- 1.3 ReAct Agent ---")
    exercise_3_react_agent()
