# 将基础镜像升级为与你本地一致的 Python 3.14
FROM python:3.14-slim

# 关闭 Python 输出缓冲，确保 print() 和日志实时显示在 docker logs 中
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
COPY . .
EXPOSE 8000
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]