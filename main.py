import streamlit as st
import time
from openai import OpenAI
import os
import json
from dotenv import load_dotenv

# --- 1. 加载.env 
load_dotenv()

# --- 2. 初始化日志系统 ---
LOG_FILE = "performance_log.json"

def load_logs():
    """从本地文件加载历史日志"""
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def save_log(entry):
    """将新日志追加到本地文件"""
    # 读取现有日志
    logs = load_logs()
    # 追加新数据
    logs.append(entry)
    # 写回文件
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, ensure_ascii=False, indent=4)

# 在程序启动时加载历史数据到 Session State
if "perf_logs" not in st.session_state:
    st.session_state.perf_logs = load_logs()

# --- 3. 页面配置 ---
st.set_page_config(
    page_title="DeepSeek 代码助手",
    page_icon="🤖",
    layout="wide"
)

# --- 4. 侧边栏：性能监控 ---
with st.sidebar:
    st.title("📊 性能监控")

    st.markdown("### ⚙️ 设置")
    temperature = st.slider("Temperature", 0.0, 1.0, 0.3)
    
    if st.button("🗑️ 清空对话与日志"):
        st.session_state.messages = []
        st.session_state.perf_stats = []
        st.rerun()
        # 同时清空本地文件
        if os.path.exists(LOG_FILE):
            os.remove(LOG_FILE)
        st.rerun()

    st.divider()

    # 显示历史性能记录
    st.markdown("### 📜 历史性能记录")
    if st.session_state.perf_logs:
        # 倒序显示，最新的在最上面
        for log in reversed(st.session_state.perf_logs):
            with st.expander(f"🕒 {log['time']} ({log['total_cost_s']}s)"):
                st.write(f"**提问**: {log['user_query'][:30]}...")
                st.write(f"- 首字延迟: {log['first_token_delay_s']}s")
                st.write(f"- 总耗时: {log['total_cost_s']}s")
                st.write(f"- 模型: {log['model']}")
    else:
        st.info("暂无历史记录")

# --- 5. 主界面与 API 初始化 ---
st.title("🤖 DeepSeek 智能代码助手")
st.caption("基于 DeepSeek API 构建")

# 1. 从 .env 读取 Key
api_key = os.getenv("DEEPSEEK_API_KEY")

if not api_key:
    st.error("🔑 严重错误：未找到 API Key！")
    st.stop()


# 2. 初始化客户端
client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com/v1"
)

# --- 6. 聊天逻辑 ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("请输入代码问题..."):
    # 1. 显示用户输入
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. 显示助手回复
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # ⏱️ 记录开始时间
        request_start_time = time.time() 
        first_token_time = None

        try:
            stream = client.chat.completions.create(
                model="deepseek-chat",
                messages=st.session_state.messages,
                stream=True,
                temperature=temperature 
            )
            
            # 逐字显示回复
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    # 记录第一个字生成的时间点
                    if first_token_time is None:
                        first_token_time = time.time()
                        
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            
            # ⏱️ 记录结束时间
            total_cost = round(time.time() - request_start_time, 3)
            first_token_delay = round(first_token_time - request_start_time, 3) if first_token_time else 0.0

            # --- 7. 生成日志并保存 (新增核心逻辑) ---
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            
            # 构建日志对象 (完全对应你截图的格式)
            log_entry = {
                "time": current_time,
                "model": "deepseek-chat",
                "user_query": prompt,
                "llm_reply": full_response, # 注意：如果回复很长，日志文件会变得很大
                "first_token_delay_s": first_token_delay,
                "total_cost_s": total_cost
            }
            
            # 1. 保存到内存
            st.session_state.perf_logs.append(log_entry)
            # 2. 保存到本地文件
            save_log(log_entry)

            # 将回复存入对话历史
            st.session_state.messages.append({"role": "assistant", "content": full_response})

            # 刷新侧边栏以显示新日志
            st.rerun() 

        except Exception as e:
            st.error("🔴 API 调用失败")
            st.markdown(f"**错误详情**: {e}")
            # 错误处理：根据错误类型显示不同提示
            error_msg = str(e).lower()
            
            if "authentication" in error_msg or "401" in error_msg or "governor" in error_msg:
                st.markdown("""
                ### 🛑 认证被拦截 (Governor)
                **这通常不是代码问题，而是 Key 或网络问题：**
                
                1. **密钥错误**：请检查 `.env` 中的 Key 是否**完全复制**（没有多余的空格或换行）。
                2. **密钥失效**：请去 DeepSeek 官网重新生成一个新的 Key。
                3. **网络限制**：你所在的网络（福建福州）可能无法直接访问 api.deepseek.com。
                   * 尝试开启/关闭代理（Clash/V2Ray）。
                   * 或者在终端 `ping api.deepseek.com` 看看是否超时。
                """)
            else:
                st.markdown(f"**其他错误**: {e}")

# 保持 main guard 兼容性
if __name__ == "__main__":
    pass