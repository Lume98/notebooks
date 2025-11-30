from langchain_openai import ChatOpenAI

from . import config

llm = ChatOpenAI(model=config.OPENAI_MODEL, base_url=config.OPENAI_BASE_URL)
