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

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.messages import BaseMessage, HumanMessage, ToolMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

load_dotenv()

# ============================================
# 练习 1.1: 基础模型调用
# ============================================
def exercise_1_basic_chat():
    """
    任务: 创建一个 ChatOpenAI 实例并完成一次最基础的对话调用。
    """
    
    print("\n--- 开始执行 1.1 基础模型调用 (DeepSeek 版) ---")
    # 步骤 1: 实例化模型
    # 因为底层完全兼容，所以依然用 ChatOpenAI。
    # 这里需要把 model 参数换成 DeepSeek 的模型名
    llm = ChatOpenAI(model="deepseek-chat")
    # 步骤 2: 调用模型
    response = llm.invoke("你好，介绍一下你自己")
    # 步骤 3: 打印结果
    print(f"🤖 模型回答: {response.content}")
    


# ============================================
# 练习 1.2: Function Calling / Tool Use
# ============================================
# 步骤 1: 定义一个工具
# @tool 装饰器会把这个普通的 Python 函数变成 LangChain 认识的工具
# 注意：函数下面的 """文档字符串(Docstring)""" 非常重要，模型就是靠读这段话来决定要不要用这个工具的！
@tool
def get_weather(location: str) -> str:
    """获取指定城市的当前天气。"""
    print(f"   [系统底层执行] 正在调用假天气API查询 {location} ...")
    if "洛杉矶" in location:
        return "晴朗，气温 25°C"
    return "未知天气"



def exercise_2_tool_use():
    """
    任务: 手动完成一次 Tool Calling 闭环。
    
    步骤:
    1. 把工具绑定到模型
    2. 先让模型返回 tool_calls
    3. 由 Python 手动执行工具
    4. 把工具结果作为 ToolMessage 发回模型
    5. 获得最终自然语言回答
    """
    print("\n--- 开始执行 1.2 Tool Use ---")
    llm = ChatOpenAI(model="deepseek-chat")
    
    # 步骤 1: 将工具绑定给模型 (告诉大脑：你现在拥有查天气的超能力了)
    llm_with_tools = llm.bind_tools([get_weather])

    # 步骤 2: 提问一个必须用工具才能回答的问题
    question = "洛杉矶今天的天气怎么样？"
    print(f"👤 用户提问: {question}")
    messages: list[BaseMessage] = [HumanMessage(content=question)]

    # 第一次调用：模型先告诉你它打算调用什么工具。
    response = llm_with_tools.invoke(messages)
    print("\n🤖 模型第一次返回（此时还不是最终答案）:")
    print(response)

    if not response.tool_calls:
        print("\n⚠️ 这次模型没有触发工具调用，直接返回了内容：")
        print(response.content)
        return

    messages.append(response)

    # 第二次处理：由你的 Python 代码真正执行工具。
    for tool_call in response.tool_calls:
        print(f"\n🔧 模型请求调用工具: {tool_call['name']}({tool_call['args']})")

        if tool_call["name"] != "get_weather":
            continue

        tool_result = get_weather.invoke(tool_call["args"])
        print(f"🛠 工具执行结果: {tool_result}")

        # 把工具结果发回给模型，模型才能继续生成最终答案。
        messages.append(
            ToolMessage(
                content=tool_result,
                tool_call_id=tool_call["id"],
            )
        )

    # 第三次调用：模型基于工具结果，组织成最终自然语言回答。
    final_response = llm_with_tools.invoke(messages)
    print(f"\n✅ 最终回答: {final_response.content}")

    

# ============================================
# 练习 1.3: ReAct Agent
# ============================================
def exercise_3_react_agent():
    """
    任务: 使用 Agent 自动完成“模型决策 -> 工具调用 -> 结果整理”闭环。
    """
    print("\n--- 开始执行 1.3 Agent ---")
    
    # langchain 1.x 中 create_agent 会自动完成：
    # 选择工具 -> 调用工具 -> 把结果再交还给模型 -> 输出最终答案。
    agent = create_agent(
        model=ChatOpenAI(model="deepseek-chat"),
        tools=[get_weather],
        system_prompt="你是一个乐于助人的天气助手，遇到天气问题时优先调用工具获取信息。",
    )
    
    question = "洛杉矶今天的天气怎么样？"
    print(f"👤 用户提问: {question}")
    
    result = agent.invoke(
        {"messages": [{"role": "user", "content": question}]}
    )
    
    # 取最后一条消息作为最终回答。
    print(f"\n✅ 最终回答: {result['messages'][-1].content}")



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
