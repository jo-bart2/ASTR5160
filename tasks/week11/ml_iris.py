import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn import neighbors

# JAB Recreate the iris problem based on the Machine Learning Example
# JAB Most of code taken directly from ML Example. I made sure to understand 
# JAb what it was doing, but I'm not sure if we were supposed to change it 
iris = load_iris()

# JAB Plot the iris data
fig = plt.figure()
ax = fig.add_subplot(111)
for i in range(3):
    target_class = iris.target == i
    ax.scatter(iris.data[target_class, 0], iris.data[target_class, 1], s=80,
               label=iris.target_names[i])
    ax.set_xlabel('Sepal Length (cm)')
    ax.set_ylabel('Sepal Width (cm)')
    ax.set_title('Iris Classifications')
    ax.legend()
plt.show()

# JAB Use k-NN to determine type of iris for fake data set
# JAB Generate fake data set
num = 100000
mock_data = []
for i in range(2):
    col_min = np.min(iris.data[...,i])
    col_max = np.max(iris.data[...,i])
    
    mock_meas = np.random.random(num)*(col_max - col_min) + col_min
    mock_data.append(mock_meas)

mock_data = np.reshape(mock_data, (2, num)).T

# JAB Determine type of iris
knn = neighbors.KNeighborsClassifier(n_neighbors=1)
knn.fit(iris.data[..., :2], iris.target)
mock_target_class = knn.predict(mock_data)

fig2 = plt.figure()
ax2 = fig2.add_subplot(111)
for i in range(3):
    target_class = mock_target_class == i
    ax2.scatter(mock_data[target_class, 0], mock_data[target_class, 1], s=10,
                label=iris.target_names[i])
    ax2.set_xlabel('Sepal Length (cm)')
    ax2.set_ylabel('Sepal Width (cm)')
    ax2.set_title('Iris Classifications - Mock Data')
    ax2.legend(loc = 'upper right')
plt.show()

# JAB Determine percentage of irises that are virginica
