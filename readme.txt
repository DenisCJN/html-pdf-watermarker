# Watermarked PDF Generator

This application allows you to generate watermarked PDFs using a simple REST API, powered by FastAPI. It includes functionality to post HTML and watermark images to be converted into a PDF file.

## Prerequisites

Ensure you have Python and pip installed on your system. You will need Python 3.7 or newer.

## Installation

To install the necessary dependencies, follow these steps:

1. Clone the repository to your local machine.
2. Navigate to the cloned directory.
3. Install the dependencies using pip:

   ```bash
   pip install -r install.txt
   ```

## Running the Application

To start the server, use the following command:

```bash
uvicorn main:app --reload
```

The `--reload` flag enables auto-reloading of the server when there are changes to the code.

## Usage

To create a watermarked PDF, you can use the following `curl` command:

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/create-watermarked-pdf/' \
  -H 'accept: application/pdf' \
  -H 'Content-Type: multipart/form-data' \
  -F 'html_file=@input.html;type=text/html' \
  -F 'watermark_image=@watermark.png;type=image/png'
```

This command sends a POST request to the API with a `.html` file and a watermark `.png` image as form-data. The response is a URL pointing to the generated watermarked PDF, which you can download.

## Downloading the PDF

Upon successful creation, the server will respond with a JSON containing a URL to download the generated PDF. You can access this file through the provided link, typically pointing towards a download directory on the server.