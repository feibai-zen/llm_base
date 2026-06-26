from typing import TypedDict
import time
from langgraph.graph import StateGraph
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.types import Command


# --------------------------
# 1. 定义工作流状态
# --------------------------
class BatchState(TypedDict):
    current_step: int  # 记录当前循环下标，断点核心标记
    processed_list: list[int]  # 已处理数据集合


# --------------------------
# 2. 模拟单步业务处理（每步2分钟，这里缩短为2秒方便测试）
# --------------------------
def process_step(state: BatchState):
    idx = state["current_step"]
    print(f"【正在处理】第 {idx} 步")
    # 模拟耗时计算/API调用
    time.sleep(2)
    # 写入已完成记录
    state["processed_list"].append(idx)
    # 下标自增，准备下一轮
    state["current_step"] += 1
    return state


# --------------------------
# 3. 构建循环长任务工作流
# --------------------------
def build_long_task_graph():
    builder = StateGraph(BatchState)
    # 注册批量处理节点
    builder.add_node("batch_process", process_step)
    # 起始入口
    builder.add_edge("__start__", "batch_process")

    # 循环路由：未跑完100步则重复执行，完成则结束
    def loop_router(state: BatchState):
        if state["current_step"] < 100:
            return "batch_process"
        return "__end__"

    builder.add_conditional_edges("batch_process", loop_router)

    # 关键：SQLite 持久化存储（文件可共享，实现跨进程/机器恢复）
    # 本地文件：同机器多进程共享；挂载NAS/共享盘可实现跨机器
    # 使用 with 语句管理 SqliteSaver 生命周期
    checkpointer = SqliteSaver.from_conn_string("./durable_checkpoint.db")
    graph = builder.compile(checkpointer=checkpointer)
    return graph, checkpointer


# --------------------------
# 4. 执行入口：支持中断后重复调用续跑
# --------------------------
if __name__ == "__main__":
    # 全局唯一会话ID，同一个thread_id绑定同一份任务进度
    task_config = {
        "configurable": {
            "thread_id": "3hour_batch_task_001"
        }
    }

    # 使用 with 语句确保 checkpointer 正确管理
    with SqliteSaver.from_conn_string("./durable_checkpoint.db") as checkpointer:
        builder = StateGraph(BatchState)
        builder.add_node("batch_process", process_step)
        builder.add_edge("__start__", "batch_process")


        def loop_router(state: BatchState):
            if state["current_step"] < 100:
                return "batch_process"
            return "__end__"


        builder.add_conditional_edges("batch_process", loop_router)

        graph = builder.compile(checkpointer=checkpointer)

        # 首次启动初始化状态；后续重启会自动忽略初始值，加载历史快照
        init_state = {
            "current_step": 0,
            "processed_list": []
        }

        try:
            # 流式执行，每一步完成自动落地checkpoint
            for chunk in graph.stream(init_state, config=task_config):
                pass
        except KeyboardInterrupt:
            # 手动Ctrl+C终止进程，状态自动保存到sqlite文件
            print("\n进程手动终止，进度已持久保存，下次运行自动续跑")