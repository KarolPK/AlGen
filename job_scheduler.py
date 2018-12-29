import random

class Job(maxStartTime, maxLength):
	def __init__(self):
		start_time =  random.uniform(0, maxStartTime)
		job_length = random.uniform(0, maxLength)
	
def returnJobSchedule(numberOfJobs, maxStartTime, maxLength):
	jobSchedule = []
	for i in range (0, numberOfJobs):
		jobSchedule.append(Job(maxStartTime, maxLength))
