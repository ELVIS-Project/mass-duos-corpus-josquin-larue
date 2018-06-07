# coding: utf-8
from vis.models.indexed_piece import Importer
import copy
import numpy as np
import operator
import json
import sys

horiz_setts = {
'quality': False,
'simple or compound': 'compound',
'directed': True
}

vert_setts = {
'quality': False,
'simple or compound': 'compound',
'directed': True,
}

ngram_setts = {
'n': 3,
'vertical': 'all',
'horizontal': 'all'
}

globalngrams = {}
ngramsperscore= {}

def heldAsRepeated(df):
	return df.fillna(method='ffill')

def ignoreRests(df):
	tmpdf = df[df != "Rest"]
	return tmpdf.dropna(how="any")

def cutRests(df):
    levels = df.columns.levels
    # Stupid pandas black-magic to index MultiIndex dataframes
    i = levels[0][0]
    k = levels[1][0]
    ##########################################################
    new_indexes = df[i][k].apply(lambda x: 'Rest' not in x)
    return df[new_indexes]

def halfNoteSlices(df):
	a = np.arange(df.index[0], df.index[-1] + 2.0, 2.0)
	tmpdf = df.reindex(df.index.union(a))
	tmpdf = tmpdf.fillna(method='ffill')
	return tmpdf.reindex(a)

def removeDuplicates(df):
	tmpdf = df[df != df.shift(1)].dropna(how='all')
	return tmpdf.fillna(method='ffill')
           
# Half note slices, ignoring rests in one voice + no repeats
def analysisHalfNotesNoRepeats(s):
	hn = copy.deepcopy(s)
	hnnr = hn.get_data('noterest')
	hnnr = halfNoteSlices(hnnr)
	hnnr = ignoreRests(hnnr)
	hnnr = removeDuplicates(hnnr)
	hn._analyses['noterest'] = hnnr
	hnv = hn.get_data('vertical_interval', settings=vert_setts)
	hnh = hn.get_data('horizontal_interval', settings=horiz_setts)
	hnngram = hn.get_data('ngram', data=[hnv,hnh], settings=ngram_setts)
	return hn, hnngram


# Half note slices, cutting ngrams when finding a rest in one voice
def analysisHalfNotesCutAtRestNoRepeats(s):
    hn = copy.deepcopy(s)
    hnnr = hn.get_data('noterest')
    hnnr = halfNoteSlices(hnnr)    
    hnnr = removeDuplicates(hnnr)
    hn._analyses['noterest'] = hnnr
    hnv = hn.get_data('vertical_interval', settings=vert_setts)
    hnh = hn.get_data('horizontal_interval', settings=horiz_setts)
    hnngram = hn.get_data('ngram', data=[hnv,hnh], settings=ngram_setts)
    # Easier to get the ngrams first and filter later
    hnngram = cutRests(hnngram)    
    return hn, hnngram


# Half note slices, ignoring rests in one voice
def analysisHalfNotes(s):
	hn = copy.deepcopy(s)
	hnnr = hn.get_data('noterest')
	hnnr = halfNoteSlices(hnnr)
	hnnr = ignoreRests(hnnr)
	hn._analyses['noterest'] = hnnr
	hnv = hn.get_data('vertical_interval', settings=vert_setts)
	hnh = hn.get_data('horizontal_interval', settings=horiz_setts)
	hnngram = hn.get_data('ngram', data=[hnv,hnh], settings=ngram_setts)
	return hn, hnngram

# Attacks only, ignoring rests in one voice
def analysisAttackNotes(s):
	an = copy.deepcopy(s)
	annr = an.get_data('noterest')
	annr = heldAsRepeated(annr)
	annr = ignoreRests(annr)
	an._analyses['noterest'] = annr
	anv = an.get_data('vertical_interval', settings=vert_setts)
	anh = an.get_data('horizontal_interval', settings=horiz_setts)
	anngram = an.get_data('ngram', data=[anv,anh], settings=ngram_setts)
	return an, anngram

# Half note slices, marking rests in one voice as ngrams
def analysisHalfRests(s):
	hr = copy.deepcopy(s)
	hrnr = hr.get_data('noterest')
	hrnr = halfNoteSlices(hrnr)
	hr._analyses['noterest'] = hrnr
	hrv = hr.get_data('vertical_interval', settings=vert_setts)
	hrh = hr.get_data('horizontal_interval', settings=horiz_setts)
	hrngram = hr.get_data('ngram', data=[hrv,hrh], settings=ngram_setts)
	return hr, hrngram

# Attacks only, marking rests in one voice as ngrams
def analysisAttackRests(s):
	ar = copy.deepcopy(s)
	arnr = ar.get_data('noterest')
	arnr = heldAsRepeated(arnr)
	ar._analyses['noterest'] = arnr
	arv = ar.get_data('vertical_interval', settings=vert_setts)
	arh = ar.get_data('horizontal_interval', settings=horiz_setts)
	arngram = ar.get_data('ngram', data=[arv,arh], settings=ngram_setts)
	return ar, arngram

def inverseNGramDict(d, file):
	reverse = {}
	for offset,ngram in d.items():
		reverse[ngram] = reverse.get(ngram, [])
		reverse[ngram].append((file, offset))
		globalngrams[ngram] = globalngrams.get(ngram, [])
		globalngrams[ngram].append((file, offset))
	return reverse

def printGlobalNGram():
	for k,v in globalngrams.items():
		print('{}\t{}\t{}'.format(len(v),k,v))


def runAnalysis(scorelist, output_json, output_tsv):
	with open(scorelist) as f:
	    pathnames = f.readlines()
	    pathnames = [f.strip() for f in pathnames]
	    for filename in pathnames:
	        print(filename)
	        s = Importer(filename)
	    	### Workaround for getting the part names because the 'all' setting in vis-framework does not seem to be working for horizontal intervals
	        parts = [x.id for x in s._analyses['part_streams']]
	        parts = list(reversed(parts))
	        parts = [tuple(parts)]
	        ngram_setts['horizontal'] = parts
	        ###################################
	        hn, ngrams = analysisHalfNotesCutAtRestNoRepeats(s)
	        ngramdict = ngrams.iloc[:,0].to_dict()
	        reversengram = inverseNGramDict(ngramdict, filename)
	        ngramsperscore[filename] = ngramdict              

	    with open(output_json, 'w') as o:
	    	o.write(json.dumps(ngramsperscore, sort_keys=True, indent=4))
	   
	    with open(output_tsv, 'w') as o:
	    	top10 = []
	    	header = 'Occurrences\tNGram\tComposer\tWork\tOffset (Minim)\n'
	    	o.write(header)
	    	for k,v in sorted(globalngrams.items(), reverse=True, key=lambda kv: len(kv[1])):
	    		top10.append('{}, {}'.format(len(v),k))
	    		o.write('{}\t{}\n'.format(len(v),k))
	    		for x in v:
	    			offset = x[1]
	    			f = x[0].split('/')
	    			composer = f[2]
	    			work = f[3]
	    			o.write('\t\t{}\t{}\t{}\n'.format(composer,work,offset))
	    print('Top 10')
	    for x in top10[:10]:
	    	print('\t',x)

if __name__ == '__main__':
	scorelist = sys.argv[1]
	output_json = sys.argv[2]
	output_tsv = sys.argv[3]
	runAnalysis(scorelist, output_json, output_tsv)