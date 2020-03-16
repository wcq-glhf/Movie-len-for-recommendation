# -*- coding: utf-8 -*-
import time
import os
from model.item_cf import ItemCf


def run():
    assert os.path.exists('data/ratings.csv'), \
        'File not exists in path, run preprocess.py before this.'
    print('Start..')
    start = time.time()
    movies = ItemCf().calculate()
    for movie in movies:
        print(movie)
    print('Cost time: %f' % (time.time() - start))
