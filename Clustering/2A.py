from itertools import combinations, cycle

from scipy.spatial.distance import pdist, squareform
import numpy as np
import matplotlib.pyplot as plt

c1 = "C1.txt"
c2 = "C2.txt"
c3 = "C3.txt"

def  main():
	points = get_coordinate(c2)
	kmeanplus_experiment(3,points)



def gonzalez_experiment(k,points):
	center,phi = Gonzalez(3,points)
	report(center,phi,points)
	picturize(center,phi,points)


def kmeanplus_experiment(k,points):
	g_center,g_phi = Gonzalez(3,points)

	g_subset = pid_subsets(g_center,g_phi)

	data = []
	verify_subset = []
	for i in range(40):
		center,phi = K_means_plus_plus(3,points)
		data.append(report(center,phi,points))
		verify_subset.append(g_subset==pid_subsets(center,phi))


	print("Fraction of time the results are same as that of Gonzalez: %.4f" % (sum(verify_subset)/len(verify_subset)))
	cdf(data,"Cumulative density function of the 3-means cost")


def pid_subsets(center,phi):
	subsets = set()
	for i,c in enumerate(center):
		subsets.add(tuple([pid+1 for pid,pid_center in enumerate(phi) if pid_center==(i+1)]))
	return subsets


def k_mean_clustering(points):
	P = len(points)
	center,phi = Gonzalez(4,points)
	print("Start w/ Gonzalez " + str(center) )
	center.insert(0,0)
	center,phi = k_median(center,points)
	print("Final subset = " + str(center))

	print("-----------------------------------------------------REPORT---------------------------------------------------")
	print("Centers are: ")
	for i,cid in enumerate(center):
		to_print = [cid]
		to_print.extend(points[cid])
		print("%d\t%.7f\t%.7f\t%.7f\t%.7f\t%.7f" % tuple(to_print))

	distances = [distance(points[center[center_index-1]],points[pid+1]) for pid,center_index in enumerate(phi)]
	print("Cost1(P, C) = "+str(np.sum(distances)/P)) 


def fixed_points(points):
	center,phi = Lloyd([0,1,2,3],points)
	print("Final subset = " + str(center))
	report(center,phi,points)


def start_w_gonzalez(points):
	center,phi = Gonzalez(3,points)
	print("Start w/ Gonzalez " + str(center) )
	center.insert(0,0)
	center,phi = Lloyd(center,points)
	print("Final subset = " + str(center))
	report(center,phi,points)

# def start_w_gonzalez(points):
# 	center,phi = Gonzalez(4,points)
# 	print("Start w/ Gonzalez " + str(center) )
# 	center.insert(0,0)
# 	center,phi = k_median(center,points)
# 	print("Final subset = " + str(center))
# 	report(center,phi,points)

def start_w_Kmean(points):
	data = []
	subset = []
	verify_subset = []
	for i in range(40):
		old_center,old_phi = K_means_plus_plus(3,points)
		old_subset = pid_subsets(old_center,old_phi)

		center = old_center[:]
		center.insert(0,0)
		center,phi = Lloyd(center,points)
		data.append(report(center,phi,points))
		verify_subset.append(old_subset==pid_subsets(center,phi))
		# print("Kmean++ center: " + str(old_center) +" Lloyd's center: " + str(center) )

	cdf(data,"cumulative density function of Lloyd 40 trials")

	# # cdf(data)
	print("Fraction of time the subsets are same as that of K-means++: %.4f" % (sum(verify_subset)/len(verify_subset)))

def k_median(centers,points):
	n = len(points)
	old_centers = [0]*len(centers)
	phi = np.ones(n+1,dtype=int)
	count = 0
	while (not unchanged(old_centers,centers)) and (count<40):
		old_centers = centers[:]
		phi = assign_center(centers,points)

		# evaluate center
		for i in range(1,len(centers)):
			v = [j for j in range(1,len(phi)) if phi[j]==i]
			# print(v)
			if v:
				centers[i] = int(np.median(v))

		# centers = evaluate_center(centers,phi)
		# print("old_centers " + str(old_centers) + " new_centers "+str(centers))
		count += 1
	return centers[1:],phi[1:]



