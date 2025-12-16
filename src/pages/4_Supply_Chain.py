import sys
from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.express as px

# === 1. 路径修复 ===
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from src.core.grid_builder import InteractiveTable
from src.config import RAW_DIR

# === 2. 页面配置 ===
st.set_page_config(page_title="Supply Chain Command", page_icon="🚛", layout="wide")

# === 3. 权限检查 ===
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("🔒 Please login first.")
    st.stop()


# === 4. 数据加载函数 (带缓存) ===
@st.cache_data
def load_inventory():
    path = RAW_DIR / "inventory_mock.csv"
    if not path.exists():
        return None
    df = pd.read_csv(path)
    return df


# === 5. 核心页面逻辑 ===
st.title("🚛 供应链指挥舱 (Supply Chain Dashboard)")

df = load_inventory()

if df is None:
    st.error("库存数据缺失！请先运行 `scripts/gen_inventory_data.py` 生成数据。")
else:
    # --- KPI 区域 ---
    # 计算核心指标
    total_cars = len(df)
    total_value = df["Cost_Price"].sum()

    # 滞销定义：库龄 > 90 天
    aging_threshold = 90
    aging_cars = df[df["Days_In_Stock"] > aging_threshold]
    aging_count = len(aging_cars)
    aging_value = aging_cars["Cost_Price"].sum()

    # 布局
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("总库存量", f"{total_cars} 台", delta="稳定")
    col2.metric("库存总值 (Cost)", f"${total_value/10000:.2f} 万")

    # 红色预警指标
    col3.metric(
        "⚠️ 滞销车辆 (>90天)",
        f"{aging_count} 台",
        delta=f"-{aging_count}",
        delta_color="inverse",
    )
    col4.metric("滞销资金占用", f"${aging_value/10000:.2f} 万", delta_color="inverse")

    st.divider()

    # --- 图表分析区域 ---
    c1, c2 = st.columns([2, 1])

    with c1:
        st.subheader("📊 库存车龄分布 (Inventory Age Structure)")
        # 直方图：看库存主要集中在哪个时间段
        fig_hist = px.histogram(
            df,
            x="Days_In_Stock",
            nbins=20,
            color="Model",
            title="Distribution of Days in Stock",
        )
        # 加上一条 90 天的警戒线
        fig_hist.add_vline(
            x=aging_threshold,
            line_width=3,
            line_dash="dash",
            line_color="red",
            annotation_text="90 Days Alert",
        )
        st.plotly_chart(fig_hist, use_container_width=True)

    with c2:
        st.subheader("🚗 车型库存占比")
        fig_pie = px.pie(df, names="Model", values="Cost_Price", hole=0.5)
        st.plotly_chart(fig_pie, use_container_width=True)

    # --- 交互式明细表 (Action Area) ---
    st.subheader("📝 库存明细操作台")
    st.info("💡 滞销车辆已自动标记为红色。请勾选车辆并导出处理清单。")

    # 使用 Ag-Grid 展示
    # 高级技巧：我们可以在这里配置 Cell Style，但这需要写 JS (gridOptions)，略复杂。
    # 这里我们先用 Pandas Style 或者简单的排序把滞销车排在前面。

    # 按库龄降序排列，让滞销车排在最前面
    df_sorted = df.sort_values("Days_In_Stock", ascending=False)

    table = InteractiveTable(df_sorted)
    # 偷懒做法：我们直接用之前封装好的 builder
    # 如果想做红底高亮，需要在 grid_builder.py 里改 configure_grid_options 的 jscode，这属于进阶内容。
    # 今天的重点是数据流。

    response = table.show(key_prefix="inventory_grid")

    selected = response.get("selected_rows")
    if selected is None:
        selected = []

    if len(selected) > 0:
        st.error(f"已选中 {len(selected)} 台车辆进行处理")

        # 模拟一个“一键促销”按钮
        if st.button("💸 生成促销方案 (Generate Promo)"):
            df_promo = pd.DataFrame(selected)
            # 简单的逻辑：滞销车打 9 折
            df_promo["Promo_Price"] = df_promo["Cost_Price"] * 0.9

            st.write("促销清单预览：")
            st.dataframe(
                df_promo[["VIN", "Model", "Days_In_Stock", "Cost_Price", "Promo_Price"]]
            )

            csv = df_promo.to_csv(index=False).encode("utf-8")
            st.download_button("📥 下载促销清单", csv, "promo_list.csv", "text/csv")
