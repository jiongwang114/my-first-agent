# core/agent.py
import re
from core.logger import logger
from core.llm_engine import LLMEngine
from prompts.templates import build_system_prompt
from tools.calculator import CalculatorTool
from tools.web_search import WebSearchTool
from core.memory.session_memory import SessionMemory

class Agent:
    def __init__(self):
        """初始化 Agent：装载大脑、工具和灵魂"""
        self.engine = LLMEngine()
        # 把我们写好的两个工具挂载上来
        self.tools = [CalculatorTool(), WebSearchTool()]
        # 动态生成包含工具说明的 System Prompt
        self.system_prompt = build_system_prompt(self.tools)
        # 设定最大循环次数，防止大模型陷入死循环
        self.max_loops = 5
        # 给 Agent 装上短期记忆
        self.memory = SessionMemory()

    def run(self, user_query: str,session_id: str = "default_user") -> str:
        """Agent 的核心运行逻辑：ReAct 循环"""
        # 1. 组装初始消息，包含系统指令和用户问题
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"Question: {user_query}"}
        ]
        # 拿着用户的 session_id 去取属于他的记忆
        messages.extend(self.memory.get_history(session_id))

        print(f"👤 用户问题: {user_query}\n" + "="*40)

        # 在后台记录用户提问
        logger.info(f"收到用户提问: {user_query}")

        # 开启思考循环
        for i in range(self.max_loops):
            print(f"\n🔄 第 {i+1} 轮思考开始...")
            
            # 2. 把当前所有上下文交给大模型思考
            response = self.engine.chat(messages,stop=["Observation:"])
            print(f"🤖 大模型输出:\n{response}\n" + "-"*40)
            
            # 记录大模型每一轮的原生思考文本
            logger.info(f"第 {i+1} 轮大模型原始输出:\n{response}")

            # 必须把大模型自己的回复也存入历史记录，否则它会失忆
            messages.append({"role": "assistant", "content": response})

            # 3. 解析大模型是否得出了最终结论，如果是，则退出循环 (Break)
            if "Final Answer:" in response:
                final_answer = response.split("Final Answer:")[-1].strip()
                # 👇 新增：记录最终得出的答案
                logger.info(f"成功得出最终答案: {final_answer}")
                # 👇 新增：在返回答案前，把这一轮的问答存入海马体！
                self.memory.add_message(session_id,"user", user_query)
                self.memory.add_message(session_id,"assistant", final_answer)
                return final_answer
                
            # 4. 解析大模型是否想调用工具（使用正则表达式提取 Action 和 Action Input）
            action_match = re.search(r"Action:\s*(.*?)\n", response)
            action_input_match = re.search(r"Action Input:\s*(.*?)(?:\n|$)", response)
            
            if action_match and action_input_match:
                action_name = action_match.group(1).strip()
                action_input = action_input_match.group(1).strip()
                # 👇 新增：记录准备调用哪个工具，以及参数
                logger.info(f"准备调用工具: {action_name}, 参数: {action_input}")
                # 5. 执行对应的 Python 工具代码，拿到结果
                observation = self._execute_tool(action_name, action_input)
                print(f"🛠️ 工具观察结果 (Observation): {observation}")
                # 👇 新增：记录工具真实返回的结果
                logger.info(f"工具返回结果: {observation}")
                # 6. 把工具返回的结果喂给大模型，进入下一轮循环
                messages.append({"role": "user", "content": f"Observation: {observation}"})
            else:
                # 容错机制：如果大模型没有按格式输出，提醒它重试
                messages.append({
                    "role": "user", 
                    "content": "Observation: 你的输出格式不符合要求，请严格按照 Thought/Action/Action Input/Observation 的格式输出。"
                })
                # 👇 新增：记录大模型格式错误的警告
                logger.warning("大模型输出格式错误，触发容错机制。")
        return "Agent 思考次数超限，未能得出最终答案。"
    
    def _execute_tool(self, tool_name: str, tool_input: str) -> str:
        """内部辅助方法：根据工具名寻找并执行工具"""
        for tool in self.tools:
            if tool.name == tool_name:
                return tool.run(tool_input)
        return f"错误：找不到名为 {tool_name} 的工具。"
    
"""
# --- 本地测试区块，测试能否记住历史对话 ---
if __name__ == "__main__":
    agent = Agent()
    
    # 第一轮对话：赋予信息
    query1 = "你好，我叫 Alice，我最喜欢的数字是 7。"
    print(agent.run(query1))
    
    print("\n" + "*"*50 + "\n")
    
    # 第二轮对话：考察记忆与工具的结合
    query2 = "我的名字是什么？请把我的名字包含的字母数量，乘以我最喜欢的数字，告诉我结果。"
    print(agent.run(query2))
    """
"""# --- 本地测试区块,测试记忆隔离与否 ---
if __name__ == "__main__":
    # 我们只实例化一个 Agent 大脑（模拟服务器上运行的唯一程序）
    shared_agent = Agent()
    
    print("=== 并发对话模拟开始 ===\n")
    
    # 张三发来第一句话
    print("👨 张三: 我叫张三，我最喜欢红色。")
    ans1 = shared_agent.run("我叫张三，我最喜欢红色。", session_id="user_zhangsan")
    print(f"🤖 专属回复张三: {ans1}\n")
    
    # 紧接着，李四也连接上了服务器发了一句话
    print("🧔 李四: 你好，我是李四。")
    ans2 = shared_agent.run("你好，我是李四。", session_id="user_lisi")
    print(f"🤖 专属回复李四: {ans2}\n")
    
    # 张三再次提问，测试有没有被李四覆盖
    print("👨 张三: 我是谁？我最喜欢什么颜色？")
    ans3 = shared_agent.run("我是谁？我最喜欢什么颜色？", session_id="user_zhangsan")
    print(f"🤖 专属回复张三: {ans3}\n")"""