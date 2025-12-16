import sys
from pathlib import Path

import pandas as pd

sys.path.append(str(Path(__file__).resolve().parent.parent))
# 引入配置里的路径
from src.config import RECON_DATA_DIR


def create_mock_files():
    print(f"--- Generating Mock Data in: {RECON_DATA_DIR} ---")

    # 1. 公司内部账 (ERP)
    erp_data = {
        "Order_ID": [
            "ORD-001",
            "ORD-002",
            "ORD-003",
            "ORD-004",
            "ORD-005",
            "ORD-006",
            "ORD-007",
            "ORD-008",
            "ORD-009",
            "ORD-010",
        ],
        "Date": ["2024-01-01"] * 10,
        "Amount_CNY": [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000],
        "Client": [
            "Client A",
            "Client B",
            "Client C",
            "Client D",
            "Client E",
            "Client F",
            "Client G",
            "Client H",
            "Client I",
            "Client J",
        ],
    }

    # 2. 银行流水 (Bank)
    bank_data = {
        "Transaction_Ref": [
            "ORD-001",
            "ORD-002",
            "ORD-004",
            "ORD-005",
            "ORD-006",
            "ORD-007",
            "ORD-008",
            "ORD-010",
        ],
        "Txn_Date": ["2024-01-01"] * 8,
        "In_Amount": [100, 200, 400, 480, 600, 700, 800, 1000],
    }

    # 保存文件
    pd.DataFrame(erp_data).to_csv(RECON_DATA_DIR / "ERP_Records.csv", index=False)
    pd.DataFrame(bank_data).to_csv(RECON_DATA_DIR / "Bank_Statement.csv", index=False)

    print("✅ Mock files created successfully.")


if __name__ == "__main__":
    create_mock_files()
