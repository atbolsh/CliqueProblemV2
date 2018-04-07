import math
from copy import deepcopy

import numpy as np
from numpy.linalg import eig
from numpy.linalg import inv
from numpy.linalg import svd
from numpy.linalg import norm

import matplotlib.pyplot as plt


#Just fills the main diagonal
def graphToH(G):
    """For a connectivity matrix G, returns the corresponding H2."""
    H2 = deepcopy(G)
    np.fill_diagonal(H2, 1)
    return H2

#Gets the prototypical error matrix.
def getM(H2):
    """Matrix of all the holes"""
    return np.ones(H2.shape) - H2

def getm(H2):
    """returns ones of the right size"""
    return np.ones(H2.shape[0])

#Useful for norms below 2.
def ReLu(x):
    """Rectified Linear Unit"""
    return np.maximum(x, 0)


#We keep the vectors normalized, to avoid falling into the origin.
#This one traps y on the unit sphere.
def renormL2(y):
    return y/norm(y)

#This one traps y on the unit cube.
def renormCube(y):
    return y/np.max(np.fabs(y))


def projection(a, b):
    """Compute the projection of a onto b."""
    d = np.dot(a, b)
    s = np.sum(b*b)
    return b*d/s

def energy(x, M):
    return np.sum(np.outer(x, x)*M)

def seek(x, H2, ren=renormL2, beta = 0.001, cutoff=1e-6, maxIter = 100000, recordStep=100):
    """The main loop. Assumes that the energy of x is 0"""
    M  = getM(H2)
    m  = getm(H2)
    errors = []
    i = 0
    y = ren(x)
    while i < maxIter:
        #### First, the deep math.
        # Gradient of energy.
        g = np.matmul(M, y)
        # Step direction
        step = m - projection(m, g) - projection(m, y)
        r = norm(step)
        #  Grad descent.
        y = y + beta*step
        #  Renorm
        g2 = np.matmul(M, y)
        y = y - projection(y, g2) #Return to 0 energy
        y = ren(y)
        #### Next the logistics; counters, etc.
        s = np.sum(ReLu(np.sign(np.round(y, 1))))
        if recordStep != 0 and i % recordStep == 0:
            print y
            print r
            print s
            print '#####'
            errors.append(r)
        i += 1
        if r < cutoff:
            break
    #Return vector, the clique it represents, and the error trace.
    return y, ReLu(np.sign(np.round(y, 4))), errors


