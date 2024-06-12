import os
from typing import Any, Callable, Dict, List, Optional, Tuple, Type, Union

import chromadb
from PIL import Image
from termcolor import colored

import autogen
from autogen import Agent, AssistantAgent, ConversableAgent, UserProxyAgent
from autogen.agentchat.contrib.img_utils import _to_pil, get_image_data
from autogen.agentchat.contrib.multimodal_conversable_agent import MultimodalConversableAgent
from autogen.agentchat.contrib.retrieve_assistant_agent import RetrieveAssistantAgent
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent
from autogen.code_utils import DEFAULT_MODEL, UNKNOWN, content_str, execute_code, extract_code, infer_lang
import os 

config_list = [
    {
        "model": "gemini-1.5-flash",
        "api_key": "AIzaSyAIO4KL1gDpl5OcPSzMj7O-lnHws-zdO_g",
        "api_type": "google"
    }
]

def termination_msg(x):
    return isinstance(x, dict) and "TERMINATE" == str(x.get("content", ""))[-9:].upper()

stylist_agent = RetrieveAssistantAgent(
    name="stylist",
    system_message='''You are a fashion sytlist assistant. Your job is to help create an outfit for the user from the clothes that they have.
    Figure out what kind of clothes the user needs based on the occasion described in their question. You are given a list of clothes and accessories that the user has.
    Respond with the best fit outfit. Be creative and fashionable. Take into consideration the color, texture and formality and date last used of the outfit.
      ''',
    default_auto_reply="Reply `TERMINATE` if the task is done.",
    llm_config={
        "timeout": 600,
        "cache_seed": 42,
        "config_list": config_list,
    },
)

closet_agent = RetrieveUserProxyAgent(
    name="closet",
    is_termination_msg=termination_msg,
    human_input_mode="NEVER",
    default_auto_reply="Reply `TERMINATE` if the task is done.",
    max_consecutive_auto_reply=3,
    retrieve_config={
        "task": "code",
        "docs_path": ["wardrobe.txt"],
        "chunk_token_size": 1000,
        "model": config_list[0]["model"],
        "collection_name": "groupchat",
        "overwrite": True,
        "get_or_create": True,
    },
    code_execution_config=False,  # we don't want to execute code in this case.
    description="Assistant who has extra content retrieval power for solving difficult problems.",
)

def rag_chat(instructions):

    chat_result = closet_agent.initiate_chat(
            stylist_agent, message=closet_agent.message_generator, problem=instructions,
        )

    return chat_result