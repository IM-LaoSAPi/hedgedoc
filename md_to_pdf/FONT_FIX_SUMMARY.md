# 字體路徑修正摘要

## 問題診斷

檢查發現以下 CSS 檔案使用了 Windows 絕對路徑：
- `style.css`
- `style_modern.css`
- `style_latex.css`

原本的字體路徑：
```css
url('file:///C:/Windows/Fonts/NotoSansTC-VF.ttf')
url('file:///C:/Windows/Fonts/seguiemj.ttf')
url('file:///C:/Windows/Fonts/seguisym.ttf')
```

## 已完成的修正

### 1. ✅ 建立字體目錄
- 路徑：`md_to_pdf/template/fonts/`

### 2. ✅ 複製字體檔案
已從 `C:\Windows\Fonts\` 複製以下字體：
- `NotoSansTC-VF.ttf` (11.9 MB) - 繁體中文字體
- `seguiemj.ttf` (12.5 MB) - 表情符號
- `seguisym.ttf` (2.5 MB) - 符號字體

總大小：約 26.9 MB

### 3. ✅ 更新 CSS 檔案
將所有 CSS 檔案中的字體路徑改為相對路徑：
```css
/* 更新後 */
url('fonts/NotoSansTC-VF.ttf')
url('fonts/seguiemj.ttf')
url('fonts/seguisym.ttf')
```

更新的檔案：
- ✅ `template/style.css`
- ✅ `template/style_modern.css`
- ✅ `template/style_latex.css`

### 4. ✅ 建立說明文件
- `template/fonts/README.md` - 字體使用說明和授權資訊

## 優點

✨ **相對路徑的優勢**：
1. **可攜性**：專案可在不同電腦上執行，不依賴 Windows 系統字體
2. **穩定性**：字體版本固定，不會因系統更新而改變
3. **跨平台**：理論上可在 macOS/Linux 上使用（如果字體支援）
4. **自包含**：專案包含所有必要資源

## 測試建議

測試轉換功能：
```powershell
cd c:\Users\cdyti\Documents\GitHub\hedgedoc\md_to_pdf
python scripts\convert.py -i input\NASA_Hw8.md -s modern
```

如果轉換成功，PDF 應該能正確顯示：
- ✅ 繁體中文字元
- ✅ 表情符號 (emoji)
- ✅ 特殊符號

## 注意事項

⚠️ **Git 儲存庫大小**：
- 字體檔案約 27 MB，會增加儲存庫大小
- 如果團隊協作，所有成員都會下載這些檔案

💡 **建議方案**：
1. 保持現狀（適合小團隊或個人專案）
2. 使用 Git LFS 管理大型檔案
3. 將 `fonts/` 加入 `.gitignore`，由使用者自行安裝字體

## 後續步驟

如需進一步優化，可以：
1. 測試 PDF 轉換確認字體正常載入
2. 考慮是否需要減少字體檔案（如使用子集化）
3. 確認是否需要額外的字體支援其他語言
