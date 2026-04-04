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
    
    角色:
    - 研究员 (Researcher): 负责搜集信息
    - 写作者 (Writer): 负责撰写报告
    
    步骤:
    1. 定义 Agent（角色、目标、背景故事）
    2. 定义 Task（描述、预期输出、分配给哪个 Agent）
    3. 创建 Crew（agents, tasks, process）
    4. 运行 crew.kickoff()
    
    提示:
        from crewai import Agent, Task, Crew, Process
        
        researcher = Agent(
            role="Senior Researcher",
            goal="研究关于 {topic} 的最新进展",
            backstory="你是一位资深研究员...",
            verbose=True
        )
        
        research_task = Task(
            description="调查 {topic} 的最新发展",
            expected_output="一份包含要点的研究报告",
            agent=researcher
        )
        
        crew = Crew(
            agents=[researcher, writer],
            tasks=[research_task, writing_task],
            process=Process.sequential
        )
        
        result = crew.kickoff(inputs={"topic": "AI Agents"})
    """
    # TODO: 创建你的第一个 Crew
    pass


# ============================================
# 练习 3.2: 层级流程
# ============================================

def exercise_2_hierarchical():
    """
    任务: 创建一个层级（Hierarchical）流程的 Crew
    
    在层级模式下，系统会自动创建一个 Manager Agent
    来协调其他 Agent 的工作
    
    提示:
        crew = Crew(
            agents=[...],
            tasks=[...],
            process=Process.hierarchical,
            manager_llm=ChatOpenAI(model="gpt-4")
        )
    """
    # TODO: 创建层级流程的 Crew
    pass


# ============================================
# 练习 3.3: 使用 Flows 编排工作流
# ============================================

def exercise_3_flows():
    """
    任务: 使用 CrewAI Flows 创建事件驱动的工作流
    
    流程:
    1. 获取用户需求 (start)
    2. 研究分析 (listen)
    3. 根据结果路由 (router)
    4. 生成报告 或 请求更多信息
    
    提示:
        from crewai.flow.flow import Flow, listen, start, router
        from pydantic import BaseModel
        
        class ResearchState(BaseModel):
            topic: str = ""
            findings: list = []
            confidence: float = 0.0
        
        class ResearchFlow(Flow[ResearchState]):
            @start()
            def gather_requirements(self):
                self.state.topic = "AI Agents"
                return self.state.topic
            
            @listen(gather_requirements)
            def research(self, topic):
                # 可以在这里调用 Crew
                pass
            
            @router(research)
            def evaluate(self):
                if self.state.confidence > 0.8:
                    return "generate_report"
                return "need_more_info"
    """
    # TODO: 创建 Flow 编排
    pass


if __name__ == "__main__":
    print("=" * 50)
    print("练习 3: CrewAI 多智能体协作")
    print("=" * 50)
    
    print("\n--- 3.1 第一个 Crew ---")
    exercise_1_first_crew()
    
    print("\n--- 3.2 层级流程 ---")
    exercise_2_hierarchical()
    
    print("\n--- 3.3 Flows 编排 ---")
    exercise_3_flows()
