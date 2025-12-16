import sys
from pathlib import Path
import streamlit as st
import pandas as pd

# === 路径魔法 ===
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from src.services.recon_bot import ReconBot

st.set_page_config(page_title="Recon Bot", page_icon="🤖", layout="wide")

if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("请先在首页登录！")
    st.stop()

st.header("🤖 自动对账机器人")

if st.button("🚀 开始对账"):
    try:
        bot = ReconBot()
        bot.load_data().reconcile()
        st.success("✅ 对账完成！")

        # 展示异常
        exceptions = bot.df_result[bot.df_result["Status"] != "✅ Matched (对平)"]
        st.dataframe(exceptions, width="stretch")
    except Exception as e:
        st.error(f"Error: {e}")
