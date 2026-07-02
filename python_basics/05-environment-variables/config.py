import os
from dotenv import load_dotenv

load_dotenv()


def get_required_env(name: str) -> str:
    value = os.getenv(name)
    if value is None or value == "":
        raise ValueError(f"缺少必须的环境变量:{name}")
    return value


LLM_MODEL = get_required_env("LLM_MODEL")
LLM_TEMPERATURE = float(get_required_env("LLM_TEMPERATURE"))
LLM_SYSTEM_PROMPT = get_required_env("LLM_SYSTEM_PROMPT")
