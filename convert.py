#!/usr/bin/env python

"""
4m20
"""

import cPickle as pickle
#import pickle
import numpy as np

def main():
	f = open('dict.dat','r')
	d = pickle.load(f)
	f.close()
	words = np.array(d.keys())
	freqs = np.array(d.values())
	del d

	mapper = dict(zip(words,range(len(words))))

	nwords = np.sum(freqs)
	codes = np.empty(nwords,dtype=np.int32)
	f = open('train_v2.txt','r')
	line_count,word_count = 0,0
	for line in f:
		line_count += 1
		if line_count % 100000 == 0:
			print 'processed %dK lines' % (line_count/1000)
		for word in line.split():
			codes[word_count] = mapper[word]
			word_count += 1
	f.close()
	print 'Read %d lines and %d words (%d unique)' % (line_count,word_count,len(mapper))

	np.savez_compressed('train.npy',words=words,freqs=freqs,codes=codes)

if __name__ == '__main__':
	main()
