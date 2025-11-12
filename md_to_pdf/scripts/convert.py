#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===========================================
Markdown to PDF Converter
專案：LSAP - 穩定版面轉換系統
功能：將 Markdown 檔案轉換為格式穩定的 PDF
===========================================
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

try:
    import markdown
    import pdfkit
except ImportError as e:
    print(f"❌ 缺少必要套件：{e}")
    print("請執行：pip install -r requirements.txt")
    sys.exit(1)


class MarkdownToPDFConverter:
    """Markdown 轉 PDF 轉換器"""
    
    def __init__(self, config_path=None):
        """初始化轉換器"""
        self.base_dir = Path(__file__).parent.parent
        self.input_dir = self.base_dir / "input"
        self.output_dir = self.base_dir / "output"
        self.template_dir = self.base_dir / "template"
        
        # 載入設定檔
        self.config = self._load_config(config_path)
        
        # 確保目錄存在
        self.output_dir.mkdir(exist_ok=True)
    
    def _load_config(self, config_path=None):
        """載入設定檔"""
        if config_path is None:
            config_path = self.base_dir / "config.json"
        
        default_config = {
            "page_size": "A4",
            "margin_top": "25mm",
            "margin_bottom": "25mm",
            "margin_left": "20mm",
            "margin_right": "20mm",
            "encoding": "UTF-8",
            "enable_toc": False,
            "markdown_extensions": [
                "tables",
                "fenced_code",
                "codehilite",
                "nl2br",
                "sane_lists"
            ]
        }
        
        if config_path.exists():
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    user_config = json.load(f)
                    default_config.update(user_config)
            except Exception as e:
                print(f"⚠️  設定檔載入失敗，使用預設值：{e}")
        
        return default_config
    
    def convert(self, input_file, output_file=None, title=None, style="modern"):
        """
        轉換單一 Markdown 檔案為 PDF
        
        Args:
            input_file: 輸入的 Markdown 檔案路徑
            output_file: 輸出的 PDF 檔案路徑 (可選)
            title: PDF 標題 (可選)
            style: CSS 樣式 ("modern" 或 "latex"，預設為 "modern")
        """
        input_path = Path(input_file)
        
        if not input_path.exists():
            print(f"❌ 檔案不存在：{input_path}")
            return False
        
        # 決定輸出路徑
        if output_file is None:
            output_file = self.output_dir / f"{input_path.stem}.pdf"
        else:
            output_file = Path(output_file)
        
        # 決定標題
        if title is None:
            title = input_path.stem
        
        print(f"\n📄 開始轉換：{input_path.name}")
        print(f"📍 輸出位置：{output_file}")
        
        try:
            # 1️⃣ 讀取 Markdown 內容
            with open(input_path, "r", encoding="utf-8") as f:
                md_content = f.read()
            
            # 2️⃣ 轉換為 HTML
            html_content = self._markdown_to_html(md_content)
            
            # 3️⃣ 套用模板
            html_full = self._apply_template(html_content, title)
            
            # 4️⃣ 轉換為 PDF
            success = self._html_to_pdf(html_full, output_file, style)
            
            if success:
                print(f"✅ 轉換成功！")
                print(f"📦 檔案大小：{output_file.stat().st_size / 1024:.2f} KB")
                return True
            else:
                print(f"❌ 轉換失敗")
                return False
                
        except Exception as e:
            print(f"❌ 轉換過程發生錯誤：{e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _markdown_to_html(self, md_content):
        """將 Markdown 轉換為 HTML"""
        import re
        
        # 🔧 修正：移除 HackMD 語法的驚嘆號（如 ```bash! → ```bash）
        # 這樣標準的 fenced_code 擴展才能正確解析
        md_content = re.sub(r'```(\w+)!', r'```\1', md_content)
        
        # 🔧 表情符號替換 - 將常見表情符號轉換為可顯示的 HTML
        emoji_map = {
            '✅': '<span style="color: #28a745;">✓</span>',
            '❌': '<span style="color: #dc3545;">✗</span>',
            '⚠️': '<span style="color: #ffc107;">⚠</span>',
            '⚠': '<span style="color: #ffc107;">⚠</span>',
            '💡': '<span style="color: #ffc107;">💡</span>',
            '📄': '<span style="color: #007bff;">📄</span>',
            '📍': '<span style="color: #dc3545;">📍</span>',
            '📦': '<span style="color: #6c757d;">📦</span>',
            '🔧': '<span style="color: #17a2b8;">🔧</span>',
        }
        
        for emoji, replacement in emoji_map.items():
            md_content = md_content.replace(emoji, replacement)
        
        # 配置 codehilite 擴展以支援語法高亮
        from markdown.extensions.codehilite import CodeHiliteExtension
        from markdown.extensions.fenced_code import FencedCodeExtension
        
        # 準備擴展列表
        extensions = []
        for ext in self.config["markdown_extensions"]:
            if ext == "codehilite":
                # 使用配置過的 CodeHilite
                extensions.append(CodeHiliteExtension(
                    linenums=False,
                    guess_lang=True,
                    pygments_style='default',
                    noclasses=False
                ))
            elif ext == "fenced_code":
                # 使用 fenced_code 擴展
                extensions.append(FencedCodeExtension())
            else:
                extensions.append(ext)
        
        # 轉換 Markdown 為 HTML
        html = markdown.markdown(
            md_content,
            extensions=extensions
        )
        
        # 處理任務清單：將 [ ] 和 [x] 轉換為 HTML checkbox
        # 未勾選的任務
        html = re.sub(
            r'<li>\[ \]\s*',
            r'<li class="task-list-item">',
            html
        )
        
        # 已勾選的任務
        html = re.sub(
            r'<li>\[x\]\s*',
            r'<li class="task-list-item checked">',
            html
        )
        html = re.sub(
            r'<li>\[X\]\s*',
            r'<li class="task-list-item checked">',
            html
        )
        
        return html
    
    def _apply_template(self, html_content, title):
        """套用 HTML 模板"""
        template_path = self.template_dir / "template.html"
        
        if template_path.exists():
            with open(template_path, "r", encoding="utf-8") as f:
                template = f.read()
        else:
            # 使用內建模板
            template = """<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <title>{{title}}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
{{content}}
</body>
</html>"""
        
        # 替換佔位符
        html_full = template.replace("{{title}}", title)
        html_full = html_full.replace("{{content}}", html_content)
        
        return html_full
    
    def _html_to_pdf(self, html_content, output_path, style="modern"):
        """將 HTML 轉換為 PDF"""
        
        # 設定 wkhtmltopdf 路徑
        wkhtmltopdf_path = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
        config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)
        
        # PDF 選項
        options = {
            'page-size': self.config["page_size"],
            'margin-top': self.config["margin_top"],
            'margin-bottom': self.config["margin_bottom"],
            'margin-left': self.config["margin_left"],
            'margin-right': self.config["margin_right"],
            'encoding': self.config["encoding"],
            'no-outline': None,
            'enable-local-file-access': None,
            'print-media-type': None,
        }
        
        # 加入目錄
        if self.config["enable_toc"]:
            options['toc'] = None
        
        # 根據風格選擇 CSS 檔案
        if style == "latex":
            css_path = self.template_dir / "style_latex.css"
        else:
            css_path = self.template_dir / "style.css"
        
        try:
            pdfkit.from_string(
                html_content,
                str(output_path),
                options=options,
                css=str(css_path) if css_path.exists() else None,
                configuration=config
            )
            return True
        except Exception as e:
            print(f"⚠️  PDF 生成錯誤：{e}")
            return False
    
    def batch_convert(self, pattern="*.md", style="modern"):
        """批次轉換所有 Markdown 檔案"""
        md_files = list(self.input_dir.glob(pattern))
        
        if not md_files:
            print(f"⚠️  在 {self.input_dir} 中找不到符合的檔案：{pattern}")
            return
        
        print(f"\n📚 找到 {len(md_files)} 個檔案")
        print("=" * 50)
        
        success_count = 0
        for md_file in md_files:
            if self.convert(md_file, style=style):
                success_count += 1
            print("-" * 50)
        
        print(f"\n✨ 完成！成功轉換：{success_count}/{len(md_files)}")


