from graph import build_graph


def main() -> None:
    diagram = build_graph().compile().get_graph()
    print(diagram.draw_mermaid())
    print(diagram.draw_ascii())


if __name__ == "__main__":
    main()
