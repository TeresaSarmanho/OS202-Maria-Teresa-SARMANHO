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

# Elements à trier
N = 32

reste = N%nbp
NLoc  = N//nbp

if reste != 0:
    print("Le nombre de processeur doit diviser le nombre d'éléments à trier.")
    globCom.Abort(-1)

values = []

if(rank == 0):
    # Génération du tableau local de valeurs
    values = np.random.rand(nbp, NLoc)
   
    #  Sort données locaux pour trouver les intervals des buckets
    values.sort()
    
    # Take nbp+1 values at regular intervals
    div = np.linspace(values[0], values[-1], nbp+1)

    # Choose the best values to be the intervals of the buckets
    

  #  print(values)   
    print(div)
     # Gather the values in the bucket array
    #values = np.concatenate(values) 

     # Envoi des tableaux à chaque processus
    #  for i in range(nbp):
    #     data_to_send = values 
    #     globCom.send(data_to_send, dest=(i + 1))


# elif(rank != 0):
#     data_received = []
#     data_received = globCom.recv(source=0)



# def bucketSort(array):
#     bucket = []
#     for i in range(len(array)):
#         bucket.append([])
#     for j in array:
#         index_b = int(10 * j)
#         bucket[index_b].append(j)
#     for i in range(len(array)):
#         bucket[i] = sorted(bucket[i])
#     k = 0
#     for i in range(len(array)):
#         for j in range(len(bucket[i])):
#             array[k] = bucket[i][j]
#             k += 1
#     return array


