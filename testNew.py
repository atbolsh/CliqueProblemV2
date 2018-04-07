from newRegress import *
from graphReader import *
from BigC import biggestClique
from BigC import verifyClique

#First, a simplistic test.
G = np.array(
[[0, 1, 1, 0, 0],
[1, 0, 1, 0, 1],
[1, 1, 0, 1, 0],
[0, 0, 1, 0, 0],
[0, 1, 0, 0, 0]])

H = graphToH(G)
start = np.array([0, 0, 0, 0, 1])
x, c, errors = seek(start, H, renormL2, 1e-2, 1e-6, 10000, 100)
print c


G = getGraph()
#We add the main diagonal (that's really it).
H2 = graphToH(G)

Y = []
for i in range(125):
   x = np.zeros(125)
   x[i] = 1
   y, c2, errors2 = seek(x, H2, renormL2, 1e-2, 1e-8, 100000000000000, 1000)
   Y.append(y)
   R = biggestClique(np.fabs(y), G)
   print R
   print len(R)
   print verifyClique(R, G)

