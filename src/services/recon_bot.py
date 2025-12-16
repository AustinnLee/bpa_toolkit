from datetime import datetime

import pandas as pd

from src.config import RECON_DATA_DIR


class ReconBot:
    def __init__(self):
        # 使用 config.py 里配置好的绝对路径
        self.data_dir = RECON_DATA_DIR
        self.df_erp = None
        self.df_bank = None
        self.df_result = None

    def load_data(self):
        print("📥 [Bot] Loading ledgers...")

        # 拼接文件路径
        erp_path = self.data_dir / "ERP_Records.csv"
        bank_path = self.data_dir / "Bank_Statement.csv"

        # 检查文件是否存在，不存在提示先运行生成脚本
        if not erp_path.exists() or not bank_path.exists():
            raise FileNotFoundError(
                f"Missing data files in {self.data_dir}. Please run 'Generate Reconciliation Mock Data' first."
            )

        # 读取数据
        self.df_erp = pd.read_csv(erp_path)
        self.df_bank = pd.read_csv(bank_path)

        # 预处理：统一关键列名 (Key Mapping)
        # 把银行的 Transaction_Ref 改名为 Order_ID，方便后续对比
        self.df_bank = self.df_bank.rename(
            columns={"Transaction_Ref": "Order_ID", "In_Amount": "Bank_Amount"}
        )

        # 把 ERP 的 Amount 改名
        self.df_erp = self.df_erp.rename(columns={"Amount_CNY": "ERP_Amount"})

        # 确保 ID 都是字符串，防止 "001" 变成 1
        self.df_erp["Order_ID"] = self.df_erp["Order_ID"].astype(str)
        self.df_bank["Order_ID"] = self.df_bank["Order_ID"].astype(str)

        return self

    def reconcile(self):
        print("⚙️ [Bot] Reconciling transactions...")

        # --- 核心逻辑：Outer Join ---
        # indicator=True 会生成一个 '_merge' 列
        self.df_result = pd.merge(
            self.df_erp, self.df_bank, on="Order_ID", how="outer", indicator=True
        )

        # 计算金额差异 (Diff)
        self.df_result["ERP_Amount"] = self.df_result["ERP_Amount"].fillna(0)
        self.df_result["Bank_Amount"] = self.df_result["Bank_Amount"].fillna(0)

        self.df_result["Diff"] = (
            self.df_result["Bank_Amount"] - self.df_result["ERP_Amount"]
        )

        # 打标签：Status
        def tag_status(row):
            if row["_merge"] == "left_only":
                return "❌ Missing in Bank (漏收款)"
            elif row["_merge"] == "right_only":
                return "❓ Unknown Income (不明入账)"
            elif row["Diff"] != 0:
                return "⚠️ Amount Mismatch (金额不符)"
            else:
                return "✅ Matched (对平)"

        self.df_result["Status"] = self.df_result.apply(tag_status, axis=1)

        return self

    def generate_report(self):
        print("📊 [Bot] Generating Excel report...")

        # 生成带时间戳的文件名
        output_path = (
            self.data_dir / f"Recon_Report_{datetime.now().strftime('%Y%m%d')}.xlsx"
        )

        # 使用 ExcelWriter 可以在同一个文件里写多个 Sheet
        with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
            # Sheet 1: 汇总摘要
            summary = self.df_result["Status"].value_counts().to_frame("Count")
            summary.to_excel(writer, sheet_name="Summary")

            # Sheet 2: 异常明细 (只看有问题的)
            exceptions = self.df_result[self.df_result["Status"] != "✅ Matched (对平)"]
            exceptions.to_excel(writer, sheet_name="Exceptions", index=False)

            # Sheet 3: 全量数据
            self.df_result.to_excel(writer, sheet_name="Full_Data", index=False)

        print(f"✅ Report saved to: {output_path}")
        print("\n--- Summary ---")
        print(summary)


# 封装成函数，供 main.py 调用
def run_recon_bot():
    print("🤖 [Service] Starting Reconciliation Bot...")
    try:
        bot = ReconBot()
        (bot.load_data().reconcile().generate_report())
    except Exception as e:
        print(f"❌ Error during reconciliation: {e}")


if __name__ == "__main__":
    run_recon_bot()
