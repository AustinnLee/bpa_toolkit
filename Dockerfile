# 1. 选择基础镜像
FROM python:3.12-slim-bookworm

# 2. 复制 uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 3. 设置工作目录
WORKDIR /app

# 4. 环境变量设置
ENV PYTHONUNBUFFERED=1

# === 关键修复点 ===
# 告诉系统：优先使用 /app/.venv/bin 下的 python 和 pip
# 这样运行 "python" 时，实际上运行的是 ".venv/bin/python"
ENV PATH="/app/.venv/bin:$PATH"
# =================

# 5. 复制依赖描述文件
COPY pyproject.toml uv.lock ./

# 6. 安装依赖
# uv sync 会自动创建 .venv，并将包安装进去
RUN uv sync --frozen

# 7. 复制源码
COPY src/ ./src/
COPY data/ ./data/

# 8. 启动
# 由于配置了 PATH，这里的 python 会自动指向 .venv 里的 python
CMD ["python", "src/main.py"]
