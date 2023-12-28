import src.util as util

if __name__ == "__main__":
    print("this is main.")
    sqls_list = util.get_sql_list("./sqls")
    compare_pairs = util.generate_pairs(sqls_list)
    assert util.check_same(compare_pairs) == False
    result_histo = util.generate_histo_dict(sqls_list)
    for acc in range(0, len(result_histo)-1, 2):
        print("The acc is ", acc)
        group_dict = util.generate_group(result_histo, acc)
        
        for k,v in group_dict.items():
            print(k, v)
        