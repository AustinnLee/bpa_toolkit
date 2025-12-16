import sys
from pathlib import Path
import streamlit as st
import time
import os
from dotenv import load_dotenv

# === 路径魔法 (所有页面都要加，为了能找到 src.xxx) ===
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))
# === 2. 加载环境变量 ===
# load_dotenv 会自动寻找根目录下的 .env 文件
# 把它放在路径修复之后，确保能找到
load_dotenv(ROOT_DIR / ".env")

# 从环境变量获取密码
# 如果没找到，给个默认值（开发环境兜底）
VALID_USER = os.getenv("ADMIN_USER", "admin")
VALID_PASS = os.getenv("ADMIN_PASSWORD", "default_pass")

# === 页面配置 ===
# 注意：set_page_config 必须是每个页面执行的第一条 Streamlit 命令
st.set_page_config(page_title="BPA Home", page_icon="🏠", layout="wide")

# === Session State 初始化 ===
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False


# === 登录页逻辑 ===
def login_page():
    st.title("🔐 BPA Enterprise System")
    st.markdown("### 请登录以访问敏感数据")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if username == VALID_USER and password == VALID_PASS:
                st.success("验证成功！正在跳转...")
                st.session_state["logged_in"] = True
                time.sleep(0.5)
                st.rerun()
            else:
                st.error("用户名或密码错误")


# === 主页逻辑 ===
def home_page():
    st.title("🏠 欢迎使用 BPA Toolkit")

    # 侧边栏登出
    with st.sidebar:
        st.write("User: **Admin**")
        if st.button("🚪 Logout"):
            st.session_state["logged_in"] = False
            st.rerun()

    st.info("请从左侧侧边栏选择功能模块。")
    st.markdown(
        """
    ### 系统概览
    - **🏭 Data Factory**: 通用数据清洗 ETL。
    - **🤖 Reconciliation**: 财务对账机器人。
    - **📈 Analytics**: 销售数据可视化大屏。
    """
    )

    # 搞点 KPI 撑场面
    c1, c2, c3 = st.columns(3)
    c1.metric("Server Status", "Online", "🟢")
    c2.metric("API Latency", "45ms", "-12ms")
    c3.metric("Processed Jobs", "1,024", "+5")


# === 路由控制 ===
if not st.session_state["logged_in"]:
    login_page()
else:
    home_page()
