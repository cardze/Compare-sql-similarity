from difflib import SequenceMatcher

import os

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def quater_score(score:float):
    return int(score * 4)

def group_score(score:float , group_number:int):
    return int(score * group_number)

def get_sql_content(path):
    ret = ""
    with open(path, "r") as file:
        for i in file.readlines():
            ret+=i
        return ret

def get_sql_list(from_here):
    tmp_dct = {}
    for query in os.listdir(from_here):
        tmp_dct[query] = get_sql_content(from_here+"/"+query)
    return tmp_dct

def generate_pairs(sqls:dict)->list:
    key_list = []
    for k,v in sqls.items():
        key_list.append(k)
    ret = []
    for i in range(len(key_list)-1):
        for j in range(i+1 , len(key_list)):
            ret.append((key_list[i], key_list[j]))
    return ret

def check_same(i:list)->bool:
    for item in i:
        if item[0] == item[1]:
            return True
    return False
    
def generate_histo_dict(sqls:dict)->dict:
    pair_list = generate_pairs(sqls)
    group_number = len(sqls)
    ret = {}
    for i in range(group_number+1):
        ret[i] = []
    for i in pair_list:
        print("comparing ... ",i[0], i[1])
        score_key = group_score(similar(sqls[i[0]], sqls[i[1]]), group_number)
        ret[score_key].append(i)
    return ret


def change_group_tag_to_key(group_dict:dict):
    ret={}
    for k,v in group_dict.items():
        if v in ret:
            ret[v].append(k)
            continue
        ret[v] = [k]
    return ret


def generate_group(histo:dict, acc:int = 0)->dict:
    group_num = len(histo)-1
    if acc >= group_num:
        print("Wrong accuracy number...")
        return {}
    max_tag = 0
    ret = {}
    for i in range(group_num - acc):
        for item in histo[group_num - i]:
            if item[0] in ret and item[1] in ret:
                # both has a group tag
                continue
            if item[0] in ret:
                ret[item[1]] = ret[item[0]]
                continue
            if item[1] in ret:
                ret[item[0]] = ret[item[1]]
                continue
            # else 
            ret[item[0]] = max_tag
            ret[item[1]] = max_tag
            max_tag+=1
    ret = change_group_tag_to_key(ret)    
    return ret

