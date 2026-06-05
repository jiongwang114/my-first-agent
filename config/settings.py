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

# 启动时校验：确保关键配置不为空（fail-fast 原则）
if not Config.OPENAI_API_KEY:
    raise RuntimeError(
        "OPENAI_API_KEY 未设置！\n"
        "本地开发：在项目根目录创建 .env 文件并设置 OPENAI_API_KEY\n"
        "Docker 部署：通过 docker-compose env_file 或 docker run -e 传入"
    )

# 实例化一个全局配置对象供其他文件导入
settings = Config()
