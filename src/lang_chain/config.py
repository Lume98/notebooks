import os

from dotenv import load_dotenv

# 加载环境变量
load_dotenv(override=True)

# OpenAI 配置
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "glm-4.5-flash")  # 默认使用 glm-4.5-flash

# 确保必要的配置存在
assert OPENAI_API_KEY, "OPENAI_API_KEY 环境变量未设置"
assert OPENAI_BASE_URL, "OPENAI_BASE_URL 环境变量未设置"
