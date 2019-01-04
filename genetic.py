from job_scheduler import *
import copy

jobSchedule = createJobSchedule(20, 20, 15)
populacja = []
for i in range(1,1000):
	populacja.append(copy.deepcopy(jobSchedule))

#for job in jobSchedule:
#	print(str(job.start_time) + " " + str(job.work_left) + " " + str(job.done))
#print("Working..." + '\n')
#	
#print(evaluateLoop([1,1,1], jobSchedule))



	