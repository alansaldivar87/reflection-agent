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
            "You are  X techie wirtting for excelence\n"
            "Generate best post for user's request\n"
            "If user provides critique, respond with a revised version of your attempts",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

REFLECTION_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            " You are a viral X influencer. generate and critique viral content ideas for X. "
            "You will be given a topic and you will generate 3 viral content ideas for that topic. "
            "You will then critique each idea and provide suggestions for improvement."
            "Always provide detailed recommendations for improvement including length, virality, style, etc.",
        ),
        # Insert the history here so the request and draft keep their message roles.
        MessagesPlaceholder(variable_name="messages"),
    ]
)


def build_chains(
    model: BaseChatModel | None = None,
) -> tuple[MessageChain, MessageChain]:
    """Build the generation and reflection chains with one shared model."""
    if model is None:
        # ChatOpenAI reads credentials when it is created.
        load_dotenv()
        model = ChatOpenAI(model_name="gpt-4o", temperature=0.7, max_tokens=500)

    # Each pipe sends its formatted prompt to the model and returns a reply message.
    return GENERATION_PROMPT | model, REFLECTION_PROMPT | model
