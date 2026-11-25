from langchain_core.messages import HumanMessage

from graph import build_graph


def main() -> None:
    graph = build_graph().compile()
    diagram = graph.get_graph()
    print(diagram.draw_mermaid())
    print(diagram.draw_ascii())

    request = HumanMessage(
        content="Write a short X post about reflection loops in LangGraph."
    )
    result = graph.invoke({"messages": [request]})
    print(result["messages"][-1].text)


if __name__ == "__main__":
    main()
