import uuid,hashlib

def main():
	filename = "S1.txt"
	f = list(open(filename).read())
	# print(f)
	part1(f,filename)
	filename = "S2.txt"
	f = list(open(filename).read())
	part1(f,filename)
	# part2(f)
	

def part1(f,filename):
	counters = 9
	C,L = misra_gries(counters,len(f),f)
	phi = 0.2
	report_occurence(filename,len(f),phi,counters+1,C,L)


def part2(f):
	k = 10
	t = 5
	salts = random_salt(t)

	C = min_sketch(10,5,f,salts)
	print(min([C[j][hash_with_salt('a',salts[j],k)] for j in range(t)]))
	print(min([C[j][hash_with_salt('b',salts[j],k)] for j in range(t)]))
	print(min([C[j][hash_with_salt('c',salts[j],k)] for j in range(t)]))

def misra_gries(counters,m,doc):
	C = [0]*counters
	L = ['']*counters
	for i in doc:
		j = L.index(i) if i in L else None
		if j is not None:
			C[j] += 1
		else:
			# print(j)
			j = C.index(0) if 0 in C else None
			# print("index of 0 " + str(j))
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

def report_occurence(filename,m,phi,k,counts,labels):
	# might = sum([fj for fj in counts if ((phi-epsilon)<=fj and fj<phi)])
	might = sum([(cj+m/(2*k))>m*phi for cj in counts])
	must = sum([cj>m*phi for cj in counts])
	print("%d objects might occur more than 20%% of the time in %s" % (might,filename))
	print("%s must occur more than 20%% of the time in %s" % (str(must),filename))

if __name__ == "__main__":
	main()