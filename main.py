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
from nltk.corpus import genesis,wordnet_ic
genesis_ic = wn.ic(genesis, False, 0.0)
brown_ic = wordnet_ic.ic('ic-brown.dat')
semcor_ic = wordnet_ic.ic('ic-semcor.dat')


def compute_similarity(a,b):
    return simple_similarity(a,b)

def compute_similarities(s1,s2,sim):
    if sim == "path":
        return wn.path_similarity(s1,s2)
    elif sim == "lch":
        return wn.lch_similarity(s1,s2)
    elif sim == "wup":
        return wn.wup_similarity(s1,s2)
    elif sim == "res":
        return wn.res_similarity(s1,s2,genesis_ic)
    elif sim == "jcn":
        return wn.jcn_similarity(s1,s2,genesis_ic)
    elif sim == "lin":
        return wn.lin_similarity(s1,s2,genesis_ic)

def flatten_list(l):
    return [item for sublist in l for item in sublist]

def simple_similarity_matrix(product_category_list,site_category_list):
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
                        temp_sim.append(compute_similarity(prod,sit))
                    elif wn.synsets(sit) and '_' in prod:
                        prod_sep = prod.split('_')
                        for pro in prod_sep:
                            if wn.synsets(pro):
                                temp_sim.append(compute_similarity(pro,sit))
                            else:
                                temp_sim.append(0)
                    else:
                        temp_sim.append(0)
            product_row.append(max(temp_sim))
            #print('printing max temporal similar score')
            #print(max(temp_sim))
        score_matrix.append(product_row)
    result = pd.DataFrame(score_matrix, index=tf.product_ctgr_name, columns=df.name)
    result.to_csv("simple_lch.tsv", sep="\t", encoding="utf-8")




def similarity_matrix(sim,rep):

    score_matrix = []

    for product in product_category_list:
        #この時点でproductはリスト
        product_row = []
        for site in site_category_list:
            # product site ともにリスト、中身は一つ〜
            best = 0
            allsyns1 = set(ss for word in product for ss in (wn.synsets(word) if wn.synsets(word) else flatten_list([wn.synsets(w) for w in word.split("_")])))
            allsyns2 = set(ss for word in site for ss in (wn.synsets(word) if wn.synsets(word) else flatten_list([wn.synsets(w) for w in word.split("_")])))
            #allsynsには入っているのは各単語のsynsetのset
            comparison_result = [(compute_similarities(s1, s2,sim) or 0, s1, s2) for s1, s2 in prd(allsyns1, allsyns2) if s1.pos() == s2.pos() and s1.pos() != "s"]
            if "games" in product and "Games" in site:
                print("{}, {}".format(product, site))
                print("{}".format(comparison_result[:10]))
            if comparison_result:
                if rep == "max":
                    best = max([x[0] for x in comparison_result])
                elif rep == "mean":
                    best = np.mean([x[0] for x in comparison_result])
                elif rep == "median":
                    best = np.median([x[0] for x in comparison_result])
                elif rep == "min":
                    best = min([x[0] for x in comparison_result])
            product_row.append(best)

        score_matrix.append(product_row)

    file_name = sim + "_" + rep + ".tsv"
    result = pd.DataFrame(score_matrix, index=tf.product_ctgr_name, columns=df.name)
    result.to_csv(file_name, sep="\t", encoding="utf-8")


if __name__ == '__main__':

    site_category_list = []
    #loading site categories
    df = pd.read_csv('google_site_category_master.csv')
    df = df.head(10)
    #extracting name column
    for item in df['name'].values.tolist(): 
        item = item[1:]
        item = item.replace(' & ','/').replace(' ','_')
        words = item.split('/')
        print(words)
        
        site_category_list.append(words)

    product_category_list = []
    tf = pd.read_csv('product_ctgr_master.csv')
    for item in tf['product_ctgr_name']:
        item = support.clean_string(item)


        if '/' in item:
            words = item.split('/')
            product_category_list.append(words)
        else:
            product_category_list.append([item])


    pprint(site_category_list)
    print(len(site_category_list))
    pprint(product_category_list)
    print(len(product_category_list))

    similarity_measures = ["path","lch","wup","res","jcn","lin"]
    reppresentation_measures = ["max","mean","median","min"]

    for sim,rep in prd(similarity_measures,reppresentation_measures):
        similarity_matrix(sim,rep)

    # simple_similarity_matrix(product_category_list,site_category_list)



    # score_matrix = []

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


        #     #original line
        #     for prod in product:
        #         for sit in site:
        #             # print(prod)
        #             # print(sit)
        #             if wn.synsets(prod) and wn.synsets(sit):
        #                 temp_sim.append(compute_similarity(prod,sit))
        #             elif wn.synsets(sit) and '_' in prod:
        #                 prod_sep = prod.split('_')
        #                 for pro in prod_sep:
        #                     if wn.synsets(pro):
        #                         temp_sim.append(compute_similarity(pro,sit))
        #                     else:
        #                         temp_sim.append(0)
        #             else:
        #                 temp_sim.append(0)
        #     product_row.append(max(temp_sim))
        #     #print('printing max temporal similar score')
        #     #print(max(temp_sim))
        # score_matrix.append(product_row)
    
    # for product in product_category_list:
    #     product_row = []
    #     #print(product)
    #     #print("Above is the product #############################################")
    #     for site in site_category_list:
    #         #print(site)
    #         #temp_sim = []
    #         best = 0
    #         allsyns1 = set(ss for word in product for ss in (wn.synsets(word) if wn.synsets(word) else flatten_list([wn.synsets(w) for w in word.split("_")])))
    #         allsyns2 = set(ss for word in site for ss in (wn.synsets(word) if wn.synsets(word) else flatten_list([wn.synsets(w) for w in word.split("_")])))

    #         # print('synsets')
    #         # print
    #         # print(allsyns1)
    #         # print
    #         # print(allsyns2)
    #         # print('product')
    #         # print(prd(allsyns1,allsyns2))

    #         comparison_result = [(compute_similarities(s1, s2) or 0, s1, s2) for s1, s2 in prd(allsyns1, allsyns2) if s1.pos() == s2.pos() and s1.pos() != "s"]
    #         if comparison_result:
    #             #best = max([x[0] for x in comparison_result])
    #             #best = np.mean([x[0] for x in comparison_result])
    #             #best = np.median([x[0] for x in comparison_result])
    #             best = min([x[0] for x in comparison_result])

    #         product_row.append(best)

    #     score_matrix.append(product_row)


    

    # result = pd.DataFrame(score_matrix, index=tf.product_ctgr_name, columns=df.name)
    # result.to_csv("lin_min.tsv", sep="\t", encoding="utf-8")
    # with open("test.tsv", "w") as sink:
    #     for row in score_matrix:
    #         sink.write("{}\n".format("\t".join(list(map(str, row)))))












