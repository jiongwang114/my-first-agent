# core/memory/short_term.py

class ShortTermMemory:
    def __init__(self):
        """初始化一个空的列表，用来存放多轮对话记录"""
        self.history = []
        
    def add_message(self, role: str, content: str):
        """
        向记忆中添加一条新消息
        :param role: 只能是 'user' 或 'assistant'
        :param content: 说话的具体内容
        """
        self.history.append({"role": role, "content": content})
        
    def get_history(self) -> list:
        """获取所有短期记忆"""
        return self.history
        
    def clear(self):
        """清空记忆（相当于开启新对话）"""
        self.history = []