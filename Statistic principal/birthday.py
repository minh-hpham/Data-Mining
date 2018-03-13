import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from random import randint
from time import time

def  main():
	# birthday paradox
	print(birthday_paradox_A(4000))
	# birthday_paradox_B_plot_C()
	

def birthday_paradox_A(n):
	numbers = set()

	while True:
		x = randint(1,n)
		if x in numbers:
			break
		numbers.add(x)

	return len(numbers)+1


def birthday_paradox_B(m,n):
	trials = list()
	for i in range(1,m):
		trials.append(birthday_paradox_A(n))
	x = set(trials)
	x.add(1)
	x = list(x)
	y = [sum(j <= i for j in trials)/m for i in x]
	
	return x,y,trials

def birthday_paradox_B_plot_C():
	m = 300
	n = 4000
	start = time()
	x,y,trials = birthday_paradox_B(m,n)
	print("trials = \n" + str(trials))
	print("Running time = "+ str(time()-start))
	plt.scatter(x,y,s=5,c='red')
	plt.xlim(0,max(x))
	plt.ylim(0,1)
	plt.title('Birthday paradox\'s cumulative density plot')
	plt.xlabel('number of trials k')
	plt.ylabel('fraction of succeeded experiment')
	plt.show()

	print("Expected number of k = "+ str(sum(trials)/len(trials)))

def birthday_paradox_C():
	pass
	
def loop_in_D(m,all_n):
	r = []
	for n in all_n:
		start = time()
		birthday_paradox_B(m,n)
		r.append(time()-start)

	return r


def  birthday_paradox_D():
	# all_n = [4000*i for i in range(1,250)]
	all_n = [i for i in range(100000,1000000+1,100000)]
	# all_n[0] = 4000
	m = 300
	y_300 = loop_in_D(m,all_n)
	m = 5000
	y_5000 = loop_in_D(m,all_n)
	m = 10000
	y_10000 = loop_in_D(m,all_n)

	# plt.set_prop_cycle( cycler('color', colr_list) )
	plt.gca().set_color_cycle(['red', 'green', 'blue'])

	plt.plot(all_n,y_300)
	plt.plot(all_n,y_5000)
	plt.plot(all_n,y_10000)

	plt.title('Running Time Experiment')
	plt.xlabel('Value of n')
	plt.ylabel('Number of seconds')
	plt.legend(['m = 300', 'm = 5000', 'm = 10000'], loc='upper left')
	plt.show()

if __name__ == "__main__":
	main()