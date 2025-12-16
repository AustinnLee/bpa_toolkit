import sys
from pathlib import Path
import streamlit as st
import pandas as pd

# === 路径魔法 ===
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from src.services.charts import SalesChartFactory
from src.config import PROCESSED_DIR

st.set_page_config(page_title="Analytics", page_icon="📈", layout="wide")

if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("请先在首页登录！")
    st.stop()

st.header("📈 销售数据分析")
data_path = PROCESSED_DIR / "clean_bba_sales.csv"

if data_path.exists():
    df = pd.read_csv(data_path)
    factory = SalesChartFactory(df)

    st.plotly_chart(factory.create_region_bar_chart(), width="stretch")
    st.plotly_chart(factory.create_daily_trend_chart(), width="stretch")
else:
    st.error("数据未找到，请先进行清洗。")
