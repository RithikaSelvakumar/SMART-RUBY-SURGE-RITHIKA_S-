import pytesseract
from PIL import Image
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Set Tesseract path if needed (Windows users)
# If Tesseract is not found, set the path manually
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_image(image_path):
    """Extracts text from an image using Tesseract OCR."""
    try:
        image = Image.open(image_path)  # Open image
        extracted_text = pytesseract.image_to_string(image)  # Extract text
        return extracted_text.strip()
    except Exception as e:
        print(f"Error extracting text from {image_path}: {e}")
        return ""

def save_text_to_pdf(text, output_pdf):
    """Saves extracted text to a PDF file."""
    c = canvas.Canvas(output_pdf, pagesize=letter)
    width, height = letter
    y_position = height - 50  # Initial Y position for text
    c.setFont("Helvetica", 10)
    
    for line in text.split('\n'):
        if y_position < 50:  # Start a new page if space runs out
            c.showPage()
            c.setFont("Helvetica", 10)
            y_position = height - 50
        c.drawString(50, y_position, line)
        y_position -= 15  # Line spacing
    
    c.save()

def process_images_in_folder(folder_path, output_folder):
    """Processes all images in a folder and saves extracted text in individual PDFs."""
    os.makedirs(output_folder, exist_ok=True)
    images = [f for f in os.listdir(folder_path) if f.lower().endswith(('png', 'jpg', 'jpeg'))]
    if not images:
        print("⚠ No images found in the folder!")
        return
    
    for image_file in images:
        image_path = os.path.join(folder_path, image_file)
        print(f"Processing: {image_file}")
        extracted_text = extract_text_from_image(image_path)
        
        if extracted_text:
            pdf_filename = os.path.splitext(image_file)[0] + ".pdf"
            pdf_path = os.path.join(output_folder, pdf_filename)
            save_text_to_pdf(extracted_text, pdf_path)
            print(f"✅ Extracted text saved to {pdf_path}")
        else:
            print(f"⚠ No text extracted from {image_file}.")

# Define folder paths
images_folder = "images"  # Update with your images folder path
output_folder = "source_documents"

# Process images and generate PDFs
process_images_in_folder(images_folder, output_folder)
