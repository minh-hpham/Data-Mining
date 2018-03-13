import numpy as np 
from matplotlib import pyplot as plt 


a = np.random.random_sample(1000)
plt.hist(a)
plt.show()
# np.histogram(a)