import itertools, uuid, hashlib, math
import matplotlib
import matplotlib.pyplot as plt
from time import time
 

def  main():
	indexes = [i for i in range(1,5)]

	sample = "D0.txt"
	char2_dict = dict()
	char3_dict = dict()
	word2_dict = dict()
	G2_Jaccard = dict()
	print("Problem 1. Creating k-Grams\n")
	print("1A. Distinct k-grams for each document:\n")
	for index in indexes:
		filename = sample.replace("0", '' + str(index))
		
		data = open(filename,'r').read()
		char2,char2_len = char_k_grams(data,2)
		char3,char3_len = char_k_grams(data,3)
		word2,word2_len = word_k_grams(data.split(),2)

		char2_dict[filename] = char2
		char3_dict[filename] = char3
		word2_dict[filename] = word2
		print("===============================================\n")
		print("Document %s\n" % filename )
		print("Number of 2-grams based on characters: %s\n" 
			% str(char2_len))
		print("Number of 3-grams based on characters: %s\n" 
			% str(char3_len))
		print("Number of 2-grams based on words: %s\n"
			% str(word2_len))
	print("===============================================\n")
	print("1B. Jaccard similarity between: \n")
	cbine =  itertools.combinations(indexes, 2)
	for pair in cbine:
		doc1 = sample.replace("0", '' + str(pair[0]))
		doc2 = sample.replace("0", '' + str(pair[1]))
		print("===============================================\n")
		js = len(char2_dict[doc1].intersection(char2_dict[doc2]))/len(char2_dict[doc1].union(char2_dict[doc2]))
		print("%s %s 2-grams based on characters: %.4f\n" 
			% (doc1,doc2,js))
		js = len(char3_dict[doc1].intersection(char3_dict[doc2]))/len(char3_dict[doc1].union(char3_dict[doc2]))
		G2_Jaccard[doc1+doc2] = js
		print("%s %s 3-grams based on characters: %.4f\n" 
			% (doc1,doc2,js))
		js = len(word2_dict[doc1].intersection(word2_dict[doc2]))/len(word2_dict[doc1].union(word2_dict[doc2]))
		print("%s %s 2-grams based on words: %.4f\n" 
			% (doc1,doc2,js))
		print("\n")

	print("===============================================\n")
	print("Problem 2. Min Hashing\n")
	print("2A. Min Hashing using grams G2 for D1 and D2: \n")
	doc1 = char3_dict["D1.txt"]
	doc2 = char3_dict["D2.txt"]
	ts = [20, 60, 150, 300, 600, 750, 900, 1050, 1200, 1350]
	# ts = [20, 60, 150, 300, 600, 750]
	tv = []
	tt = []
	for t in ts:
		start = time()
		v = min_hashing(doc1,doc2,t)
		tt.append(time()-start)
		tv.append('%.2f' % v)
		print("t = %d: %.2f" % (t,v))
	ac = G2_Jaccard["D1.txt"+"D2.txt"]
	second_b_plot(ts,tv,tt,'%.2f' % ac)

	print("===============================================\n")
	print("Problem 3. LSH\n")
	print("3A. Find b and r for f(s) with t=160: \n")
	t = 160
	tao = 0.7
	b = 14.2291#(-math.log(t,tao))
	print("b = %.4f\n" % b)
	r = 159.99834#math.pow(tao,-b)
	print("r = %.4f\n" % r)
	print("3B. Probability of each G2 pair for being estimated to having similarity grate than tao=.7: \n")
	indexes = [i for i in range(1,5)]
	cbine =  itertools.combinations(indexes, 2)
	for pair in cbine:
		doc1 = sample.replace("0", '' + str(pair[0]))
		doc2 = sample.replace("0", '' + str(pair[1]))
		s = G2_Jaccard[doc1+doc2]
		p = 1 - math.pow(1-math.pow(s,b),r)
		print("pr[%s %s] = %.12f\n" % (doc1,doc2,p))


def second_b_plot(ts,tv,tt,ac):
	fig = plt.figure()
	ax1 = fig.add_subplot(1,2,1)
	ax2 = fig.add_subplot(1, 2, 2)
	ax1.plot(ts, tv, label='Accuracy')
	ax1.axhline(y=ac,c='red')
	ax2.plot(ts, tt, label='Time')

	ax1.set_xlabel('Value of t')
	ax1.set_ylabel('Accuracy')
	ax1.set_title('Accuracy per t')
	ax1.legend()
	ax2.set_xlabel('Value of t')
	ax2.set_ylabel('Time it takes')
	ax2.set_title('Running time per t')
	ax2.legend()

	plt.show()

def min_hashing(doc1,doc2,t):
	a = []
	b = []
	for index in range(t):
		salt = uuid.uuid4().hex
		a.append(min(int(apply_salt(i,salt),16) % t for i in doc1))
		b.append(min(int(apply_salt(i,salt),16) % t for i in doc2))

	return sum(i==j for i,j in zip(a,b))/t

	# return sum([i==j for i in itertools.islice(a,t) 
	# 		for j in itertools.islice(a,t)])/t

def apply_salt(gram,salt):
    return hashlib.sha1(salt.encode() + gram.encode()).hexdigest()

def char_k_grams(doc,k):
	out = set([doc[i:i+k] for i in range(len(doc)-1)])
	return out,len(out)

def word_k_grams(str_array,k):
	out = set(list(zip(*[str_array[i:] for i in range(k)])))
	return out,len(out)





if __name__ == "__main__":
	main()