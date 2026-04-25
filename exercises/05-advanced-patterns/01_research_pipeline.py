"""
练习 5: 高级 Agent 编排模式 — 研究管道
==========================================
目标: 综合运用所学知识，构建一个完整的研究管道

前置条件:
    pip install langgraph langchain-openai python-dotenv

这个练习将 LangGraph 的多种模式结合在一起：
- 顺序执行
- 条件路由
- 并行执行
- 循环（迭代优化）
- 子图
- Human-in-the-loop
"""

import os
from typing import TypedDict, Annotated, Literal
import operator

def merge_dicts(a: dict, b: dict) -> dict:
    """安全的字典合并函数，用于处理多个源的并发写入"""
    c = a.copy()
    c.update(b)
    return c

class ResearchState(TypedDict):
    """研究管道的状态定义"""
    topic: str                    # 研究主题
    research_plan: list[str]      # 研究方向列表
    # ⭐️ 核心点：当多个并行节点同时往一个状态字段写入时，必须用 Annotated + reducer 来聚合。
    sources: Annotated[dict[str, str], merge_dicts]  # 各来源的搜索结果
    analysis: str                 # 汇总分析
    quality_score: float          # 质量评分 (0-1)
    iteration: int                # 当前迭代次数
    max_iterations: int           # 最大迭代次数
    report: str                   # 最终报告
    human_feedback: str           # 人类反馈
    status: str                   # 当前状态


def build_research_pipeline():
    """
    任务: 构建完整的研究管道
    
    步骤:
    1. 定义所有节点函数
    2. 创建主图和子图
    3. 添加条件路由和循环
    4. 编译并运行
    
    挑战:
    - 实现并行搜索（使用 fan-out/fan-in 模式）
    - 实现质量评估的循环优化
    - 添加 human-in-the-loop 检查点
    """
    from langgraph.graph import StateGraph, START, END
    
    # === 节点定义 ===
    
    def plan_research(state: ResearchState) -> dict:
        """规划研究方向"""
        # TODO: 使用 LLM 或规则生成研究方向
        # 例如: 将主题分解为 3 个子方向
        return {
            "research_plan": [
                f"{state['topic']} - 技术原理",
                f"{state['topic']} - 应用场景", 
                f"{state['topic']} - 未来趋势",
            ],
            "status": "planning_done"
        }
    
    def search_source_a(state: ResearchState) -> dict:
        """搜索来源 A（模拟）"""
        return {"sources": {"source_a": "来源A的结果..."}}
    
    def search_source_b(state: ResearchState) -> dict:
        """搜索来源 B（模拟）"""
        return {"sources": {"source_b": "来源B的结果..."}}
    
    def search_source_c(state: ResearchState) -> dict:
        """搜索来源 C（模拟）"""
        return {"sources": {"source_c": "来源C的结果..."}}
    
    def analyze(state: ResearchState) -> dict:
        """汇总分析所有搜索结果"""
        # TODO: 使用 LLM 分析汇总
        all_sources = state.get("sources", {})
        analysis = f"基于 {len(all_sources)} 个来源的分析..."
        return {"analysis": analysis, "status": "analyzed"}
    
    def evaluate_quality(state: ResearchState) -> dict:
        """评估研究质量"""
        # TODO: 使用 LLM 评估质量或使用规则
        iteration = state.get("iteration", 0) + 1
        # 模拟: 每次迭代质量提升
        score = min(0.5 + iteration * 0.2, 1.0)
        return {"quality_score": score, "iteration": iteration}
    
    def should_refine(state: ResearchState) -> Literal["refine", "generate"]:
        """决定是否需要继续优化"""
        if (state["quality_score"] < 0.8 and 
            state["iteration"] < state.get("max_iterations", 3)):
            return "refine"
        return "generate"
    
    def generate_report(state: ResearchState) -> dict:
        """生成最终报告"""
        # TODO: 使用 LLM 生成结构化报告
        report = f"""
# 研究报告: {state['topic']}

## 分析结果
{state.get('analysis', '无')}

## 质量评分: {state.get('quality_score', 0):.2f}
## 迭代次数: {state.get('iteration', 0)}
"""
        return {"report": report, "status": "report_generated"}
    
    # === 构建图 ===
    workflow = StateGraph(ResearchState)
    
    # 1. 添加所有节点
    workflow.add_node("plan", plan_research)
    workflow.add_node("search_a", search_source_a)
    workflow.add_node("search_b", search_source_b)
    workflow.add_node("search_c", search_source_c)
    workflow.add_node("analyze", analyze)
    workflow.add_node("evaluate", evaluate_quality)
    workflow.add_node("report", generate_report)
    
    # 2. 添加边 (控制数据流向)
    workflow.add_edge(START, "plan")
    
    # [并行处理 - 扇出 / Fan-out] 一个节点连接多个下游节点，LangGraph 会自动并行执行它们
    workflow.add_edge("plan", "search_a")
    workflow.add_edge("plan", "search_b")
    workflow.add_edge("plan", "search_c")
    
    # [等待汇聚 - 扇入 / Fan-in] 多个节点指向同一个目标，需等到它们全执行完才触发下游
    workflow.add_edge(["search_a", "search_b", "search_c"], "analyze")
    
    # 顺序执行分析和评估
    workflow.add_edge("analyze", "evaluate")
    
    # [条件路由与循环优化] 根据质量评分决定是重新规划还是生成报告
    workflow.add_conditional_edges(
        "evaluate",
        should_refine,
        {
            "refine": "plan",      # 返回上游，形成循环
            "generate": "report"   # 进入最终阶段
        }
    )
    
    workflow.add_edge("report", END)
    
    # 4. 编译
    app = workflow.compile()
    
    # 5. 运行测试
    print("🚀 开始运行研究管道...")
    initial_state = {
        "topic": "AI Agent 架构演进与商业落地",
        "iteration": 0,
        "max_iterations": 3,
        "sources": {}
    }
    
    for step in app.stream(initial_state, stream_mode="updates"):
        for node_name, state_update in step.items():
            print(f"✅ 完成节点: [{node_name}]")
            if "quality_score" in state_update:
                print(f"   -> 评估分数: {state_update['quality_score']:.2f}")
            if "report" in state_update:
                print(f"\n🎯 最终产出:\n{state_update['report']}")


if __name__ == "__main__":
    print("=" * 50)
    print("练习 5: 高级 Agent 编排 — 研究管道")
    print("=" * 50)
    
    build_research_pipeline()
