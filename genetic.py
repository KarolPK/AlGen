from job_scheduler import *



jobSchedule = createJobSchedule(1, 5, 10)
for job in jobSchedule:
	print(str(job.start_time) + " " + str(job.work_left) + " " + str(job.done))
	
evaluateLoop([1,1,1], jobSchedule)

for job in jobSchedule:
	print(str(job.start_time) + " " + str(job.work_left) + " " + str(job.done))

	