
def housing_mat_run():
	'''Linear Regression with SKLearn
	Task to do :
	Use the training data to train a model using Linear Regression. Use cross validation and select the best model.
	Using the Linear Regression model selected above, predict the labels for the test set (test_X).
	Using these predicted labels, calculate the error percentage with respect to the true labels provided to you in "test_Y". Plot a scatter-plot graph containing the true label and the predicted label.
	For the scatter-plot, the x-axis should represent the data point from the validation set, and y-axis should represent the value for "median house income".

	Output: 1. print the accuracy on training and validation datasets
			2. plot a scatter graph
	'''

	import scipy.io
	from sklearn.linear_model import LinearRegression
	from sklearn.metrics import mean_squared_error
	from sklearn.model_selection import KFold
	import numpy as np
	from sklearn.model_selection import GridSearchCV, cross_val_score
	import matplotlib.pyplot as plt

	#Load dataset Housing_data.mat
	housing_data = scipy.io.loadmat("housing_data.mat")

	training_X = housing_data['Xtrain']
	training_Y = housing_data['Ytrain']
	validation_X = housing_data['Xvalidate']
	validation_Y = housing_data['Yvalidate']

	#########################################
	########### WRITE FROM HERE #############
	#########################################

	kf = KFold(n_splits=10)
	kf.get_n_splits(training_X)

	# for train_indices, test_indices in kf.split(training_X):
	# 	print('Train: %s | test: %s' % (train_indices, test_indices))

	regr = LinearRegression()

	temp = [regr.fit(training_X[train], training_Y[train]).score(training_X[test], training_Y[test]) for train, test in kf.split(training_X)]
	print(np.array(temp).mean())
	print("MSE =",mean_squared_error(validation_Y, regr.predict(validation_X)))
	print("Score =",regr.score(validation_X, validation_Y))

	plt.figure()
	plt.scatter(validation_Y, regr.predict(validation_X), edgecolors=(0,0,0))
	plt.plot([validation_Y.min(), validation_Y.max()], [validation_Y.min(), validation_Y.max()], 'k--', lw=4)
	plt.xlabel("True value")
	plt.ylabel("Predicted value")
	plt.show()

	# regr = LinearRegression()
	# regr.fit(training_X, training_Y)
	# LinearRegression(copy_X=True, fit_intercept=True, n_jobs=1, normalize=True)
	# print(regr.coef_)


housing_mat_run()
