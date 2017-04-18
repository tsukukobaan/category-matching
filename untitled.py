site_category_list = []
df = pd.read_csv('sitecategorymaster.csv')
for item in df['name']:
	item = support.clean_string(item)

	if '/' in item:
        words = item.split('/')
        site_category_list.append(words)
	else:
        site_category_list.append(item)

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
    print(product)
    print("Above is the product #############################################")
    for site in site_category_list:
        print(site)
        if isinstance(product,list):
            temp_sim = []
            for prod in product:
                if wn.synsets(site) and wn.synsets(prod):
                    temp_sim.append(simple_similarity(prod,site))
                else:
                    temp_sim.append(0)
            print(max(temp_sim))
            product_row.append(max(temp_sim))
        elif isinstance(site, list):
            product_row.append(0)
        else:
            if not wn.synsets(product):
                product_row.append(0)
            elif not wn.synsets(site):
                product_row.append(0)
            else:
                product_row.append(simple_similarity(product,site))
                print(simple_similarity(product,site))
    score_matrix.append(product_row)
    csvWriter.writerow(product_row)