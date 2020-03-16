import os
from surprise import SVD
from surprise import SVDpp
from surprise import Dataset
from surprise import accuracy
from surprise.model_selection import train_test_split
from surprise import KNNBasic
from surprise import BaselineOnly
from surprise import Reader
from surprise.model_selection import KFold
from surprise.model_selection import cross_validate
from surprise.model_selection import GridSearchCV
import pandas as pd



#指定文件所在路径
file_path=os.path.expanduser('./data/ratings.dat')
#告诉文本阅读器，文本的格式是怎样的
reader=Reader(line_format='user item rating timestamp',sep="::")
#加载数据
surprise_data=Dataset.load_from_file(file_path,reader=reader)

all_trainset = surprise_data.build_full_trainset()
algo = KNNBasic(k=40,min_k=10,sim_options={'user_based': True}) # sim_options={'name': 'cosine','user_based': True} cosine/msd/pearson/pearson_baseline
algo.fit(all_trainset)

def getSimilarUsers(top_k,u_id):
    user_inner_id = algo.trainset.to_inner_uid(u_id)
    user_neighbors = algo.get_neighbors(user_inner_id, k=top_k)
    user_neighbors = (algo.trainset.to_raw_uid(inner_id) for inner_id in user_neighbors)
    return user_neighbors

print(list(getSimilarUsers(10,'1')))

item_algo = KNNBasic(k=40,min_k=3,sim_options={'user_based': False}) # sim_options={'name': 'cosine','user_based': True} cosine/msd/pearson/pearson_baseline
item_algo.fit(all_trainset)

print("OK")

def getSimilarItems(top_k,item_id):
    item_inner_id = item_algo.trainset.to_inner_iid(item_id)
    item_neighbors = item_algo.get_neighbors(item_inner_id, k=top_k)
    f_item_neighbors = (item_algo.trainset.to_raw_iid(inner_id)
                       for inner_id in item_neighbors)
    return f_item_neighbors

print(list(getSimilarItems(10,'1')))



