# coding: utf-8
from vis.models.indexed_piece import Importer
with open('all_scores.txt') as f:
    pathnames = f.readlines()
    pathnames = [f.strip() for f in pathnames]
    for filename in pathnames:
        print(filename)
        s = Importer(filename)
        if s:
            print('\t Importing to vis... Ok')
        else:
            print('\t Importing to vis... Error')
            
