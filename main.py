from fpdf import FPDF
import pathlib
pdf = FPDF("P","in","Letter")
image_list = list(pathlib.Path(pathlib.Path(__file__).parent.resolve(),'test-images').iterdir())
# imagelist is the list with all image filenames
images_per_page = 2
for i, image in enumerate(image_list,1):
    print(image)
    page_image_number = images_per_page  if (i % images_per_page) == 0 else (i % images_per_page)
    img_height = 10/images_per_page
    if page_image_number == 1:
        pdf.add_page()
        pdf.image(str(image),x=0,y=0,w=0,h=img_height)
    else:
        pdf.image(str(image),x=None,y=(page_image_number-1)*img_height,w=0,h=img_height)
pdf.output("pdfit_output.pdf", "F")
