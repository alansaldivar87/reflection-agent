# TypedDict lets us describe the named fields that make up the graph's state.
from typing import TypedDict, Annotated

# BaseMessage is the common LangChain message type; HumanMessage represents user input.
from langchain_core.messages import BaseMessage, HumanMessage

# StateGraph builds a graph whose nodes update shared state; END marks its terminal point.
from langgraph.graph import END, StateGraph

# add_messages defines how new messages are combined with the existing message history.
from langgraph.graph.message import add_messages

# These chains are intended for drafting and reflecting on posts.
from chains import generate_chain, reflect_chain

# Define the shape of the data that will be passed between graph nodes.
class MessageGraph(TypedDict):
    # Annotated attaches a reducer so graph updates append/merge messages into this history.
    messages: Annotated[list[BaseMessage], add_messages]

# Keep startup logic in a function so it can also be imported without running the app.
def main() -> None:
    """Run the reflection agent entry point."""
    # Placeholder output; the graph is not constructed or invoked yet.
    print("Reflection agent")

# Run main only when this file is executed directly, not when another module imports it.
if __name__ == "__main__":
    # Start the application entry point.
    main()

