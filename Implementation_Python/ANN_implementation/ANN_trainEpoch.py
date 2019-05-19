# back propagation
import numpy as np


# for sigmoid units return the function value at x or the value of the derivative at x
# dependeing upon derivative flag

def sgm(x,Derivative=False):
	if not Derivative:
		return 1.0/(1.0+np.exp(-x))
	else:
		out = sgm(x)
		return out*(1.0-out)


def linear(x,Derivative=False):
	if not Derivative:
		return x
	else:
		return 1.0


def guassian(x,Derivative=False):
	if not Derivative:
		return np.exp(-x**2)
	else:
		return -2*x*np.exp(-x**2)


def tanh(x,Derivative=False):
	if not Derivative:
		return np.tanh(x)
	else:
		return (1.0-np.tanh(x)**2)





class BackPropagationNetwork:

    #Class members
    layerCount=0
    shape=None;
    weights=[]

    # Class methods

    def __init__(self,layerSize):

        #Intialize the network

        #Layer Info
        self.layerCount=len(layerSize)-1 #as no. Input layer is not counted here 
        self.shape=layerSize

        #Input/Output data from last Run
        self._layerInput=[]
        self._layerOutput=[]

        #Create the weight arrays
        for(l1,l2) in zip(layerSize[:-1],layerSize[1:]):
            self.weights.append(np.random.normal(scale=0.1, size = (l2,l1+1))) # 1 is added to l1 for bias

    # Run method
        
    def Run(self, input):

        lnCases = input.shape[0] # return the number of rows..i.e. here no. of test cases

        #Clear out the previous intermediate value lists
        self._layerInput = []
        self._layerOutput = []

        #Running
        for index in range(self.layerCount):

        #Determining the layer input for input layer and for hidden layer
            if index == 0:
                layerInput = self.weights[0].dot(np.vstack([input.T, np.ones([1,lnCases])]))
            else:
                layerInput = self.weights[index].dot(np.vstack([self._layerOutput[-1], np.ones([1, lnCases])]))

            self._layerInput.append(layerInput)
            self._layerOutput.append(sgm(layerInput))

        return self._layerOutput[-1].T  #finla output is again transposed

    # TrainEpoch method
    def TrainEpoch(self,input,target,trainingRate=0.2):         #training rate default value taken here is 0.2
        # method to train the network
        
        delta=[]
        lnCases=input.shape[0]   # return the number of rows..i.e. here no. of test cases
    
        #Run the Network
        self.Run(input)

        # Calculation of delta
        # Since backpropagation, so start at output layer and move backward

        for index in reversed(range(self.layerCount)):
            if index == self.layerCount-1:
                
                output_delta = self._layerOutput[index] - target.T              # this is also the gradient at output if we take the least square error function
                error = np.sum(output_delta**2)                                 # sum of all the elements along all dimensions
                delta.append(output_delta * sgm(self._layerInput[index],True))

            else:
                delta_pullback = self.weights[index+1].T.dot(delta[-1])

                # weight matrix has extra weight of bias in it, that's why deltaPullback[:-1,:] which gives evrything bt last row and all of the column
                delta.append(delta_pullback[:-1,:]*sgm(self._layerInput[index],True))

        '''
        deltaPullback is the matrix where j'th column shows the gradient of the activation for j'th training example.
        Now the last row of the deltaPullback matrix is for the gradients of the activation for bias units we add to each hidden layer
        We know to compute the gradient at the preactivation from the gradient at the activation, we need preactivation first
        and for bias units we dun have preactivation (i.e we dun have value of preactivation of bias units in self._layerInput[i])
        We should remove this row as while calculating the delta of the layer (gradient at preactivation)

        '''

        # Compute weight deltas

        '''
        All the parameters (i.e. weight or _layerInput or _layerOutput) except delta list appear from front to back bt delta appear
        from back to front as we have calculated delta from output layer towards input layer

        '''

    
        for index in range(self.layerCount):
            delta_index=self.layerCount-1-index
            if index ==0:
                layerOutput=np.vstack([input.T, np.ones([1,lnCases])]) # 1 rows and as many columns as test cases
            else:
                layerOutput=np.vstack([self._layerOutput[index-1],np.ones([1,self._layerOutput[index-1].shape[1]])])


            '''
            list of layerOutput is from preceding layer, and so all the outputs from preceding layer are going to be multipled by deltas from
            current layer inorder to update the weights that connect the output from the previous layer to the delta in the current layer 

            
            A = np.array([[1,1],[2,2]]).T   #if this is array defined
            A # output of A and outputss => array([[1,1],
                                                   [2,2]])
            A.T # output of A.T and outputs => array([[1,2],
                                                      [1,2]])
            # after transposing overall integrity of array structue is courrupted in numpy

            # so here in delta ...one of these element in delta will be potentially a matrix where each column is a 'delta' from different training case

            # so here 1's correspond to the deltas for one training case, 2's for another training case
            
            
            
            
            A=A.T
            so colimn needs to be sliced => A[None,:,:] outputs array([[[1,2],
                                                                      [1,2]]])

                                          # A currently holds array([[1,2],
                                                                     [1,2]])                            
                                         => A[None,:,:].transpose(2,1,0) outputs array([[[1],
                                                                                         [1]],

                                                                                        [[2],
                                                                                         [2]]])
                                         => A[None,:,:].transpose(2,0,1) outputs array([[[1,1]],
                                                                                       [[2,2]]])
            
            '''
            
            
            weightDelta=np.sum(\
                               layerOutput[None,:,:].transpose(2,0,1)*delta[delta_index][None,:,:].transpose(2,1,0)\
                               ,axis=0)

            self.weights[index]-= trainingRate*weightDelta

        return error



                                                      
        

# If run as a script, create a test object

if __name__ == "__main__":
    bpn=BackPropagationNetwork((2,2,1))
    #print(bpn.shape)
    #print(bpn.weights)
    
    lvInput = np.array([[0, 0], [1, 1], [0, 1],[1,0]])
    lvTarget = np.array([[0.05],[0.05],[0.95],[0.95]])

    lnMax=100000
    lnErr = 1e-5

    for i in range(lnMax+1):
        err=bpn.TrainEpoch(lvInput,lvTarget)
        if i%2500 == 0:
            print ("Iteration {0}\tError: {1:0.6f}".format(i,err))
        if err <= lnErr:
            print ("Minimum error reached at iteration {0}".format(i))
            break


    #Display output
    lvOutput=bpn.Run(lvInput)

    for i in range(lvInput.shape[0]):
        print("Input: {0} Output: {1}".format(lvInput[i], lvOutput[i]))
        





    
