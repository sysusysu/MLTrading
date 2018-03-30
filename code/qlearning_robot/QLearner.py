

import numpy as np
import random as rand

class QLearner(object):

    def __init__(self, \
        num_states=100, \
        num_actions = 4, \
        alpha = 0.2, \
        gamma = 0.9, \
        rar = 0.5, \
        radr = 0.99, \
        dyna = 0, \
        verbose = False):

        self.verbose = verbose
        self.num_actions = num_actions
        self.num_states = num_states
        self.qtable = np.zeros((num_states,num_actions),dtype=float)
        self.alpha = alpha
        self.gamma = gamma
        self.rar = rar
        self.radr = radr
        self.dyna = dyna
        self.verbose = verbose
        
        self.s = 0
        self.a = 0
        
        if self.dyna>0:
            self.Tc = np.ones((num_states,num_actions,num_states))*0.00001
            self.R = np.zeros((num_states,num_actions))
#         print(self.qtable)
    def querysetstate(self, s):
        """
        @summary: Update the state without updating the Q-table
        @param s: The new state
        @returns: The selected action
        """
        self.s = s
        
        ## take a random number to decided whether return action by random
        action = 0
        if np.random.uniform(low=0.0, high=1.0)<=self.rar:
            action = rand.randint(0, self.num_actions-1)
        ## get best action from Q table
        else:
            action = np.argmax(self.qtable[s])
            
        self.a = action
            
        if self.verbose: print "s =", s,"a =",action
        
        return action
    def query(self,s_prime,r):
        """
        @summary: Update the Q table and return an action
        @param s_prime: The new state
        @param r: The ne state
        @returns: The selected action
        """
        action = 0
        ## take a random number to decided whether return action by random
        if np.random.uniform(low=0.0, high=1.0)<=self.rar:
            action = rand.randint(0, self.num_actions-1)
        ## get best action from Q table
        else:
            action = np.argmax(self.qtable[s_prime])
            
        self.rar *= self.radr
        
        ## update Q table
        self.qtable[self.s, self.a] = (1-self.alpha)*self.qtable[self.s, self.a] + self.alpha*(r+self.gamma*self.qtable[s_prime,action])
        
        
        ## update Tc and R
        if self.dyna>0:
            self.R[self.s, self.a] = (1-self.alpha)*self.R[self.s, self.a] + self.alpha*r
            self.Tc[self.s, self.a, s_prime] += 1
        
        ## hallucinate
        for i in range(self.dyna):
            rand_a = rand.randint(0, self.num_actions-1)
            rand_s = rand.randint(0, self.num_states-1)
            # infer Tc
            # new_s = 0
            # rand_nb = np.random.uniform(low = 0.0, high = float(np.sum(self.Tc[rand_s, rand_a, :])))
            # sum_tc = 0
            # for i in range(self.Tc.shape[2]):
            #     sum_tc += self.Tc[rand_s, rand_a, i]
            #     if sum_tc >= rand_nb:
            #         new_s = i
            #         break
            new_s = np.argmax(self.Tc[rand_s, rand_a, :])
            # infer R
            new_r = self.R[rand_s, rand_a]
            # update Q
            new_a = np.argmax(self.qtable[new_s])
            self.qtable[rand_s, rand_a] = (1-self.alpha)*self.qtable[rand_s, rand_a] + self.alpha*(new_r+self.gamma*self.qtable[new_s,new_a])
        
        
        self.s = s_prime
        self.a = action
        
        if self.verbose: print "s =", s,"a =",action
        return action 
        



if __name__=="__main__":
    print "Remember Q from Star Trek? Well, this isn't him"
