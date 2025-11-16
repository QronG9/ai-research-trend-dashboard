FROM python:3.11-slim

# 安装一些基础依赖（可选，但推荐）
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 先复制 requirements，安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 再复制项目代码
COPY . .

# Cloud Run 会注入 $PORT，我们设一个默认值方便本地测试
ENV PORT=8080

# 启动 FastAPI 后端
CMD ["uvicorn", "src.frontend_api.server:app", "--host", "0.0.0.0", "--port", "8080"]
