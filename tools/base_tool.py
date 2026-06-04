# tools/base_tool.py
from abc import ABC, abstractmethod

class BaseTool(ABC):
    """
    所有工具的抽象基类。
    任何具体的工具（如计算器、搜索器）都必须继承这个类。
    """

    # 1. 工具的名称（必须是唯一的纯英文，Agent 大脑通过这个名字来下达调用指令）
    name: str = ""

    # 2. 工具的描述（核心灵魂！大模型就是靠阅读这段文字，来决定当前情况该不该用这个工具）
    description: str = ""

    @abstractmethod
    def run(self, *args, **kwargs) -> str:
        """
        3. 工具的具体执行逻辑。
        所有的子类都必须重写 (Override) 这个方法，并且规定返回值最好统一为字符串 (str)。
        """
        pass