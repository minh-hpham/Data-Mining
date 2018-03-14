import uuid,hashlib

def main():

	# filename = "test.txt"
	# f = list(open(filename).read())
	# # print(f)
	# part1(f,filename)

	filename = "S1.txt"
	f = list(open(filename).read())
	part1(f,filename)
	print("\n")
	part2(f,filename)
	filename = "S2.txt"
	f = list(open(filename).read())
	print("\n")
	part1(f,filename)
	print("\n")
	part2(f,filename)
	

def part1(f,filename):
	print("In %s" % filename)

	counters = 9
	C,L = misra_gries(counters,len(f),f)
	print(L)
	print(C)

	phi = 0.2
	report_occurence(len(f),phi,counters+1,C,L)


def part2(f,filename):
	print("In %s" % filename)
	k = 10
	t = 5
	salts = random_salt(t)

	C = min_sketch(10,5,f,salts)
	fa_hat = min([C[j][hash_with_salt('a',salts[j],k)] for j in range(t)])
	fb_hat = min([C[j][hash_with_salt('b',salts[j],k)] for j in range(t)])
	fc_hat = min([C[j][hash_with_salt('c',salts[j],k)] for j in range(t)])
	

	m = len(f)
	# me = m*(2/k)
	phi = 0.2
	print("f^a %d might occur more than 20%% of the time: %r" % (fa_hat,fa_hat>(phi*m)))
	print("f^b %d might occur more than 20%% of the time: %r" % (fb_hat,fb_hat>(phi*m)))
	print("f^c %d might occur more than 20%% of the time: %r" % (fc_hat,fc_hat>(phi*m)))



def misra_gries(counters,m,doc):
	C = [0]*counters
	L = ['']*counters
	for i in doc:
		j = L.index(i) if i in L else None
		if j is not None:
			C[j] += 1
		else:
			j = C.index(0) if 0 in C else None
			if j is not None:
				L[j] = i
				C[j] = 1
			else:
				C[:] = [c-1 for c in C]
	return C,L


def min_sketch(k,t,doc,salts):
	C = [[0]*k for i in range(t)]
	for a in doc:
		for j in range(t):
			C[j][hash_with_salt(a,salts[j],k)] += 1
	return C


def random_salt(number_of_functions):
	return [uuid.uuid4().hex for i in range(number_of_functions)]

def hash_with_salt(char,salt,k):
    return int(hashlib.sha1(salt.encode() + char.encode()).hexdigest(),16) % k

def report_occurence(m,phi,k,counts,labels):
	# might = sum([fj for fj in counts if ((phi-epsilon)<=fj and fj<phi)])
	might = sum([(cj+(m/k))>(m*phi) for cj in counts])
	must = [labels[j] for j,cj in enumerate(counts) if cj>(m*phi)]

	print("%d objects might occur more than 20%% of the time" % might)
	print("%s must occur more than 20%% of the time" % str(must))

if __name__ == "__main__":
	main()