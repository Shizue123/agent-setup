"""
练习 2: LangGraph 工作流编排
==============================
目标: 掌握 LangGraph 的核心概念 — StateGraph, Node, Edge

前置条件:
    pip install langgraph langchain-openai python-dotenv
"""

from typing import TypedDict
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
        # 这里可以初始化一些起始消息
        # 实际上在这个练习中，start_node 可以跳过，因为 START 连接直接到 process
        return {"messages": state["messages"] + ["开始处理"], "current_step": "start"}
    
    def process_node(state: SimpleState) -> dict:
        """处理节点：处理数据"""
        # 处理逻辑：模拟一个处理步骤
        return {"messages": state["messages"] + ["处理中..."], "current_step": "process"}
    
    def summarize_node(state: SimpleState) -> dict:
        """总结节点：生成总结"""
        # 汇总所有的消息处理结果
        count = len(state["messages"])
        return {"messages": state["messages"] + [f"总结完成，共处理 {count} 条消息"], "current_step": "summarize"}
    
    # 创建 State 图
    graph = StateGraph(SimpleState)
    
    # 添加三个节点
    graph.add_node("start", start_node)
    graph.add_node("process", process_node)
    graph.add_node("summarize", summarize_node)
    
    # 添加边来连接节点
    graph.add_edge(START, "start")       # START → start
    graph.add_edge("start", "process")   # start → process
    graph.add_edge("process", "summarize")  # process → summarize
    graph.add_edge("summarize", END)     # summarize → END
    
    # 编译成可执行的应用
    app = graph.compile()
    
    # 执行应用
    initial_state: SimpleState = {"messages": [], "current_step": ""}
    result = app.invoke(initial_state)
    
    # 打印结果
    print("=== 顺序图执行结果 ===")
    print(f"最终状态: {result['current_step']}")
    print(f"消息流程:")
    for i, msg in enumerate(result["messages"], 1):
        print(f"  {i}. {msg}")
    
    return result


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
    
    # 1. 节点：分类器
    def classify_node(state: RouterState) -> dict:
        query = state["query"]
        if "密码" in query or "登录" in query:
            return {"category": "tech"}
        elif "投诉" in query or "退款" in query:
            return {"category": "complaint"}
        else:
            return {"category": "general"}
            
    # 2. 节点：具体的处理分支
    def tech_support_node(state: RouterState) -> dict:
        return {"response": f"[技术组] 重启试试？(收到问题: {state['query']})"}
        
    def general_support_node(state: RouterState) -> dict:
        return {"response": f"[客服组] 您好，有什么可以帮您？(收到问题: {state['query']})"}
        
    def complaint_handler_node(state: RouterState) -> dict:
        return {"response": f"[特服组] 抱歉给您带来不好体验，立刻处理！(收到问题: {state['query']})"}

    # 3. 路由函数：根据状态返回要去的目标 key
    def route_function(state: RouterState) -> str:
        return state["category"]

    # 4. 构建图
    graph = StateGraph(RouterState)
    
    # 添加节点
    graph.add_node("classify", classify_node)
    graph.add_node("tech_support", tech_support_node)
    graph.add_node("general_support", general_support_node)
    graph.add_node("complaint_handler", complaint_handler_node)
    
    # 核心连接点
    graph.add_edge(START, "classify")
    
    # 核心魔法：条件路由边
    graph.add_conditional_edges(
        "classify",          # 来源节点
        route_function,      # 决定去哪儿的函数
        {                    # 映射表：返回值 -> 下一个节点
            "tech": "tech_support",
            "general": "general_support",
            "complaint": "complaint_handler"
        }
    )
    
    # 终点连接
    graph.add_edge("tech_support", END)
    graph.add_edge("general_support", END)
    graph.add_edge("complaint_handler", END)
    
    app = graph.compile()
    
    # 5. 测试不同路由
    print("=== 路由图执行结果 ===")
    test_queries = [
        "我的密码忘记了，登不进去",
        "我要投诉，退款！",
        "你们周末上班吗？"
    ]
    
    for q in test_queries:
        initial_state: RouterState = {"query": q, "category": "", "response": ""}
        result = app.invoke(initial_state)
        print(f"用户问题: {q}")
        print(f"路由路径: classify -> {result['category']}")
        print(f"最终回复: {result['response']}\n")


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
    
    # 1. Agent 节点：负责思考和决定（模拟大模型）
    def agent_node(state: AgentState) -> dict:
        iteration = state.get("iteration", 0) + 1
        messages = state.get("messages", [])
        
        print(f"  [Agent] 思考中... (第 {iteration} 轮)")
        
        # 模拟大模型思考逻辑：如果没有拿到足够信息（没达到最大轮数），就去调工具
        if iteration < state["max_iterations"]:
            return {
                "iteration": iteration,
                "tool_calls": ["search_weather"],  # 决定调用天气工具
                "messages": messages + [f"Agent 决定调用工具: search_weather"],
                "final_answer": ""
            }
        else:
            # 信息够了，生成最终答案
            return {
                "iteration": iteration,
                "tool_calls": [],
                "messages": messages + ["Agent 得出最终结论"],
                "final_answer": "今天天气晴朗，温度25度，适合出行！"
            }

    # 2. Tool 节点：负责执行工具（模拟外部动作）
    def tool_node(state: AgentState) -> dict:
        tool_name = state["tool_calls"][0] if state.get("tool_calls") else "unknown"
        print(f"  [Tool] 执行工具... ({tool_name})")
        
        # 模拟工具的返回结果
        tool_result = "25度，晴朗"
        
        return {
            "messages": state["messages"] + [f"工具返回结果: {tool_result}"],
            "tool_calls": [] # 用完工具就清空
        }

    # 3. 路由函数：在这个岔路口决定是继续循环，还是结束
    def should_continue(state: AgentState) -> str:
        # 如果 Agent 已经在公文包里写了 final_answer，图就结束
        if state.get("final_answer"):
            return "end"
        # 否则，去调工具
        return "continue"

    # 4. 构建图
    graph = StateGraph(AgentState)
    
    graph.add_node("agent", agent_node)
    graph.add_node("tool", tool_node)
    
    # 构建执行流
    graph.add_edge(START, "agent")
    
    # 核心 1：离开 Agent 后，看路牌决定去向
    graph.add_conditional_edges(
        "agent",           # 从 agent 出来
        should_continue,   # 问路牌
        {
            "continue": "tool",  # 如果还没结论，去 tool 节点
            "end": END           # 如果有了结论，去 END 节点
        }
    )
    
    # 核心 2：工具用完后，必须把结果还给 Agent 再次评估（闭环形成！）
    graph.add_edge("tool", "agent")
    
    app = graph.compile()
    
    # 5. 执行图
    print("=== 循环图执行结果 ===")
    initial_state: AgentState = {
        "messages": ["北京天气怎么样？"], 
        "tool_calls": [], 
        "iteration": 0, 
        "max_iterations": 3,
        "final_answer": ""
    }
    
    result = app.invoke(initial_state)
    
    print("\n[最终输出]:", result["final_answer"])
    print("[包含的完整轨迹]:")
    for msg in result["messages"]:
        print(" -", msg)


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
    from langchain_openai import ChatOpenAI
    from langchain_core.tools import tool
    from langgraph.prebuilt import create_react_agent
    import os
    
    import requests

    # 1. 准备工具（把你的 Python 函数变成 Agent 的手脚）
    import re
    
    @tool
    def search_weather(city_query: str) -> str:
        """根据地点/城市名称查询最新的真实气象和天气状况。如果查询国内城市，请直接传入中文（如：北京）；如果是国外城市，请传入英文拼写。"""
        import re
        has_chinese = bool(re.search(r'[\u4e00-\u9fa5]', city_query))
        
        try:
            # ==========================================
            # 【通道 A：中国腾讯天气通道】
            # ==========================================
            if has_chinese:
                print(f"\n  [Tools] 🧭 检测到中文【{city_query}】，优先走【腾讯天气大通道】...")
                tencent_key = "TJFBZ-N2WKT-O6TXV-LVJSA-2ZFFV-6CFB5"
                
                # 第一步：腾讯地图地理编码，获取精确经纬度
                geo_url = f"https://apis.map.qq.com/ws/geocoder/v1/?address={city_query}&key={tencent_key}"
                geo_res = requests.get(geo_url, timeout=5).json()
                
                if geo_res.get("status") == 0:
                    loc = geo_res["result"]["location"]
                    lat, lng = loc["lat"], loc["lng"]
                    city_disp = geo_res["result"]["title"]
                    
                    # 第二步：腾讯位置服务 - 智能气象 API
                    weather_url = f"https://apis.map.qq.com/ws/weather/v1/?location={lat},{lng}&key={tencent_key}"
                    w_res = requests.get(weather_url, timeout=5).json()
                    
                    if w_res.get("status") == 0:
                        realtime = w_res["result"]["realtime"][0]
                        info = realtime.get("infos", {})
                        return (
                            f"【通道 A：腾讯智能气象】\n"
                            f"请求位置：{city_disp}\n"
                            f"天气：{info.get('weather')}\n"
                            f"温度：{info.get('temperature')}°C\n"
                            f"湿度：{info.get('humidity')}%\n"
                            f"风况：{info.get('wind_direction')} {info.get('wind_power')}"
                        )
                    else:
                        print(f"  [Router] ⚠️ 腾讯天气获取失败，转向国际兜底通道 (Fallback)...")
                else:
                    print(f"  [Router] ⚠️ 腾讯地理位置解析无结果，转向国际兜底通道 (Fallback)...")

            # ==========================================
            # 【通道 B：国际通用通道 (OpenWeatherMap) 】
            # ==========================================
            print(f"\n  [Tools] 🌐 切换至【OpenWeatherMap 全球通用通道】...")
            # 修正了你提供的可用 Key
            openweathermap_key = "39bcae3d76102e09964fba4e4981bcd0"
            weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city_query}&appid={openweathermap_key}&units=metric&lang=zh_cn"
            
            weather_resp = requests.get(weather_url, timeout=5)
            
            if weather_resp.status_code == 200:
                data = weather_resp.json()
                city_name = data.get("name")
                temp = data["main"]["temp"]
                feels_like = data["main"]["feels_like"]
                desc = data["weather"][0]["description"]
                wind = data["wind"]["speed"]
                
                return (
                    f"【通道 B：OpenWeatherMap 天气数据】\n"
                    f"城市：{city_name}\n"
                    f"天气：{desc}\n"
                    f"温度：{temp}°C (体感: {feels_like}°C)\n"
                    f"风速：{wind} m/s"
                )
            else:
                error_msg = weather_resp.text
                print(f"  [Error] ❌ OpenWeatherMap API 请求失败: {error_msg}")
                return f"系统提示：获取 {city_query} 天气时发生错误。如果这是国外城市，请务必将其翻译为纯英文（例如 New York, Paris）后重新调用本工具再次查询！原错误：{error_msg}"
                
        except Exception as e:
            return f"系统提示：执行查天气双通道路由时发生内部错误：{str(e)}"
        
    @tool
    def calculate_travel_time(distance_km: float, speed_kmh: float) -> str:
        """计算旅行需要花费的时间。"""
        print(f"\n  [Tools] 计算中：{distance_km}/{speed_kmh}...")
        hours = distance_km / speed_kmh
        return f"大约需要 {hours:.1f} 小时"

    tools = [search_weather, calculate_travel_time]

    # 2. 从环境变量读取 KEY 进行测试
    if not os.environ.get("OPENAI_API_KEY"):
        print("⚠️ 无法真正运行：你还没有在 exercises/.env 配置 OPENAI_API_KEY！")
        print("💡 架构启示：这是正常现象！在真实世界中，只要配好大模型的 Key，下面就会跑通。")
        return

    try:
        # 3. 创建模型与 Agent 编排
        # 💡 [10% 局部微调]：把 OpenAI 换成 DeepSeek，只需要改这里的 model 和 base_url
        model = ChatOpenAI(
            model="deepseek-chat", 
            temperature=0,
            base_url=os.environ.get("OPENAI_API_BASE", "https://api.deepseek.com/v1") # 兼容部分没有写 /v1 的情况
        )
        
        # 魔法所在：用一句话就干了我们在 2.3 里写的所有事情！
        agent_executor = create_react_agent(model, tools)
        
        # 4. 执行并观察全路径流转
        print("=== 真实 LLM Agent 执行轨迹 ===")
        test_queries = [
            "拉萨现在还有多冷啊？",
            "我要去洛杉矶看比赛，那边会下雨吗？",
            "那纽约现在的天气呢？"
        ]
        
        for idx, user_query in enumerate(test_queries, 1):
            print(f"\n[{idx}] 🙋‍♂️ 用户提问: {user_query}")
            
            result = agent_executor.invoke({"messages": [("user", user_query)]})
            
            print("\n[🎯 Agent 的所有思考与动作（轨迹）]:")
            for msg in result["messages"][1:]:
                msg.pretty_print()
            print("="*40)
            
    except Exception as e:
        print(f"执行出错（可能是网络或 API 余额问题）: {e}")

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
