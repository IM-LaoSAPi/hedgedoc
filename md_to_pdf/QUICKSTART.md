# 快速開始指南

## 🚀 三步驟快速使用

### 步驟 1：安裝 wkhtmltopdf
```powershell
# Windows (使用 Chocolatey)
choco install wkhtmltopdf

# 或手動下載：https://wkhtmltopdf.org/downloads.html
```

### 步驟 2：安裝 Python 套件
```powershell
pip install -r requirements.txt
```

### 步驟 3：執行轉換
```powershell
# 轉換範例檔案
python scripts/convert.py -i input/demo.md

# 批次轉換所有檔案
python scripts/convert.py --batch
```

## 📝 使用你自己的 Markdown

1. 將你的 `.md` 檔案放入 `input/` 目錄
2. 執行：`python scripts/convert.py -i input/你的檔案.md`
3. 在 `output/` 目錄找到生成的 PDF

## 🎨 自訂樣式

編輯 `template/style.css` 可修改：
- 字體大小與顏色
- 表格樣式
- 程式碼區塊外觀
- 頁面邊界

---

更多資訊請參閱 [README.md](README.md)
