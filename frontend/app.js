// app.js
document.addEventListener('DOMContentLoaded', () => {
    const chatHistory = document.getElementById('chat-history');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    
    // 生成一个随机的 Session ID 供当前浏览器标签页使用
    const sessionId = 'session_' + Math.random().toString(36).substring(2, 9);

    // 自动调整输入框高度
    userInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
    });

    // 监听回车键发送
    userInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    sendBtn.addEventListener('click', sendMessage);

    async function sendMessage() {
        const text = userInput.value.trim();
        if (!text) return;

        // 1. 在页面上渲染用户的问题
        appendMessage('user', '🧑', text);
        userInput.value = '';
        userInput.style.height = 'auto'; // 恢复默认高度

        // 2. 准备渲染 Agent 的回复框（先放置一个空框）
        const { messageDiv, contentDiv, statusDiv } = appendAgentMessagePlaceholder();

        try {
            // 3. 向我们刚才写的 FastAPI 后端发起 POST 请求
            const response = await fetch('http://localhost:8000/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query: text, session_id: sessionId })
            });

            if (!response.ok) throw new Error('网络请求失败');

            // 4. 🔥 核心魔法：读取 SSE 数据流
            const reader = response.body.getReader();
            const decoder = new TextDecoder('utf-8');
            let buffer = '';

            while (true) {
                const { value, done } = await reader.read();
                if (done) break;
                
                buffer += decoder.decode(value, { stream: true });
                
                // 🔥 修复点 1：使用正则表达式，同时兼容 \r\n\r\n 和 \n\n
                const blocks = buffer.split(/\r?\n\r?\n/);
                // 留下最后一个可能还没接收完整的部分
                buffer = blocks.pop(); 

                for (const block of blocks) {
                    if (!block.trim()) continue; // 跳过空区块

                    // 🔥 修复点 2：优化正则，确保能精准抓取多行内容
                    const eventMatch = block.match(/event:\s*(.*)/);
                    const dataMatch = block.match(/data:\s*(.*)/);
                    
                    if (eventMatch && dataMatch) {
                        const event = eventMatch[1].trim();
                        // 注意：这里 dataMatch[1] 不要用 trim()，否则会吃掉 AI 回复时的排版空格！
                        const data = dataMatch[1]; 

                        if (event === 'status') {
                            statusDiv.textContent = data;
                        } else if (event === 'message') {
                            // 将接收到的字符直接追加到页面上
                            contentDiv.textContent += data;
                            scrollToBottom();
                        } else if (event === 'done') {
                            statusDiv.textContent = '';
                        } else if (event === 'error') {
                            contentDiv.textContent += `\n[系统错误]: ${data}`;
                            statusDiv.textContent = '';
                        }
                    }
                }
            }
        } catch (error) {
            console.error('通信错误:', error);
            contentDiv.textContent = "[网络连接异常，请检查后端服务器是否已启动]";
            statusDiv.textContent = '';
        }
    }

    // 辅助函数：追加普通消息
    function appendMessage(role, avatarText, text) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${role}`;
        msgDiv.innerHTML = `
            <div class="avatar">${avatarText}</div>
            <div class="message-content">${text}</div>
        `;
        chatHistory.appendChild(msgDiv);
        scrollToBottom();
    }

    // 辅助函数：创建 Agent 回复的空占位符（包含状态栏和内容区）
    function appendAgentMessagePlaceholder() {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message assistant`;
        
        const avatarDiv = document.createElement('div');
        avatarDiv.className = 'avatar';
        avatarDiv.textContent = '✨';

        const wrapperDiv = document.createElement('div');
        wrapperDiv.style.flex = '1';

        const statusDiv = document.createElement('div');
        statusDiv.className = 'status-text';
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';

        wrapperDiv.appendChild(statusDiv);
        wrapperDiv.appendChild(contentDiv);
        msgDiv.appendChild(avatarDiv);
        msgDiv.appendChild(wrapperDiv);

        chatHistory.appendChild(msgDiv);
        scrollToBottom();

        return { messageDiv: msgDiv, contentDiv, statusDiv };
    }

    // 辅助函数：页面始终滚动到最底部
    function scrollToBottom() {
        chatHistory.scrollTo({
            top: chatHistory.scrollHeight,
            behavior: 'smooth'
        });
    }
});