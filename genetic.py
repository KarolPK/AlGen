from job_scheduler import *
import bit_array
import random

poolSize = 100
startAgeCoefficient = 512
startRemainingTimeCoeff = 512
startCostOfTrans = 100

import numpy as np

class SchParams:
    def __init__(self, jobSchedule):
        self.workLeftParam = random.uniform(0, startAgeCoefficient)
        self.timeOfBirthParam = random.uniform(0, startRemainingTimeCoeff)
        self.costOfTransition = random.uniform(0, startCostOfTrans)
        self.eval = evaluateLoop([self.workLeftParam, self.timeOfBirthParam, self.costOfTransition], jobSchedule)
        self.accEval = 0
        
class Genetic:
    # exampleGen
    def __init__(self, poolSize):
        self.pool = []
        self.jobSchedule = createJobSchedule(5, 15, 10)

        for i in range(poolSize):
            self.pool.append(SchParams(self.jobSchedule))

    def mutate(self):
        for genom in self.pool:
            for gen in genom:
                pass
    def select(self):
        selectedPop = []
        #normalizacja fitness 
        norm = 0
        for sch in self.pool:
            norm += sch.eval
        for sch in self.pool:
            sch.eval /= norm
        #akumulacja
        self.pool.sort(key=lambda x: x.eval, reverse = True)
        tempAccEval = 0
        for sch in self.pool:
            tempAccEval += sch.eval
            sch.accEval = tempAccEval
        while selectedPop < len(self.pool):
            pick = random.uniform(0, 1)
            for i in range(1,len(self.pool)):
                if self.pool[i].accEval > pick:
                    selectedPop.append(self.pool[i])
                    break
        self.pool = selectedPop
        
        
        
            
        
        
        


pop = Genetic(100)
pop.select()


