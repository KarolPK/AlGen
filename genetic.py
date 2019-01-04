from job_scheduler import *
import copy
import bit_array

poolSize = 100
startAgeCoefficient = 512
startRemainingTimeCoeff = 512
startCostOfTrans = 100

import numpy as np

class Item:
    def __init__(self):
        self.workLeftParam = random.uniform(0, startAgeCoefficient)
        self.timeOfBirthParam = random.uniform(0, startRemainingTimeCoeff)
        self.costOfTransition = random.uniform(0, startCostOfTrans)
        self.eval = np.nan

class Genetic:
    # exampleGen
    def __init__(self, poolSize):
        self.pool = []

        for i in range(poolSize):
            self.pool.append([random.uniform(0, startAgeCoefficient),
                              random.uniform(0, startRemainingTimeCoeff),
                              startCostOfTrans])

    def mutate(self):
        for genom in self.pool:
            for gen in genom:
                pass

jobSchedule = createJobSchedule(5, 15, 10)

for job in jobSchedule:
	print(job)

print("Working..." + '\n')
print("cel:", evaluateLoop([1, 1, 1], jobSchedule), '\n')

for i in Genetic(10).pool:
    print(i)