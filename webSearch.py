import os
import autogen
from dotenv import load_dotenv

load_dotenv()

config_list = [
    {
        'model': 'gpt-4',
        'api_key': os.getenv('OPENAI_KEY'),
    }
]

llm_config = {
    "request_timeout": 600,
    "config_list": config_list,
    "seed": 47,
    "temperature": 0
}

# create an AssistantAgent instance named "assistant"
assistant = autogen.AssistantAgent(
    name="assistant",
    llm_config=llm_config,
)
# create a UserProxyAgent instance named "user_proxy"
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="TERMINATE",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={"work_dir": "web"},
    llm_config=llm_config,
    system_message="""Reply TERMINATE if the task has been solved at full satisfaction.
Otherwise, reply CONTINUE, or the reason why the task is not solved yet."""
)
# the assistant receives a message from the user, which contains the task description
user_proxy.initiate_chat(
    assistant,
    message="""
read this page: https://en.wikipedia.org/wiki/Ashoka
What was Askoka religion?
""",
)
