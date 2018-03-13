from itertools import islice

def main():
	data = open('D1.txt','r').read()

	print(word_k_grams(data.split(),2))


def char_k_grams(doc,k):
	return set([doc[i:i+k] for i in range(len(doc)-1)])

# kgram = set()
# length = len(doc)- k + 1; 
# for i in range(length):
# 	kgram.add(doc[i:i+k])
# return kgram

def word_k_grams(str_array,k):
	return set(list(zip(*[str_array[i:] for i in range(k)])))

if __name__ == '__main__':
	main()