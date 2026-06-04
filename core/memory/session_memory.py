# core/memory/session_memory.py

class SessionMemory:
    def __init__(self):
        """
        初始化一个空字典，用来存放所有用户的多轮对话记录。
        数据结构类似:
        {
            "user_zhangsan": [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}],
            "user_lisi": [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]
        }
        """
        self.sessions = {}
        
    def _init_session_if_not_exists(self, session_id: str):
        """内部防呆机制：如果这个用户是第一次来，给他建一个空的记忆列表"""
        if session_id not in self.sessions:
            self.sessions[session_id] = []

    def add_message(self, session_id: str, role: str, content: str):
        """向特定用户的记忆中添加一条新消息"""
        self._init_session_if_not_exists(session_id)
        self.sessions[session_id].append({"role": role, "content": content})
        
    def get_history(self, session_id: str) -> list:
        """获取特定用户的所有短期记忆"""
        self._init_session_if_not_exists(session_id)
        return self.sessions[session_id]
        
    def clear(self, session_id: str):
        """清空特定用户的记忆（相当于该用户点击了“开启新对话”）"""
        if session_id in self.sessions:
            self.sessions[session_id] = []