#!/usr/bin/env python

"""
Read 30301028 lines and 768648884 words (2425337 unique) [~5 mins]
"""

import cPickle as pickle
#import pickle

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
	d = { }
	f = open('/data/kaggle/train_v2.txt','r')
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
