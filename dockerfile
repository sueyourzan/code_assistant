# 1. 基础镜像：使用 Azure 中国镜像源加速拉取
# 对应 devcontainer.json 中的 "image": "mcr.azure.cn/devcontainers/python:3.11-bullseye"
FROM mcr.azure.cn/devcontainers/python:3.11-bullseye

# 2. 设置环境变量：配置 pip 使用清华源
# 对应 containerEnv 字段，加速国内 Python 包下载
ENV PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple \
    PIP_TRUSTED_HOST=pypi.tuna.tsinghua.edu.cn \
    # 对应 containerEnv.PYTHONNOUSERSITE
    PYTHONNOUSERSITE=1

# 3. 配置非 root 用户 (vscode)
# 对应 devcontainer.json 中的 "remoteUser": "vscode"
# 镜像中通常已预创建该用户，这里确保环境归属
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_GID

# 4. 复制项目文件
# 将本地代码复制到容器内的工作目录
# 注意：devcontainer 默认工作目录通常为 /workspaces/<repo-name> 或 /home/vscode
WORKDIR /home/${USERNAME}

# 5. 安装依赖
# 对应 postCreateCommand
# 注意：requirements.txt 需要与 Dockerfile 在同一目录下
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. 切换到非 root 用户运行
# 对应 remoteUser 设置
USER ${USERNAME}

# 7. 暴露端口
# Streamlit 默认端口
EXPOSE 8501

# 8. 启动命令
# 对应之前的 Streamlit 启动逻辑
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]