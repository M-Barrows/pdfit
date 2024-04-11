from fpdf import FPDF 
import pathlib
import requests
import shutil
import logging
from bs4 import BeautifulSoup
from datetime import datetime
from PIL import Image 
from src.db import Image as DBImage, Document as DBDocument 


HEADERS = {'User-Agent': 'PDF-it'} 
def get_image_url(base_url:str): 
    response = requests.get(f"{base_url}?version=print", headers = HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")
    img_src = soup.find("div", id = "closure").find('img').get('src')
    return img_src

def validate_image_extension(ext:str):
    if ext not in ['png','jpg']:
        return False
    else: 
        return True

def download_image(url:str):
    errors = list()
    if url == '':
        logging.error('Blank URL')
    page_response = requests.get(url, headers=HEADERS, stream = True) 
    if page_response.status_code == 200:
        img_src = get_image_url(url)
        file_name = f"files/image-library/{img_src.split('/')[-1]}"
        if pathlib.Path(file_name).is_file():
            logging.info(f"⏱️i using cached image at {file_name}") 
            return file_name, errors
        img_response = requests.get(img_src, headers=HEADERS, stream = True) 
        if img_response.status_code == 200:
            file_type = img_src.split('.')[-1]
            if not validate_image_extension(file_type):
                logging.warn(f"⛔ Unsupported file type ({file_type}) for {img_src}")
                errors.append((img_src,f"Unsupported file type: {file_type}"))
            else:
                with open(file_name,"wb") as f:
                    shutil.copyfileobj(img_response.raw, f)
                logging.info(f"✅ Successfully downloaded image from {url}")
                return file_name, errors
    else: 
        logging.warn(f"⛔ Could not download image from {url}. Skipping.")
        return None

def scale_dimensions(img_path,max_w:int=1200,max_h:int=750):
    img = Image.open(img_path) 
    img_name = img_path.split('.')[:-1][0]
    size = max_w,max_h
    img.thumbnail(size,Image.Resampling.LANCZOS)
    img.save(f"{img_name}_{max_w}_{max_h}.png")
    return f"{img_name}_{max_w}_{max_h}.png"

def create_pdf(images=list()):
    if len(images) < 1:
        raise ValueError("No files provided")
    else:
        images_to_manually_print = list()
        successful_images = list()
        pdf = FPDF("P","in","Letter")
        images_per_page = 2
        for i, image in enumerate(images,1):
            img_file_path,errors = download_image(image)
            if len(errors) > 0:
                images_to_manually_print.append(errors[0])
                continue
            page_image_number = images_per_page  if (i % images_per_page) == 0 else (i % images_per_page)
            img_height = 10/images_per_page
            img_file_path = scale_dimensions(img_file_path)
            if page_image_number == 1:
                pdf.add_page()
                pdf.image(str(img_file_path),x=0,y=0,w=0,h=img_height)
            else:
                pdf.image(str(img_file_path),x=None,y=(page_image_number-1)*img_height,w=0,h=img_height)
            img_object = DBImage(image_url = image, storage_location = img_file_path)
            successful_images.append(img_object)
        today = datetime.now().strftime("%Y%m%d_%H%M%S")
        pdf_file_name = f"{today}_pdfit_output.pdf"
        pdf_file_path = f"files/output/{pdf_file_name}"
        pdf.output(pdf_file_path, "F")
        doc_object = DBDocument( name= pdf_file_name, storage_location= pdf_file_path, created_date=datetime.now(),images = successful_images)
        return doc_object, images_to_manually_print
