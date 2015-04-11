#!/usr/bin/env python

"""
4m20
"""

import cPickle as pickle
import numpy as np

def sanitize(word):
	if "://" in word:
		return "URL"
	if "" in word.split("-"):
		if word.split("-").remove(""):
			if len(word.split("-").remove("")) > 3: #more than three and it isn't a hyphenated word, it is a hyphenated sentence.
				return "EXCESSIVE_HYPHENS"
	else:
		if len(word.split("-")) > 3:
			return "EXCESSIVE_HYPHENS"
	if word.count("-") > 15 or word.count(".") > 15:
		return "PUNCTUATION_BLOCK"
	if word.count(collections.Counter(word).most_common(1)[0][0]) > 30:
		return "SPAM"
	if len(word) > 10:
		intervals = []  #Tracks patterns. If it finds repetition, assumes word is spam.
		last_found = 0
		for index in range(len(word)):
			found = word.find(collections.Counter(word).most_common(1)[0][0],index)
			if found != last_found:
				intervals.append(found-last_found)
			last_found = found
		if len(set(intervals[1:-1])) <= 1:
			return "SPAM"
	if "-" in word:
		return "HYPHENATED"
	if len(word) > 20:
		return "TOO_LONG"
	if word == "," or word == ":" or word == ";" or word == "\"" or word == "'" or word == "--" or word == "-" or word == ".":
		return "PUNCTUATION_MARK"
	return word

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
	f = open('/data/kaggle/train_v2.txt','r')
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
