
################################################################################
def devnagriPreprocessing():
	''' Load the image files(Training and Test images) into List of Intergers.
		You may want to use Python Imaging Library (PIL) for reading images. 
		Put train and Test folder in current directory. '''

	pass



################################################################################
def normalizeData():
	''' You may want to normalize the image data.
		One of the most important step in machine learning '''

	pass


################################################################################
def createOneHotEncoding():
	''' Output of an image will be a number between 0-35.
		Why should convert into OneHot Encoding format ? 
		'''

	pass



################################################################################
def devnagriTensorflow( X, y, X_test, y_test ):

	'''	Do not modify the parameters 

	Here you will write the code for Neural Network model.
		You must use Tensorflow(only) to implement this.

		Input :  X, y, X_test, y_test (All are list)

			X.shape =  (51505, 1024)
			y.shape = (51505, 46)
			X_test.shape = (33744, 1024)
			y_test.shape = (33744, 46)

        Output : List[
                        Accuracy on Training Data,
                        Accuracy on Test Data ,
                        Learning Rate,
                        Number of Epochs
                    ]

        
	'''
	
	import numpy as np
	import tensorflow as tf


	#####################################
	#############  START Here ###########


	pass




################################################################################
def plotGraph():
	''' Plot Graph 
		y-axis : cost
		x-axis : Number of Epochs

		Output: graph
		'''

	pass

