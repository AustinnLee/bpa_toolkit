from pathlib import Path

import pandas as pd


def create_mock_files():
    root = Path(__file__).resolve().parent.parent / "data" / "reconciliation"
    root.mkdir(parents=True, exist_ok=True)

    # 1. 公司内部账 (ERP) - 10 笔交易
    # 注意：列名是内部叫法
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

    # 2. 银行流水 (Bank) - 只有 8 笔，且有一笔金额不一致
    # 场景：ORD-003 丢单了（漏收款），ORD-009 丢单了。
    # 场景：ORD-005 金额只有 480 (可能是扣了手续费)。
    # 注意：列名完全不同，且没有 Client 名字
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
        "In_Amount": [100, 200, 400, 480, 600, 700, 800, 1000],  # ORD-005 少了20块
    }

    pd.DataFrame(erp_data).to_csv(root / "ERP_Records.csv", index=False)
    pd.DataFrame(bank_data).to_csv(root / "Bank_Statement.csv", index=False)

    print(f"✅ Created mock files in {root}")


if __name__ == "__main__":
    create_mock_files()
