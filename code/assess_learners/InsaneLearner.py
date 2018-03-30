import numpy as np, BagLearner, LinRegLearner
class InsaneLearner(object):
    def __init__(self, verbose = False):
        self.models = []
        self.verbose = verbose
        for i in range(20):
            baglearner = BagLearner.BagLearner(LinRegLearner.LinRegLearner, kwargs={}, bags = 20)
            self.models.append(baglearner)   
    
    def addEvidence(self,dataX,dataY):   ## add evidence
        for i in range(len(self.models)):self.models[i].addEvidence(dataX, dataY)
    def query(self, points):    ## query 
        response = []
        for i in range(len(self.models)):response.append(self.models[i].query(points))
        response = np.array(response)
        result = np.mean(response, axis=0)
        return result