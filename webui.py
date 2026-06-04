# webui.py
import streamlit as st
import uuid
from core.agent import Agent

# ==========================================
# 1. 页面基本配置 (必须放在脚本最开头)
# ==========================================
st.set_page_config(page_title="我的超级 Agent", page_icon="🤖", layout="centered")

st.title("🤖 我的专属 AI Agent")
st.caption("✨ 提示：我不仅会聊天，还会自动调用搜索引擎和计算器哦！")

# ==========================================
# 2. 初始化全局大模型与会话状态
# ==========================================
# 使用 st.cache_resource 装饰器，确保 Agent 核心大脑只被初始化一次，避免每次发消息都重新加载
@st.cache_resource
def get_agent():
    return Agent()

agent = get_agent()

# 给当前打开网页的用户随机发一张“专属身份证” (Session ID)
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# 初始化网页端用来渲染气泡的聊天记录列表
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "你好！我是你的 AI 助手，今天想查点什么？"}]

# ==========================================
# 3. 渲染历史聊天气泡
# ==========================================
# 每次网页刷新时，把之前存下来的聊天记录画到屏幕上
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ==========================================
# 4. 核心交互：处理用户新输入的问题
# ==========================================
# st.chat_input 会在网页底部生成一个发送框
if user_query := st.chat_input("请输入你的问题..."):
    
    # 第一步：把用户输入的问题立刻画到网页上
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    # 第二步：呼叫 Agent 处理，并显示“思考中”的转圈圈动画
    with st.chat_message("assistant"):
        with st.spinner("Agent 正在思考并调用工具... 稍等片刻"):
            # 这里的 session_id 确保了后台的隔离记忆生效
            response = agent.run(user_query, session_id=st.session_state.session_id)
            # 把最终答案渲染到网页上
            st.markdown(response)

    # 第三步：把 Agent 的回答存入网页状态，以便下次刷新时不消失
    st.session_state.messages.append({"role": "assistant", "content": response})