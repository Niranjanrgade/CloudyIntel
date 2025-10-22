from dotenv import load_dotenv
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, add_messages, START, END
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode, tools_condition

load_dotenv(override=True)

from langchain_community.utilities import GoogleSerperAPIWrapper

serper = GoogleSerperAPIWrapper()

tool_web_search = Tool(
        name="web_search",
        func=serper.run,
        description="Useful for when you need more information from an online search",
    )
tools = [tool_web_search]


# Step 1: Define the State object
class State(TypedDict):
    messages: Annotated[list, add_messages]

# Step 2: Start the Graph Builder with this State class
graph_builder = StateGraph(State)

llm = ChatOpenAI(model="gpt-5-mini")
llm_with_tools = llm.bind_tools(tools)

def aws_compute_domain_architect(state: State) -> State:
    """
    This function is used to architect the AWS compute domain.
    """
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}

memory = MemorySaver()

web_search_tool_node = ToolNode(tools=tools)

graph_builder.add_node("aws_compute_domain_architect", aws_compute_domain_architect)
graph_builder.add_node("web_search_tool_node", web_search_tool_node)

graph_builder.add_edge(START, "aws_compute_domain_architect")
graph_builder.add_conditional_edges("aws_compute_domain_architect", tools_condition, ["web_search_tool_node", END])
graph_builder.add_edge("web_search_tool_node", "aws_compute_domain_architect")

graph = graph_builder.compile(checkpointer=memory)