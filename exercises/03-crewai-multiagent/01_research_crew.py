"""
练习 3: CrewAI 多智能体协作
==============================
目标: 使用 CrewAI 构建一个多 Agent 协作团队

前置条件:
    pip install crewai crewai-tools python-dotenv
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ============================================
# 练习 3.1: 创建你的第一个 Crew
# ============================================

def exercise_1_first_crew():
    """
    任务: 创建一个研究+写作的 Crew
    """
    from crewai import Agent, Task, Crew, Process, LLM
    import os
    
    # 配置使用 DeepSeek 大模型
    llm = LLM(
        model="deepseek/deepseek-chat",
        temperature=0.3,
        base_url=os.environ.get("OPENAI_API_BASE", "https://api.deepseek.com"),
        api_key=os.environ.get("OPENAI_API_KEY")
    )
    
    # 1. 雇佣员工（定义 Agent）
    researcher = Agent(
        role="资深行业分析师",
        goal="挖掘并总结关于 {topic} 的最新突破和核心发展趋势",
        backstory="你是一位在科技领域工作了15年的金牌分析师，你总是能从复杂的信息中提炼出最核心的洞察。",
        verbose=True,
        llm=llm
    )
    
    writer = Agent(
        role="金牌内容主编",
        goal="将复杂的研究报告转化为通俗易懂、引人入胜的科普推文",
        backstory="你曾是《连线》杂志的首席主笔，擅长用最生动的语言向大众解释前沿科技。",
        verbose=True,
        llm=llm
    )
    
    # 2. 下达任务（定义 Task）
    research_task = Task(
        description="系统性地调查 {topic} 领域的 3 个最新发展趋势，并指出其对未来行业的影响。",
        expected_output="一份包含3个核心趋势及其影响的结构化研究报告，要求用词严谨专业。",
        agent=researcher
    )
    
    writing_task = Task(
        description="基于研究员提供的分析报告，写一篇面向大众的科普博客。要求：1. 有吸引人的标题；2. 语言幽默生动；3. 包含适当的 emoji。",
        expected_output="一篇 500 字左右的微信公众号/小红书风格科普推文。",
        agent=writer
    )
    
    # 3. 组建公司开始运转（定义 Crew）
    crew = Crew(
        agents=[researcher, writer],
        tasks=[research_task, writing_task],
        process=Process.sequential  # 像流水线一样，研究员做完给写作者
    )
    
    print("🎬 导演喊 Action！Crew 开始工作...")
    result = crew.kickoff(inputs={"topic": "AI Agent (人工智能代理)"})
    print("\n==================================")
    print("🏆 最终产出结果：\n")
    print(result)


# ============================================
# 练习 3.2: 层级流程
# ============================================

def exercise_2_hierarchical():
    """
    任务: 创建一个层级（Hierarchical）流程的 Crew
    """
    from crewai import Agent, Task, Crew, Process, LLM
    import os

    # 配置使用 DeepSeek 大模型
    llm = LLM(
        model="deepseek/deepseek-chat",
        temperature=0.3,
        base_url=os.environ.get("OPENAI_API_BASE", "https://api.deepseek.com"), 
        api_key=os.environ.get("OPENAI_API_KEY")
    )

    # 1. 雇佣基层员工
    researcher = Agent(
        role="市场调研员",
        goal="收集关于 {topic} 的市场数据和竞品信息",
        backstory="你擅长在互联网上快速搜集准确的市场信息并进行数据汇总。",
        verbose=True,
        llm=llm
    )

    writer = Agent(
        role="商业报告撰写人",
        goal="根据市场调研数据，撰写一份专业的商业分析报告",
        backstory="你曾在顶级咨询公司工作，精通商业洞察和报告撰写格式。",
        verbose=True,
        llm=llm
    )

    # 2. 定义宏观任务（不指定给具体某个人）
    complex_task = Task(
        description="针对 {topic} 完成一份全面的商业调研报告。这需要先进行市场数据收集，然后再由专人整合成一份专业的报告文档。",
        expected_output="一份包含市场现状、竞品分析和商业建议的结构化洞察报告。"
        # 注意：在层级模式中，我们不需要手动在这里写 agent=researcher，
        # 项目经理（Manager）会自动根据员工的人设进行任务拆解和分发！
    )

    # 3. 组建公司开启层级模式
    crew = Crew(
        agents=[researcher, writer],
        tasks=[complex_task],
        process=Process.hierarchical,  # 开启层级（项目经理）模式
        manager_llm=llm                # 赋予项目经理一个用来思考的大脑 (LLM)
    )

    print("👔 项目经理已就位，开始审视任务并向下属派发工作...")
    result = crew.kickoff(inputs={"topic": "2026年全屋智能家居市场"})
    print("\n==================================")
    print("🏆 最终产出结果：\n")
    print(result)
# ============================================
# 练习 3.3: 使用 Flows 编排工作流
# ============================================

def exercise_3_flows():
    """
    任务: 使用 CrewAI Flows 创建事件驱动的工作流
    """
    from crewai.flow.flow import Flow, listen, start, router
    from pydantic import BaseModel
    import random

    # 1. 定义状态 (类似 LangGraph 的 State)
    class ResearchState(BaseModel):
        topic: str = ""
        findings: list = []
        confidence: float = 0.0

    # 2. 定义工作流 (流程编排)
    class ResearchFlow(Flow[ResearchState]):
        
        @start()
        def gather_requirements(self):
            print("🚀 [Step 1] 收到需求...")
            self.state.topic = "AI Agents"
            # 模拟初始置信度
            self.state.confidence = random.uniform(0.6, 0.99)
            return self.state.topic

        @listen(gather_requirements)
        def research(self, topic):
            print(f"🔍 [Step 2] 开始针对 '{topic}' 进行初步研究...")
            # 这里原本可以像 3.1 一样调用一个完整的 Crew 去做深度研究
            # 为了演示流程编排，我们直接模拟返回数据
            self.state.findings = [f"发现 1: {topic} 正在重塑软件架构", f"发现 2: 推理成本正在急剧下降"]
            print(f"   当前研究置信度: {self.state.confidence:.2f}")
            return self.state.findings

        @router(research)
        def evaluate(self):
            print("⚖️ [Step 3] 评估研究结果是否足够...")
            if self.state.confidence > 0.8:
                return "generate_report"
            return "need_more_info"
            
        @listen("generate_report")
        def success_ending(self):
            print("✅ [Step 4 分支A] 置信度达标，正在生成最终报告！")
            print(f"   最终报告包含内容：{self.state.findings}")
            return "流程结束: 报告已生成"
            
        @listen("need_more_info")
        def fallback_ending(self):
            print("⚠️ [Step 4 分支B] 置信度过低，需要人工介入或再次搜索。")
            return "流程结束: 任务被中止"

    # 3. 运行工作流
    print("🎬 启动 Flow 工作流...")
    flow = ResearchFlow()
    result = flow.kickoff()
    print("\n==================================")
    print("🏆 最终汇总结果:\n", result)


if __name__ == "__main__":
    print("=" * 50)
    print("练习 3: CrewAI 多智能体协作")
    print("=" * 50)

    # print("\n--- 3.1 第一个 Crew ---")
    # exercise_1_first_crew()

    # print("\n--- 3.2 层级流程 ---")
    # exercise_2_hierarchical()

    print("\n--- 3.3 Flows 编排 ---")
    exercise_3_flows()
