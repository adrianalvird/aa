import pdfplumber
from googletrans import Translator
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, SimpleDocTemplate
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import os

# Register a Bengali font
font_path = "Siyamrupali.ttf"  # Ensure this file exists in the script's directory
if os.path.exists(font_path):
    pdfmetrics.registerFont(TTFont("BengaliFont", font_path))
else:
    raise FileNotFoundError(f"Font file '{font_path}' not found. Ensure the font is present in the script's directory.")

def clean_text(text):
    """Clean text by removing unwanted characters."""
    return text.replace('\n', '').strip()

def extract_text_with_formatting(pdf_path):
    """Extract text and formatting metadata from a PDF."""
    extracted = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                for obj in page.extract_words():
                    text = clean_text(obj['text'])
                    font_size = obj.get('size', 12)  # Default font size
                    bold = 'Bold' in obj.get('fontname', '')
                    extracted.append({'text': text, 'font_size': font_size, 'bold': bold})
    except Exception as e:
        print(f"Error extracting text: {e}")
    return extracted

def translate_text(text, source_lang='sa', target_lang='bn'):
    """Translate Sanskrit text to Bengali using Google Translate."""
    translator = Translator()
    try:
        translated = translator.translate(text, src=source_lang, dest=target_lang)
        return translated.text
    except Exception as e:
        print(f"Translation error for text '{text}': {e}")
        return text  # Return original text if translation fails

def create_pdf(translated_content, output_path):
    """Create a new PDF with translated text and formatting."""
    try:
        doc = SimpleDocTemplate(output_path, pagesize=letter)
        styles = getSampleStyleSheet()

        # Create a custom style for Bengali text
        bengali_style = ParagraphStyle(
            name="Bengali",
            fontName="BengaliFont",
            fontSize=12,
            leading=14
        )

        elements = []
        for item in translated_content:
            style = bengali_style.clone('BengaliNormal')
            if item['bold']:
                style.fontSize = 14  # Slightly larger for bold text
            style.fontSize = item['font_size']
            elements.append(Paragraph(item['text'], style))

        doc.build(elements)
    except Exception as e:
        print(f"Error creating PDF: {e}")

def main():
    input_pdf = "sans.pdf"  # Input file (Sanskrit text)
    output_pdf = "mahabharata_bengali.pdf"  # Output file (Translated Bengali text)

    # Step 1: Extract text with formatting
    if not os.path.exists(input_pdf):
        print(f"Input PDF '{input_pdf}' not found.")
        return

    print("Extracting text with formatting...")
    formatted_text = extract_text_with_formatting(input_pdf)

    # Step 2: Translate each block of text
    print("Translating text to Bengali...")
    translated_content = []
    for item in formatted_text:
        translated_text = translate_text(item['text'])
        translated_content.append({
            'text': translated_text,
            'font_size': item['font_size'],
            'bold': item['bold']
        })

    # Step 3: Create a new PDF with translated content
    print("Creating translated PDF...")
    create_pdf(translated_content, output_pdf)
    print(f"Translation completed. File saved as {output_pdf}")

if __name__ == "__main__":
    main()
