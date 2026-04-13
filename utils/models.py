"""Centralized model initialization.

Switch providers by uncommenting the relevant section below.
"""

from dotenv import load_dotenv
load_dotenv(dotenv_path="../../.env", override=True)
from langchain.chat_models import init_chat_model

model = init_chat_model("openai:gpt-4.1-mini")

# Anthropic
# model = init_chat_model("anthropic:claude-sonnet-4-20250514")

# Azure OpenAI
# from langchain_openai import AzureChatOpenAI
# model = AzureChatOpenAI(azure_deployment="gpt-4.1-mini", streaming=True)

# AWS Bedrock
# from langchain_aws import ChatBedrockConverse
# model = ChatBedrockConverse(provider="anthropic", model_id="anthropic.claude-sonnet-4-20250514-v1:0")
