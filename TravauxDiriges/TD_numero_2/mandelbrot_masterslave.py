# Calcul de l'ensemble de Mandelbrot en python
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

@dataclass
class MandelbrotSet:
    max_iterations: int
    escape_radius:  float = 2.0

    def __contains__(self, c: complex) -> bool:
        return self.stability(c) == 1

    def convergence(self, c: complex, smooth=False, clamp=True) -> float:
        value = self.count_iterations(c, smooth)/self.max_iterations
        return max(0.0, min(value, 1.0)) if clamp else value

    def count_iterations(self, c: complex,  smooth=False) -> int | float:
        z:    complex
        iter: int

        # On vérifie dans un premier temps si le complexe
        # n'appartient pas à une zone de convergence connue :
        #   1. Appartenance aux disques  C0{(0,0),1/4} et C1{(-1,0),1/4}
        if c.real*c.real+c.imag*c.imag < 0.0625:
            return self.max_iterations
        if (c.real+1)*(c.real+1)+c.imag*c.imag < 0.0625:
            return self.max_iterations
        #  2.  Appartenance à la cardioïde {(1/4,0),1/2(1-cos(theta))}
        if (c.real > -0.75) and (c.real < 0.5):
            ct = c.real-0.25 + 1.j * c.imag
            ctnrm2 = abs(ct)
            if ctnrm2 < 0.5*(1-ct.real/max(ctnrm2, 1.E-14)):
                return self.max_iterations
        # Sinon on itère
        z = 0
        for iter in range(self.max_iterations):
            z = z*z + c
            if abs(z) > self.escape_radius:
                if smooth:
                    return iter + 1 - log(log(abs(z)))/log(2)
                return iter
        return self.max_iterations

# On peut changer les paramètres des deux prochaines lignes
mandelbrot_set = MandelbrotSet(max_iterations=50, escape_radius=10)
width, height = 1024, 1024

scaleX = 3./width
scaleY = 2.25/height

# Calcul de l'ensemble de mandelbrot par ligne :
# en packets de lignes divisée par le processeurs
lines = height // nbp

# Master
if rank == 0:
    deb = time()
    lines_per_pack = 10
    total_lines = height
    current_line = 0
    convergence = np.empty((height, width), dtype=np.double)  # Matriz para armazenar os resultados
    for slave_rank in range(1, nbp):
        if current_line < total_lines:
            series_to_send = []
            for y_rel in range(lines_per_pack):
                if current_line < total_lines:
                    for x in range(width):
                        y = current_line + y_rel 
                        c = complex(-2. + scaleX * x, -1.125 + scaleY * y)
                        convergence[y, x] = mandelbrot_set.convergence(c, smooth=True)
                    current_line += 1
            globCom.send(convergence[current_line - lines_per_pack:current_line], dest=slave_rank)  # Enviar parte da matriz para o escravo
        else:
            break
    # Send termination signal to all slave processes
    for slave_rank in range(1, nbp):
        globCom.send(None, dest=slave_rank)
    fin = time()
    print(f"Temps d'exécution : {fin - deb}")

    # Constitution de l'image résultante :
    deb = time()
    image = Image.fromarray(np.uint8(matplotlib.cm.plasma(convergence.T)*255))
    fin = time()
    print(f"Temps de constitution de l'image : {fin-deb}")
    image.show()

else:
# Slave
    while True:
        series = globCom.recv(source=0)
        if series is None: break
        computed_series = []
        for row in series:
            for c in row:
                computed_series.append(mandelbrot_set.convergence(c, smooth=True))
        globCom.send(computed_series, dest=0)
