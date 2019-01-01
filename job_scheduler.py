import random
import numpy as np
import math

class Job:
	def __init__(self, maxStartTime, maxLength):
		self.start_time =  random.uniform(0, maxStartTime)
		self.job_length = random.uniform(0, maxLength)
		self.work_left = self.job_length
		self.done = 0
		self.done_time = 0
		
def createJobSchedule(numberOfJobs, maxStartTime, maxLength):
	jobSchedule = []
	for i in range (0, numberOfJobs):
		jobSchedule.append(Job(maxStartTime, maxLength))
	jobSchedule.sort(key = lambda x: x.start_time)
	return jobSchedule
	
def doWork(wagi, jobSchedule, workTokens):
	print("debug...")
	print("tokens - " + str(workTokens))
	print("wagi: ")
	for waga in wagi:
		print(waga)
		
	if (workTokens == -1):
		#ostatni job, wykonujemy po kolei
		for job in jobSchedule:
			job.done = 1
			job.work_left = 0
		return
	max_index = np.nanargmax(wagi)
	if (jobSchedule[max_index].work_left > workTokens):
		jobSchedule[max_index].work_left = jobSchedule[max_index].work_left - workTokens
		taskInProgress = jobSchedule[max_index]
	else:
		if (jobSchedule[max_index].done == 1):
			return
		jobSchedule[max_index].done = 1
		wagi[max_index] = math.nan
		workTokens = workTokens - jobSchedule[max_index].work_left
		jobSchedule[max_index].work_left = 0
		if (workTokens != 0):
			doWork(wagi, jobSchedule, workTokens)
	print("stan...")
	for job in jobSchedule:
		print(str(job.start_time) + " " + str(job.work_left) + " " + str(job.done))

def evaluateLoop(params, jobSchedule):
	workLeftParam = params[0]
	timeOfBirthParam = params[1]
	costOfTransition = params[2]
	presentTime = 0
	taskInProgress = None
	workTokens = 0
#wyznacza wagę zadań w danym momencie i decyduje o kolejności wykonania na podstawie parametrów
	for i in range(0, len(jobSchedule)):
	#wiem że są posegregowane asc start_time
		workTokens = 0
		if (i+1 < len(jobSchedule)):
			workTokens = jobSchedule[i+1].start_time - jobSchedule[i].start_time
		else:
			workTokens = -1 #ostatni element, będzie pracował ile trzeba. Przypadek do uwzględnienia później
		wagi = np.zeros(i+1)
		for j in range(0, i+1):
		#dla i = 0 wykona się raz
			if (jobSchedule[j].done == 0):
				if (taskInProgress != jobSchedule[j]):
					wagi[j] = (timeOfBirthParam * (jobSchedule[i].start_time - jobSchedule[j].start_time) - costOfTransition) - (workLeftParam * jobSchedule[j].work_left)
					# czyli waga = [ a ( teraz - timeOfBirth) - karaZaPrzejście ] - ( b * work_left) 
				else:
					wagi[j] = (timeOfBirthParam * (jobSchedule[i].start_time - jobSchedule[j].start_time)) - (workLeftParam * jobSchedule[j].work_left)
					# bez kosztu zmiany
			else:
				wagi[j] = math.nan
		doWork(wagi, jobSchedule, workTokens)
		
		
#zrobić self done time

