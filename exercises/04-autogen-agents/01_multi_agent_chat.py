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
    from autogen_agentchat.agents import AssistantAgent
    from autogen_ext.models.openai import OpenAIChatCompletionClient
    from autogen_core.models import ModelInfo
    import os

    print("🤖 [Step 1] 初始化模型客户端 (DeepSeek)...")
    model_client = OpenAIChatCompletionClient(
        model="deepseek-chat",
        api_key=os.environ.get("OPENAI_API_KEY", "dummy"),
        base_url=os.environ.get("OPENAI_API_BASE", "https://api.deepseek.com"),
        model_info=ModelInfo(vision=False, function_calling=True, json_output=False, structured_output=False, family="unknown")
    )
    
    print("🧑‍💻 [Step 2] 创建 AssistantAgent...")
    agent = AssistantAgent(
        name="assistant", 
        model_client=model_client,
        system_message="你是一个幽默的人工智能助手，请用一句简短、带有emoji的中文回答问题。"
    )
    
    print("🎯 [Step 3] 开始运行 Agent...")
    result = await agent.run(task="你好，向我做个简短的自我介绍吧！")
    
    print("\n==================================")
    print("🏆 最终产出结果：\n")
    for msg in result.messages:
        content_val = getattr(msg, "content", None)
        if content_val is None:
            content_val = str(msg)
        content_str = content_val if isinstance(content_val, str) else str(content_val)
        source_name = getattr(msg, "source", "unknown")
        print(f"[{source_name}]: {content_str}")

# ============================================
# 练习 4.2: 多 Agent 编排（AgentTool）
# ============================================

async def exercise_2_multi_agent():
    from autogen_agentchat.agents import AssistantAgent
    from autogen_ext.models.openai import OpenAIChatCompletionClient
    from autogen_core.models import ModelInfo
    from autogen_agentchat.tools import AgentTool
    import os

    print("🤖 1. 初始化模型客户端...")
    model_client = OpenAIChatCompletionClient(
        model="deepseek-chat",
        api_key=os.environ.get("OPENAI_API_KEY", "dummy"),
        base_url=os.environ.get("OPENAI_API_BASE", "https://api.deepseek.com"),
        model_info=ModelInfo(vision=False, function_calling=True, json_output=False, structured_output=False, family="unknown")
    )

    print("🧮 2. 创建【数学专家】Agent...")
    math_agent = AssistantAgent(
        name="math_expert",
        model_client=model_client,
        system_message="你是一个数学专家，擅长解答算术、代数等数学计算问题。请只输出计算步骤和最终数字结果。",
        description="当用户询问数学计算问题、求解方程等相关内容时，必须调用此专家。",
    )
    math_tool = AgentTool(math_agent, return_value_as_last_message=True)

    print("💻 3. 创建【编程专家】Agent...")
    code_agent = AssistantAgent(
        name="code_expert",
        model_client=model_client,
        system_message="你是一个Python编程专家。请根据需求直接输出Python代码块，不需要长篇大论的解释。",
        description="当遇到需要写代码、写Python脚本解决问题时，必须调用此专家。",
    )
    code_tool = AgentTool(code_agent, return_value_as_last_message=True)

    print("🧠 4. 创建【主调度总管】Agent...")
    main_agent = AssistantAgent(
        name="main_assistant",
        model_client=model_client,
        system_message="你是一个主调度员。遇到具体问题时，你会使用数学专家或编程专家工具来找寻答案，最后把所有结果汇总给用户。",
        tools=[math_tool, code_tool],
    )

    task = "首先解一下方程：3x + 12 = 36 求出x。然后写一段Python代码，用for循环打印出 x 次 'Hello Agent'。"
    print(f"\n🎯 下达复杂任务: {task}\n")
    print("---------------- 执行开始 ----------------")
    
    result = await main_agent.run(task=task)
    
    print("\n==================================")
    print("🏆 小组协作结束，汇总对话记录：\n")
    for msg in result.messages:
        source_name = getattr(msg, "source", "unknown")
        content_val = getattr(msg, "content", None)
        if content_val is None:
            content_val = str(msg)
        content_str = content_val if isinstance(content_val, str) else str(content_val)
        if len(content_str) > 150:
            content_str = content_str[:150] + " ...[截断]..."
        print(f"[{source_name}]: {content_str}")

# ============================================
# 练习 4.3: 带 MCP 工具的 Agent
# ============================================

async def exercise_3_mcp_agent():
    from autogen_agentchat.agents import AssistantAgent
    from autogen_ext.models.openai import OpenAIChatCompletionClient
    from autogen_core.models import ModelInfo
    from autogen_ext.tools.mcp import McpWorkbench, StdioServerParams
    import os

    print("🤖 [Step 1] 初始化模型客户端...")
    model_client = OpenAIChatCompletionClient(
        model="deepseek-chat",
        api_key=os.environ.get("OPENAI_API_KEY", "dummy"),
        base_url=os.environ.get("OPENAI_API_BASE", "https://api.deepseek.com"),
        model_info=ModelInfo(vision=False, function_calling=True, json_output=False, structured_output=False, family="unknown")
    )

    print("🔌 [Step 2] 启动 MCP (Model Context Protocol) Server...")
    server_params = StdioServerParams(
        command="npx",
        args=["-y", "@modelcontextprotocol/server-memory"]
    )

    try:
        async with McpWorkbench(server_params) as mcp:
            print("🧠 [Step 3] 创建挂载了 MCP 工具箱的 Agent...")
            # 在新版 autogen_ext 0.7 中，直接将 workbench=mcp 传给 AssistantAgent 即可
            agent = AssistantAgent(
                name="mcp_agent",
                model_client=model_client,
                workbench=mcp,
                system_message="你是一个高级智能体。当被要求记住信息时，请务必调用工具存入记忆网络中。"
            )
            
            print("🎯 [Step 4] 第一轮：要求使用工具记录秘密")
            result1 = await agent.run(task="请帮我记住这个加密信息：我的真实代号是'特工零零发'。请马上调用工具存入记忆！")
            
            for msg in result1.messages:
                content_val = getattr(msg, "content", None)
                if content_val is None:
                    content_val = str(msg)
                content_str = str(content_val)[:100] + "..." if len(str(content_val)) > 100 else str(content_val)
                source_name = getattr(msg, "source", "unknown")
                print(f"  [{source_name}]: {content_str}")
                
    except Exception as e:
        print(f"\n⚠️ MCP Server 运行失败!\n原因: 缺少 Node.js / npx 环境或下载超时。\n错误内容: {e}\n(此为正常测试保护)")

if __name__ == "__main__":
    print("=" * 50)
    print("练习 4: AutoGen 多 Agent 对话")
    print("=" * 50)
    
    print("\n--- 4.1 基础 Agent ---")
    asyncio.run(exercise_1_basic_agent())
    
    # print("\n--- 4.2 多 Agent 编排 ---")
    # asyncio.run(exercise_2_multi_agent())
    
    # 为了避免没有配置 nodejs 环境的同学卡死报错，这里先把它注释掉。需要测试运行的话可以自行取消注释。
    print("\n--- 4.3 MCP Agent ---")
    asyncio.run(exercise_3_mcp_agent())
