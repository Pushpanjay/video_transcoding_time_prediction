# back propagation

import numpy as np          # a powerful N-dimensional array object
import csv


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


class BackPropagationNetwork:

    #Class members
    layerCount=0
    shape=None;
    weights=[]          #at each position holds the pointer to a numpy array..which is matrix of weights which connects previous layer to current layer
    layerFunction=[]

    # Class methods

    def __init__(self,layerSize,layerTransferFunc=None):

        #Intialize the network

        #Layer Info
        self.layerCount=len(layerSize)-1 #as Input layer is not counted here; only (len(layerSize))sets of weight are required
        self.shape=layerSize

        if layerTransferFunc is None:
            lFuncs=[]
            for i in range(self.layerCount):
                if i==self.layerCount-1:
                    lFuncs.append(linear)
                else:
                    lFuncs.append(sgm)
        else:
            if len(layerTransferFunc) != len(layerSize):
                raise ValueError("Incompatible no of transfer functions.")
            elif layerTransferFunc[0] is not None:
                raise ValueError("no transfer functions for input layer.")
            else:
                lFuncs = layerTransferFunc[1:] # from 1 to end....removes 'None' which is present for input layer

        self.layerFunction=lFuncs

        # Data from last Run
        self._layerInput=[]
        self._layerOutput=[]
        self._previousWeightDelta=[]

        #Create the weight arrays and intializing weight array and previousWeightDelta
        for(l1,l2) in zip(layerSize[:-1],layerSize[1:]):        # a pair of element in one layer to element in second layer is created
            self.weights.append(np.random.normal(scale=0.1, size = (l2,l1+1))) # 1 is added to l1 for bias; a matrix of dimension [l1+1,l2] is created with random weight of scale 0.1
                                                                               # since input vector have 10 rows for 10 parameter...that's why (l2,l1+1) as weight matrix needs 10 column  to perform matrix multiplication
            self._previousWeightDelta.append(np.zeros((l2,l1+1)))              

    # Run method; simple forward propagation
        
    def Run(self, input):

        lnCases = input.shape[0]            # return the number of rows..i.e. here no. of input cases; .shape[0] return the no. of row

        #Clear out the previous intermediate value lists
        self._layerInput = []
        self._layerOutput = []

        #Running
        for index in range(self.layerCount):        

        #Determining the layer input for input layer and for hidden layer
            if index == 0:
                layerInput = self.weights[0].dot(np.vstack([input.T, np.ones([1,lnCases])]))    # here vertical stack is created and then fake input i.e. for bias term 
            else:                                                                               # here input is transposed, then is appended by a matrix of onr row and lncases columns
                layerInput = self.weights[index].dot(np.vstack([self._layerOutput[-1], np.ones([1, lnCases])]))

            self._layerInput.append(layerInput)
            self._layerOutput.append(self.layerFunction[index](layerInput))

        return self._layerOutput[-1].T  #finla output is again transposed

    # TrainEpoch method
    def TrainEpoch(self,input,target,trainingRate=0.2,momentum=0.5):         # training rate default value taken here is 0.2 and momentum default value is 0.5
        # method to train the network
        
        delta=[]
        lnCases=input.shape[0]   # return the number of rows..i.e. here no. of test cases
    
        #Run the Network
        self.Run(input)


        # Calculation of delta

        # Since backpropagation, so started at output layer and moved backward

        for index in reversed(range(self.layerCount)):          # reversed function reverse the input list
            if index == self.layerCount-1:
                
                output_delta = self._layerOutput[index] - target.T              # for the last layer simply delta is target-output_of_the_layer
                error = np.sum(output_delta**2)                                 # sum of all the delta's
                delta.append(output_delta * self.layerFunction[index](self._layerInput[index],True))        # from coursera (lect 9-1) cost

            else:
                delta_pullback = self.weights[index+1].T.dot(delta[-1])     # delta from the next layer is calculated

                # weight matrix has extra weight of bias in it, that's why deltaPullback[:-1,:] which gives evrything bt last row and all of the column
                delta.append(delta_pullback[:-1,:]*self.layerFunction[index](self._layerInput[index],True))



        # Compute weight deltas

        '''
        All the parameters (i.e. weight or _layerInput or _layerOutput) except delta list appear from front to back bt delta appear
        from back to front as we have calculated delta from output layer towards input layer

        '''

    
        for index in range(self.layerCount):
            delta_index=self.layerCount-1-index         # since delta is stored from output layer towards input layer
            if index ==0:
                layerOutput=np.vstack([input.T, np.ones([1,lnCases])]) # 1 rows and as many columns as test cases
            else:
                layerOutput=np.vstack([self._layerOutput[index-1],np.ones([1,self._layerOutput[index-1].shape[1]])])    # shape[1] to get no. of columns


            '''
            list of layerOutput is from preceding layer, and so all the outputs from preceding layer are going to be multipled by deltas from
            current layer inorder to update the weights that connect the output from the previous layer to the delta in the current layer 

            
            A = np.array([[1,1],[2,2]])   #if this is array defined
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
            
            
            curWeightDelta=np.sum(\
                               layerOutput[None,:,:].transpose(2,0,1)*delta[delta_index][None,:,:].transpose(2,1,0)\
                               ,axis=0)

            weightDelta = trainingRate*curWeightDelta + momentum*self._previousWeightDelta[index]          

            self.weights[index]-=weightDelta

            self._previousWeightDelta[index]=weightDelta   # accumulate momentum in _previousWeightDelta
            

        return error



        

# run

if __name__ == "__main__":
    
    #bpn=BackPropagationNetwork((5,5,1))
    #print(bpn.shape)
    #print(bpn.weights)

    
    
    f=open('dataset.csv')
    
    csv_f=csv.reader(f)
    count=0
    train=[]
    target=[]
    t=[]
    for row in csv_f:
        if count==0:
            count+=1
            continue
        #t.append(float(row[0])/100)
        t.append(float(row[1])/100)
        t.append(float(row[2])/100)
        t.append(float(row[3])/1000)
        t.append(float(row[4])/10)
        #t.append(float(row[5])/1000)
        #t.append(float(row[6]))
        t.append(float(row[7])/1000)
        t.append(float(row[8])/10)
        t.append(float(row[9])/100)
        t.append(float(row[10])/100)        
        train.append(t)
        t=[]
        target.append([float(row[11])/1000])
        count+=1
        if count==10:
            break
    
    lvInput = np.array(train)
    lvTarget = np.array(target)
    lFuncs = lFuncs=[None,sgm,linear]

    bpn=BackPropagationNetwork((8,8,1),lFuncs)

    
    


    
    '''
    lvInput = np.array([[1.76, 1.44, 54.59, 1.2, 56.0, 1.2, 1.76, 1.44], [1.76, 1.44, 54.59, 1.2, 56.0, 1.2, 3.2, 2.4], [1.76, 1.44, 54.59, 1.2, 56.0, 1.2, 4.8, 3.6], [1.76, 1.44, 54.59, 1.2, 56.0, 1.2, 6.4, 4.8], [1.76, 1.44, 54.59, 1.2, 56.0, 1.2, 12.8, 7.2], [1.76, 1.44, 54.59, 1.2, 56.0, 1.2, 19.2, 10.8], [1.76, 1.44, 54.59, 1.2, 56.0, 1.5, 1.76, 1.44], [1.76, 1.44, 54.59, 1.2, 56.0, 1.5, 3.2, 2.4], [1.76, 1.44, 54.59, 1.2, 56.0, 1.5, 4.8, 3.6]])
    lvTarget = np.array([[0.000612], [0.00098], [0.001216], [0.001692], [0.003456], [0.00632], [0.000728], [0.000944], [0.0014759999999999999]])
    lFuncs=[None,sgm,linear]

    bpn=BackPropagationNetwork((8,8,1),lFuncs)
    '''
    
    





    '''
    lvInput = np.array([[0, 0], [1, 1], [0, 1],[1,0]])
    lvTarget = np.array([[0.00],[0.00],[1.00],[1.00]])
    lFuncs=[None,sgm,linear]

    bpn=BackPropagationNetwork((2,2,1),lFuncs)
    '''
    
    lnMax=100000
    lnErr = 1e-5        # means 10^-5

    for i in range(lnMax+1):
        err=bpn.TrainEpoch(lvInput,lvTarget,momentum=0.7)
        if i%2500 == 0:
            print ("Iteration {0}\tError: {1:0.6f}".format(i,err))
        if err <= lnErr:
            print ("Minimum error reached at iteration {0}".format(i))
            break


    #Display output
    lvOutput=bpn.Run(lvInput)

    for i in range(lvInput.shape[0]):
        print("Input: {0} Output: {1}".format(lvInput[i],lvOutput[i]))






    
