# X Tech Post Reflection Agent

A small project for generating polished technology posts for X. The planned
reflection workflow uses LangGraph to draft a post, critique it, and revise it
based on feedback.

## Tech stack

- Python 3.12+
- LangGraph and LangChain
- OpenAI chat models through `langchain-openai`

## Setup

Install dependencies with [uv](https://docs.astral.sh/uv/):

```shell
uv sync
```

Create a `.env` file in the project root and add your OpenAI API key:

```dotenv
OPENAI_API_KEY=your-api-key
```

Keep `.env` local; it is ignored by Git.

## Run

```shell
uv run python main.py
```

The current entry point only prints a startup message. The generation and
reflection prompt chains are defined in `chain.py`; the LangGraph workflow
that connects them and runs the draft-review-revision loop is not implemented
yet.
