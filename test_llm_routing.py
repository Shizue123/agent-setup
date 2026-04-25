import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
import logging
import warnings

# 屏蔽 LangChain 过时的烦人警告，让输出干净点
warnings.filterwarnings("ignore")

import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "exercises", "02-langgraph-workflow"))
from importlib import import_module
simple_graph = import_module("01_simple_graph")
search_weather = simple_graph.search_weather

load_dotenv()

# 初始化你的专属 DeepSeek Agent
model = ChatOpenAI(
    model="deepseek-chat",
    temperature=0,
    base_url=os.environ.get("OPENAI_API_BASE", "https://api.deepseek.com/v1")
)

tools = [search_weather]
agent_executor = create_react_agent(model, tools)

print("==================================================")
print(" 🚀 联合架构边缘测试 (Agent + 双通道代理 + Fallback) ")
print("==================================================\n")

test_queries = [
    "帮我查一下拉萨现在的天气情况。",
    "我马上要去洛杉矶(Los Angeles)出差，那边天气咋样？", 
    "纽约现在几度了？" # 这是一个坑坑 Agent 的陷阱问题！
]

for i, query in enumerate(test_queries, 1):
    print(f"[{i}] 用户提问: {query}")
    print("-" * 50)
    
    result = agent_executor.invoke({"messages": [("user", query)]})
    
    print(f"\n[✨ DeepSeek 最终回复]:\n{result['messages'][-1].content}\n")
    print("=" * 50 + "\n")
