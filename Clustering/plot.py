import matplotlib.pyplot as plt


def plotLine(p1, p2):
    plt.plot( [p1[0], p2[0]], [p1[1], p2[1]] )

Lat = [1,2,3,4]
Long = [2,3,1,3]
id_point=['A','B','C','D']

# Fill a dictionary with the points
points = {} # Create empty dictionary
for idx, point in enumerate(zip(Lat,Long)):
    points[id_point[idx]] = point 

# Plot points and their names
plt.plot(Lat, Long,'o') #Plot the points as you did
for key in points:
    plt.annotate(key, xy=points[key]) #Print name of point

plotLine(points['A'], points['B']) #Connect point A and B
plt.show()