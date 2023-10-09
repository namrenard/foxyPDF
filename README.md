![](foxy_pdf_v1.png)

# FoxyPDF
FoxyPDF is a small program written in python in order to combine or extract image or texte from PDF file.


## Warning
- Combined function work only on PDF with no corrupted header information inside.
Try ghostscript v.10.00.00 to regenerate the PDF if you have any problem regarding the fusion.
- PDF files need to be in the root directory of the script or else, don't forget to
add in the name given the directory where is the PDF. (ex : /path/name_of_pdf)

## Changelog

Current stable version : v1.3

- Combine different pages from different pdf together
- FIX : Change name method "fusion_file" to "combine_menu"
- FIX : Change type of extracts' methods into "static method"

v1.2

- Combine complete PDF together
- Extract text from one PDF file to text format (full or page selection)
- Extract image from PDF file (total or selected page)
  - Extract method 1 if the image was compressed inside the PDF
  - Extract method 2 to force extraction but with no warranty about the result.

v1.1

- Combine complete PDF together
- Extract text from one PDF file to .txt (full or page selection)

v1.0

- Combine complete PDF together

## Features

- Text extraction of full document or pages to other format (word, md, lateX ?...)
- CLI Interface with argparse or click libraries (?)
- GUI Interface

## Want to fork it ?

 > see requirement-dev.txt 
 > and https://pypdf2.readthedocs.io

## Author

Nicolas Renard

## Other party licence

part of the logo : Image by <a href="https://pixabay.com/users/klikovam-5635591/?utm_source=link-attribution&utm_medium=referral&utm_campaign=image&utm_content=7414046">Michaela</a> from <a href="https://pixabay.com//?utm_source=link-attribution&utm_medium=referral&utm_campaign=image&utm_content=7414046">Pixabay</a>
