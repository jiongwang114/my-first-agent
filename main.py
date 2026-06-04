# main.py
import sys
from core.agent import Agent

def print_welcome_message():
    """打印漂亮的欢迎启动画面"""
    print("="*50)
    print("🚀 欢迎使用你的专属 AI Agent！")
    print("💡 提示：它可以进行数学计算、联网搜索，并拥有短期记忆。")
    print("输入 'exit', 'quit' 或按下 Ctrl+C 退出聊天。")
    print("="*50 + "\n")

def main():
    # 1. 实例化我们亲手打造的 Agent
    agent = Agent()
    
    # 2. 打印欢迎语
    print_welcome_message()

# 3. 开启无限对话循环
    while True:
        try:
            # 等待用户在终端输入文字
            user_input = input("\n🧑 你: ")

            # 如果用户直接敲回车（没输入内容），则跳过本次循环
            if not user_input.strip():
                continue

            # 检查用户是否想要退出
            if user_input.lower() in ['exit', 'quit']:
                print("\n👋 拜拜！期待下次与你聊天。")
                break

            # 4. 将用户输入交给 Agent 处理，并获取回答
            # 这里会自动触发 agent.py 里的 ReAct 核心循环和工具调用
            answer = agent.run(user_input)

            # 5. 打印最终结果
            print(f"\n🤖 Agent: {answer}")

            # 捕获 Ctrl+C 快捷键中断
        except KeyboardInterrupt:
            print("\n\n👋 检测到中断信号，正在退出... 拜拜！")
            sys.exit(0)

            # 捕获其他未知错误，防止程序崩溃退出
        except Exception as e:
            print(f"\n❌ 发生了未知的错误: {e}")
            print("请重试。")

if __name__ == "__main__":
    main()