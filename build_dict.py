#!/usr/bin/env python

"""
Read 30301028 lines and 768648884 words (2425337 unique) [~5 mins]
"""

import cPickle as pickle
#import pickle

def main():
	d = { }
	f = open('train_v2.txt','r')
	line_count,word_count = 0,0
	for line in f:
		line_count += 1
		if line_count % 100000 == 0:
			print 'processed %dK lines' % (line_count/1000)
		for word in line.split():
			word_count += 1
			count = d.get(word,0) + 1
			d[word] = count
	f.close()
	print 'Read %d lines and %d words (%d unique)' % (line_count,word_count,len(d))

	f = open('dict.dat','w')
	#pickle.dump(d,f,protocol=2)
	pickle.dump(d,f)
	f.close()

if __name__ == '__main__':
	main()
