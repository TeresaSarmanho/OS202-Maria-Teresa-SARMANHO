
# TD1

`pandoc -s --toc README.md --css=./github-pandoc.css -o README.html`





## lscpu

```
CPU(s):                  4
   Thread(s) per core:  2
    Core(s) per socket:  2
    Socket(s):           1
Caches (sum of all):     
  L1d:                   64 KiB (2 instances)
  L1i:                   64 KiB (2 instances)
  L2:                    512 KiB (2 instances)
  L3:                    4 MiB (1 instance) 
```

*Des infos utiles s'y trouvent : nb core, taille de cache*



## Produit matrice-matrice
1023
Test passed
Temps CPU produit matrice-matrice naif : 1.66079 secondes
MFlops -> 1289.27

1024   
Test passed
Temps CPU produit matrice-matrice naif : 6.01662 secondes
MFlops -> 356.926

1025
Test passed
Temps CPU produit matrice-matrice naif : 1.58869 secondes
MFlops -> 1355.7


### Permutation des boucles

*Expliquer comment est compilé le code (ligne de make ou de gcc) : on aura besoin de savoir l'optim, les paramètres, etc. Par exemple :*

`make TestProduct.exe && ./TestProduct.exe 1024`

Tests avec 1023
MFlops - operations sur des nombres réeles realisées par second
Plus faible le nb des retours, plus vite on peut faire les opérations, plus elevée le nombre de flops.

  ordre           | time    | MFlops  | MFlops(n=2048) 
------------------|---------|---------|----------------
i,j,k (origine)   | 2.73764 | 782.476 | 227.888               
j,i,k             | 2.7028  | 792.215 | 229.177   
i,k,j             | 19.3813 | 110.477 | 101.704   
k,i,j             | 19.2673 | 111.131 | 101.904   
j,k,i             | 1.18529 | 1806.48 | 1776.4   
k,j,i             | 1.00822 | 2123.74 | 2105.18   


*Discussion des résultats*

Du point de vue des opérations arithmétiques, le temps d'exécution devrait être le même. Cependant, les accès mémoire changent le temps de retour, et leur complexité doit être prise en compte pour le calcul de l'efficacité du code. Cela devient important avec la multiplication des cœurs des machines et l'utilisation des différents niveaux de mémoire cache.

Il est préférable de réaliser les opérations avec une continuité de mémoire afin de ne pas avoir à rechercher plusieurs informations à des endroits différents. Les données des matrices sont généralement stockées par colonnes, par conséquent, il est plus rapide de réaliser les opérations par colonnes. Ainsi, l'exécution sera plus rapide si nous augmentons le nombre d'opérations par colonnes.

*(Explicar as operações por colunas e os saltos feitos para acessar os elementos do produto caso seja feito por coluna ou por linha)*


### OMP sur la meilleure boucle 

`make TestProduct.exe && OMP_NUM_THREADS=8 ./TestProduct.exe 1024`

 8 threads: 0.417000 secondes, Acceleration = 3.738
 7 threads: 0.430886 secondes, Acceleration = 3.617
 6 threads: 0.473715 secondes, Acceleration = 3.290
 5 threads: 0.513591 secondes, Acceleration = 3.057
 2 threads: 0.912695 secondes, Acceleration = 1.707
 1 thread: 1.65728 secondes, Acceleration = 0.940


### Produit par blocs

`make TestProduct.exe && ./TestProduct.exe 1024`

La taille de bloc optimale été 256 et le temps employé 0.651482 secondes


### Bloc + OMP

Avec la parallélisation par bloc on obtient: 

8 threads: 0.179194 secondes, Acceleration = 3.693
7 threads: 0.183049 secondes, Acceleration = 3.615
6 threads: 0.199149 secondes, Acceleration = 3.323
5 threads: 0.23183 secondes, Acceleration = 2.855
2 threads: 0.370078 secondes, Acceleration = 1.789
1 thread: 0.656961 secondes, Acceleration ≈ 1

### Comparaison with BLAS

Temps CPU produit matrice-matrice naif : 0.0281789 secondes
Rapport = 6.399

# Tips 

```
	env 
	OMP_NUM_THREADS=4 ./produitMatriceMatrice.exe
```

```
    $ for i in $(seq 1 4); do elap=$(OMP_NUM_THREADS=$i ./TestProductOmp.exe|grep "Temps CPU"|cut -d " " -f 7); echo -e "$i\t$elap"; done > timers.out
```
