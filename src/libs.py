from fpdf import FPDF
import pathlib
import requests
import shutil
import secrets
import logging


def download_image(url:str):
    response = requests.get(url, headers={'User-Agent': 'PDF-it'}, stream = True)
    if response.status_code == 200:
        file_name = secrets.token_hex(10)
        file_type = url.split('.')[-1]
        file_name = f"image-cache/{file_name}.{file_type}"
        with open(file_name,"wb") as f:
            shutil.copyfileobj(response.raw, f)
        logging.info(f"Successfully downloaded image from {url}")
        return file_name
    else: 
        logging.warn(f"⛔ Could not download image from {url}. Skipping.")
        return None

def create_pdf(images=list()):
    if len(images) < 1:
        raise ValueError("No files provided")
    else:
        pdf = FPDF("P","in","Letter")
        images_per_page = 2
        for i, image in enumerate(images,1):
            print(image)
            img_file_path = download_image(image)
            page_image_number = images_per_page  if (i % images_per_page) == 0 else (i % images_per_page)
            img_height = 10/images_per_page
            if page_image_number == 1:
                pdf.add_page()
                pdf.image(str(img_file_path),x=0,y=0,w=0,h=img_height)
            else:
                pdf.image(str(img_file_path),x=None,y=(page_image_number-1)*img_height,w=0,h=img_height)
        pdf.output("pdfit_output.pdf", "F")
