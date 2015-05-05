__author__ = 'cvogl'
import numpy as np
import matplotlib.pyplot as plt
from scipy import constants

c = 0.01 * constants.c  # in cm s^-1
xi = 100.


class Packet:
    def __init__(self, E):
        self.E = E
        self.y = 0.
        self.mu = 2 * np.random.random() - 1
        self.ltot = 0.

    def step(self):
        l_free = -np.log(np.random.random()) / xi
        self.y += self.mu * l_free
        self.mu = 2 * np.random.random() - 1
        self.ltot += l_free

    def getltot(self):
        return self.ltot

    def gety(self):
        return self.y


class Experiment:
    def __init__(self, E, N):
        self.E = E
        self.N = N

    def getEpacket(self):
        return self.E / float(self.N)

    def Radfield_at_time(self, t):
        ylist = np.zeros(self.N)
        epacket = self.E / float(self.N)
        for i in xrange(self.N):
            Testpacket = Packet(epacket)
            while Testpacket.getltot() / c <= t:
                Testpacket.step()
            ylist[i] = Testpacket.gety()
        return ylist


Exp1 = Experiment(10 ** 8, 10000)
Exp1list = Exp1.Radfield_at_time(5 * 10 ** (-12))
plt.hist(Exp1list, 50, normed=1, facecolor='g', alpha=0.75, histtype='step')
plt.show()


