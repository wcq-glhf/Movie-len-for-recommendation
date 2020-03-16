# coding: utf-8 -*-
import math
import pandas as pd
import time
from numpy import *


class ItemCf:

    def __init__(self):
        self.file_path = 'data/ratings.csv'
        self._init_frame()

    def _init_frame(self):
        self.frame = pd.read_csv(self.file_path)

    @staticmethod
    def _cosine_sim(target_movies, movies):
        '''
        simple method for calculate cosine distance.
        e.g: x = [1 0 1 1 0], y = [0 1 1 0 1]
             cosine = (x1*y1+x2*y2+...) / [sqrt(x1^2+x2^2+...)+sqrt(y1^2+y2^2+...)]
             that means union_len(movies1, movies2) / sqrt(len(movies1)*len(movies2))
        '''
        union_len = len(set(target_movies) & set(movies))
        if union_len == 0: return 0.0
        product = len(target_movies) * len(movies)
        cosine = union_len / math.sqrt(product)
        return cosine

    def get_correlation_items(self):
        '''
        calculate correlation_items
        '''
        start=time.time()
        item_dict={}
        all_movies=list(set(self.frame['MovieID']))  #取重同时为了算后边物品之间的相关度



        all_movies_users=[self.frame[self.frame["MovieID"]== i]["UserID"] for i in all_movies]     #提前计算电影用户的数量防止后边计算浪费时间
        all_movies_users_count=[len(i) for i in all_movies_users]
        item_relateditems = dict()
        for i in range(len(all_movies)):
            for j in range(len(all_movies)):
                if all_movies[j]==all_movies[i]:
                    pass
                else:

                    if all_movies[i] not in item_relateditems:
                        item_relateditems[all_movies[i]] = set()
                    item_relateditems[all_movies[i]].add(all_movies[j])

                    if (all_movies[j],all_movies[i]) in item_dict:
                        item_dict[(all_movies[i],all_movies[j])]=item_dict[(all_movies[j],all_movies[i])]
                    else:
                        item_dict[(all_movies[i],all_movies[j])]=len((set(all_movies_users[i])&set(all_movies_users[j])))/math.sqrt(all_movies_users_count[i]*all_movies_users_count[j])

        print("物品相关度计算完毕,花费时间{}".format(time.time()-start))
        return item_dict,item_relateditems

    def get_top_n_items(self, item_relateditems, target_user_id, item_dict, k, top_n):
        '''
        calculate the top_n_items
        :param target_user_id:
        :param item_dict:     items hashtable
        :param k:       the most correlation items' amount of the item
        :param top_n:   to recommend the goods
        :return:
        '''
        target_user_item=self.frame[self.frame["UserID"]==target_user_id]["MovieID"]
        candidates_items = set()
        for item in target_user_item:
            candidates_items = candidates_items.union(item_relateditems[item])  # 候选列表

        all_item=self.frame["MovieID"]
        all_score=[]


        for i in range(len(candidates_items)):
            print("物品{}".format(i))
            item=list(candidates_items)[i]
            print(item)
            item_sort_list=[]

            items=item_relateditems[item]
            for j in items:
                if j==item:
                    pass
                else:
                    item_sort_list.append((j,item_dict[(item,j)]))


            item_sort_list = sorted(item_sort_list, key=lambda x: x[1], reverse=True)[:k]


            temp=[i for i in item_sort_list if i[0] in set(target_user_item)]
            all_score.append((item, sum([i[1] * float(self.frame[(self.frame["MovieID"]==i[0]) & (self.frame["UserID"]==target_user_id)]["Rating"].values) for i in temp])))


        all_score=sorted(all_score, key=lambda x:x[1],reverse=True)[:top_n]

        return all_score

    def calculate(self, target_user_id=1, top_n=8, k=5):
        """
        user-cf for movies recommendation.
        """

        #calculate correlation of items
        item_dict,item_relateditems=self.get_correlation_items()
        top_n_movies=self.get_top_n_items(item_relateditems,target_user_id,item_dict,k,top_n)

        return top_n_movies
