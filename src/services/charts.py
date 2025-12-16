import pandas as pd
import plotly.express as px


class SalesChartFactory:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def create_region_bar_chart(self):
        # 注意：这里全是小写 region, sales
        region_sales = self.df.groupby("region")["sales"].sum().reset_index()

        fig = px.bar(
            region_sales,
            x="region",
            y="sales",
            color="region",
            text_auto=".2s",
            title="Total Revenue by Region",
        )
        # hovertemplate 里的变量名也要对应 x, y
        fig.update_traces(hovertemplate="Region: %{x}<br>Sales: $%{y:,.0f}")
        return fig

    def create_daily_trend_chart(self):

        # === 修复开始 ===
        # 1. 强制转换日期，错误的变成 NaT (coerce)
        self.df["date"] = pd.to_datetime(self.df["date"], errors="coerce")

        # 2. 只有日期合法的行才保留，把 "Invalid" 那一行删掉
        # 注意：这里我们创建一个临时 df_clean 用于画图，不影响 self.df 原数据
        df_clean = self.df.dropna(subset=["date"]).copy()
        # === 修复结束 ===

        # 后面用 df_clean 画图，而不是 self.df
        daily_sales = df_clean.groupby("date")["sales"].sum().reset_index()

        fig = px.line(
            daily_sales, x="date", y="sales", markers=True, title="Daily Sales Trend"
        )
        fig.update_layout(xaxis=dict(rangeslider=dict(visible=True)))
        return fig

    def create_salesperson_pie_chart(self):
        # 注意：salesperson, sales
        fig = px.pie(
            self.df,
            names="salesperson",
            values="sales",
            hole=0.4,
            title="Sales Share by Person",
        )
        return fig