def main():
    """主程式"""
    parser = argparse.ArgumentParser(
        description="Markdown to PDF 轉換工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
範例：
  # 轉換單一檔案
  python convert.py -i ../input/report.md
  
  # 指定輸出路徑
  python convert.py -i ../input/report.md -o ../output/my_report.pdf
  
  # 批次轉換所有 Markdown
  python convert.py --batch
  
  # 轉換特定模式的檔案
  python convert.py --batch --pattern "chapter_*.md"
        """
    )
    
    parser.add_argument(
        "-i", "--input",
        help="輸入的 Markdown 檔案路徑"
    )
    
    parser.add_argument(
        "-o", "--output",
        help="輸出的 PDF 檔案路徑 (可選)"
    )
    
    parser.add_argument(
        "-t", "--title",
        help="PDF 文件標題 (可選)"
    )
    
    parser.add_argument(
        "-s", "--style",
        choices=["modern", "latex"],
        default="modern",
        help="PDF 樣式風格：modern (現代風格) 或 latex (LaTeX 風格，預設: modern)"
    )
    
    parser.add_argument(
        "--batch",
        action="store_true",
        help="批次轉換 input 目錄中的所有檔案"
    )
    
    parser.add_argument(
        "--pattern",
        default="*.md",
        help="批次轉換時的檔案模式 (預設: *.md)"
    )
    
    parser.add_argument(
        "-c", "--config",
        help="設定檔路徑 (預設: config.json)"
    )
    
    args = parser.parse_args()
    
    # 建立轉換器
    converter = MarkdownToPDFConverter(config_path=args.config)
    
    # 執行轉換
    if args.batch:
        converter.batch_convert(pattern=args.pattern, style=args.style)
    elif args.input:
        converter.convert(
            input_file=args.input,
            output_file=args.output,
            title=args.title,
            style=args.style
        )
    else:
        parser.print_help()
        print("\n💡 提示：使用 -i 指定檔案，或使用 --batch 批次轉換")
        print("💡 使用 -s latex 可切換為 LaTeX 風格")


if __name__ == "__main__":
    main()
