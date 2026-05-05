from node import *
import pandas as pd
import time
import random

df = pd.read_csv("student.csv")
storage = df.to_dict('records')

random.seed(10)

def calc_utilization(tree):
    return (tree.key_cnt / (tree.node_cnt*tree.order*2))

def get_avg_insert_time(tree, order, times):
    res = 0
    for i in range(times):
        btree = tree(order)
        start = time.perf_counter()
        for rid, records in enumerate(storage):
            btree.insert(records['Student ID'], rid)
        end = time.perf_counter()
        res += (end - start)*1000 #ms
        split_cnt = btree.split_cnt
        util = calc_utilization(btree)
    
    return btree, res/times, split_cnt, util

# exp1

for d in [3, 5, 10]:
    print(f"\n============= Exp1 (d={d}) =============")

    btree, btree_insert_time, btree_split_cnt, btree_util = get_avg_insert_time(BTree, d, 3)
    bplus, bplus_insert_time, bplus_split_cnt, bplus_util = get_avg_insert_time(BPlusTree, d, 3)
    bstar, bstar_insert_time, bstar_split_cnt, bstar_util = get_avg_insert_time(BStarTree, d, 3)

    print(f"Btree insert time avg : {btree_insert_time:.3f}ms")
    print(f"B+tree insert time avg : {bplus_insert_time:.3f}ms")
    print(f"B*tree insert time avg : {bstar_insert_time:.3f}ms")

    print(f"Btree split count : {btree_split_cnt}")
    print(f"B+tree split count : {bplus_split_cnt}")
    print(f"B*tree split count : {bstar_split_cnt}")

    print(f"Btree utilization : {(btree_util*100):.3f}%")
    print(f"B+tree utilization : {(bplus_util*100):.3f}%")
    print(f"B*tree utilization : {(bstar_util*100):.3f}%")


# exp2
d = 5
print(f"\n============= Exp2 (d={d}) =============")

btree, _, _, _ = get_avg_insert_time(BTree, d, 1)
bplus, _, _, _ = get_avg_insert_time(BPlusTree, d, 1)
bstar, _, _, _ = get_avg_insert_time(BStarTree, d, 1)

keys = []
for records in storage:
    keys.append(records['Student ID'])

random_keys = random.sample(keys, 10000)

def get_avg_search_time(tree, keys):
    start = time.perf_counter()
    for key in keys:
        tree.search(key)
    end = time.perf_counter()
    return ((end-start) / len(keys)) * 1000

btree_search_time = get_avg_search_time(btree, random_keys)
bplus_search_time = get_avg_search_time(bplus, random_keys)
bstar_search_time = get_avg_search_time(bstar, random_keys)

print(f"Btree avg search time : {btree_search_time:.6f}ms")
print(f"B+tree avg search time : {bplus_search_time:.6f}ms")
print(f"B*tree avg search time : {bstar_search_time:.6f}ms")


# exp 3

print(f"\n============= Exp3 (d={d}) =============")

def calc_range_query(tree, start, end):
    if isinstance(tree, BPlusTree):
        time_start = time.perf_counter()
        rids = tree.range_query(start, end)

        gpa_sum = 0
        height_sum = 0
        male_cnt = 0
        gpa_avg = 0
        height_avg = 0
        
        for rid in rids:
            record = storage[rid]
            if record["Gender"] == "Male" :
                gpa_sum += record["GPA"]
                height_sum += record["Height"]
                male_cnt += 1
        
        if male_cnt > 0:
            gpa_avg = gpa_sum / male_cnt
            height_avg = height_sum / male_cnt
        
        time_end = time.perf_counter()

    else:
        keys = []
        for row in storage:
            key = row['Student ID']
            if key >= start and key <= end :
                keys.append(key)

        time_start = time.perf_counter()
        gpa_sum = 0
        height_sum = 0
        male_cnt = 0
        gpa_avg = 0
        height_avg = 0

        for key in keys:
            rid = tree.search(key)
            record = storage[rid]
            if record["Gender"] == "Male" :
                gpa_sum += record["GPA"]
                height_sum += record["Height"]
                male_cnt += 1

        if male_cnt > 0:
            gpa_avg = gpa_sum / male_cnt
            height_avg = height_sum / male_cnt
        
        time_end = time.perf_counter()

    return (time_end - time_start)*1000, gpa_avg, height_avg

