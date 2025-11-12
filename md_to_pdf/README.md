# 📄 LSAP - Markdown to PDF Converter

> **穩定版面**的 Markdown 轉 PDF 專案  
> 透過可控的轉換流程，確保輸出的 PDF 不會因環境或編輯器不同而跑版！

---

## ✨ 特色

- ✅ **穩定排版**：統一的 CSS 樣式控制，不受編輯器影響
- 🎨 **自訂主題**：可自由修改 `template/style.css` 調整外觀
- 📦 **批次轉換**：一次處理多個 Markdown 檔案
- 🔧 **彈性設定**：透過 `config.json` 調整頁面大小、邊界等參數
- 🌍 **中文支援**：完整支援 UTF-8 與繁體中文字型

---

## 📁 專案結構

```
LSAP/
├── input/              # 📝 放置要轉換的 Markdown 檔案
│   └── demo.md
├── output/             # 📦 轉換後的 PDF 輸出位置
├── template/           # 🎨 樣式模板
│   ├── style.css       # CSS 樣式表
│   └── template.html   # HTML 模板
├── scripts/            # ⚙️ 轉換腳本
│   └── convert.py      # 主要轉換程式
├── config.json         # 🔧 設定檔
├── requirements.txt    # 📦 Python 相依套件
└── README.md           # 📖 說明文件
```

---

## 🚀 快速開始

### 1️⃣ 安裝 wkhtmltopdf

這是轉換 HTML 為 PDF 的核心工具。

**Windows:**
```powershell
# 使用 Chocolatey
choco install wkhtmltopdf

# 或手動下載安裝
# https://wkhtmltopdf.org/downloads.html
```

**macOS:**
```bash
brew install wkhtmltopdf
```

**Linux:**
```bash
sudo apt update
sudo apt install wkhtmltopdf
```

### 2️⃣ 安裝 Python 套件

```bash
pip install -r requirements.txt
```

### 3️⃣ 轉換單一檔案

```bash
python scripts/convert.py -i input/demo.md
```

轉換後的 PDF 會儲存在 `output/demo.pdf`。

### 4️⃣ 批次轉換

```bash
python scripts/convert.py --batch
```

會將 `input/` 目錄下所有 `.md` 檔案轉換為 PDF。

---

## 📖 使用方式

### 基本指令

```bash
# 轉換單一檔案
python scripts/convert.py -i input/report.md

# 指定輸出路徑
python scripts/convert.py -i input/report.md -o output/my_report.pdf

# 自訂標題
python scripts/convert.py -i input/report.md -t "專案報告"

# 批次轉換
python scripts/convert.py --batch

# 批次轉換特定模式的檔案
python scripts/convert.py --batch --pattern "chapter_*.md"

# 使用自訂設定檔
python scripts/convert.py -i input/report.md -c my_config.json
```

### 查看完整說明

```bash
python scripts/convert.py --help
```

---

## ⚙️ 設定檔說明

編輯 `config.json` 可調整轉換參數：

```json
{
  "page_size": "A4",              // 頁面大小 (A4, Letter, Legal)
  "margin_top": "25mm",           // 上邊界
  "margin_bottom": "25mm",        // 下邊界
  "margin_left": "20mm",          // 左邊界
  "margin_right": "20mm",         // 右邊界
  "encoding": "UTF-8",            // 編碼格式
  "enable_toc": false,            // 是否啟用目錄
  "markdown_extensions": [        // Markdown 擴充功能
    "tables",                     // 表格支援
    "fenced_code",                // 程式碼區塊
    "codehilite",                 // 程式碼高亮
    "nl2br",                      // 換行轉 <br>
    "sane_lists"                  // 改進的清單處理
  ]
}
```

---

## 🎨 自訂樣式

編輯 `template/style.css` 可自訂 PDF 外觀：

```css
/* 修改主字型 */
body {
  font-family: "微軟正黑體", sans-serif;
  font-size: 12pt;
}

/* 修改標題顏色 */
h1 {
  color: #ff6600;
  border-bottom: 3px solid #ff6600;
}

/* 修改表格樣式 */
th {
  background: #ff6600;
  color: white;
}

/* 修改程式碼區塊背景 */
pre {
  background: #2d2d2d;
  color: #f8f8f2;
}
```

---

## 💡 進階功能

### 1️⃣ 加入封面頁

在 Markdown 檔案開頭加入：

```markdown
---
title: "專案報告"
author: "Your Name"
date: "2025-11-12"
---

<div class="page-break"></div>

# 第一章
...
```

### 2️⃣ 強制換頁

在需要換頁的地方插入：

```markdown
<div class="page-break"></div>
```

或在 CSS 中設定 H1 自動換頁（已內建）：

```css
h1 {
  page-break-before: always;
}
```

### 3️⃣ 多主題切換

建立多份 CSS 檔案：

```
template/
├── style-light.css
├── style-dark.css
└── style-corporate.css
```

在 `template.html` 中修改引用：

```html
<link rel="stylesheet" href="style-dark.css">
```

---

## 🐛 疑難排解

### ❌ 找不到 wkhtmltopdf

**錯誤訊息：**
```
OSError: No wkhtmltopdf executable found
```

**解決方式：**
1. 確認已安裝 wkhtmltopdf
2. 將執行檔路徑加入系統 PATH
3. 或在程式中指定路徑：

```python
import pdfkit

config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
pdfkit.from_string(html, output_path, configuration=config)
```

### ❌ 中文字顯示為方塊

**解決方式：**
1. 確認系統已安裝中文字型
2. 在 `style.css` 中明確指定字型：

```css
body {
  font-family: "Microsoft JhengHei", "微軟正黑體", sans-serif;
}
```

### ❌ 表格或圖片跨頁分割

**解決方式：**
在 CSS 中加入：

```css
table, img {
  page-break-inside: avoid;
}
```

---

## 📚 延伸資源

- [Markdown 語法說明](https://markdown.tw)
- [wkhtmltopdf 官方文件](https://wkhtmltopdf.org/usage/wkhtmltopdf.txt)
- [Python Markdown 套件](https://python-markdown.github.io)
- [CSS Print 樣式指南](https://www.smashingmagazine.com/2015/01/designing-for-print-with-css/)

---

## 📝 授權

本專案採用 MIT 授權。

---

## 🙌 貢獻

歡迎提交 Issue 或 Pull Request！

---

**專案維護**：LSAP Team  
**最後更新**：2025-11-12  
**版本**：v1.0
