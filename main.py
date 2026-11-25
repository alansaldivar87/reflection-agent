from langchain_core.language_models.fake_chat_models import FakeMessagesListChatModel

from graph import build_graph


def main() -> None:
    model = FakeMessagesListChatModel(responses=[])
    diagram = build_graph(model).compile().get_graph()
    print(diagram.draw_mermaid())
    print(diagram.draw_ascii())


if __name__ == "__main__":
    main()
