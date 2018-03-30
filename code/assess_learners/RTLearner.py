import numpy as np
import scipy.stats

class RTLearner(object):

    def __init__(self, leaf_size = 1, verbose = False):
        self.leaf_size = leaf_size
        self.verbose = verbose
        self.tree = None


    
    ## tree structure: feature/leaf, value, left child, right child
    def make_tree(self, dataX, dataY, leaf_size):
        ## return if there is only one data point
        if dataX.shape[0] <= leaf_size:
            return np.array([['leaf', np.mean(dataY), np.nan, np.nan]])

        else:
            compare = dataY[0] == dataY
            ## return if all data points have the same value
            if np.sum(compare) == dataY.shape[0]:
                return np.array([['leaf', dataY[0], np.nan, np.nan]])

            else:
                    ## determine the best feature to split using correlation
                
                best_idx = np.random.randint(0, dataX.shape[1])
                split_val = np.median(dataX[:,best_idx])
                selected = dataX[:, best_idx]<=split_val
                ## make sure it is a valid split
                if np.sum(selected) == len(selected):
                    #print "--problem coo: ", result
                    #print "--problem index: ", best_idx, "; split val: ",split_val," co: ", scipy.stats.pearsonr(dataX[:,best_idx], dataY)
                    #print dataX
                    split_val = np.mean(dataX[:,best_idx])
                    selected = dataX[:, best_idx]<=split_val
                    
                while np.sum(selected) == len(selected) or np.sum(selected)==0:
                    best_idx = np.random.choice(dataX.shape[1])
                    split_val = np.mean(dataX[:,best_idx])
                    selected = dataX[:, best_idx]<=split_val

                left_tree = self.make_tree(dataX[selected,:], dataY[selected], leaf_size)
                inverse_selected = np.invert(selected)
                right_tree = self.make_tree(dataX[inverse_selected,:], dataY[inverse_selected], leaf_size)
                root = np.array([[best_idx, split_val, 1, left_tree.shape[0]+1]])
                return np.concatenate((root, left_tree, right_tree), axis=0)
                

    def addEvidence(self,dataX,dataY):
        """
        @summary: Add training data to learner
        @param dataX: X values of data to add
        @param dataY: the Y training values
        """

        # make tree
        ##[feature, value, left, right]

        self.tree = self.make_tree(dataX, dataY, self.leaf_size)
        
    def query2(self, tree, point):
        result = -1
        if tree[0,0] == 'leaf':
            return float(tree[0,1])
        idx = int(float(tree[0,0]))
        if point[idx] <= float(tree[0,1]):
            result = self.query2(tree[1:, :], point)
        else:
            right_idx = int(float(tree[0,3]))
            result = self.query2(tree[right_idx:], point)
        return result

    def query(self, points):
        response = []
        for i in range(points.shape[0]):
            response.append(self.query2(self.tree, points[i,:]))
        return np.array(response)
  