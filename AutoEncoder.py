# -*- coding: utf-8 -*-

import numpy as np
import theano
import theano.tensor as T


class AutoEncoder(object):
    def __init__(self, np_rng, n_vis, n_hid, input=None, W=None, b_hid=None, b_vis=None):
        """
            Theory
            ++++++
            An autoencoder takes an input :math:`x` and maps it to a hidden representation :math:`y` \
            through 
            
            .. math::      
            
               y = f(Wx + b)
               
            Then the hidden representation is mapped back into a reconstruction :math:`z` of teh same \
            shape as :math:`x` through
            
            .. math::
            
                z = f(W^' y + b^')
                
            In this implementation we used tied weights, which means that :math:`W^' =W^T`. 
            Using the above, the parameters of an autoencoder model can be represented
            by the set :math:`params = \{W, b, b^i\}`.
            
            Function definition
            +++++++++++++++++++
            
            .. py:function:: __init__(np_rng, n_vis, n_hid, input=None, W=None, b_hid=None, b_vis=None)

               Initializes the parameters of an autoencoder model.

               :param numpy.random.RandomState np_rng: number random generator used to generate weights
               :param int n_vis: number of input/visible neurons
               :param int n_hid: number of hidden neurons
               :param theano.tensor.TensorType input: a symbolic description of the input
               :param theano.tensor.TensorType W: autoencoder model weights :math:`W`.
               :param theano.tensor.TensorType b_hid: hidden layer bias :math:`b`.
               :param theano.tensor.TensorType b_vis: output layer bias :math:`b^'`.              
           
        """
        
        self.n_vis = n_vis
        self.n_hid = n_hid
        
        if not W:
            initial_W = np.asarray(np_rng.uniform(low=-4 * np.sqrt(6. / (n_hid + n_vis)),
                                                  high=4 * np.sqrt(6. / (n_hid + n_vis)),
                                                  size=(n_vis, n_hid)), 
                                                  dtype=theano.config.floatX)                                                 
            self.W = theano.shared(value=initial_W, name='W')
            
        if not b_hid:
            initial_b_hid = np.zeros(n_hid, dtype=theano.config.floatX)            
            b_hid = theano.shared(value=initial_b_hid, name='bhid')
            
        if not b_hid:
            initial_b_vis = np.zeros(n_vis, dtype=theano.config.floatX)
            b_vis = theano.shared(value=initial_b_vis, name='bvis')
            
            
        self.W = W
        self.W_prime = self.W.T
        self.b = b_hid
        self.b_prime = b_vis
        
        if input == None:
            self.x = T.dmatrix(name='input')
        else:
            self.x = input
            
        self.params = [self.W, self.b, self.b_prime]
        
        
    def get_cost_updates(self, learning_rate):
        """
            Function definition
            +++++++++++++++++++
            
            .. py:function:: get_cost_updates(learning_rate)
            
               Calculates the derivatives of cost function 
               
               .. math::      
            
                   L(x,z;W,b,b^') = \\frac{1}{2} ||x-z||^2
                   
               with respect to :math:`W, b, b^'`. Then, it uses the learning rate to calculate the 
               updates for the autoencoder model parameters that are going to be used with a gradient based
               optimization method during model training.

               :param float learning_rate: learning rate for a gradient based optimization algorithm.
               :return: the evaluation of the cost function and the updates for the autoencoder 
                        model parameters that are going to be used by gradient based optimization 
                        during training phase.
               :rtype: float - list of floats
        """
       
        y = T.nnet.sigmoid(T.dot(self.x,self.W) + self.b)
        z = T.nnet.sigmoid(T.dot(y, self.W_prime) + self.b_prime)
        
        L = T.sum(((self.x - z)**2)/2, axis=1)
        cost = T.mean(L)
        
        gparams = T.grad(cost, self.params)

        updates = []
        
        for param, gparam in zip(self.params, gparams):
            updates.append((param, param - learning_rate * gparam))
        
        return (cost, updates)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        