import random
import numpy as np
import copy
debug = 0


class Job:
    def __init__(self, maxStartTime, maxLength):
        self.start_time = random.uniform(0, maxStartTime)
        self.job_length = random.uniform(0, maxLength)
        self.work_left = self.job_length
        self.done = 0
        self.done_time = 0
        self.time_waited = 0

    def __repr__(self):
        return str(self.start_time) + " " + str(self.work_left) + " " + str(self.done)

def createJobSchedule(numberOfJobs, maxStartTime, maxLength):
    jobSchedule = []
    for i in range(0, numberOfJobs):
        jobSchedule.append(Job(maxStartTime, maxLength))
    jobSchedule.sort(key=lambda x: x.start_time)
    return jobSchedule


def doWork(wagi, jobSchedule, workTokens, startTime, taskInProgress):
    if debug:
        print("debug...")
        print("time is " + str(startTime))
        print("tokens - " + str(workTokens))
        print("wagi: ")
        for waga in wagi:
            print(waga)
    startTokens = workTokens # Tokeny odliczają czas wykonania zadania
    if (workTokens == -99999):
        startTokens = 1000000
        workTokens = 1000000
    try:
        max_index = np.nanargmax(wagi)
    except ValueError:
        return

    # Tu dzieje się coś nowego
    if (taskInProgress[0] != None):
        if debug:
            print("taskInProgress = " + str(taskInProgress[0].start_time))
    if ((taskInProgress[0] != None) and (taskInProgress[0] != jobSchedule[max_index])):
        workTokens = workTokens - 1
        if debug:
            print("zmiana kontekstu, workTokens - 1")
    if (jobSchedule[max_index].work_left > workTokens):
        jobSchedule[max_index].work_left = jobSchedule[max_index].work_left - workTokens
        taskInProgress[0] = jobSchedule[max_index]
    else:
        # if (jobSchedule[max_index].done == 1): załatwione trycatchem wyzej
        #	return
        jobSchedule[max_index].done = 1
        wagi[max_index] = np.nan
        workTokens = workTokens - jobSchedule[max_index].work_left
        usedTokens = startTokens - workTokens
        jobSchedule[max_index].work_left = 0
        jobSchedule[max_index].time_waited = startTime + usedTokens - jobSchedule[max_index].start_time
        jobSchedule[max_index].done_time = startTime + usedTokens
        taskInProgress[0] = None

        if debug:
            print("time waited = " + str(jobSchedule[max_index].time_waited))
            print("time done = " + str(jobSchedule[max_index].done_time))
        if (workTokens != 0):
            doWork(wagi, jobSchedule, workTokens, startTime + usedTokens, taskInProgress)
    if debug:
        print("stan...")
        for job in jobSchedule:
            print(
                str(job.start_time) + " " + str(job.work_left) + " " + str(job.done) + " " + str(job.done_time) + " " + str(
                    job.time_waited))


def evaluateLoop(params, orygJobSchedule):
    jobSchedule = copy.deepcopy(orygJobSchedule)
    workLeftParam = int(params[0])
    timeOfBirthParam = int(params[1])
    costOfTransition = int(params[2])

    presentTime = 0
    taskInProgress = []
    taskInProgress.append(None)
    workTokens = 0
    # wyznacza wagę zadań w danym momencie i decyduje o kolejności wykonania na podstawie parametrów
    for i in range(0, len(jobSchedule)):
        # wiem że są posegregowane asc start_time
        workTokens = 0
        if (i + 1 < len(jobSchedule)):
            workTokens = jobSchedule[i + 1].start_time - jobSchedule[i].start_time
        else:
            workTokens = -99999  # ostatni element, będzie pracował ile trzeba. Przypadek do uwzględnienia później
        wagi = np.zeros(i + 1)
        for j in range(0, i + 1):
            # dla i = 0 wykona się raz
            if (jobSchedule[j].done == 0):
                if (taskInProgress[0] != jobSchedule[j]):
                    wagi[j] = (timeOfBirthParam * (
                                jobSchedule[i].start_time - jobSchedule[j].start_time) - costOfTransition) - (
                                          workLeftParam * jobSchedule[j].work_left)
                # czyli waga = [ a ( teraz - timeOfBirth) - karaZaPrzejście ] - ( b * work_left)
                else:
                    wagi[j] = (timeOfBirthParam * (jobSchedule[i].start_time - jobSchedule[j].start_time)) - (
                                workLeftParam * jobSchedule[j].work_left)
                # bez kosztu zmiany
            else:
                wagi[j] = np.nan
        doWork(wagi, jobSchedule, workTokens, jobSchedule[i].start_time, taskInProgress)
    avg_waited = 0
    for job in jobSchedule:
        avg_waited = avg_waited + job.time_waited
    avg_waited = avg_waited / float(len(jobSchedule))
    list_for_time_done = [job.done_time for job in jobSchedule]
    sum_time = max(list_for_time_done)
    if debug:
        print([avg_waited, sum_time])
    return (1 / sum_time) + (1 / avg_waited)  # wstępna funkcja celu
