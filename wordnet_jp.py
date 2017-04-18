#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, sqlite3
from collections import namedtuple
from pprint import pprint
import pandas as pd
from nltk.corpus import wordnet as wn

from nltk.corpus import wordnet as wn

def simple_similarity(a, b):
    if wn.path_similarity(wn.synsets(a)[0], wn.synsets(b)[0]) == None:
    	return 0
    else:
    	return wn.path_similarity(wn.synsets(a)[0], wn.synsets(b)[0])

conn = sqlite3.connect("./wnjpn.db")
conn.text_factory = str

Word = namedtuple('Word','wordid lang lemma pron pos')

def getWords(lemma):
	cur = conn.execute("select * from word where lemma=?",(lemma,))
	return [Word(*row) for row in cur]

Sense = namedtuple('Sense','synset wordid lang rank lexid freq src')

def getSenses(word):
	cur = conn.execute("select * from sense where wordid=?",(word.wordid,))
	return [Sense(*row) for row in cur]

Synset = namedtuple('Synset','synset pos name src')

def getSynset(synset):
	cur = conn.execute("select * from synset where synset=?",(synset,))
	return Synset(*cur.fetchone())

def getWordsFromSynset(synset,lang):
	cur = conn.execute("select word.* from sense, word where synset=? and word.lang=? and sense.wordid = word.wordid;",(synset,lang))
	return [Word(*row) for row in cur]

def getWordsFromSenses(sense, lang="jpn"):
	synonym = {}
	for s in sense:
		lemmas = []
		syns = getWordsFromSynset(s.synset,lang)
		for sy in syns:
			lemmas.append(sy.lemma)
		synonym[getSynset(s.synset).name] = lemmas
	return synonym

def getSynonym(word):
	synonym = {}
	words = getWords(word)
	if words:
		for w in words:
			sense = getSenses(w)
			s = getWordsFromSenses(sense)
			synonym = dict(list(synonym.items()) + list(s.items()))
	return synonym

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        synonym = getSynonym(sys.argv[1])
        pprint(synonym)
    else:
        print("You need at least 1 argument as a word like below.\nExample:\n  $ python3 wordnet_jp 楽しい")







