from sklearn import datasets
from sklearn.naive_bayes import GaussianNB

iris = datasets.load_iris()
gnb = GaussianNB()
y_pred = gnb.fit(iris.data, iris.target).predict([[5.1, 3.5, 1.4, 0.2]])

print "iris data", iris.data[0]
print "iris target", iris.target[0]
print "result", y_pred

print("Number of mislabeled points out of a total %d points : %d"
      % (iris.data.shape[0], (iris.target != y_pred).sum()))
