import pdfkit
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io

input_file = "input.html"
output_file = "output.pdf"
watermarked_output = "watermarkedpdf.pdf"
watermark_image = "watermark.png"
try:
    # Convert HTML to PDF
    pdfkit.from_file(input_file, output_file)
except Exception as e:
    print(f"Failed to convert HTML to PDF: {e}")
# Create a PDF with watermark
reader = PdfReader(output_file)
writer = PdfWriter()

for page_number in range(len(reader.pages)):
    packet = io.BytesIO()
    # create a new PDF with Reportlab
    can = canvas.Canvas(packet, pagesize=letter)
    can.drawImage(watermark_image, x=100, y=500)  # Adjust x, y to position the watermark
    can.save()

    # move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfReader(packet)
    watermark_page = new_pdf.pages[0]

    original_page = reader.pages[page_number]
    original_page.merge_page(watermark_page)
    writer.add_page(original_page)

with open(watermarked_output, "wb") as f_out:
    writer.write(f_out)