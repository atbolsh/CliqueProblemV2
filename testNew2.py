from regressLn2 import *
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
start = np.array([1, 0, 0, 0, 0])
x, c, errors = seek(start, H, renormL2, 1, 1e-2, 1e-6, 10000, 100)
print c


G = getGraph(h10_4, N10_4)
#We add the main diagonal (that's really it).
H2 = graphToH(G)

Y = []
C = []
for i in range(0, N10_4, 1):
   x = np.random.rand(N10_4)*0.001
   x[i] = 1
   y, c2, errors2 = seek(x, H2, renormL2, 64,  1e-3, 1e-8, 100000000000000, 1000)
   Y.append(y)
   R = biggestClique(np.fabs(y), G)
   f = open('Results_h10_4_L26_2', 'a')
   f.write('\n\n' + str(R) + '\n' + str(len(R)) + '\n\n')
   f.close()
   C.append(R)
   print R
   print len(R)
   print verifyClique(R, G)

print max([len(R) for R in C])

