FROM python:3.9-slim
WORKDIR /app

# 设置国内时区
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' > /etc/timezone

# 复制依赖文件
COPY requirements.txt .

# 🌟 核心修改：使用 -i 参数强制指定清华大学镜像源
RUN pip install --no-cache-dir --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 拷贝剩余项目文件
COPY . .

EXPOSE 8080
CMD ["python", "app.py"]