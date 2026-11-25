import sys

from langchain_core.messages import HumanMessage
from openai import APIConnectionError, APITimeoutError

from graph import GENERATE, REFLECT, build_graph


def main() -> None:
    graph = build_graph().compile()
    diagram = graph.get_graph()
    print(diagram.draw_mermaid())
    print(diagram.draw_ascii())

    request = HumanMessage(
        content=(
            "Write one X post of at most 280 characters about how this LangGraph "
            "reflection agent works. Use these implementation facts: the generate node "
            "writes a draft, the reflect node critiques it, and the graph adds the "
            "feedback to its message history. The generate node reads that history "
            "to revise the draft. The loop changes the draft text while the model "
            "weights stay fixed."
        )
    )
    print("Drafting the X post...", file=sys.stderr, flush=True)
    final_draft = None
    try:
        for update in graph.stream({"messages": [request]}, stream_mode="updates"):
            if GENERATE in update:
                final_draft = update[GENERATE]["messages"][-1]
            elif REFLECT in update:
                print(
                    "Critique received. Revising the draft...",
                    file=sys.stderr,
                    flush=True,
                )
    except APITimeoutError:
        raise SystemExit("An OpenAI request timed out. Run the agent again.") from None
    except APIConnectionError:
        raise SystemExit(
            "Could not connect to OpenAI. Check your network and try again."
        ) from None

    if final_draft is None:
        raise SystemExit("The agent finished without producing a draft.")
    print(final_draft.text)


if __name__ == "__main__":
    main()
