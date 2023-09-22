from numpy import array, zeros, reshape
from numpy.random import normal
class GenericSensor:
    """ This class is mother class to simulate any sensor. Class memmbers are:
            -> m_std  = standard deviation use to compute sensor white noise.
            -> m_bias = sensor bias
            -> m_SAM  = Scalling and mis-Alignement Matrix, it simulates scaling factors and
                        misaligement between sensor axes
            -> m_size = size of measured signal.
                            - m_std and m_bais should both have a size of m_size
                            - m_SAM shoudl have a size of (m_size x m_size)
                        
        It has 2 methods :
            -> constructor
            -> GetMeasurement : It takes the true value as input and return a measurement

                measurement = SAM * trueValue + bias + noise

                Noise is a white noise with zero mean and std as standard deviation

    """     
    m_std = zeros((1,1))
    m_bias = zeros((1,1))
    m_SAM = zeros((1,1))
    m_shape = (1,1)
    def __init__(self, p_std : list, p_bias : list , p_SAM : list):
        self.m_shape    = (len(p_std), 1)
        self.m_std      = reshape(array(p_std), self.m_shape)
        self.m_bias     = reshape(array(p_bias), self.m_shape)
        self.m_SAM      = reshape(array(p_SAM), self.m_shape)
        

    def GetMeasurement(self, p_trueValue : array):
        noise = normal(zeros(self.m_shape), self.m_std, self.m_shape)
        return self.m_SAM @ p_trueValue + self.m_bias + noise
    
