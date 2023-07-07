from numpy import argmax, exp, array, random
import numpy as np

# #Génération des poids dans l'interval [-1;1]
random.seed(1)
borneMin = -1
borneMax = 1

class NN:
    vectEntrees = np.empty(0)
    poidsEntrees = np.empty([0, 0])
    poidsSorties = np.empty([0, 0])
    vectSorties = np.empty(0)
    
    def __init__(self, neurE,neurC,neurS):
            self.poidsEntrees = np.empty([neurC, neurE])
            self.poidsSorties = np.empty([neurS, neurC])
            for i in range(0,neurC):
                for j in range(0,neurE):
                    self.poidsEntrees[i,j] = (borneMax-borneMin) * random.random() + borneMin
            for i in range(0,neurS):
                for j in range(0,neurC):
                    self.poidsSorties[i,j] = (borneMax-borneMin) * random.random() + borneMin                   
    
    def AssignEntrees(self,Entrees):
        self.vectEntrees = Entrees
    
    def ComputeSorties(self):
        sumPondInter = np.dot(self.poidsEntrees,self.vectEntrees)
        for i in range(np.size(sumPondInter)):
            sumPondInter[i] = max(0,sumPondInter[i])
        sorties = np.dot(self.poidsSorties,sumPondInter)
        return np.argmax(sorties)
            
            
    


def somme_ponderee(X1,W11,X2,W21,B,WB):
    return (B*WB+( X1*W11 + X2*W21))

def somme_ponderee2(X,poidsEntrees,poidsSorties):
    sumPondInter = np.dot(poidsEntrees,X)
    return np.dot(poidsSorties,sumPondInter)
