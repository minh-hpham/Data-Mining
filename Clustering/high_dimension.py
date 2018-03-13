import math
import matplotlib.pyplot as plt



def main():
	
	c = []
	c.append(1.128379167)
	c.append(1.240906158)
	c.append(1.341876534)
	
	large_d = [2*math.pow(math.factorial(d/2),1/d)/math.sqrt(math.pi) for d in range(6,21,2)]
	c.extend(large_d)
	d = [2,3,4]
	d.extend(list(range(6,21,2)))


	plt.title('the expansion factor c up to d = 20')
	plt.xlabel('d')
	plt.ylabel('c')
	plt.scatter(d, c, color='r')
	plt.show()

if __name__ == "__main__":
	main()