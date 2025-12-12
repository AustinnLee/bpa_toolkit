// === 1. 变量声明 ===
// Python: name = "BBA"
const clientName = "BBA";    // 常量 (推荐)
let orderCount = 100;        // 变量 (相当于 Python 变量)
// var 已经过时了，别用。

// === 2. 打印输出 ===
// Python: print(f"Client: {name}")
console.log(`Client: ${clientName}, Orders: ${orderCount}`); // 注意用反引号 `

// === 3. 列表与字典 (Array & Object) ===
// Python: data = {"id": 1, "list": [10, 20]}
const data = {
    id: 1,
    list: [10, 20],
    isActive: true // Python 是 True (大写)，JS 是 true (小写)
};

// === 4. 循环 (Loop) ===
// Python: for item in data["list"]:
for (const item of data.list) {
    console.log("Item:", item);
}

// === 5. 核心：处理 JSON (自动化最常用的) ===
// 模拟从 API 拿到的数据 (Array of Objects)
const orders = [
    { id: 101, amount: 500, status: "paid" },
    { id: 102, amount: 300, status: "pending" },
    { id: 103, amount: 700, status: "paid" }
];

// Python: [o for o in orders if o["status"] == "paid"]
// JS: .filter()
const paidOrders = orders.filter(order => order.status === "paid");

// Python: [o["amount"] * 1.1 for o in orders]
// JS: .map()
const taxedAmounts = orders.map(order => order.amount * 1.1);

console.log("Paid Orders:", paidOrders);
console.log("Taxed Amounts:", taxedAmounts);

// === 实战作业 ===
const rawInput = [
    { name: "John", contact: "JOHN@bba.com" },
    { name: "Mike", contact: null }, // 有脏数据
    { name: "Sara", contact: "Sara@Audi.de" }
];

// 任务：提取有效邮箱，转小写，存入新数组
// 1. 过滤掉 null
// 2. 提取 contact 字段
// 3. 转小写

const cleanEmails = rawInput
    .filter(item => item.contact !== null)  // 过滤
    .map(item => item.contact.toLowerCase()); // 转换

console.log("Clean Emails:", cleanEmails);