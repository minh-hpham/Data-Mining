
from itertools import combinations, cycle
from urllib.request import urlopen
from queue import PriorityQueue
from scipy.spatial.distance import pdist, squareform
import numpy as np
import matplotlib.pyplot as plt

c1 = "C1.txt"
c2 = "C2.txt"
c3 = "C3.txt"

def  main():
	Single_link()

def Mean_Link():
	points = get_coordinate(c1)
	clusters = {}
	for key in points.keys():
		clusters[key] = set([key])

	while len(clusters) > 4: 
		p_queue = PriorityQueue()
		avg_coor = {}
		
		for key,value in clusters.items():
			avg_coor[key] = average_coor(value,points)

		# find distance of mean coor	
		keys = combinations(list(clusters.keys()),2)
		for pair in keys:
			x = [avg_coor[pair[0]],avg_coor[pair[1]]]
			distance = pdist(x, 'euclidean')[0]
			p_queue.put((distance,pair))

		# form new cluster
		pair = p_queue.get()[1] # this pair has smallest distance
		id1 = pair[0]
		id2 = pair[1]
		
		newset = clusters[id1].union(clusters[id2])
		clusters[id1] = newset
		del clusters[id2]

	Hierarchical_Clustering(clusters,points)



def average_coor(pids,points):
	return sum(np.array(points[pid]) for pid in pids)/len(pids)

def Single_link():
	points = get_coordinate(c1)
	p_queue = sort_distance(points)

	clusters = {}
	for key in points.keys():
		clusters[key] = set([key])
	

	while len(clusters) > 4: 
		pair = p_queue.get()[1]
		id1 = pair[0]
		id2 = pair[1]
		index = set()
		for key,value in clusters.items():
			if (id1 in value) or (id2 in value):
				index.add(key)

		if len(index) == 2:
			id1 = index.pop()
			id2 = index.pop()
			newset = clusters[id1].union(clusters[id2])
			clusters[id1] = newset
			del clusters[id2]

	Hierarchical_Clustering(clusters,points)


def Hierarchical_Clustering(clusters,points):
	colors = cycle(["C1", "C2", "C3", "C4", "C5", "C6", "C7"])

	plt.title('Hierarchical Clusters - Mean distance')
	plt.xlabel('1st Dimension Value')
	plt.ylabel('2nd Dimension Value')
	for key,value in clusters.items():
		X = [points[pid][0] for pid in value]
		Y = [points[pid][1] for pid in value]
		plt.scatter(X, Y, color=next(colors))
		for pid in value:
			plt.annotate(pid,xy=points[pid])

	plt.show()


def get_coordinate(filename):
	coor = {}
	data = [line.rstrip() for line in open(filename)]
	for line in data:
		array = line.split("\t")
		coor[int(array[0])]= [float(s) for s in array[1:]]

	return coor


def sort_distance(points):
	p_queue = PriorityQueue()
	keys = combinations(list(points.keys()),2)
	for pair in keys:
		x = [points[pair[0]],points[pair[1]]]
		distance = pdist(x, 'euclidean')[0]
		p_queue.put((distance,pair))

	# while not p_queue.empty():
	# 	print(p_queue.get())

	return p_queue



if __name__ == "__main__":
	main()