import pdfplumber
from googletrans import Translator
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

# Register a Unicode-compliant font
pdfmetrics.registerFont(TTFont("NotoSans", "NotoSans-Regular.ttf"))

def clean_text(text):
    """Remove invalid or non-standard characters from text."""
    return ''.join(char for char in text if char.isprintable())

def extract_text_with_formatting(pdf_path):
    """Extract text along with formatting metadata using pdfplumber."""
    extracted = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            for obj in page.extract_words():
                text = clean_text(obj['text'])
                font_size = obj.get('size', 12)
                bold = 'Bold' in obj.get('fontname', '')
                extracted.append({'text': text, 'font_size': font_size, 'bold': bold})
    return extracted

def translate_text(text, source_lang='auto', target_lang='bn'):
    """Translate text using Google Translate."""
    translator = Translator()
    try:
        return translator.translate(text, src=source_lang, dest=target_lang).text
    except Exception as e:
        print(f"Translation error for text '{text}': {e}")
        return text  # Return the original text if translation fails

def create_pdf(translated_content, output_path):
    """Create a new PDF with translated content and formatting."""
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    for item in translated_content:
        style = styles['Normal']
        style.fontName = "NotoSans"  # Use the registered Unicode-compliant font
        if item['bold']:
            style = styles['Heading2']  # Use a bold style for headings
        style.fontSize = item['font_size']
        elements.append(Paragraph(item['text'], style))

    doc.build(elements)

def main():
    input_pdf = "mahabharata_sanskrit.pdf"
    output_pdf = "mahabharata_bengali.pdf"

    # Step 1: Extract text with formatting
    print("Extracting text from PDF...")
    formatted_text = extract_text_with_formatting(input_pdf)

    # Step 2: Translate the text
    print("Translating text...")
    translated_content = []
    for item in formatted_text:
        translated_text = translate_text(item['text'])
        translated_content.append({
            'text': translated_text,
            'font_size': item['font_size'],
            'bold': item['bold']
        })

    # Step 3: Create a new PDF
    print("Creating translated PDF...")
    create_pdf(translated_content, output_pdf)
    print(f"Translation complete. Saved to {output_pdf}.")

if __name__ == "__main__":
    main()
