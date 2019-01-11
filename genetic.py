from job_scheduler import *
import random
import math
import matplotlib.pyplot as plt
import os
alias = 'piatek_4e'
os.mkdir(alias)

timeOfBirthBits = 9
workLeftBits = 9
costOfTransitionBits = 7
allBits = timeOfBirthBits + workLeftBits + costOfTransitionBits
pMutation = 0.005
pCrossover = 0.1

debug = 0

 # To delete
# maxTimeOfBirth = 1 << timeOfBirthBits - 1
# maxWorkLeft = 1 << workLeftBits - 1
# maxcostOfTransition = 1 << costOfTransitionBits - 1

# for (int i = 0; i <= 7; i++) {
# 	        bool_array[7-i] = (integer_ & (1 << i)) != 0;
# 	    }
# 	}
#
#
# this.rule = new boolean[8];
# 	    for (int i = 0; i <= 7; i++) {
# 	        this.rule[7-i] = (rule & (1 << i)) != 0;
# 	    }
# 	}


class SchParams():
    def __init__(self, jobSchedule): # self.workLeftParam(), self.timeOfBirthParam(), self.costOfTransition()
        self.bits = list(format(random.randrange(0, (1 << allBits) - 1), '0'+str(allBits)+'b'))
        # print(self.bits)
        for i, bit in enumerate(self.bits):
            self.bits[i] = int(bit)
        self.eval = evaluateLoop([self.workLeftParam(), self.timeOfBirthParam(), self.costOfTransition()], jobSchedule)
        self.accEval = 0

    # def __init__(self, value):
    #     if isinstance(value, list):
    #         self.bits = value
    #     else:

    def __str__(self):
        return '0b' + self.__repr__()

    def __repr__(self):
        return ''.join([bin(i)[2:] for i in self.bits])

    # def __int__(self):
    #     return int(self.__repr__(), 2)

    def __int__(self, gene):
        out = 0
        for bit in self.bits:
            out = (out << 1) + bit
        return out

    def __getitem__(self, index):
        if isinstance(index, slice):
            return [self[x] for x in range(*index.indices(len(self)))]
        else:
            if index > len(self.bits):
                raise IndexError
            return self.bits[index]

    def __setitem__(self, key, value):
        if key == -1:
            self.bits = [value] + list(
                "{0:b}".format(random.randrange(0, (1 << timeOfBirthBits + workLeftBits + costOfTransitionBits) - 1)))
            for i, bit in enumerate(self.bits):
                self.bits[i] = int(bit)
        else:
            self.bits[key] = value

    def __len__(self):
        return len(self.bits)

    # def __add__(self, other):
    #     return int(self.bits() + other.bits(), 2)

    def __eq__(self, other):
        if len(self) == len(other):
            for index in range(len(self)):
                if self.bits[index] != other[index]:
                    return False
                return True
        else:
            return False


    def workLeftParam(self):
        out = 0
        for bit in self.bits[0:timeOfBirthBits]:
            out = (out << 1) + bit
        return out

    def timeOfBirthParam(self):
        out = 0
        for bit in self.bits[timeOfBirthBits:timeOfBirthBits + workLeftBits]:
            out = (out << 1) + bit
        return out

    def costOfTransition(self):
        out = 0
        for bit in self.bits[timeOfBirthBits + workLeftBits:]:
            out = (out << 1) + bit
        return out

