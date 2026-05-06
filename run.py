import os
import sys
import subprocess
import socket
import time
import platform
from pathlib import Path

def check_port(port):
    """检查端口是否可用"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            return s.connect_ex(('localhost', port)) != 0
    except Exception as e:
        print(f"端口检查错误: {e}")
        return False

def find_available_port(start_port=8501, max_attempts=5):
    """查找可用端口"""
    for port in range(start_port, start_port + max_attempts):
        if check_port(port):
            return port
    return None

def validate_environment():
    """验证环境配置"""
    # 检查API密钥
    api_key = os.getenv('DEEPSEEK_API_KEY')
    if not api_key:
        env_file = Path('.env')
        if env_file.exists():
            try:
                with open(env_file, 'r') as f:
                    for line in f:
                        if line.strip() and not line.startswith('#'):
                            key, value = line.strip().split('=', 1)
                            if key.strip() == 'DEEPSEEK_API_KEY':
                                api_key = value.strip()
                                break
            except Exception as e:
                print(f"读取.env文件错误: {e}")
    
    if not api_key:
        print("❌ 错误：未配置DEEPSEEK_API_KEY")
        print("   请通过以下任一方式配置：")
        print("   1. 创建.env文件，内容：DEEPSEEK_API_KEY=your_api_key_here")
        print("   2. 设置环境变量：export DEEPSEEK_API_KEY=your_api_key_here")
        return False
    
    # 检查main.py是否存在
    if not Path('main.py').exists():
        print("❌ 错误：找不到main.py文件")
        return False
    
    return True

def get_system_info():
    """获取系统信息"""
    return {
        'platform': platform.platform(),
        'python_version': sys.version.split()[0],
        'cpu_count': os.cpu_count() or 1,
        'memory': '未知'
    }

def start_streamlit(port):
    """启动Streamlit应用"""
    cmd = [
        sys.executable, '-m', 'streamlit', 'run', 'main.py',
        f'--server.port={port}',
        '--server.address=0.0.0.0',
        '--browser.gatherUsageStats=false'
    ]
    
    print(f"🚀 启动代码助手 - 端口: {port}")
    print(f"🔗 访问地址: http://localhost:{port}")
    print("🔄 正在启动应用，请稍候...")
    
    try:
        # 使用Popen以便实时显示输出
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        
        # 监控启动过程
        start_time = time.time()
        timeout = 30  # 30秒超时
        
        while True:
            output = process.stdout.readline()
            if output:
                print(output.strip())
                
                # 检测Streamlit成功启动
                if "You can now view your Streamlit app in your browser" in output:
                    print(f"✅ 应用启动成功! (耗时: {time.time() - start_time:.1f}秒)")
                    print(f"🌐 打开浏览器访问: http://localhost:{port}")
                    break
            
            # 检查超时
            if time.time() - start_time > timeout:
                print("❌ 启动超时，请检查错误信息")
                process.terminate()
                return False
            
            # 检查进程是否结束
            if process.poll() is not None:
                print("❌ 应用启动失败")
                return False
        
        # 保持进程运行
        process.wait()
        return True
    
    except KeyboardInterrupt:
        print("\n✋ 正在停止应用...")
        return False
    except Exception as e:
        print(f"❌ 启动错误: {e}")
        return False

def main():
    """主函数"""
    print("🤖 DeepSeek 代码助手启动器")
    print("=" * 50)
    
    # 获取系统信息
    sys_info = get_system_info()
    print(f"💻 系统: {sys_info['platform']}")
    print(f"🐍 Python版本: {sys_info['python_version']}")
    print(f"⚙️  CPU核心数: {sys_info['cpu_count']}")
    
    # 验证环境
    if not validate_environment():
        sys.exit(1)
    
    # 查找可用端口
    port = find_available_port()
    if not port:
        print("❌ 错误：找不到可用端口 (8501-8505)")
        print("   请关闭占用这些端口的应用，或手动指定端口:")
        print("   streamlit run main.py --server.port=9000")
        sys.exit(1)
    
    # 启动应用
    success = start_streamlit(port)
    
    if not success:
        print("❌ 应用启动失败，请检查错误信息")
        sys.exit(1)

if __name__ == "__main__":
    main()