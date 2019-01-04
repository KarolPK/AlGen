from job_scheduler import *
import copy

poolSize = 100
startAgeCoefficient = 512
startRemainingTimeCoeff = 512
startCostOfTrans = 100
class Genetic:

    # exampleGen
    def __init__(self, poolSize):
        self.pool = []

        for i in range(poolSize):
            self.pool.append([random.uniform(0, startAgeCoefficient),
                              random.uniform(0, startRemainingTimeCoeff),
                              startCostOfTrans])

    def mutate:
        for genom in self.pool:
            for gen in genom:



jobSchedule = createJobSchedule(5, 15, 10)
tries = []*10
for i, t in enumerate(tries):
    tries[i] = copy.deepcopy(jobSchedule)
for job in jobSchedule:
	print(str(job.start_time) + " " + str(job.work_left) + " " + str(job.done))
print("Working..." + '\n')
	
print(evaluateLoop([1, 1, 1], jobSchedule), '\n')

for i in Genetic(10).pool:
    print(i)