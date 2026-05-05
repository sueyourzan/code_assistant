# 🤖 DeepSeek 智能代码助手

> **"基于 Dev Containers 的云端开发环境与 DeepSeek 大模型API的项目"**

本项目是一个现代化的 AI 代码助手，旨在为你提供一个**无需配置环境**、**开箱即用**的本地化开发体验。无论你是 Python 新手还是资深工程师，只需一键启动，即可享受 DeepSeek 模型带来的极速代码生成与解释服务。

---

## 🚀 核心特性

### 🐳 极致的环境管理 (Dev Containers)
告别繁琐的环境配置！本项目利用 Docker 容器技术，封装了所有依赖：
*   **基础环境**: Python 3.11 (官方镜像)
*   **开发工具**: 内置 GitHub CLI，支持直接管理代码仓库
*   **自动化**: 容器启动后自动安装依赖，无需手动 `pip install`

### 🌐 智能交互界面 (Streamlit)
*   **实时聊天**: 支持流式输出（打字机效果），低延迟交互。
*   **性能监控**: 独特的侧边栏面板，实时记录 API 调用耗时与 Token 消耗，帮助你优化提示词。
*   **响应式设计**: 适配桌面与移动端浏览。

### ⚡ 强大的后端支持 (DeepSeek API)
*   **高性能模型**: 对接 DeepSeek 最新 `deepseek-chat` 模型，专为代码生成优化。
*   **安全隔离**: API Key 通过环境变量管理，保障账户安全。

---

## 📂 项目结构

```bash
.
├── .devcontainer/          # Docker 容器配置目录
│   └── devcontainer.json   # 定义基础镜像、工具安装及自动化脚本
├── main.py                 # Streamlit 主程序 (包含 UI 与 API 调用逻辑)
├── requirements.txt        # Python 依赖列表
└── .env                    # (可选) 本地环境变量文件