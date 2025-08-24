import os
import sys
import argparse
import base64
import subprocess
import fitz  # PyMuPDF
import httpx
import asyncio
from dotenv import load_dotenv

# --- SETUP ---
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

# --- CORE FUNCTIONS ---

def check_pandoc():
    """Checks if Pandoc is installed on the system."""
    try:
        subprocess.run(["pandoc", "--version"], check=True, capture_output=True)
        print("✅ Pandoc is installed.")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Error: Pandoc is not installed or not in your system's PATH.")
        print("Please install it from https://pandoc.org/installing.html")
        return False

def pdf_to_images(pdf_path):
    """Converts each page of a PDF into a high-resolution image."""
    try:
        doc = fitz.open(pdf_path)
        image_paths = []
        print(f"📄 Found {len(doc)} pages in the PDF.")
        for i, page in enumerate(doc):
            print(f"  -> Converting page {i + 1} to image...")
            pix = page.get_pixmap(dpi=300)
            image_path = f"temp_page_{i}.png"
            pix.save(image_path)
            image_paths.append(image_path)
        return image_paths
    except Exception as e:
        print(f"❌ Error processing PDF: {e}")
        return []

def image_to_base64(image_path):
    """Encodes an image file into a base64 string."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

async def translate_image_to_markdown(client, image_base64, target_language):
    """Sends an image to the OpenAI API and gets the translated content as Markdown."""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    # --- THIS IS THE NEW, MORE DETAILED PROMPT ---
    prompt = (
        "You are an expert document analyst and translator. "
        f"Analyze this image of a document page. Extract all text, tables, and structural elements like headings and lists. "
        f"Translate all extracted content to {target_language}. "
        "Your entire response MUST be a single, clean Markdown document. "
        "When you generate a table, it MUST be a valid GitHub Flavored Markdown table. "
        "This means it must have a header row and a separator line made of dashes (---) beneath it. "
        "For example: \n"
        "| Header 1 | Header 2 |\n"
        "| --- | --- |\n"
        "| Data 1 | Data 2 |\n"
    )

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{image_base64}"}
                    }
                ]
            }
        ],
        "max_tokens": 4000
    }

    response = await client.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=120.0
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

def markdown_to_docx(md_content, output_docx_path):
    """Converts a Markdown string to a DOCX file using Pandoc."""
    md_file_path = "temp_translated.md"
    try:
        print("🖋️ Generating final Word Document (.docx) using Pandoc...")
        with open(md_file_path, "w", encoding="utf-8") as f:
            f.write(md_content)

        # This command is much simpler and more reliable than the PDF one.
        subprocess.run(
            ["pandoc", md_file_path, "-o", output_docx_path],
            check=True
        )
        print(f"🎉 Success! Translated document saved to: {output_docx_path}")
    except Exception as e:
        print(f"❌ An error occurred during DOCX generation: {e}")
    finally:
        if os.path.exists(md_file_path):
            os.remove(md_file_path)

# --- MAIN EXECUTION ---

async def main(pdf_path, language):
    """Main function to orchestrate the PDF translation workflow."""
    if not API_KEY:
        print("❌ Error: OPENAI_API_KEY is not set in your .env file.")
        return

    if not check_pandoc():
        return

    image_paths = pdf_to_images(pdf_path)
    if not image_paths:
        return

    full_markdown = ""
    async with httpx.AsyncClient() as client:
        for i, img_path in enumerate(image_paths):
            print(f"🧠 Translating page {i + 1}/{len(image_paths)}...")
            base64_image = image_to_base64(img_path)
            try:
                markdown_part = await translate_image_to_markdown(client, base64_image, language)
                full_markdown += markdown_part + "\n\n"
            except httpx.HTTPStatusError as e:
                print(f"❌ API Error on page {i + 1}: {e.response.status_code} - {e.response.text}")
                break
            finally:
                os.remove(img_path)

    if full_markdown:
        base_name = os.path.splitext(pdf_path)[0]
        # Change the output extension to .docx
        output_path = f"{base_name}_translated.docx"
        markdown_to_docx(full_markdown, output_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Translate a PDF to a structured Word Document.")
    parser.add_argument("pdf_file", help="The path to the PDF file to translate.")
    parser.add_argument("language", help="The target language (e.g., 'Italian', 'French', 'Japanese').")
    args = parser.parse_args()

    asyncio.run(main(args.pdf_file, args.language))