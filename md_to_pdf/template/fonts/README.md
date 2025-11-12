# 字體檔案說明

此目錄包含 PDF 轉換所需的字體檔案。

## 已包含的字體

- **NotoSansTC-VF.ttf** - Noto Sans 繁體中文（支援可變字重）
- **seguiemj.ttf** - Segoe UI Emoji（表情符號支援）
- **seguisym.ttf** - Segoe UI Symbol（符號支援）

## 字體來源

這些字體檔案是從 Windows 系統字體資料夾 (`C:\Windows\Fonts\`) 複製而來。

## 如何重新取得字體

如果字體檔案遺失，可以從以下位置複製：

### Windows 系統
```powershell
Copy-Item "C:\Windows\Fonts\NotoSansTC-VF.ttf" ".\fonts\"
Copy-Item "C:\Windows\Fonts\seguiemj.ttf" ".\fonts\"
Copy-Item "C:\Windows\Fonts\seguisym.ttf" ".\fonts\"
```

### 其他來源

- **Noto Sans TC**: https://fonts.google.com/noto/specimen/Noto+Sans+TC
- **Segoe UI Emoji/Symbol**: Windows 10/11 內建字體

## 授權資訊

- Noto Sans TC: [SIL Open Font License 1.1](https://scripts.sil.org/OFL)
- Segoe UI 系列: Microsoft 所有，僅供 Windows 使用者使用

## 注意事項

⚠️ 這些字體檔案總大小約 26 MB，已加入 Git 儲存庫中。如果需要減少儲存庫大小，可考慮：
1. 將字體檔案加入 `.gitignore`
2. 使用 Git LFS (Large File Storage)
3. 在部署時動態下載字體
