# 語法高亮測試

這個文件用來測試不同程式語言的語法高亮效果。

## Python 範例

```python
# Python 程式碼範例
def calculate_fibonacci(n):
    """計算費氏數列"""
    if n <= 1:
        return n
    return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)

# 測試
for i in range(10):
    print(f"F({i}) = {calculate_fibonacci(i)}")
```

## JavaScript 範例

```javascript
// JavaScript 程式碼範例
const greet = (name) => {
    console.log(`Hello, ${name}!`);
};

class Person {
    constructor(name, age) {
        this.name = name;
        this.age = age;
    }
    
    introduce() {
        return `我是 ${this.name}，今年 ${this.age} 歲。`;
    }
}

const person = new Person('小明', 25);
greet(person.name);
```

## Bash 範例

```bash
# Bash 腳本範例
#!/bin/bash

echo "開始安裝 OpenLDAP 客戶端工具"
pacman -Sy --noconfirm openldap

# 檢查安裝結果
if [ $? -eq 0 ]; then
    echo "✅ 安裝成功！"
else
    echo "❌ 安裝失敗！"
    exit 1
fi
```

## SQL 範例

```sql
-- SQL 查詢範例
SELECT 
    u.user_id,
    u.username,
    COUNT(o.order_id) AS total_orders,
    SUM(o.amount) AS total_amount
FROM users u
LEFT JOIN orders o ON u.user_id = o.user_id
WHERE u.created_at >= '2024-01-01'
GROUP BY u.user_id, u.username
HAVING COUNT(o.order_id) > 0
ORDER BY total_amount DESC
LIMIT 10;
```

## Java 範例

```java
// Java 程式碼範例
public class HelloWorld {
    private String message;
    
    public HelloWorld(String message) {
        this.message = message;
    }
    
    public void printMessage() {
        System.out.println(this.message);
    }
    
    public static void main(String[] args) {
        HelloWorld hello = new HelloWorld("Hello, World!");
        hello.printMessage();
    }
}
```

## C++ 範例

```cpp
// C++ 程式碼範例
#include <iostream>
#include <vector>
#include <algorithm>

template<typename T>
class Stack {
private:
    std::vector<T> elements;
    
public:
    void push(const T& element) {
        elements.push_back(element);
    }
    
    T pop() {
        if (elements.empty()) {
            throw std::out_of_range("Stack is empty");
        }
        T top = elements.back();
        elements.pop_back();
        return top;
    }
    
    bool empty() const {
        return elements.empty();
    }
};

int main() {
    Stack<int> stack;
    stack.push(42);
    std::cout << "Top: " << stack.pop() << std::endl;
    return 0;
}
```

## HTML/CSS 範例

```html
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <title>語法高亮測試</title>
    <style>
        body {
            font-family: 'Noto Sans TC', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>歡迎！</h1>
        <p>這是一個測試頁面。</p>
    </div>
</body>
</html>
```

## JSON 範例

```json
{
  "name": "markdown-to-pdf",
  "version": "1.0.0",
  "description": "將 Markdown 轉換為 PDF",
  "dependencies": {
    "markdown": ">=3.5",
    "pdfkit": ">=1.0.0",
    "pygments": ">=2.15.0"
  },
  "config": {
    "page_size": "A4",
    "enable_syntax_highlighting": true
  }
}
```

## 行內程式碼測試

在文字中使用 `inline code`，例如 `print("Hello")` 或 `const x = 42;`。

---

**測試說明**：
- 每個程式碼區塊應該根據語言顯示不同的顏色
- 關鍵字、字串、註解等應該有不同的顏色
- 使用 Monokai 配色主題（深色背景）
