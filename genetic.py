from job_scheduler import *



jobSchedule = createJobSchedule(5, 15, 10)
for job in jobSchedule:
	print(str(job.start_time) + " " + str(job.work_left) + " " + str(job.done))
print("Working..." + '\n')
	
evaluateLoop([1,1,1], jobSchedule)



	