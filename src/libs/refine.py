#!/usr/bin/env python3.5
from __future__ import absolute_import, unicode_literals

import re

from konlpy.tag import Mecab



class Refine(object):
    """Refine"""

    @staticmethod
    def text(doc):
        name = '%s.text' % __name__
        try:
            result = re.sub(r'\n', ' ', doc)
            result = re.sub('&lt;', '<', result)
            result = re.sub('&gt;', '>', result)
            result = re.sub('&quot;', '"', result)
            result = re.sub('&amp;', '&', result)
            result = re.sub('&nbsp;', ' ', result)
            result = re.sub(r'\s{2,}', ' ', result).strip()
            return result
        except Exception as e:
            raise Exception(e)

    def doc(self, doc):
        name = '%s.doc' % __name__

        result = ''
        for line in doc.split('\n'):
            l = self.text(line)

            if len(l) == 0:
                continue

            if 'Compliance Notice' in l:
                return result

            if re.search(r'^자료', l) is not None:
                continue

            if re.search(r'^주[0-9]]', l) is not None:
                continue

            if re.search(r'\[(.*)\]', l) is not None:
                continue

            l = re.sub(r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)', '', l)
            l = re.sub(r'\(.*\)', '', l)

            tmp = re.sub(r'[0-9,.-]', '', l)
            if len(tmp) < 6:
                continue

            pos_tagger = Mecab()
            nouns = [t[0] for t in pos_tagger.pos(l) if re.search(r'^NN[GP]$', t[1])]
            if len(nouns) < 3:
                continue

            if l[-1] == '.':
                l += ' '
            result += l
        return result