"""
练习 4: Microsoft AutoGen 多 Agent 对话
==========================================
目标: 使用 AutoGen 构建多 Agent 对话系统

前置条件:
    pip install autogen-agentchat autogen-ext[openai] python-dotenv
"""

import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

# ============================================
# 练习 4.1: 基础 Agent
# ============================================

async def exercise_1_basic_agent():
    """
    任务: 创建一个基础的 AutoGen Agent
    
    步骤:
    1. 创建 OpenAIChatCompletionClient
    2. 创建 AssistantAgent
    3. 运行 agent.run()
    
    提示:
        from autogen_agentchat.agents import AssistantAgent
        from autogen_ext.models.openai import OpenAIChatCompletionClient
        
        model_client = OpenAIChatCompletionClient(model="gpt-4")
        agent = AssistantAgent("assistant", model_client=model_client)
        result = await agent.run(task="Say hello!")
        print(result)
        await model_client.close()
    """
    # TODO: 创建基础 Agent
    pass


# ============================================
# 练习 4.2: 多 Agent 编排（AgentTool）
# ============================================

async def exercise_2_multi_agent():
    """
    任务: 使用 AgentTool 实现多 Agent 协作
    
    架构:
    - 主 Agent (General Assistant)
      - 工具1: 数学专家 Agent
      - 工具2: 编程专家 Agent
    
    主 Agent 根据问题类型自动调用专家
    
    提示:
        from autogen_agentchat.tools import AgentTool
        
        math_agent = AssistantAgent(
            "math_expert",
            model_client=model_client,
            system_message="You are a math expert.",
            description="A math expert assistant.",
        )
        math_tool = AgentTool(math_agent, return_value_as_last_message=True)
        
        main_agent = AssistantAgent(
            "assistant",
            model_client=model_client,
            tools=[math_tool, code_tool],
        )
    """
    # TODO: 创建多 Agent 编排
    pass


# ============================================
# 练习 4.3: 带 MCP 工具的 Agent
# ============================================

async def exercise_3_mcp_agent():
    """
    任务: 创建一个使用 MCP Server 工具的 Agent
    
    MCP (Model Context Protocol) 是一种标准化的工具协议
    
    提示:
        from autogen_ext.tools.mcp import McpWorkbench, StdioServerParams
        
        server_params = StdioServerParams(
            command="npx",
            args=["@playwright/mcp@latest", "--headless"],
        )
        async with McpWorkbench(server_params) as mcp:
            agent = AssistantAgent(
                "web_agent",
                model_client=model_client,
                workbench=mcp,
            )
            await Console(agent.run_stream(task="..."))
    """
    # TODO: 创建 MCP Agent（需要安装对应的 MCP Server）
    pass


if __name__ == "__main__":
    print("=" * 50)
    print("练习 4: AutoGen 多 Agent 对话")
    print("=" * 50)
    
    print("\n--- 4.1 基础 Agent ---")
    asyncio.run(exercise_1_basic_agent())
    
    print("\n--- 4.2 多 Agent 编排 ---")
    asyncio.run(exercise_2_multi_agent())
    
    print("\n--- 4.3 MCP Agent ---")
    asyncio.run(exercise_3_mcp_agent())
