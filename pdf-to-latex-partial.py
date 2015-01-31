from subprocess import call
import glob
import string
import os

# Script to convert PDFs w/ scanned page images into LaTeX partials.

target_file = "Mina Loy - History of Religion of Eros.pdf"

# This requires poppler to work
return_status = call(["pdfimages", "-png", target_file, "page-images/page"])

# This version uses ghostscript and imagemagick but doesn't produce as high-quality results:
#return_status = call(["convert", '-trim', target_file, '-resize 500%','-quality 100','-sharpen 0x1.0',  os.getcwd() + "/page-images/page.png"])

# Make the directory:
if not os.path.exists("page-images"):
    os.makedirs("page-images")

# Get a list of all the page numbers:
page_images = glob.glob(os.getcwd() + '/page-images/*.png')

# Base from which we include each image file:
base_image_template = "\\begin{{figure}}[hbt]\n\t\\centering\n\t\\includegraphics[height=11in,width=8.5in,keepaspectratio]{{{}}}\n\\end{{figure}}\n\n"

# Open a LaTeX file
f = open(target_file.replace(".pdf", ".tex"), "w")

# Write the geometry and page fraction reset code:
f.write("\\newgeometry{{margin=0in}}\n\\providecommand{\\oldpagefraction}{\\floatpagefraction}\n\\renewcommand{\\floatpagefraction}{0.1}\n\n")

for page_image in page_images:
    f.write(base_image_template.format(page_image.replace(".png", "").replace(os.getcwd() + "/","")))

# Write the geometry and page fraction restore code:
f.write("\\restoregeometry\n\\renewcommand{\\floatpagefraction}{\\oldpagefraction}")
f.close()