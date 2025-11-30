from typing import TypedDict

from langchain_core.messages import BaseMessage, HumanMessage, ToolMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph


# 1️⃣ 定义状态
class State(TypedDict):
    messages: list[BaseMessage]


# 2️⃣ 定义节点
def model_node(state: State) -> State:
    """调用模型"""
    llm = ChatOpenAI(model="gpt-4o")
    response = llm.invoke(state["messages"])
    return {"messages": state["messages"] + [response]}


def tool_node(state: State) -> State:
    """执行工具"""
    # 从最后的 AI 消息提取工具调用
    tool_calls = state["messages"][-1].tool_calls
    results = []

    for call in tool_calls:
        if call["name"] == "get_weather":
            location = call["args"]["location"]
            weather = f"Weather in {location}: Sunny, 72°F"
            results.append(ToolMessage(weather, tool_call_id=call["id"]))

    return {"messages": state["messages"] + results}


# 3️⃣ 判断是否使用工具
def should_use_tools(state: State) -> str:
    """条件边函数"""
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tool_node"
    return END


# 4️⃣ 构建图
graph = StateGraph(State)

# 添加节点
graph.add_node("model", model_node)
graph.add_node("tool", tool_node)

# 添加边
graph.add_edge(START, "model")  # 开始 → 模型
graph.add_conditional_edges(  # 模型 → 条件边
    "model", should_use_tools, {"tool_node": "tool", END: END}
)
graph.add_edge("tool", "model")  # 工具 → 模型（循环）

# 5️⃣ 编译图
app = graph.compile()

# 6️⃣ 运行
result = app.invoke(
    {"messages": [HumanMessage("What's the weather in San Francisco?")]}
)

print(result["messages"][-1].content)
