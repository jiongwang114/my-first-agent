# config/settings.py
import os
from dotenv import load_dotenv

# 加载 .env 文件中的变量到系统环境变量中
load_dotenv()

class Config:
    """集中管理所有配置项的类"""
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    BASE_URL = os.getenv("BASE_URL", "https://api.deepseek.com") # 提供默认值
    MODEL_NAME = os.getenv("MODEL_NAME", "deepseek-v4-flash")

# 实例化一个全局配置对象供其他文件导入
settings = Config()
