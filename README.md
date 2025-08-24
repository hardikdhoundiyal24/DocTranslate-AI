# 🤖 DocTranslate AI
Translate PDF documents into **structured Word files** using the power of AI.  
DocTranslate AI analyzes your PDF’s layout, translates the content, and rebuilds it into a **clean, editable `.docx` file**.  

---

## ✨ Core Features
- 🌐 **Multi-Language Translation** – Translate into dozens of languages  
- 🏛️ **Structure Preservation** – Headings, lists, paragraphs, and tables remain intact  
- 🤖 **AI-Powered** – Understands layout visually  
- 📄 **Clean Output** – Generates well-formatted `.docx` files  
- 🚀 **Simple to Use** – Straightforward command-line interface  

---

## 🛠️ Technology Stack
- **Backend** → Python  
- **PDF Processing** → PyMuPDF (fitz)  
- **AI Model** → OpenAI GPT-4o mini  
- **Document Generation** → Pandoc  
- **API Communication** → httpx  

---

## 💡 How It Works
1. 🔍 **Analyze** → Convert each PDF page into a high-resolution image  
2. 🧠 **Understand & Translate** → AI extracts text and translates it  
3. 📝 **Structure** → AI outputs structured Markdown  
4. 🏗️ **Rebuild** → Pandoc converts Markdown → `.docx`  

---

## 📌 A Note on Perfection
- ✅ Preserves **headings, lists, tables, paragraphs**  
- ⚠️ Does **not** replicate exact design (fonts, columns, image placement)  
- 🎯 Goal = **Readable, functional translation**, not pixel-perfect copy  

---

