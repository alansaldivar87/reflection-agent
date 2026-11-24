from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages
from chains import generate_chain, reflect_chain

def main() -> None:
    """Run the reflection agent entry point."""
    print("Reflection agent")

if __name__ == "__main__":
    main()

