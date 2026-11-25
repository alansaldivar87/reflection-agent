from dotenv import load_dotenv
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import Runnable
from langchain_openai import ChatOpenAI

type MessageChain = Runnable[dict[str, list[BaseMessage]], BaseMessage]

# The writer uses the same prompt for a first draft and later revisions.
GENERATION_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Write one concise, technically accurate X post that answers the original request. "
            "When the request supplies implementation facts, ground every technical claim "
            "in those facts. Respect any character limit in the original request. "
            "Later messages may contain feedback on an earlier draft. Use that feedback to "
            "revise the latest draft while keeping the original topic and format. "
            "Return only the text of the post.",
        ),
        MessagesPlaceholder(variable_name="messages"),
        (
            "human",
            "Return the complete X post for the original request. Apply the latest "
            "critique when it calls for changes. If the draft already meets the request, "
            "return the full draft unchanged. Output only the post text.",
        ),
    ]
)

REFLECTION_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Review the latest X post draft against the original request. "
            "Give brief, actionable feedback on technical accuracy, clarity, and length. "
            "When the request supplies implementation facts, flag any unsupported claims "
            "and ask the writer to remove or correct them. "
            "Return feedback on the existing draft only.",
        ),
        # Insert the history here so the request and draft keep their message roles.
        MessagesPlaceholder(variable_name="messages"),
        (
            "human",
            "Review the latest draft above. If it meets the original request, "
            "instruct the writer to keep the full draft as written.",
        ),
    ]
)


def build_chains(
    model: BaseChatModel | None = None,
) -> tuple[MessageChain, MessageChain]:
    """Build the generation and reflection chains with one shared model."""
    if model is None:
        # ChatOpenAI reads credentials when it is created.
        load_dotenv()
        model = ChatOpenAI(
            model_name="gpt-4o",
            temperature=0.7,
            max_tokens=500,
            timeout=30,
            max_retries=1,
        )

    # Each pipe sends its formatted prompt to the model and returns a reply message.
    return GENERATION_PROMPT | model, REFLECTION_PROMPT | model
