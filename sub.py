import sys, sqlite3
from collections import namedtuple
from pprint import pprint
import pandas as pd
from wordnet_jp import getSynonym

if __name__ == '__main__':

    df = pd.read_csv('product_ctgr_master.tsv', delimiter='\t')
    
    for category in df['product_ctgr_name']:
        cat = category.lower().lstrip('/')
        print(cat)
        synonym = getSynonym(cat)
        pprint(synonym)