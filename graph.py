from functools import cache
from typing import Annotated, Literal, TypedDict

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages
from langgraph.types import Command

from chains import build_chains

GENERATE = "generate"
REFLECT = "reflect"
MAX_HISTORY_MESSAGES = 6


class MessageState(TypedDict):
    # LangGraph appends new message IDs and replaces messages with matching IDs.
    messages: Annotated[list[BaseMessage], add_messages]


def should_continue(state: MessageState) -> Command[Literal["reflect", "__end__"]]:
    """Route to reflection until the conversation passes the message limit."""
    if len(state["messages"]) > MAX_HISTORY_MESSAGES:
        return Command(goto=END)
    return Command(goto=REFLECT)


def build_graph(model: BaseChatModel | None = None) -> StateGraph:
    """Register the draft and critique nodes on a fresh graph builder."""

    # Initialize the shared model on the first node call. Drawing only needs the graph.
    @cache
    def chains():
        return build_chains(model)

    def generation_node(state: MessageState) -> MessageState:
        generate_chain, _ = chains()
        draft = generate_chain.invoke({"messages": state["messages"]})
        # The reducer merges this one new draft into the conversation history.
        return {"messages": [draft]}

    def reflection_node(state: MessageState) -> MessageState:
        _, reflect_chain = chains()
        critique = reflect_chain.invoke({"messages": state["messages"]})
        # Put the critique in the human role so the writer sees a revision request.
        return {"messages": [HumanMessage(content=critique.content)]}

    builder = StateGraph(state_schema=MessageState)
    builder.add_node(GENERATE, generation_node)
    builder.add_node(REFLECT, reflection_node)
    builder.add_node(should_continue)
    builder.set_entry_point(GENERATE)

    builder.add_edge(GENERATE, "should_continue")
    # Send each critique back to the writer for another draft.
    builder.add_edge(REFLECT, GENERATE)
    return builder
