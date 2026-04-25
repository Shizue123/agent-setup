from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# ============================================
# 实战：反思与自我修正工作流 (Reflection Loop)
# 个人开发者最常用的高阶玩法：让 AI 自己检查自己写的代码或文章
# ============================================

class DraftState(TypedDict):
    """状态容器：存放草稿和审稿意见"""
    topic: str
    draft: str
    feedback: str
    revision_count: int

def generator_node(state: DraftState) -> dict:
    """生成器：负责写初稿或根据意见修改"""
    count = state.get("revision_count", 0)
    topic = state["topic"]
    feedback = state.get("feedback", "")
    
    print(f"\n[生成器] 第 {count} 次生成...")
    if count == 0:
        # 第一次写初稿
        new_draft = f"关于【{topic}】的文章初稿：这是一篇很基础的介绍。"
    else:
        # 根据反馈修改
        new_draft = f"关于【{topic}】的修改稿：(结合了建议'{feedback}') 增加了深度和细节。"
        
    return {
        "draft": new_draft,
        "revision_count": count + 1
    }

def reviewer_node(state: DraftState) -> dict:
    """审查器：负责挑刺。如果觉得不行就给出反馈"""
    draft = state["draft"]
    count = state["revision_count"]
    
    print(f"[审查器] 正在审查第 {count} 版...")
    
    # 模拟审查逻辑：必须修改至少 1 次才算通过
    if count < 2:
        print("  -> 审查不通过，打回重写！")
        return {"feedback": "太浅了，需要增加高级特性的介绍。"}
    else:
        print("  -> 审查通过，可以发布！")
        return {"feedback": "PASS"} # 标志词

def should_publish(state: DraftState) -> str:
    """路由函数：看审查器的意见，决定是发布还是重写"""
    if state["feedback"] == "PASS":
        return "end"
    else:
        return "rewrite"

def build_practical_workflow():
    # 1. 搭建骨架
    graph = StateGraph(DraftState)
    
    # 2. 注册节点
    graph.add_node("generator", generator_node)
    graph.add_node("reviewer", reviewer_node)
    
    # 3. 连接工作流
    graph.add_edge(START, "generator")
    graph.add_edge("generator", "reviewer")
    
    # 4. 核心：条件路由（不过关就打回）
    graph.add_conditional_edges(
        "reviewer",
        should_publish,
        {
            "rewrite": "generator",
            "end": END
        }
    )
    
    return graph.compile()

if __name__ == "__main__":
    print("=" * 50)
    print("🚀 第二模块实战：自我修正工作流 (Reflection Loop)")
    print("=" * 50)
    
    app = build_practical_workflow()
    initial_state: DraftState = {"topic": "LangGraph 核心架构", "draft": "", "feedback": "", "revision_count": 0}
    
    print("开始执行...\n")
    final_state = app.invoke(initial_state)
    
    print("\n🏁 [最终交付结果]:")
    print(final_state["draft"])
