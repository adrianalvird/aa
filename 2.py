import pdfplumber
from googletrans import Translator
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate

def extract_text_with_formatting(pdf_path):
    """Extract text along with formatting metadata using pdfplumber."""
    extracted = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            for obj in page.extract_words():
                text = obj['text']
                font_size = obj.get('size', 12)  # Default to 12 if not available
                bold = 'Bold' in obj.get('fontname', '')
                extracted.append({'text': text, 'font_size': font_size, 'bold': bold})
    return extracted

def translate_text(text, source_lang='sa', target_lang='bn'):
    """Translate text using Google Translate."""
    translator = Translator()
    try:
        return translator.translate(text, src=source_lang, dest=target_lang).text
    except Exception as e:
        print(f"Translation error for text '{text}': {e}")
        return text  # Fallback to the original text in case of an error

def create_pdf(translated_content, output_path):
    """Create a new PDF with translated content and formatting."""
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    for item in translated_content:
        style = styles['Normal']
        if item['bold']:
            style = styles['Heading2']  # Use a bold style
        style.fontSize = item['font_size']
        elements.append(Paragraph(item['text'], style))

    doc.build(elements)

def main():
    input_pdf = "sans.pdf"
    output_pdf = "translated_bengali.pdf"

    # Step 1: Extract text with formatting
    formatted_text = extract_text_with_formatting(input_pdf)

    # Step 2: Translate the text
    translated_content = []
    for item in formatted_text:
        translated_text = translate_text(item['text'])
        translated_content.append({
            'text': translated_text,
            'font_size': item['font_size'],
            'bold': item['bold']
        })

    # Step 3: Create a new PDF
    create_pdf(translated_content, output_pdf)
    print(f"Translation complete. Saved to {output_pdf}.")

if __name__ == "__main__":
    main()
