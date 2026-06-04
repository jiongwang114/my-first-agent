# tools/web_search.py
from tools.base_tool import BaseTool
from ddgs import DDGS

class WebSearchTool(BaseTool):
    # 1. 严格遵守出厂标准，定义工具名
    name = "web_search"
    
    # 2. 灵魂描述：告诉大模型什么时候该用它，以及输入什么
    description = (
        "当你需要获取最新信息、新闻、或者回答你不知道的客观事实时，请使用此工具。"
        "输入应该是一个精简的搜索关键词，例如 '北京今天天气' 或 '2024年奥斯卡最佳影片'。"
    )

    def run(self, query: str) -> str:
        """执行具体的联网搜索逻辑"""
        try:
            # 限制只抓取前 3 条结果，避免给大模型喂太多字导致“撑爆”上下文（Token超限）
            results = DDGS().text(query, max_results=3)
            
            if not results:
                return "搜索完毕，但未找到相关结果。"

            # 把搜到的结构化数据（列表/字典）拼装成大模型容易阅读的纯文本字符串
            formatted_results = []
            for item in results:
                # 提取每条搜索结果的标题和摘要
                formatted_results.append(f"【标题】: {item['title']}\n【摘要】: {item['body']}")
            
            return "搜索结果如下:\n" + "\n---\n".join(formatted_results)
            
        except Exception as e:
            return f"搜索工具执行失败，错误信息: {e}"
