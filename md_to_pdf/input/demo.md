# 📘 測試文件範例

這是一份用於測試 **Markdown to PDF** 轉換系統的範例文件。

---

## 📋 目錄

1. 文字格式測試
2. 清單測試
3. 表格測試
4. 程式碼區塊測試
5. 圖片與連結測試

---

## ✨ 1. 文字格式測試

### 基本格式

這是 **粗體文字**，這是 *斜體文字*，這是 ***粗斜體***。

這是 `行內程式碼`，用於標示變數或指令。

> 這是引用區塊（blockquote）。
> 
> 可以用來強調重要資訊或引述他人話語。

### 中英混排測試

LSAP 是 **Low-latency Streaming Audio Platform** 的縮寫，專為即時音訊處理設計。

支援 UTF-8 編碼，能正確顯示中文、English、日本語、한국어。

---

## 📝 2. 清單測試

### 無序清單

- 項目一
- 項目二
  - 子項目 2.1
  - 子項目 2.2
    - 子子項目 2.2.1
- 項目三

### 有序清單

1. 第一步：安裝相依套件
2. 第二步：設定環境變數
3. 第三步：執行轉換腳本
   1. 準備 Markdown 檔案
   2. 執行 `python convert.py`
   3. 檢查 output 目錄

### 任務清單

- [x] 完成專案架構
- [x] 實作轉換邏輯
- [ ] 加入自動化測試
- [ ] 撰寫使用文件

---

## 📊 3. 表格測試

### 基本表格

| 功能       | 描述                | 狀態   |
| -------- | ----------------- | ---- |
| Markdown | 支援標準 Markdown 語法  | ✅ 完成 |
| CSS 樣式  | 自訂排版樣式            | ✅ 完成 |
| PDF 輸出  | 穩定不跑版的 PDF 生成     | ✅ 完成 |
| 批次轉換     | 一次處理多個檔案          | ✅ 完成 |

### 複雜表格

| 程式語言       | 框架 / 工具                | 用途           | 難度   |
| ---------- | ---------------------- | ------------ | ---- |
| Python     | Markdown, pdfkit       | 文件轉換         | ⭐⭐   |
| JavaScript | Node.js, Puppeteer     | 網頁自動化        | ⭐⭐⭐  |
| CSS        | Flexbox, Grid          | 版面設計         | ⭐⭐   |
| Bash       | Shell Script           | 自動化部署        | ⭐⭐⭐⭐ |

---

## 💻 4. 程式碼區塊測試

### Python 程式碼

```python
# Markdown to PDF 轉換範例
import markdown
import pdfkit

def convert_md_to_pdf(input_file, output_file):
    """將 Markdown 轉換為 PDF"""
    with open(input_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    html = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])
    pdfkit.from_string(html, output_file)
    print(f"✅ 轉換完成：{output_file}")

# 執行轉換
convert_md_to_pdf('input.md', 'output.pdf')
```

### JavaScript 程式碼

```javascript
// 簡單的 Markdown 解析器
function parseMarkdown(text) {
  return text
    .replace(/^### (.*$)/gim, '<h3>$1</h3>')
    .replace(/^## (.*$)/gim, '<h2>$1</h2>')
    .replace(/^# (.*$)/gim, '<h1>$1</h1>')
    .replace(/\*\*(.*)\*\*/gim, '<strong>$1</strong>')
    .replace(/\*(.*)\*/gim, '<em>$1</em>');
}

console.log(parseMarkdown('# Hello **World**'));
```

### Shell 指令

```bash
# 批次轉換所有 Markdown 檔案
for file in input/*.md; do
    python scripts/convert.py -i "$file"
done

echo "✅ 批次轉換完成！"
```

### JSON 設定檔

```json
{
  "page_size": "A4",
  "margin_top": "25mm",
  "encoding": "UTF-8",
  "markdown_extensions": [
    "tables",
    "fenced_code",
    "codehilite"
  ]
}
```

---

## 🔗 5. 圖片與連結測試

### 外部連結

- [GitHub](https://github.com)
- [Markdown 語法說明](https://markdown.tw)
- [wkhtmltopdf 官網](https://wkhtmltopdf.org)

### 圖片 (若有圖片檔案)

如果有圖片，可以這樣插入：

```markdown
![替代文字](path/to/image.png)
```

---

## 📌 6. 特殊格式測試

### 分隔線

上方有一條分隔線。

---

下方也有一條分隔線。

### 跳脫字元

使用反斜線可以跳脫特殊字元：\*這不是斜體\*

### 行內 HTML

這是 <span style="color: red; font-weight: bold;">紅色粗體文字</span>。

---

## ✅ 結論

這份測試文件涵蓋了常見的 Markdown 語法，包括：

- ✨ 文字格式 (粗體、斜體、程式碼)
- 📝 清單 (有序、無序、任務清單)
- 📊 表格 (簡單與複雜)
- 💻 程式碼區塊 (多語言語法高亮)
- 🔗 連結與圖片
- 📌 特殊格式

透過此系統轉換的 PDF 應該能保持穩定的排版，不會因編輯器或環境不同而跑版！

---

**生成時間**：2025-11-12  
**專案**：LSAP - Markdown to PDF Converter  
**版本**：v1.0
