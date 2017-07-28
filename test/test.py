#-*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from src.module import pdf2text
from src.module import textRank


doc = pdf2text.pdf_to_text('pdf_file/R1.pdf')
print(doc)

# 실행
ranked = textRank.run(doc)

for i, t in enumerate(ranked):
    print(i, '', t.text)