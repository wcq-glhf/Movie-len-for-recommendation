# -*- coding: utf-8 -*-
import sys
from preprocess import Channel
from workflow.cf_workflow import run as user_cf
from workflow.lfm_workflow import run as lfm
from workflow.prank_workflow import run as prank
from workflow.item_cf_workflow import run as item_cf


def manage():
    # arg = sys.argv[1]
    arg = 'lfm'
    if arg == 'preprocess':
        Channel().process()
    elif arg == 'itemcf':
        item_cf()
    elif arg == 'cf':
        user_cf()
    elif arg == 'lfm':
        lfm()
    elif arg == 'prank':
        prank()
    else:
        print('Args must in ["preprocess", "cf", "lfm"，"prank"].')
    sys.exit()


if __name__ == '__main__':
    manage()
