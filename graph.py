from typing import Annotated, TypedDict

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages

from chains import build_chains

GENERATE = "generate"
REFLECT = "reflect"
MAX_HISTORY_MESSAGES = 6


class MessageState(TypedDict):
    # LangGraph appends new message IDs and replaces messages with matching IDs.
    messages: Annotated[list[BaseMessage], add_messages]


def should_continue(state: MessageState) -> str:
    """Route to reflection until the conversation passes the message limit."""
    if len(state["messages"]) > MAX_HISTORY_MESSAGES:
        return END
    return REFLECT


def build_graph(model: BaseChatModel | None = None) -> StateGraph:
    """Register the draft and critique nodes on a fresh graph builder."""
    generate_chain, reflect_chain = build_chains(model)

    def generation_node(state: MessageState) -> MessageState:
        draft = generate_chain.invoke({"messages": state["messages"]})
        # The reducer merges this one new draft into the conversation history.
        return {"messages": [draft]}

    def reflection_node(state: MessageState) -> MessageState:
        critique = reflect_chain.invoke({"messages": state["messages"]})
        # Put the critique in the human role so the writer sees a revision request.
        return {"messages": [HumanMessage(content=critique.content)]}

    builder = StateGraph(state_schema=MessageState)
    builder.add_node(GENERATE, generation_node)
    builder.add_node(REFLECT, reflection_node)
    builder.set_entry_point(GENERATE)

    # Declare the possible destinations so LangGraph can draw both branches.
    builder.add_conditional_edges(GENERATE, should_continue, [REFLECT, END])
    return builder
