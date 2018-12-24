# TransPdf
Extracting text from pdf files and translate the text into designated language by calling google api

## Preliminary
Python 3.4+

## Set up
pip3 install googletrans

pip3 install pdfminer.six

## Basic usage
python3 translate.py # translate all pdf files under current directory

## Advanced usage
python3 translate.py -h # print all detailed helping messages

## Ref
googletrans: https://github.com/ssut/py-googletrans

pdfminer: https://github.com/pdfminer/pdfminer.six

google translate api: https://cloud.google.com/translate/

## TODO
Add support for exporting translation into docx files

Pack up and reform into a single executable file

Fix format issues (like words with letters "fi" will be weird after text extration from a pdf file)

Fix JSON Empty issues in googletrans (temporarily fix by eliminating characters whose ascii value bigger than 127)
