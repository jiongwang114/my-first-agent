# server.py
import asyncio
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse
import os
# 导入我们已经写好的强大 Agent 大脑
from core.agent import Agent

# 1. 初始化 FastAPI 应用
app = FastAPI(title="AI Agent API", description="流式前后端分离架构")

# 2. 配置跨域资源共享 (CORS) - 极其重要！
# 因为你的纯前端 HTML 是在浏览器直接打开的（比如 localhost:3000），
# 而后端在 localhost:8000，不在同一个域，必须允许跨域请求。
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有域名访问（生产环境建议写死前端域名）
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. 在内存中实例化全局 Agent（相当于开机启动大模型）
# 所有的 API 请求都将复用这个带有 SessionMemory 的全局大脑
global_agent = Agent()

# 4. 定义流式对话接口
@app.post("/chat")
async def chat_endpoint(request: Request):
    """
    接收前端发来的 JSON 数据，并通过 SSE 流式返回结果。
    """
    # 解析前端传过来的参数
    data = await request.json()
    user_query = data.get("query", "")
    session_id = data.get("session_id", "default_user")

    # 定义一个异步生成器，用于源源不断地向前端推送事件
    async def event_generator():
        try:
            # 【事件 1：状态通知】告诉前端我们开始干活了
            yield {"event": "status", "data": "Agent 正在思考并规划任务..."}
            await asyncio.sleep(0.1) # 稍微让出一下 CPU 控制权

            # 执行我们的 ReAct 核心逻辑 (这里会去调用搜索、计算器等)
            # 注：因为我们目前的 run() 是同步的，这里后台会稍微等几秒钟
            final_answer = global_agent.run(user_query, session_id=session_id)

            # 【事件 2：状态通知】告诉前端计算完毕，准备输出
            yield {"event": "status", "data": "思考完毕，正在输出结果..."}
            await asyncio.sleep(0.5)

            # 【事件 3：流式吐字】模拟真实大模型的逐字打字机效果
            # 我们把最终答案拆成一个个字符，像流水一样推给前端
            for char in final_answer:
                yield {"event": "message", "data": char}
                # 模拟 0.02 秒的打字延迟，让前端看起来无比丝滑
                await asyncio.sleep(0.02) 

            # 【事件 4：结束通知】告诉前端这句话彻底说完了
            yield {"event": "done", "data": "[DONE]"}

        except Exception as e:
            # 如果出错，优雅地把错误信息推送给前端
            yield {"event": "error", "data": str(e)}

    # 使用 sse_starlette 将生成器包装成标准的 SSE HTTP 响应
    return EventSourceResponse(event_generator())

# 挂载静态文件目录 (允许网页加载 js、css 和图片)
if os.path.exists("frontend"):
    app.mount("/static", StaticFiles(directory="frontend"), name="static")

# 将根路由 "/" 强行指向你的 index.html 网页
@app.get("/")
async def serve_frontend():
    return FileResponse("frontend/index.html")