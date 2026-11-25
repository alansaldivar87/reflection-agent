from argparse import ArgumentParser

from langchain_core.language_models.fake_chat_models import FakeMessagesListChatModel

from graph import build_graph


def main() -> None:
    """Run the reflection agent entry point."""
    parser = ArgumentParser(description="X tech post reflection agent")
    parser.add_argument(
        "--mermaid", action="store_true", help="print the workflow as Mermaid source"
    )
    args = parser.parse_args()

    if args.mermaid:
        # Rendering inspects the graph structure, so it can use a placeholder model.
        model = FakeMessagesListChatModel(responses=[])
        workflow = build_graph(model).compile()
        print(workflow.get_graph().draw_mermaid())
        return

    print("Reflection agent")


if __name__ == "__main__":
    main()
