lines = height // nbp

deb_l = time()
convergence_l = np.empty((lines, width ), dtype=np.double)

for y_rel in range(lines):
    for x in range(width):
        y = rank * lines + y_rel 
        c = complex(-2. + scaleX*x, -1.125 + scaleY * y)
        convergence_l[y_rel,x] = mandelbrot_set.convergence(c, smooth=True)
fin_l = time()
print(f"Temps du calcul de l'ensemble de Mandelbrot par ligne : {fin_l - deb_l}")

convergence_gathered = None
if rank == 0:
    convergence_gathered = np.empty((width, height), dtype=np.double)

globCom.Gather(convergence_l, convergence_gathered)

# Constitution de l'image résultante :
if rank == 0:
    deb = time()
    image = Image.fromarray(np.uint8(matplotlib.cm.plasma(convergence_gathered)*255))
    fin = time()
    print(f"Temps de constitution de l'image : {fin-deb}")
    image.show()
