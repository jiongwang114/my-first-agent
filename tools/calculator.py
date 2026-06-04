# tools/calculator.py
from tools.base_tool import BaseTool

class CalculatorTool(BaseTool):
    # 严格遵循基类制定的标准
    name = "calculator"

    # 描述必须写得非常清晰，明确告诉大模型它能干什么、输入格式是什么
    description = "当你需要进行精确的数学计算时，请使用此工具。输入必须是一个合法的数学表达式字符串，例如 '125 * 3.14' 或 '(100 + 50) / 2'。"

    def run(self, expression: str) -> str:
        """执行具体的计算逻辑"""
        try:
            # 使用 Python 内置的 eval 函数计算字符串表达式的值
            # (注：真实的工业项目中 eval 有代码注入风险，通常会使用更安全的 ast.literal_eval 或第三方数学库，这里为了学习原理保持极简)
            result = eval(expression, {"__builtins__": None}, {})
            return f"计算成功，结果是: {result}"
        except Exception as e:
            return f"计算失败，请检查表达式格式。错误信息: {e}"
