from fastapi import FastAPI, File, UploadFile
import pdfkit
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io

app = FastAPI()

@app.post("/create-watermarked-pdf/")
async def create_watermarked_pdf(html_file: UploadFile = File(...), watermark_image: UploadFile = File(...)):
    # Convert HTML to PDF
    output_pdf = "output.pdf"
    try:
        content = await html_file.read()
        pdfkit.from_string(content.decode("utf-8"), output_pdf)
    except Exception as e:
        pass
        # return {"error": f"Failed to convert HTML to PDF: {e}"}

    # Create a PDF with watermark
    reader = PdfReader(output_pdf)
    writer = PdfWriter()
    watermark_content = await watermark_image.read()
    watermark_io = io.BytesIO(watermark_content)

    for page_number in range(len(reader.pages)):
        packet = io.BytesIO()
        # create a new PDF with Reportlab
        can = canvas.Canvas(packet, pagesize=letter)
        # Save watermark image to a temporary file to use with drawImage
        temp_image_path = "temp_watermark_image.png"
        with open(temp_image_path, "wb") as image_file:
            image_file.write(watermark_io.getvalue())
        can.drawImage(temp_image_path, x=100, y=500)  # Adjust x, y to position the watermark
        can.save()

        # move to the beginning of the StringIO buffer
        packet.seek(0)
        new_pdf = PdfReader(packet)
        watermark_page = new_pdf.pages[0]

        original_page = reader.pages[page_number]
        original_page.merge_page(watermark_page)
        writer.add_page(original_page)

    watermarked_output = "download/watermarked_pdf.pdf"
    with open(watermarked_output, "wb") as f_out:
        writer.write(f_out)

    # Instead of returning the file, return a link to download the file
    return {"url": f"download/{watermarked_output}"}
