from __future__ import absolute_import, unicode_literals

from io import StringIO

from pdfminer import settings
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage

from src.libs.refine import Refine

settings.STRICT = False


def pdf_to_text(file):

    manager = PDFResourceManager(caching=False)

    refine = Refine()
    io = StringIO()

    try:
        with open(file, 'rb') as f:
            device = TextConverter(rsrcmgr=manager, outfp=io, codec='utf-8', laparams=LAParams())
            interpreter = PDFPageInterpreter(rsrcmgr=manager, device=device)
            for page in PDFPage.get_pages(f):
                interpreter.process_page(page=page)
            device.close()
    except FileNotFoundError as err:
        print('{}'.format(err))
        raise Exception(err)

    result = refine.doc(io.getvalue())

    return result


