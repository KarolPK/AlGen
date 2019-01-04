from job_scheduler import *
import random

poolSize = 100 # self.workLeftParam, self.timeOfBirthParam, self.costOfTransition
timeOfBirthBits = 9
workLeftBits = 9
costOfTransitionBits = 7
pMutation = 0.005
pCrossover = 0.05

maxTimeOfBirth = 1 << timeOfBirthBits - 1
maxWorkLeft = 1 << workLeftBits - 1
maxCostOfTransition = 1 << costOfTransitionBits - 1


class BitArray:
    def __init__(self, value):
        if isinstance(value, list):
            self.bits = value
        else:
            self.bits = list("{0:b}".format(value))
        for i, bit in enumerate(self.bits):
            self.bits[i] = int(bit)

        # temp = 0
        # for (int i = 0; i <= 7; i++) {
        #     this.rule[7 - i] = (rule & (1 << i)) != 0;
        # }

    def __str__(self):
        return '0b' + self.__repr__()

    def __repr__(self):
        return ''.join([bin(i)[2:] for i in self.bits])

    def __int__(self):
        return int(self.__repr__(), 2)

    def __getitem__(self, index):
        if isinstance(index, slice):
            return BitArray([self[x] for x in range(*index.indices(len(self)))])
        else:
            if index > len(self.bits):
                raise IndexError
            return self.bits[index]

    def __setitem__(self, key, value):
        self.bits[key] = value

    def __len__(self):
        return len(self.bits)

    def __add__(self, other):
        return BitArray(int(self.__repr__() + other.__repr__(), 2))

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


class SchParams:
    def __init__(self, jobSchedule): # self.workLeftParam, self.timeOfBirthParam, self.costOfTransition
        self.workLeftParam = BitArray(random.randrange(0, maxTimeOfBirth))
        self.timeOfBirthParam = BitArray(random.randrange(0, maxWorkLeft))
        self.costOfTransition = BitArray(random.randrange(0, maxCostOfTransition))
        self.eval = evaluateLoop([self.workLeftParam, self.timeOfBirthParam, self.costOfTransition], jobSchedule)
        self.accEval = 0


class Genetic:
    def __init__(self, poolSize):
        self.pool = []
        self.jobSchedule = createJobSchedule(5, 15, 10)

        for i in range(poolSize):
            self.pool.append(SchParams(self.jobSchedule))

    def mutate(self):
        for genome in self.pool:
            for gen in genome:
                for i in range(len(gen)):
                    if random.random() < pMutation:
                        if gen[i] == 0:
                            gen[i] = 1
                        else:
                            gen[i] = 0

    def cross(self):
        for genome1, genome2 in self.pool:
            for attr in ["workLeftParam", "timeOfBirthParam", "costOfTransition"]
                if random.random() < pCrossover:
                    cPoint = random.randrange(1, workLeftBits)
                    n_gen1 = genome1.__getattribute__(attr)[:cPoint] + genome2.__getattribute__(attr)[cPoint:]  # self.timeOfBirthParam, self.costOfTransition
                    n_gen2 = genome2.__getattribute__(attr)[:cPoint] + genome1.__getattribute__(attr)[cPoint:]
                    print(genome1.__getattribute__(attr), genome2.__getattribute__(attr), cPoint, n_gen1, n_gen2)
                    genome1.__setattr__(attr, n_gen1)
                    genome2.__setattr__(attr, n_gen2)

    def select(self):
        selectedPop = []
        #normalizacja fitness
        norm = 0
        for sch in self.pool:
            norm += sch.eval
        for sch in self.pool:
            sch.eval /= norm
        #akumulacja
        self.pool.sort(key=lambda x: x.eval, reverse = True)
        tempAccEval = 0
        for sch in self.pool:
            tempAccEval += sch.eval
            sch.accEval = tempAccEval
        while selectedPop < len(self.pool):
            pick = random.uniform(0, 1)
            for i in range(1,len(self.pool)):
                if self.pool[i].accEval > pick:
                    selectedPop.append(self.pool[i])
                    break
        self.pool = selectedPop


# pop = Genetic(100)
# pop.select()


# it = BitArray(16)
# print(repr(it))
# integ = it.__int__()
# print(type(integ), integ)
# print()
# print(it)
# for i in range(len(it)):
#     if random.random() < pMutation:
#         if it[i] == 0:
#             it[i] = 1
#         else:
#             it[i] = 0
# print(type(it), it)

# jS = createJobSchedule(5, 5, 5)
# genome1 = SchParams(jS)
# genome2 = SchParams(jS)
#
# cPoint = random.randrange(1, workLeftBits)
# n_gen1 = genome1.workLeftParam[:cPoint] + genome2.workLeftParam[cPoint:]  # self.timeOfBirthParam, self.costOfTransition
# n_gen2 = genome2.workLeftParam[:cPoint] + genome1.workLeftParam[cPoint:]
# print(genome1.workLeftParam, genome2.workLeftParam, cPoint, n_gen1, n_gen2)
# genome1.workLeftParam = n_gen1
# genome2.workLeftParam = n_gen2

# from operator import itemgetter
# temp = genome1.__set("workLeftParam")
# print(temp)
