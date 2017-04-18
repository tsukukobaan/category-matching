from wordnet_jp import getSynonym
import unicodedata

# def split_listing(lists):
# 	result_list = []
# 	temp_list = []
# 	if '・' in lists:
# 		cat = lists.split('・')
# 		for ca in cat:
# 			synonym = getSynonym(ca)
# 			temp_list.extend(list(synonym.values()))
# 		result_list.append(temp_list)

# 	else:
# 		synonym = getSynonym(lists)
# 		result_list.append(list(synonym.values()))

# 	return result_list

def is_japanese(string):
    for ch in string:
        name = unicodedata.name(ch) 
        if "CJK UNIFIED" in name \
        or "HIRAGANA" in name \
        or "KATAKANA" in name:
            return True
    return False

def clean_string(item):
	result = item.lstrip('/').replace(', ','/').replace(' and ','/').replace(' & ','/').replace('・','/').replace('·','/').replace('、','/').replace(' （','/').replace(' (','/').replace('（','/').replace('(','/').strip('） ').strip(') ').strip('）').strip(')').replace(' ','_').replace('-','/')
	return result

def concatenate_list(lists):
	result_list = []
	for list_item in lists:
		result = []
		for es in list_item:
			for e in es:
				result.append(e)
		result_list.append(result)
	return result_list

def delete_overlap(lists):
	result_list = []
	for list_item in lists:
		result_list.append(list(set(list_item)))
	return result_list