import sys, sqlite3
from collections import namedtuple
from pprint import pprint
import pandas as pd
from wordnet_jp import getSynonym
import support

if __name__ == '__main__':

    category_list = []
    df = pd.read_csv('sitecategorymaster.csv')
    for category in df['name']:
    	category = category.lower().lstrip('/').replace('/','・').replace('／','・').replace('（','・').replace('、','・').replace('(','・').strip('）').strip(')')

    	temp_list = []
    	if '・' in category:
    		cat = category.split('・')
    		for ca in cat:
    			synonym = getSynonym(ca)
    			temp_list.extend(list(synonym.values()))
    		category_list.append(temp_list)

    	else:
    		synonym = getSynonym(category)
    		category_list.append(list(synonym.values()))

    category_name_list = support.concatenate_list(category_list)
    category_name_list_final = support.delete_overlap(category_name_list)

    pprint(category_name_list_final)
    print(len(category_name_list_final))

    key_word_list = []
    tf = pd.read_csv('product_ctgr_master.csv')
    for category in tf['product_ctgr_name']:
    	category = category.replace('（','・').replace('、','・').replace('(','・').strip('）').strip(')')


    	temp_list = []
    	if '・' in category:
    		cat = category.split('・')
    		for ca in cat:
    			synonym = getSynonym(ca)
    			temp_list.extend(list(synonym.values()))
    		key_word_list.append(temp_list)

    	else:
    		synonym = getSynonym(category)
    		key_word_list.append(list(synonym.values()))

    category_key_word_list = support.concatenate_list(key_word_list)
    category_key_word_list_final = support.delete_overlap(category_key_word_list)

    pprint(category_key_word_list_final)
    print(len(category_key_word_list_final))



























