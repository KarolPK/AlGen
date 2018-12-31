import random

class Job:
	def __init__(self, maxStartTime, maxLength):
		self.start_time =  random.uniform(0, maxStartTime)
		self.job_length = random.uniform(0, maxLength)
		self.work_left = self.job_length
		self.done = 0
		
def createJobSchedule(numberOfJobs, maxStartTime, maxLength):
	jobSchedule = []
	for i in range (0, numberOfJobs):
		jobSchedule.append(Job(maxStartTime, maxLength))
	jobSchedule.sort(key = lambda x: x.start_time)
	return jobSchedule
	
def doWork(waga, jobSchedule, workTokens):
	max_waga = max(waga)
	max_index = waga.index(max_waga)
	if (jobSchedule[max_index].work_left > workTokens):
		jobSchedule[max_index].work_left = jobSchedule[max_index].work_left - workTokens
		taskInProgress = jobSchedule[max_index]
	else:
		jobSchedule[max_index].done = 1
		waga[max_index] = 0
		workTokens = workTokens - jobSchedule[max_index].work_left
		doWork(waga, jobSchedule, workTokens)

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
		wagi = [] #to zjebane, bo wzialem to za array a to lista. Musze albo zrobic z tego array uczciwy, albo waga umiescic jako atrybut joba (wtedy iteracja zawsze po calosci), albo trzymac tuple z indexem
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
				wagi[j] = 0
		doWork()
		
		
		

