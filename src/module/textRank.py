#-*- coding: utf-8 -*-

import re
import itertools
import networkx
from konlpy.tag import Twitter
from collections import Counter

twitter = Twitter()


class Sentence:
    def __init__(self, text, index=0):
        self.index = index
        self.text = text
        self.nouns = twitter.nouns(self.text)
        self.bow = Counter(self.nouns)

    def similarity(s1, s2):
        p = sum((s1.bow & s2.bow).values())
        q = sum((s1.bow | s2.bow).values())
        return p / q if q else 0

    def __eq__(self, another):
        return hasattr(another, 'index') and self.index == another.index

    def __hash__(self):
        return self.index

def get_sentences(text):
    candidates = xplit(stop_words)(text.strip())
    sentences=[]
    index=0
    for candidate in candidates:
        candidate = candidate.strip()
        if len(candidate):
            sentences.append(Sentence(candidate, index))
            index += 1
    return sentences

def build_graph(sentences):
    graph = networkx.Graph()
    graph.add_nodes_from(sentences)
    pairs = list(itertools.combinations(sentences,2))
    for eins, zwei in pairs:
        graph.add_edge(eins, zwei, weight=Sentence.similarity(eins,zwei))
    return graph


stop_words = ['. ', '? ', '! ', '\n', '.\n']

def xplit(stop_words):
    return lambda value: re.split('|'.join([re.escape(w) for w in stop_words]), value)


def run(doc):
    # make Sentence instance list
    sentences = get_sentences(doc)

    # 각각의 sentence를 노드로 하는 graph build
    graph = build_graph(sentences)

    # 해당 graph의 pagerank 값 구하기
    pagerank = networkx.pagerank(graph, weight='weight')

    # pagerank 값 기준 sorting
    reordered = sorted(pagerank, key=pagerank.get, reverse=True)

    return reordered
