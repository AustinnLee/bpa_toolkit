import sys
from pathlib import Path
import streamlit as st
import pandas as pd
import requests

# === 路径修复魔法 ===
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from src.services.charts import SalesChartFactory
from src.config import PROCESSED_DIR

# === 页面配置 ===
st.set_page_config(page_title="Analytics", page_icon="📈", layout="wide")

# === 权限检查 ===
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("🔒 Access Denied. Please login at the Home page first.")
    st.stop()

# === 缓存函数定义 (Performance Optimization) ===


@st.cache_data(ttl=3600, show_spinner="正在加载清洗后的数据...")
def load_sales_data(file_path):
    """
    读取清洗后的 CSV 数据。
    缓存机制：只要 file_path 没变，1小时内直接返回内存结果，不读硬盘。
    """
    # 可以在这里打印日志，观察缓存是否生效
    # print(">>> [Cache Miss] Loading data from disk...")
    return pd.read_csv(file_path)


@st.cache_data(ttl=3600)
def fetch_live_rates(base="USD"):
    """
    获取实时汇率 (API)。
    缓存机制：1小时内只请求一次外部 API，节省流量并提速。
    """
    try:
        url = f"https://api.exchangerate-api.com/v4/latest/{base}"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.json().get("rates", {})
    except Exception:
        return {}
    return {}


# === 页面核心逻辑 ===
st.header("📈 销售数据分析与洞察")

# 1. 尝试加载数据
data_path = PROCESSED_DIR / "clean_bba_sales.csv"

if data_path.exists():
    # 使用缓存函数读取
    df = load_sales_data(data_path)

    # 获取实时汇率 (用于 KPI 展示)
    rates = fetch_live_rates()
    cny_rate = rates.get("CNY", 7.2)  # 默认兜底 7.2

    # --- KPI 概览区域 ---
    st.subheader("核心指标 (Key Metrics)")
    col1, col2, col3 = st.columns(3)

    total_sales = df["sales"].sum()
    total_calls = df["calls"].sum()
    avg_order = df["sales"].mean()

    col1.metric("总销售额 (USD)", f"${total_sales:,.0f}")
    col2.metric("折合人民币 (CNY)", f"¥{total_sales * cny_rate:,.0f}")
    col3.metric("总通话次数", f"{total_calls:,.0f}")

    st.divider()

    # --- 图表区域 ---
    # 实例化工厂
    factory = SalesChartFactory(df)

    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.subheader("1. 区域业绩分布")
        st.plotly_chart(factory.create_region_bar_chart(), width="stretch")

    with col_chart2:
        st.subheader("2. 每日销售趋势")
        st.plotly_chart(factory.create_daily_trend_chart(), width="stretch")

    st.subheader("3. 团队表现")
    st.plotly_chart(factory.create_salesperson_pie_chart(), width="stretch")

else:
    st.error("❌ 数据未找到")
    st.info("请先前往 '🏭 Data Factory' 页面上传并清洗数据，或运行生成脚本。")
