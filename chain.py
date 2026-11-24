from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

reflection_prompt = ChatPromptTemplate.from_messages([
    (
        "system", 
        " You are a viral X influencer. generate and critique viral content ideas for X. You will be given a topic and you will generate 3 viral content ideas for that topic. You will then critique each idea and provide suggestions for improvement."
        "Always provide detailed recommendations for improvement including length, virality, style, etc."
    ),
    MessagesPlaceholder(variable_name="messages")
])

generation_prompt = ChatPromptTemplate.from_messages([
    (
        "system", 
        "You are  X techie wirtting for excelence\n"
        "Generate best post for user's request\n"
        "If user provides critique, respond with a revised version of your attempts"
    ),
    MessagesPlaceholder(variable_name="messages")
]);

llm = ChatOpenAI(model_name="gpt-4o", temperature=0.7, max_tokens=500)
generation_chain = generation_prompt | llm
reflection_chain = reflection_prompt | llm