class Genetic:
    def __init__(self, poolSize):
        self.pool = []
        self.jobSchedule = createJobSchedule(20, 30, 10)
        self.fitness = 0

        for i in range(poolSize):
            self.pool.append(SchParams(self.jobSchedule))
        for i in self.pool:
            self.fitness += i.eval

    def __str__(self):
        temp = '['
        for sch in self.pool:
            temp += str(sch.eval)[:7] + ', '
        temp = temp[:-2] + ']'
        return temp

    def eval(self):
        for sch in self.pool:
            sch.eval = evaluateLoop([sch.workLeftParam(), sch.timeOfBirthParam(), sch.costOfTransition()], self.jobSchedule)

    def mutate(self):
        if debug:
            temp = copy.deepcopy(self.pool)
        for scheme in self.pool:
            for i in range(len(scheme)):
                if random.random() < pMutation:
                    if scheme[i] == 0:
                        scheme[i] = 1
                    else:
                        scheme[i] = 0
                    scheme.eval = 0
        if debug:
            for num in range(len(self.pool)):
                if self.pool[num].bits != temp[num].bits:
                        print('mutation:', num, self.pool[num].bits, temp[num].bits)


    def gene_pairs(self):
        it = iter(self.pool)
        try:
            while True:
                a, b = next(it), next(it)
                yield a, b
        except StopIteration:
            pass

    def cross(self):
        for genome1, genome2 in self.gene_pairs():
            if not genome2: # jeśli jest pusty nie krzyżuj
                return
            if random.random() < pCrossover:
                cPoint = random.randrange(1, len(genome1.bits))
                n_gen1 = genome1.bits[:cPoint] + genome2.bits[cPoint:]
                n_gen2 = genome2.bits[:cPoint] + genome1.bits[cPoint:]
                # print(genome1.__getattribute__(attr), genome2.__getattribute__(attr), cPoint, n_gen1, n_gen2)
                genome1.bits = n_gen1
                genome2.bits = n_gen2

    def select(self):
        selectedPop = []
        #zmiana fitness
        minEval = self.pool[0].eval
        for sch in self.pool:
            if sch.eval < minEval:
                minEval = sch.eval
        minEval *= 0.9
        for sch in self.pool:
            sch.eval -= minEval

        self.fitness = 0
        for sch in self.pool:
            self.fitness += sch.eval
        for sch in self.pool:
            sch.eval /= self.fitness
        #akumulacja
        self.pool.sort(key=lambda x: x.eval, reverse = True)
        tempAccEval = 0
        for sch in self.pool:
            tempAccEval += sch.eval
            sch.accEval = tempAccEval
        while len(selectedPop) < len(self.pool):
            pick = random.random()
            for specimen in self.pool:
                if specimen.accEval > pick:
                    selectedPop.append(copy.deepcopy(specimen))
                    break
        del self.pool
        self.pool = selectedPop

    def run(self, maxGenerations=0, minDelta=0):
        logs = []
        generation = 0
        delta = 1
        lastOverallFitness = self.fitness
        while ((maxGenerations and minDelta == 0 and generation < maxGenerations) or
               (maxGenerations == 0 and minDelta and delta > minDelta) or
               (maxGenerations and minDelta and generation < maxGenerations and delta > minDelta)):

            if debug:
                print(generation)
            self.cross()
            self.mutate()
            self.eval()
            Xplt = []
            if generation == 0:
                xmin = 0.9 * (self.pool[len(self.pool) - 1].eval)
                xmax = 2 * (self.pool[0].eval) - xmin
            if not generation % 20:
                print(self)
                count = 0
                same = 0
                for a in self.pool:
                    for b in self.pool:
                        if a == b:
                            count += 1
                        if a is b:
                            same += 1
                print("Same:", same, "Identical", count, "Best:", round(self.pool[0].eval, 5), "Worst:",
                      round(self.pool[len(self.pool) - 1].eval, 5))
            if generation % 10 == 0:
                if xmin > (self.pool[len(self.pool) - 1].eval):
                    xmin = self.pool[len(self.pool) - 1].eval
                if xmax < self.pool[0].eval:
                    xmax = 1.05 * self.pool[0].eval
                for i in self.pool:
                    Xplt.append(i.eval)
                plt.clf()
                # plt.axvline(x=fifo_eval, label='FIFO', color='r')
                fig, ax = plt.subplots(1)
                plt.text(0.8, 0.9, 'FIFO: '+ str(fifo_eval), transform=ax.transAxes)
                plt.xlim([xmin, xmax])
                plt.ylim([0, len(self.pool)])
                plt.hist(Xplt, bins=20)
                plt.grid()
                plt.savefig(alias+'/'+alias+'_'+str(generation))

            temp = (generation, round(lastOverallFitness, 3), round(delta, 3))
            print(temp)

            logs.append(temp)
            logFitness.append(lastOverallFitness / len(self.pool))
            lastOverallFitness = self.fitness

            self.select() # UWAGA normalizuje sie fittness

            delta = (- self.fitness + lastOverallFitness) / lastOverallFitness
            if debug:
                pairs = 0
                for first in self.pool:
                    for second in self.pool:
                        if first is second:
                            pairs += 1
                print (len(self.pool), '\t', round(delta, 4), '\t', round(lastOverallFitness, 2), '\t', round(self.fitness, 2))

            generation += 1

        # for v1, v2, v3 in logs:
        #     print(v1, round(v2, 2), round(v3, 2))


pop = Genetic(100)

logFitness = []
fifo_eval = round(evaluateLoop([0, 1000, 0], pop.jobSchedule), 3)
print("FIFO: ", fifo_eval)
pop.run(101, 0)

plt.clf()
plt.plot(range(len(logFitness)),logFitness)
plt.grid()
plt.savefig(alias + '/' + alias + '_' + 'fitness')

plt.clf()
# fig, ax = plt.subplots(1)
# plt.xlim([xmin, xmax])
# plt.ylim([0, len(self.pool)])
# plt.hist(Xplt, bins=20)