def Lloyd(centers,points):
	n = len(points)
	old_centers = [0,0,0,0]
	phi = np.ones(n+1,dtype=int)
	count = 0
	while (not unchanged(old_centers,centers)) and (count<40):
		old_centers = centers[:]
		phi = assign_center(centers,points)
		centers = evaluate_center(centers,phi)
		# print("old_centers " + str(old_centers) + " new_centers "+str(centers))
		count += 1
	return centers[1:],phi[1:]


def unchanged(new_centers,centers):
	return set(new_centers) == set(centers)

def assign_center(new_centers,points):
	n = len(points)
	phi = np.ones(n+1,dtype=int)
	for i in points.keys():
		value = [distance(points[i],points[new_centers[j]]) for j in range(1,len(new_centers))]
		phi[i] = value.index(min(value)) + 1
	return phi


def evaluate_center(centers,phi):
	for i in range(1,len(centers)):
		v = [j for j in range(1,len(phi)) if phi[j]==i]
		# print(v)
		if v:
			centers[i] = int(np.mean(v))

	return centers


def cdf(data,title):
	
	values, base = np.histogram(data)
	#evaluate the cumulative
	cumulative = np.cumsum(values)
	
	# plot the cumulative function
	plt.plot(base[:-1], cumulative, c='blue')
	# plt.axvline(x=gonzalez_cost,c='red')
	plt.title(title)
	plt.xlabel('3-center cost c')
	plt.ylabel('bins')
	plt.show()

def K_means_plus_plus(k,points):
	n = len(points)
	c = [0,1,0,0]
	phi = np.ones(n+1,dtype=int)
	for i in range(2,k+1):
		distances = []
		distances.append(0)
		distances.extend([distance(points[j],points[c[i-1]])**2 for j in range(1,n+1)])
		distances_sum = sum(distances)

		normalize = [d/distances_sum for d in distances]

		normalize = np.cumsum(normalize)
		p = np.random.random_sample()
		for index in range(1,n+1):
			if ((normalize[index-1] < p) & (normalize[index] >= p)) :
				c[i] = index
				break
		
		for j in range(1,n+1):
			if distance(points[j],points[c[phi[j]]]) > distance(points[j],points[c[i]]):
				phi[j] = i  


	return c[1:],phi[1:]


def Gonzalez(k,points):
	n = len(points)
	c = [0]*(k+1)
	c[1] = 1
	phi = np.ones(n+1,dtype=int)
	for i in range(2,k+1):
		M = 0
		c[i] = 1
		for j in range(1,n+1):
			d = distance(points[j],points[c[phi[j]]]) 
			if d > M:
				M = d
				c[i] = j
		for j in range(1,n+1):
			if distance(points[j],points[c[phi[j]]]) > distance(points[j],points[c[i]]):
				phi[j] = i  

	return c[1:],phi[1:]

def report(center,phi,points):
	
	distances = [distance(points[center[center_index-1]],points[pid+1]) for pid,center_index in enumerate(phi)]
	cost = np.sqrt(np.sum([np.square(d) for d in distances])/len(distances))
	# print("3-center cost max = %.4f and 3-means cost = %.4f" % (max(distances),cost))
	# print("3-means cost = %.4f" % (cost))
	return cost


def picturize(center,phi,points):

	colors = cycle(["r","g","b"])

	plt.title('Gonzalez - 3 centers')
	plt.xlabel('1st Dimension Value')
	plt.ylabel('2nd Dimension Value')
	for i,label in enumerate(center):
		value = [pid+1 for pid,x in enumerate(phi) if x==(i+1)]
		X = [points[pid][0] for pid in value]
		Y = [points[pid][1] for pid in value]
		#add data points
		label_color=next(colors)
		plt.scatter(X, Y, color=label_color,alpha=0.3)
		# for pid in value:
		# 	plt.annotate(pid,xy=points[pid])
		#add label
		plt.annotate(label, points[label],horizontalalignment='left',verticalalignment='right',size=15, weight='bold',color=label_color) 

	plt.show()


def distance(p1,p2):
	x = [p1,p2]
	return pdist(x, 'euclidean')[0]


def get_coordinate(filename):
	coor = {}
	data = [line.rstrip() for line in open(filename)]
	for line in data:
		array = line.split("\t")
		coor[int(array[0])]= [float(s) for s in array[1:]]

	return coor

if __name__ == "__main__":
	main()