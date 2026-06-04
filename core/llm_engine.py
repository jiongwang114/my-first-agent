# core/llm_engine.py
from openai import OpenAI
from config.settings import settings

class LLMEngine:
    def __init__(self):
        """初始化大模型客户端"""
        # 使用我们在 settings 中配置好的参数
        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY,
            base_url=settings.BASE_URL
        )
        self.model = settings.MODEL_NAME
    
    def chat(self, messages: list, temperature: float = 0.7,stop: list = None) -> str:
        """
        向大模型发送对话并获取回复。
        :param messages: 消息列表，格式如 [{"role": "user", "content": "你好"}]
        :param temperature: 随机性参数，0最严谨，1最发散
        :return: 模型生成的文本字符串
        :stop:强制LLM在该位置停止继续生成，防止大模型自导自演
        """

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                stop=stop
            )
            # 提取并返回纯文本内容
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: 大模型调用失败，原因：{e}"
