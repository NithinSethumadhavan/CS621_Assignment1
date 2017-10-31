
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

	#Load dataset Housing_data.mat
	housing_data = scipy.io.loadmat("housing_data.mat")

	training_X = housing_data['Xtrain']
	training_Y = housing_data['Ytrain']  
	validation_X = housing_data['Xvalidate'] 
	validation_Y = housing_data['Yvalidate']

	#########################################
	########### WRITE FROM HERE #############
	#########################################




	pass

