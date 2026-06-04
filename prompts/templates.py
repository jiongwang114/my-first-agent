# prompts/templates.py
import os

def build_system_prompt(tools: list) -> str:
    """
    根据传入的工具列表，动态组装出最终的 System Prompt。
    """
    # 1. 动态生成工具的描述和名称列表
    tool_descriptions = ""
    tool_names = []

    for tool in tools:
        # 把每个工具的名字和说明书拼接起来，比如 "calculator: 用于数学计算..."
        tool_descriptions += f"- {tool.name}: {tool.description}\n"
        tool_names.append(tool.name)
        
    tool_names_str = ", ".join(tool_names)

    # 2. 读取本地的 system_prompt.txt 模板
    # 获取当前文件 (templates.py) 所在的目录路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    prompt_path = os.path.join(current_dir, "system_prompt.txt")

    with open(prompt_path, "r", encoding="utf-8") as f:
        template = f.read()

    # 3. 将占位符替换为真实的工具信息
    final_prompt = template.replace("{tool_descriptions}", tool_descriptions)
    final_prompt = final_prompt.replace("{tool_names}", tool_names_str)
    
    return final_prompt
