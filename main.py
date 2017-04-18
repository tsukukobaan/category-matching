import sys, sqlite3
from collections import namedtuple
from pprint import pprint
import pandas as pd
from wordnet_jp import getSynonym
import support
from wordnet_jp import simple_similarity,leacock_similarity,wu_palmer_similarity,resnik_similarity,jiang_conrath_similarity,l_similarity
from nltk.corpus import wordnet as wn
import csv
import numpy as np
from itertools import product as prd


def compute_similarity(a,b):
    return simple_similarity(a,b)

def compute_similarities(s1,s2):
    return wn.path_similarity(s1,s2)


if __name__ == '__main__':

    site_category_list = []
    df = pd.read_csv('google_site_category_master.csv')
    df = df.head(5)
    for item in df['name'].values.tolist(): 
        item = item[1:]
        item = item.replace(' & ','/').replace(' ','_')
        print(item)
        words = item.split('/')
        
        site_category_list.append(words)

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

    # for product in product_category_list:
    #     product_row = []
    #     #print(product)
    #     #print("Above is the product #############################################")
    #     for site in site_category_list:
    #         #print(site)
    #         temp_sim = []
    #         for prod in product:
    #             for sit in site:
    #                 # print(prod)
    #                 # print(sit)
    #                 if wn.synsets(prod) and wn.synsets(sit):
    #                     temp_sim.append(compute_similarity(prod,sit))
    #                 elif wn.synsets(sit) and '_' in prod:
    #                     prod_sep = prod.split('_')
    #                     for pro in prod_sep:
    #                         if wn.synsets(pro):
    #                             temp_sim.append(compute_similarity(pro,sit))
    #                         else:
    #                             temp_sim.append(0)
    #                 else:
    #                     temp_sim.append(0)
    #         product_row.append(max(temp_sim))
    #         #print('printing max temporal similar score')
    #         #print(max(temp_sim))
    #     score_matrix.append(product_row)

    # for product in product_category_list:
    #     product_row = []
    #     #print(product)
    #     #print("Above is the product #############################################")
    #     for site in site_category_list:
    #         #print(site)
    #         temp_sim = []

    #         for prod,sit in prd(product,site):
    #             syns1 = wn.synsets(prod)
    #             syns2 = wn.synsets(sit)
    #             if syns1 and syns2:
    #                 for sense1, sense2 in prd(syns1,syns2):
    #                     best = 0
    #                     comparison_result = [(compute_similarities(s1, s2) or 0, s1, s2) for s1, s2 in prd(syns1, syns2) if s1.pos() == s2.pos()]
    #                     if comparison_result:
    #                         best = max(comparison_result)
    #                         #best = np.mean([x[0] for x in comparison_result])
    #                     product_row.append(best)
    #             elif syns2 and '_' in prod:
    #                 prod_sep = prod.split('_')
    #                 for pro in prd(prod_sep,site):
    #                     print(pro)
    #                     syns3 = wn.synsets(pro)
    #                     if syns3:
    #                         for sense1, sense2 in prd(syns3,syns2):
    #                             best = 0
    #                             comparison_result = [(compute_similarities(s1, s2) or 0, s1, s2) for s1, s2 in prd(syns3, syns2) if s1.pos() == s2.pos()]
    #                             if comparison_result:
    #                                 best = max(comparison_result)
    #                                 #best = np.mean([x[0] for x in comparison_result])
    #                             product_row.append(best)


            # #original line
            # for prod in product:
            #     for sit in site:
            #         # print(prod)
            #         # print(sit)
            #         if wn.synsets(prod) and wn.synsets(sit):
            #             temp_sim.append(compute_similarity(prod,sit))
            #         elif wn.synsets(sit) and '_' in prod:
            #             prod_sep = prod.split('_')
            #             for pro in prod_sep:
            #                 if wn.synsets(pro):
            #                     temp_sim.append(compute_similarity(pro,sit))
            #                 else:
            #                     temp_sim.append(0)
            #         else:
            #             temp_sim.append(0)
            # product_row.append(max(temp_sim))
            # #print('printing max temporal similar score')
            # #print(max(temp_sim))
        # score_matrix.append(product_row)
    
    for product in product_category_list:
        product_row = []
        #print(product)
        #print("Above is the product #############################################")
        for site in site_category_list:
            #print(site)
            #temp_sim = []
            best = 0
            allsyns1 = set(ss for word in product for ss in wn.synsets(word))
            allsyns2 = set(ss for word in site for ss in wn.synsets(word))

            comparison_result = [(compute_similarities(s1, s2) or 0, s1, s2) for s1, s2 in prd(allsyns1, allsyns2) if s1.pos() == s2.pos()]
            if comparison_result:
                best = np.mean([x[0] for x in comparison_result])

            product_row.append(best)

        score_matrix.append(product_row)


    

    result = pd.DataFrame(score_matrix, index=tf.product_ctgr_name, columns=df.name)
    result.to_csv("max.tsv", sep="\t", encoding="utf-8")
    # with open("test.tsv", "w") as sink:
    #     for row in score_matrix:
    #         sink.write("{}\n".format("\t".join(list(map(str, row)))))












