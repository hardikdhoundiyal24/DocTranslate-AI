🤖 DocTranslate AI


Translate PDF documents into structured Word files using the power of AI. DocTranslate.ai intelligently analyzes your PDF's layout, translates the content, and rebuilds it into a clean, editable .docx file.



✨ Core Features
🌐 Multi-Language Translation: Translate your documents into dozens of languages.

🏛️ Structure Preservation: Intelligently identifies and preserves headings, lists, paragraphs, and tables.

🤖 AI-Powered: Uses a powerful multimodal AI to understand document layouts visually.

📄 Clean Output: Generates a well-formatted and editable Microsoft Word (.docx) file.

🚀 Simple to Use: A straightforward command-line interface for quick and easy translations.

🛠️ Technology Stack
Backend: Python

PDF Processing: PyMuPDF (fitz)

AI Model: OpenAI GPT-4o mini

Document Generation: Pandoc

API Communication: httpx

💡 How It Works
This project avoids the fragile process of editing PDFs directly. Instead, it follows a modern, robust workflow:

🔍 Analyze: Each page of the PDF is converted into a high-resolution image.

🧠 Understand & Translate: The image is sent to a multimodal AI, which analyzes the layout, extracts all the text, and translates it.

📝 Structure: The AI returns the translated content in a structured Markdown format.

🏗️ Rebuild: The powerful Pandoc utility takes the structured Markdown and builds a clean, final .docx document.

A Note on Perfection

This tool is designed to create a logically structured and readable document. While it does an excellent job of preserving headings, lists, and tables, it does not attempt to replicate the original PDF's visual design (like columns, fonts, or exact image placement). The goal is a clean, functional translation, not a pixel-perfect copy.
