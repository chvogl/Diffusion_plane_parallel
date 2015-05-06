__author__ = 'cvogl'
import numpy as np
import matplotlib.pyplot as plt
from scipy import constants

c = 100 * constants.c  # in cm s^-1
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


class Experiment:
    def __init__(self, E, N):
        self.E = E
        self.N = N

    def Radfield_at_time(self, t):
        ylist = np.zeros(self.N)
        epacket = self.E / float(self.N)
        for i in xrange(self.N):
            Testpacket = Packet(epacket)
            while Testpacket.ltot / c <= t:
                Testpacket.step()
            ylist[i] = Testpacket.y
        return ylist

    def TheoryPlot(self, t, plotcolor):
        """Plots theoretical prediction for the radiation
         field energy density at time t"""
        E = self.E
        D = c / (3 * xi)
        x = np.linspace(-0.5, 0.5, num=100)
        E_density = E * np.exp(-x ** 2 / (4 * D * t)) / np.sqrt(4 * np.pi * D * t)
        plt.plot(x, E_density, color=plotcolor)
        plt.ylabel('E [erg cm^-1]')
        plt.xlabel('x [cm]')
        plt.axis([-0.5, 0.5, 0, 1.4E9])

    def MCplot(self, t, no_bins, plotcolor):
        """Plots result of Monte Carlo simulation of the
        radiation field energy density at time t"""
        Explist = self.Radfield_at_time(t)
        weightslist = [self.E * no_bins / float(self.N) for i in range(len(Explist))]
        binwidth = 1. / no_bins
        bins1 = np.arange(-0.5, 0.5 + binwidth, binwidth)
        plt.hist(Explist, bins=bins1, weights=weightslist, color=plotcolor, facecolor='g', alpha=0.75, histtype='step')
        plt.ylabel('E [erg cm^-1]')
        plt.xlabel('x [cm]')
        plt.axis([-0.5, 0.5, 0, 1.4E9])


Exp1 = Experiment(10 ** 8, 10 ** 5)
Exp1.MCplot(5 * 10 ** (-12), 200, 'r')
Exp1.MCplot(10 * 10 ** (-12), 200, 'b')
Exp1.MCplot(20 * 10 ** (-12), 200, 'g')
Exp1.MCplot(50 * 10 ** (-12), 200, 'y')
Exp1.TheoryPlot(5 * 10 ** (-12), 'r')
Exp1.TheoryPlot(10 * 10 ** (-12), 'b')
Exp1.TheoryPlot(20 * 10 ** (-12), 'g')
Exp1.TheoryPlot(50 * 10 ** (-12), 'y')
plt.show()


