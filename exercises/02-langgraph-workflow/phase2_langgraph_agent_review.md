# LangGraph 与 Agent 工作流实战总结 (Phase 2)

## 核心学习理念回顾
根据之前的沟通，我们坚持 **“70% 架构思想 + 20% 代码映射 + 10% 体验微调”** 的学习范式。Agent 的核心不在于复杂的 if-else 代码，而在于**系统拓扑流转**和**大语言模型（LLM）的自主推理能力**。

---

## 1. 架构演进路线 (70% 架构思想)

### 阶段一：LangGraph 基础图结构 (2.1 - 2.3)
LangGraph 的本质是**状态机 (State Machine)**。我们从零构建了三种基础拓扑：
1. **顺序图 (Sequential Graph)**：线性执行流程 (`START -> start -> process -> summarize -> END`)。
2. **条件路由图 (Conditional Routing)**：通过 `add_conditional_edges` 赋予图“大脑”，根据用户意图（分类器提取的业务类型）动态走向不同分支（技术组/售后组/客服组）。
3. **循环图（ReAct 范式雏形）**：引入了带有 `messages`、`tool_calls` 和 `iteration` 的状态追踪，演示了 `思考 -> 动作 -> 观察 -> 再思考` 的闭环链路。

### 阶段二：引入真实 LLM 与智能体 (2.4)
使用 `langgraph.prebuilt.create_react_agent` 一行代码，代理了我们手动编写的 ReAct 循环。
- **配置节点**：将 DeepSeek 接入作为核心大模型（大脑）。
- **装备手脚**：使用 `@tool` 装饰器将 Python 函数（如查天气、计算时间）挂载到图网络中。

### 阶段三：打造真实的“高可用基建” (双通道路由工具)
在真实世界中，由于地理库差异、服务商拦截、语种支持问题，单一 API 极其脆弱。我们为 `search_weather` 工具设计了 **智能网关 (API Gateway / Router)**：
1. **输入嗅探**：通过正则检测是否包含中文字符。
2. **高速公路 (通道 A)**：匹配含中文输入 -> 调用 **腾讯位置服务 (Geocoding)** 获取精确经纬度 -> 调用 **腾讯智能气象 API** 获取国内实时数据。
3. **国际兜底 (通道 B)**：纯英文/非国内定位 -> 降级走 **OpenWeatherMap 通用 API**。
4. **Agent 自洽闭环 (The Magic)**：不再使用硬编码去处理所有国家城市的英汉对应字典，而是巧妙通过工具 `docstring` 提示词 配合 `报错日志回收` 的机制。当通道报错（如 OWM 不识别“纽约”报 404）时，将错误抛回给大模型，大模型自主判定需要将“纽约”**翻译**为 “New York” 发起第二轮工具调用。

---

## 2. 核心代码映射 (20% 代码映射)

### 核心路由与大模型代理构建
```python
from langgraph.prebuilt import create_react_agent
# tools 列表承载了所有 @tool 函数
agent_executor = create_react_agent(model, tools) 

# 调用入口，直接维护图的 messages 状态
result = agent_executor.invoke({"messages": [("user", query)]})
```

### 工具内的架构映射 (search_weather)
```python
@tool
def search_weather(city_query: str) -> str:
    """根据地点查询天气。国内城市传中文，国外城市务必传英文拼写。"""
    has_chinese = bool(re.search(r'[\u4e00-\u9fa5]', city_query))
    
    try:
        # 【通道 A：腾讯智能气象】
        if has_chinese:
            # 1. 调腾讯 Maps API (Geocode)
            # 2. 调腾讯 Weather API
            # return "腾讯天气数据..."
            
        # 【通道 B：OpenWeatherMap】
        # 1. 调 OWM Weather API
        # if success: return "OWM 天气数据..."
        # else: 
        #   将错误原样吐出，并引导 LLM 进行自我修正（如文本翻译后重试）
        #   return "获取发生错误。如果这是国外城市，请翻译为纯英文后重试！"
```

---

## 3. 踩坑与体验微调 (10% Tweaks)

1. **环境隔离重要性**：在 `try-except` 或 `if-else` 分支中，不要让工具崩溃（如 API 404 / 401 / 403 错误），而是将 `Exception` 转为自然语言字符串 `return` 回去，因为大模型是读字的，可以直接消化日志并自我纠错。
2. **和风天气 (QWeather) 403 案**：我们曾尝试接入和风天气，但获取到 `Invalid Host`。查明是因为注册的 API Key 为 Web 专属（绑定了域名白名单），在本地 Python 脚本中调取会被防盗链拦截。最终将国内通道平滑切换为腾讯地图/天气 API，瞬间通畅。
3. **Open-Meteo 与 OWM 的取舍**：最初使用免费免密 Open-Meteo，但对国外特殊地名的解析不精准。切换为你提供的 OWM Key (`39bcae...`) 后，虽然其对纯中文支持欠佳，但凭借 Agent 强大的“重试翻译心智”，完美实现了互补。

## 下一步建议
通过这几个演练，你已掌握**单体系 Agent + 多路健壮工具**的闭环。
后续可随时进入以下进阶主题：
- **LangGraph Checkpoint**: 让现在的代理拥有多轮持久化记忆。
- **CrewAI / AutoGen 框架**: 将一个全能代理，拆分为多个专职代理（如：收集端 Agent -> 评审端 Agent -> 总结端 Agent），学习去中心化的团队协作架构。