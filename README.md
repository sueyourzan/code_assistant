# 🤖 DeepSeek 智能代码助手

> **零配置、高性能的AI代码开发伴侣**  
> 基于DeepSeek大模型API + Streamlit + Dev Containers的现代化开发体验

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32%2B-green)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-orange)](LICENSE)

## 🌟 核心特性

### 🐳 **一键部署的开发环境**
- **零配置启动**：Docker容器封装所有依赖，无需手动安装
- **跨平台支持**：Windows/macOS/Linux 无缝运行
- **自动依赖管理**：容器启动时自动安装Python 3.11及项目依赖

### 💬 **智能交互体验**
- **实时流式对话**：AI回复采用打字机效果，提升交互体验
- **性能洞察面板**：实时监控API调用耗时，Token消耗量，助您优化提示词
- **响应式设计**：完美适配桌面和移动设备
- **端口冲突自动处理**：智能检测并切换可用端口

### ⚡ **专业级AI能力**
- **代码专项优化**：深度集成DeepSeek最新`deepseek-chat`模型
- **安全凭证管理**：API密钥通过环境变量隔离，保障账户安全
- **上下文感知**：完整的对话历史管理，支持复杂代码任务

## 🛠️ 快速开始

### 前置条件
- **VS Code** + [Dev Containers扩展](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
- **Docker Desktop** (最新版本)
- **DeepSeek API账户** (获取API密钥)

### 安装步骤
```bash
# 1. 克隆仓库
git clone https://github.com/sueyourzan/code_assistant.git
cd code_assistant

# 2. 在VS Code中打开项目
code .

# 3. VS Code会提示"Reopen in Container"，点击确认
# 4. 配置API密钥（选择一种方式）：
#   方式1：创建.env文件
echo "DEEPSEEK_API_KEY=your_api_key_here" > .env

#   方式2：设置环境变量
#   export DEEPSEEK_API_KEY=your_api_key_here

# 切换python环境为.venv

# 5. 使用启动器运行应用
python run.py
```


### 备用启动方式
```bash
# 直接使用Streamlit启动
streamlit run main.py --server.port=8501

# 指定不同端口
python run.py --port 9000
```
### 结束应用
```bash
#快捷键 CTRL + C
```

## 📂 项目结构
```bash
.
├── .devcontainer/           # Docker容器配置
│   ├── devcontainer.json    # 容器定义和工具配置
│   └── Dockerfile           # 自定义镜像构建文件
├── main.py                  # Streamlit核心应用
├── run.py                   # 智能启动器（端口检测、环境验证）
├── requirements.txt         # Python依赖列表
├── .env.example             # 环境变量模板
├── .gitignore               # Git忽略规则
├── LICENSE                  # MIT许可证
└── README.md                # 项目文档
```

### .env.example 
```bash
# DeepSeek API密钥
DEEPSEEK_API_KEY=your_api_key_here

# 可选配置
MODEL_TEMPERATURE=0.3
STREAMLIT_SERVER_PORT=8501