btree_range_query_time, btree_gpa, btree_height = calc_range_query(btree, 202000000, 202100000)
bplus_range_query_time, bplus_gpa, bplus_height = calc_range_query(bplus, 202000000, 202100000)
bstar_range_query_time, bstar_gpa, bstar_height = calc_range_query(bstar, 202000000, 202100000)


print(f"Btree range query time : {btree_range_query_time:.3f}ms  , avg gpa : {btree_gpa:.3f}, avg height : {btree_height:.3f}")
print(f"B+tree range query time : {bplus_range_query_time:.3f}ms , avg gpa : {bplus_gpa:.3f}, avg height : {bplus_height:.3f}")
print(f"B*tree range query time : {bstar_range_query_time:.3f}ms , avg gpa : {bstar_gpa:.3f}, avg height : {bstar_height:.3f}")


#exp 4
print(f"\n============= Exp4 (d={d}) =============")

keys = []
for records in storage:
    keys.append(records['Student ID'])

r_keys_2000 = random.sample(keys, 2000)
r_keys_10p = random.sample(keys, 10000)
r_keys_20p = random.sample(keys, 20000)


def node_check(tree, node):

    if isinstance(tree, BPlusTree):
        if node.is_leaf:
            if len(node.keys) != len(node.rids):
                return False
        else:
            if len(node.rids) != 0:
                return False
    else:
        if len(node.keys) != len(node.rids):
            return False

    for i in range(len(node.keys)-1):
        if node.keys[i] >= node.keys[i+1]:
            return False # key not sorted

    if node != tree.root:
        if len(node.keys) < tree.order:
            return False #underflow error
 
        if len(node.keys) > 2*tree.order:
            return False # overflow error
    
    if not node.is_leaf :
        if len(node.child) != len(node.keys)+1:
            return False # child count error

        for child in node.child:
            if child.parent != node:
                return False # parent pointer error
        
        for child in node.child:
            if not node_check(tree, child):
                return False

    return True

def leaf_link_check(tree):
    node = tree.root
    while not node.is_leaf:
        node = node.child[0]

    prev_key = None
    while node is not None:
        for key in node.keys:
            if prev_key is not None and prev_key >= key:
                return False
            prev_key = key
        node = node.next
    
    return True

def tree_integrity_check(tree):

    flag = node_check(tree, tree.root)

    if isinstance(tree, BPlusTree):
        flag = flag and leaf_link_check(tree)

    return flag


def delete_exp(tree, keys):
    flag = True

    start = time.perf_counter()

    for key in keys:
        tree.delete(key)
    
    end = time.perf_counter()

    for key in keys:
        if tree.search(key) != -1:
            flag = False

    flag = flag and tree_integrity_check(tree)

    return (end - start) * 1000, flag

for delete_keys, mode in [(r_keys_2000, "2000"), (r_keys_10p, "10 percent"), (r_keys_20p, "20 percent")]:
    btree, _, _, _ = get_avg_insert_time(BTree, d, 1)
    bplus, _, _, _ = get_avg_insert_time(BPlusTree, d, 1)
    bstar, _, _, _ = get_avg_insert_time(BStarTree, d, 1)

    btree_delete_time, btree_integrity = delete_exp(btree, delete_keys)
    bplus_delete_time, bplus_integrity = delete_exp(bplus, delete_keys)
    bstar_delete_time, bstar_integrity = delete_exp(bstar, delete_keys)

    print(f"\n ---- delete {mode} ----")
    print(f"Btree delete time : {btree_delete_time:.3f}ms, integrity test : {btree_integrity}")
    print(f"B+tree delete time : {bplus_delete_time:.3f}ms, integrity test : {bplus_integrity}")
    print(f"B*tree delete time : {bstar_delete_time:.3f}ms, integrity test : {bstar_integrity}")