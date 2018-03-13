import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from random import randint
from time import time

def  main():
	# birthday paradox
	# k = coupon_A(250)
	# print(k)
	# coupon_B_plot_C()
	coupon_D()

def coupon_A(n):
	# numbers = [0]*(n+1)
	generated = set()
	repeated = set()
	trials = 1
	generated.add(randint(0,n))
	while True:
		trials += 1
		x = randint(0,n) # 0 <= x <= n
		if x in repeated:
			continue
		elif x in generated:
			generated.remove(x)
			repeated.add(x)
		else:
			generated.add(x)
		if len(generated) == 0:
			break

		# numbers[x] += 1
		# if min(numbers) > 1:
		# 	break

	return trials

def coupon_B(m,n):
	trials = list()
	for i in range(m):
		trials.append(coupon_A(n))
	x = list(set(trials))
	y = [sum(j <= i for j in trials)/m for i in x]
	
	return x,y,trials

def coupon_B_plot_C():
	m = 300
	n = 250
	start = time()
	x,y,trials = coupon_B(m,n)
	print("running time = " + str(time() - start))

	plt.scatter(x,y,s=5,c='red')
	plt.xlim(0,max(x))
	plt.ylim(0,1)
	plt.title('Coupon Collectors\' cumulative density plot')
	plt.xlabel('number of trials k')
	plt.ylabel('fraction of succeeded experiment')
	plt.show()

	print("Empirical expected value of k = " +str(sum(trials)/len(trials)))

def coupon_C():
	pass
	
def loop_in_D(m,all_n):
	r = []
	for n in all_n:
		start = time()
		coupon_B(m,n)
		r.append(time()-start)

	return r


def  coupon_D():
	all_n = [i for i in range(4000,20000+1,4000)]
	all_n[0] = 300
	m = 300
	y_300 = loop_in_D(m,all_n)
	m = 2500
	y_2500 = loop_in_D(m,all_n)
	m = 5000
	y_5000 = loop_in_D(m,all_n)
	

	# plt.set_prop_cycle( cycler('color', colr_list) )
	plt.gca().set_color_cycle(['red', 'green', 'blue'])

	plt.plot(all_n,y_300)
	# plt.xticks(all_n)
	# plt.yticks(y_300)
	plt.plot(all_n,y_2500)
	# plt.yticks(y_5000)
	plt.plot(all_n,y_5000)
	# plt.yticks(y_10000)
	# plt.xticks(all_n)
	# plt.yticks(n_300)
	# plt.xlim(0,max(x))
	# plt.ylim(0,1)
	plt.title('Running Time Experiment for Coupon Collectors')
	plt.xlabel('Value of n')
	plt.ylabel('Number of seconds')
	plt.legend(['m = 300', 'm = 2500', 'm = 5000'], loc='upper left')
	plt.show()

if __name__ == "__main__":
	main()