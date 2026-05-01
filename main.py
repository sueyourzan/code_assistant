import streamlit as st
import time
from openai import OpenAI
from dotenv import load_dotenv
import os

# 1. 页面基础配置
st.set_page_config(
    page_title="DeepSeek 代码助手",
    page_icon="🤖",
    layout="wide"
)

# 2. 初始化 API 客户端
load_dotenv()
API_KEY = os.getenv("DEEPSEEK_API_KEY")

if not API_KEY:
    st.error("❌ 未检测到 API Key！请在 Secrets 中设置 `DEEPSEEK_API_KEY` 或创建 `.env` 文件。")
    st.stop()

client = OpenAI(api_key=API_KEY, base_url="https://api.deepseek.com/v1")

# 3. 侧边栏：性能分析面板
with st.sidebar:
    st.title("📊 性能监控")
    st.markdown("实时记录 API 调用数据")
    
    # 初始化会话状态中的性能记录
    if "perf_stats" not in st.session_state:
        st.session_state.perf_stats = []

    # 显示历史记录
    if st.session_state.perf_stats:
        for stat in st.session_state.perf_stats:
            with st.expander(f"⚡ {stat['time']} - {stat['tokens']} tokens"):
                st.write(f"- **耗时:** {stat['duration']}s")
                st.write(f"- **输入:** {stat['prompt_tokens']}")
                st.write(f"- **输出:** {stat['completion_tokens']}")
    else:
        st.info("暂无对话记录")

    st.divider()
    st.markdown("### ⚙️ 设置")
    temperature = st.slider("Temperature", 0.0, 1.0, 0.3)
    if st.button("🗑️ 清空对话"):
        st.session_state.messages = []
        st.session_state.perf_stats = []
        st.rerun()

# 4. 主界面标题
st.title("🤖 DeepSeek 智能代码助手")
st.caption("基于 DeepSeek API 构建 | 支持代码生成、解释与优化")

# 5. 初始化聊天历史
if "messages" not in st.session_state:
    st.session_state.messages = []

# 6. 显示历史消息
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 7. 处理用户输入
if prompt := st.chat_input("请输入代码问题（例如：用Python写一个快速排序）..."):
    # 显示用户消息
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 生成 AI 回复
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # 记录开始时间
        start_time = time.time()
        
        try:
            # 调用 API (流式输出)
            stream = client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                temperature=temperature,
                stream=True
            )
            
            # 模拟打字机效果
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            
            # 完成输出
            message_placeholder.markdown(full_response)
            
            # 记录性能数据
            end_time = time.time()
            duration = round(end_time - start_time, 2)
            
            # 注意：流式模式下，usage 信息通常在最后一个 chunk 或单独获取
            # 这里为了演示简单，我们估算或记录基础信息
            # 实际生产中可以解析最后一个 chunk 的 usage 字段
            
            perf_data = {
                "time": time.strftime("%H:%M:%S"),
                "duration": duration,
                "tokens": "N/A (流式)", 
                "prompt_tokens": "-",
                "completion_tokens": "-"
            }
            st.session_state.perf_stats.append(perf_data)
            
            # 保存 AI 回复到历史
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"API 调用失败: {str(e)}")
