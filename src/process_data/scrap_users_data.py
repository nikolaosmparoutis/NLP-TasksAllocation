import os
from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

external_dir = '/home/nikoscf/PycharmProjects/PM-Tasks-Allocation-NLP/data/external/'  # pdf files
txt_dir = '/home/nikoscf/PycharmProjects/PM-Tasks-Allocation-NLP/data/external/txt/'  # where to store txt files

'''
    Scrap texts from each file. Specificaly from .pdf files, keeping the hierarchical structure of pdf.
    (The hierarchical format is usefull for RNN or BERT arhitectures)
    Input: the path to pdfs
    Returns: text
'''


def _convert_pdf_to_txt(path):
    try:
        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        codec = 'utf-8'
        laparams = LAParams()
        device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        fp = open(path, 'rb')
        password = ""
        maxpages = 0
        caching = True
        pagenos = set()

        for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages,
                                      password=password,
                                      caching=caching,
                                      check_extractable=True):
            interpreter.process_page(page)

        fp.close()
        device.close()
        text = retstr.getvalue()
        retstr.close()
    except:
        raise IOError
    return text


'''
Scrapped texts stored to txt files
Input: the dir to store txt files
Returns: Nothing
'''


def store_txt(external_dir):
    for file_name in os.listdir(external_dir):
        if os.path.splitext(file_name)[1] == '.pdf':
            file_dir = os.path.join(external_dir, file_name)
            txt = _convert_pdf_to_txt(file_dir)
            txt_file = os.path.join(txt_dir, file_name)
            with open(txt_file + '.txt', "w") as file:
                file.write(txt)
        else:
            pass
    if os.listdir(txt_dir) is None:
        print("Not acceptable file format for data processing.Scraping and extraction stopped.")
    else:
        print("PDF's text extracted to txt files.")


store_txt(external_dir)
