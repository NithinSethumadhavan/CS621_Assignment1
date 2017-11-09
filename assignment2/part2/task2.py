import os
origpath = os.getcwd()
graph_data = {}

def model(data,h1,h2,output_nodes, hidden_layer1, hidden_layer2, output_layer, drop):
        z2=tf.add(tf.matmul(data,hidden_layer1['weights']),hidden_layer1['biases'])
        a2=tf.nn.relu(z2)

        z3=tf.add(tf.matmul(a2,hidden_layer2['weights']),hidden_layer2['biases'])
        a3=tf.nn.relu(z3)

        output=tf.add(tf.matmul(a3,output_layer['weights']),output_layer['biases'])

        return output

def train_neural_net(x,y,x_test,y_test,h1,h2,output_nodes):
        x_tf = tf.placeholder('float',[None,1024])
        y_tf = tf.placeholder('float',[None,46])
        d = tf.placeholder('float')

        hidden_layer1 = {'weights':tf.Variable(tf.Variable(tf.random_normal([1024,h1]))),'biases':tf.Variable(tf.random_normal([h1]))}
        hidden_layer2={'weights':tf.Variable(tf.Variable(tf.random_normal([h1,h2]))),'biases':tf.Variable(tf.random_normal([h2]))}
        output_layer={'weights':tf.Variable(tf.Variable(tf.random_normal([h2,output_nodes]))),'biases':tf.Variable(tf.random_normal([output_nodes]))}


        predicted_output = model(x_tf,h1,h2,output_nodes,hidden_layer1, hidden_layer2, output_layer, d )
        cost=tf.reduce_mean( tf.nn.softmax_cross_entropy_with_logits(logits=predicted_output,labels=y_tf) )
        optimizer=tf.train.AdamOptimizer().minimize(cost)
        hm_epochs=100
        with tf.Session() as sess:
                sess.run(tf.global_variables_initializer())
                for epoch in range(hm_epochs):
                        epoch_loss=0
                        i=0
                        for _ in range((len(x)//batch_size) - 2):
                                epoch_x, epoch_y=batchcreating(x,y,i)
                                _,c=sess.run([optimizer,cost],feed_dict={x_tf:epoch_x,y_tf:epoch_y})
                                epoch_loss+=c
                                i=i+batch_size
                        print('Epoch ',epoch,'completed out of ', hm_epochs,'loss:',epoch_loss)
                        graph_data[epoch] = epoch_loss


                correct=tf.equal(tf.argmax(predicted_output,1),tf.argmax(y_tf,1))
                accuracy=tf.reduce_mean(tf.cast(correct,'float'))

                results = sess.run([predicted_output],feed_dict={x_tf:x_test})
                return hm_epochs, accuracy.eval({x_tf:x,y_tf:y}), accuracy.eval({x_tf:x_test,y_tf:y_test})

def devnagriPreprocessing(train=True):
        ''' Load the image files(Training and Test images) into List of Intergers.
                You may want to use Python Imaging Library (PIL) for reading images.
                Put train and Test folder in current directory. '''
        global origpath
        x = []
        y = []
        idx=0
        path = origpath
        if train:
                path += "/Train"
        else:
                path += "/Test"

        os.chdir(path)

        path = os.getcwd()

        for directory in os.listdir():
                print(directory)
                os.chdir(path + "/" + directory)
                for f in os.listdir():
                        img = Image.open(f)
                        image = np.array(img)
                        image = image.reshape(image.shape[0]*image.shape[1])
                        x.append(image)
                        y.append(idx)
                        img.close()

                idx += 1

        ip=np.array(x)
        op=np.array(y)
        ohe_enc = createOneHotEncoding(op)
        op = ohe_enc.transform(op.reshape(op.shape[0],1)).toarray()
        ip=ip/255
        return ip,op

def batchcreating(inputdata,outputdata,i):
        temp1=inputdata[i:i+100,:]
        temp2=outputdata[i:i+100,:]
        return temp1,temp2


def normalizeData(inputdata):

        # You may want to normalize the image data.
        # One of the most important step in machine learning

        pass

################################################################################
def createOneHotEncoding(y_labels):
        ''' Output of an image will be a number between 0-35.
        Why should convert into OneHot Encoding format ?
        '''
        from sklearn.preprocessing import OneHotEncoder as ohe
        enc = ohe(46)
        enc.fit(y_labels.reshape(y_labels.shape[0],1))

        return enc


################################################################################
def devnagriTensorflow( X, y, X_test, y_test ):

        '''     Do not modify the parameters

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

        h1=1000
        h2=1000
        output_nodes=46

        global batch_size
        batch_size=100


        learning_rate = 0.001
        epochs, training_accuracy, test_accuracy = train_neural_net(X,y,X_test,y_test,h1,h2,output_nodes)

        return [training_accuracy, test_accuracy, learning_rate, epochs]


################################################################################
def plotGraph():
        ''' Plot Graph
                y-axis : cost
                x-axis : Number of Epochs

                Output: graph
                '''

        import matplotlib.pyplot as plt

        epochs = list(graph_data.keys())
        loss = list(graph_data.values())
        plt.plot(epochs, loss)
        plt.xlabel('Number of Epochs')
        plt.ylabel('Cost')
        plt.show()



if __name__ == '__main__':
        import numpy as np
        import tensorflow as tf
        import io
        import os
        from PIL import Image
        from sklearn.model_selection import train_test_split

        inputdata,outputdata = devnagriPreprocessing()
        inputdata_train, inputdata_test, outputdata_train, outputdata_test = train_test_split(inputdata, outputdata, test_size=0.2, random_state=42)

        ls = devnagriTensorflow(inputdata_train, outputdata_train, inputdata_test, outputdata_test)

        plotGraph()
