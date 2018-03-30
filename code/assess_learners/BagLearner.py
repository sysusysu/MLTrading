import numpy as np
import scipy.stats
import DTLearner
import LinRegLearner

class BagLearner(object):

    def __init__(self, learner, kwargs = {}, bags = 20, boost = False, verbose = False):
        self.models = []
        self.verbose = verbose
        for i in range(bags):
            self.models.append(learner(**kwargs))


    def addEvidence(self,dataX,dataY):
        ## do bootstrap aggregating and training
        for i in range(len(self.models)):
            #print "Iteration ", i
            chosen = np.random.choice(dataX.shape[0], dataX.shape[0], replace=True)
            self.models[i].addEvidence(dataX[chosen], dataY[chosen])
        
    def query(self, points):
        response = []
        for i in range(len(self.models)):
            
            response.append(self.models[i].query(points))
        response = np.array(response)
        if self.verbose:
            print "Result from all learners: "
            print response
        result = np.mean(response, axis=0)
        return result
