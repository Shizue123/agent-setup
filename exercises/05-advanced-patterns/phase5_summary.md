# 阶段 05: 高级 Agent 编排模式 - 研究管道总结

## 一、 核心概念与本质
在工业级落地的复杂 Agent 架构中，纯自治带来的高幻觉率和缓慢效率往往无法接受。为此，我们在 05 阶段结合 LangGraph 完整实现了**确定性编排与 Agent 动态流转的结合**。

整个研究员管线 (Research Pipeline) 具备了三个商业级核心机制：
1. **Fan-out/Fan-in (扇出与扇入 - 并行处理)**：
   - 商业诉求：同时查询多个搜索引擎、本地库、API 以节省等待时间。
   - LangGraph 实现：一个上游节点只需把边连向多个独立的下游节点，框架就会自动**并发（异步）**执行这些下游节点（此时是扇出/Fan-out）。
   - 让多个并行节点汇总连接到下一个统计节点，就构成了“扇入/Fan-in”。
2. **状态竞争解决方案 (State Reducer)**：
   - 当多个并行执行的节点同时向同一个状态字典写入时（例如都想把结果塞进 `sources`），普通的覆写会导致数据丢失。
   - 解决方式：使用 `Annotated[dict[str, str], merge_dicts]`。这告诉框架，“如果你同时收到多个 `sources` 更新，请调用 `merge_dicts` 将它们合并，而不是相互覆盖”。
3. **自我反思循环 (Reflection Loop)**：
   - 包含了一个条件边（`should_refine`）。当质量评估节点 (`evaluate_quality`) 给出的分数低于 0.8 时，系统将自动退回规划 (`plan`) 或搜索阶段。
   - 避免了直接将一次生成的低劣结果抛给用户，实现了内生迭代。

---

## 二、 组件职责与代码映射

### 1. 并发状态收集 (State Definition)
必须声明 Reducer (合并函数) 防止数据被覆盖。
```python
def merge_dicts(a: dict, b: dict) -> dict:
    c = a.copy()
    c.update(b)
    return c

class ResearchState(TypedDict):
    topic: str
    iteration: int
    quality_score: float
    # Reducer 声明，表示增量合并而非覆盖
    sources: Annotated[dict[str, str], merge_dicts] 
```

### 2. 扇出与扇入连线 (Fan-out / Fan-in)
在图构建阶段的直连就是并行的声明：
```python
workflow = StateGraph(ResearchState)

# (上略: 添加所有节点)

# [扇出 - Fan-out]: 规划结束之后，同时分发给三条线，系统会自动并行跑这三个节点
workflow.add_edge("plan", "search_a")
workflow.add_edge("plan", "search_b")
workflow.add_edge("plan", "search_c")

# [扇入 - Fan-in]: 等待这三条线都执行完，框架再进入 analyze 节点
workflow.add_edge(["search_a", "search_b", "search_c"], "analyze")
```

### 3. 条件路由与自我纠错循环 (Reflection Loop)
利用一个判断函数来返回下一个应该指向的节点名：
```python
def should_refine(state: ResearchState) -> str:
    # 评判当前的循环次数和质量
    if state["quality_score"] < 0.8 and state["iteration"] < 3:
        return "refine"
    return "generate"

# 当 evaluate 节点执行完毕后，调用 should_refine 查验。
# 并根据它的返回值，重新映射到具体节点
workflow.add_conditional_edges(
    "evaluate",
    should_refine,
    {
        "refine": "plan",      # [循环] 返回重新规划
        "generate": "report"   # [结束] 进入报告生成
    }
)
```

## 三、 执行流输出
通过终端输出我们可以极为清晰地看到上述过程的体现：
1. 第一轮遍历触发了 `[plan] -> 并行三个 [search] -> [analyze]`。
2. 进入 `[evaluate]` 后，得分仅为 `0.70 < 0.80`，系统被自动打回触发了一轮循环。
3. 循环重新跑了一轮上述步骤，第二次评估得分为 `0.90`。
4. 满意结案，放行到 `[report]` 生成最终 Markdown 报告。