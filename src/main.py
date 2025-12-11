import sys
import pandas as pd
import numpy as np

def main():
    print("--------------------------------------------------")
    print("   BPA TOOLKIT - ENTERPRISE CONTAINER STARTUP     ")
    print("--------------------------------------------------")

    # 1. 环境自检
    print(f"[System] Python Version: {sys.version.split()[0]}")
    print(f"[System] Pandas Version: {pd.__version__}")

    # 2. 模拟业务逻辑
    print("[Task] Initializing Data Processing...")
    df = pd.DataFrame({
        "status": ["active", "active", "pending"],
        "value": [100, 200, 50]
    })

    summary = df.groupby("status")["value"].sum()
    print("\n[Result] Business Logic Executed Successfully:")
    print(summary)

    print("\n--------------------------------------------------")
    print("   CONTAINER SHUTDOWN GRACEFULLY                  ")
    print("--------------------------------------------------")

if __name__ == "__main__":
    main()
