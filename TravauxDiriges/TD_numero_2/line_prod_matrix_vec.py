import numpy as np
from dataclasses import dataclass
from PIL import Image
from math import log
from time import time
import matplotlib.cm
from mpi4py import MPI

globCom = MPI.COMM_WORLD.Dup()
nbp     = globCom.size
rank    = globCom.rank
name    = MPI.Get_processor_name()

# dimension
N = 16

reste = N%nbp

if reste != 0:
    print("Le nombre de processeur doit diviser le nombre de processus.")
    globCom.Abort(-1)

# columns per task
NLoc = N // nbp

# pour que chaque processus ait son partie de la matrice
part = rank * N//nbp

# Initialisation de la matrice
A = np.array([[(i + j + part) % N+1. for i in range(N)] for j in range(NLoc)])
print("proc",rank, ": A =", A)

# Initialisation du vecteur u
u = np.array([part+i+1. for i in range(N)])
print("proc",rank,"u =",u)

# Produit matrice-vecteur
beg = time()
v_aux = A.dot(u)
v = np.empty(N)

globCom.Allgather(v_aux, v)
end = time()
diff = end - beg
print("proc",rank,": v =", v)
print("proc",rank,": time : ", diff)