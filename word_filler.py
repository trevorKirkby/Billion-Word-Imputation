import pickle
import collections

def save_object(obj, filename):
	with open(filename, 'wb') as output:
		pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

def open_object(filename):
	with open(filename, 'rb') as theinput:
		new_object = pickle.load(theinput)
		return new_object

def classify(word):
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

def load(infile="train_v2.txt"):                                            #given the size of the file, possibly pickle several chunks of the full triplet dictionary. load each in turn to get what their data states the sentences should be filled with. then compares the results at the end.
	num2word = open_object("all_words_list.pkl")                            #contains a list of all words in text file (no repeats)
	word2num = dict(zip(num2word,range(len(num2word))))
	info = open(infile,"r")
	triplets = {}
	for index, line in enumerate(info):
		if index%100000 == 0:                                               #gives a progress update every 100,000 lines
			print "\nreading line:", index, "\nlength of dictionary", len(triplets.keys())
		line = line.split()
		for middle in range(1,len(line)-2):                                 #retrieves indexes for the middles of each triplet of words.
			first = word2num[line[middle-1]]
			second = word2num[line[middle]]
			third = word2num[line[middle+1]]
			key = (first, third)
			seconds = triplets.get(key,[])
			seconds.append(second)
			triplets[key] = seconds                                         #stores the dictionary with the sets of two words in a tuple as they key, and what goes between them as the value.
	return triplets

def replace(infile="test_v2.txt",outfile="test_v2_solution.txt"):
	pass