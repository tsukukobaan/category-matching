import sys, sqlite3
from collections import namedtuple
from pprint import pprint
import pandas as pd
from wordnet_jp import getSynonym
import support
from wordnet_jp import simple_similarity
from nltk.corpus import wordnet as wn
import csv



if __name__ == '__main__':

    site_category_list = []
    df = pd.read_csv('google_site_category_master.csv')
    df = df.head(30)
    for item in df['name'].values.tolist(): 
        item = item[1:]

        # if '/' in item:
            #for the time being　continue not to dig too deep
            #continue
        item = item.replace(' & ','/').replace(' ','_')
        print(item)
        words = item.split('/')
        
        site_category_list.append(words)
        # else:
        # words = item.split(' & ')
        # site_category_list.append(words)

    product_category_list = []
    tf = pd.read_csv('product_ctgr_master.csv')
    for item in tf['product_ctgr_name']:
        item = support.clean_string(item)


        if '/' in item:
            words = item.split('/')
            product_category_list.append(words)
        else:
            product_category_list.append(item)


    pprint(site_category_list)
    print(len(site_category_list))
    pprint(product_category_list)
    print(len(product_category_list))

    score_matrix = []

    for product in product_category_list:
        product_row = []
        #print(product)
        #print("Above is the product #############################################")
        for site in site_category_list:
            #print(site)
            temp_sim = []
            for prod in product:
                for sit in site:
                    # print(prod)
                    # print(sit)
                    if wn.synsets(prod) and wn.synsets(sit):
                        temp_sim.append(simple_similarity(prod,sit))
                    elif wn.synsets(sit) and '_' in prod:
                        prod_sep = prod.split('_')
                        for pro in prod_sep:
                            if wn.synsets(pro):
                                temp_sim.append(simple_similarity(pro,sit))
                            else:
                                temp_sim.append(0)
                    else:
                        temp_sim.append(0)
            product_row.append(max(temp_sim))
            #print('printing max temporal similar score')
            #print(max(temp_sim))
        score_matrix.append(product_row)

    result = pd.DataFrame(score_matrix, index=tf.product_ctgr_name, columns=df.name)
    result.to_csv("test.tsv", sep="\t", encoding="utf-8")
    # with open("test.tsv", "w") as sink:
    #     for row in score_matrix:
    #         sink.write("{}\n".format("\t".join(list(map(str, row)))))
















