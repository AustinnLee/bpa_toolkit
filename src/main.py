import sys
from pathlib import Path

# 添加根目录到路径
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

# 引入所有模块
from scripts.gen_dirty_data import generate_chaos
from scripts.gen_mock_recon import create_mock_files
from src.services.bba_etl import run_bba_sales_etl
from src.services.recon_bot import run_recon_bot

# 如果 api_client 里你也封装了 run_exchange_demo，也可以引进来


def main():
    while True:
        print("\n=== BPA Toolkit Master Control ===")
        print("--- Scripts (生成数据) ---")
        print("1. Generate Dirty Sales Data")
        print("2. Generate Reconciliation Mock Data")
        print("--- Services (业务逻辑) ---")
        print("3. Run BBA Sales ETL (Cleaning)")
        print("4. Run Reconciliation Bot (Accounting)")
        print("q. Quit")

        choice = input("\nSelect Action: ")

        if choice == "1":
            generate_chaos()
        elif choice == "2":
            create_mock_files()
        elif choice == "3":
            run_bba_sales_etl()
        elif choice == "4":
            run_recon_bot()
        elif choice.lower() == "q":
            print("Bye!")
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()
