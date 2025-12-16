import requests


class ExchangeRateClient:
    def __init__(self, base_currency="USD"):
        self.base_currency = base_currency
        self.api_url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
        self.rates = {}  # 这是一个缓存，存我们拿到的数据

    def fetch_rates(self):
        """核心：发送 GET 请求获取数据"""
        print(f"📡 [API] Connecting to: {self.api_url} ...")

        try:
            # 1. 发起请求
            response = requests.get(self.api_url)

            # 2. 检查状态码 (200 OK)
            if response.status_code == 200:
                print("✅ [API] Connection Success!")

                # 3. 解析 JSON (把 HTTP 响应变成 Python 字典)
                data = response.json()

                # data 的结构通常是: {"date": "2024-01-01", "rates": {"EUR": 0.92, ...}}
                self.rates = data.get("rates", {})
                update_date = data.get("date")
                print(f"📊 [Data] Rates updated on: {update_date}")
                print(f"   1 USD = {self.rates.get('EUR')} EUR")
                print(f"   1 USD = {self.rates.get('CNY')} CNY")

            else:
                print(f"❌ [Error] Server returned: {response.status_code}")

        except Exception as e:
            print(f"❌ [Error] Request failed: {e}")

        return self

    def convert_currency(self, amount, from_currency):
        """
        业务逻辑：将任意货币转为 USD
        公式：USD_Amount = Amount / Rate_of_Source_Currency
        (例如：1 USD = 7.2 CNY。那 720 CNY 就是 720 / 7.2 = 100 USD)
        """
        if not self.rates:
            print("⚠️ Rates not loaded. Fetching now...")
            self.fetch_rates()

        rate = self.rates.get(from_currency)

        if not rate:
            print(f"⚠️ Currency '{from_currency}' not found!")
            return None

        return round(amount / rate, 2)


if __name__ == "__main__":
    # 1. 初始化客户端
    client = ExchangeRateClient(base_currency="USD")

    # 2. 获取实时汇率
    client.fetch_rates()

    # 3. 模拟业务场景：BBA 各国分公司的销售额
    sales_data = [
        {"region": "Germany", "currency": "EUR", "amount": 50000},
        {"region": "China", "currency": "CNY", "amount": 880000},
        {"region": "Japan", "currency": "JPY", "amount": 12000000},
        {"region": "USA", "currency": "USD", "amount": 45000},
    ]

    print("\n>>> [Finance] Converting Global Revenue to USD:")

    total_usd = 0
    for sale in sales_data:
        usd_amount = client.convert_currency(sale["amount"], sale["currency"])
        total_usd += usd_amount
        print(
            f"   {sale['region']}: {sale['amount']:,.0f} {sale['currency']} -> ${usd_amount:,.2f} USD"
        )

    print(f"-------------------------------------------")
    print(f"💰 Global Total Revenue: ${total_usd:,.2f} USD")
