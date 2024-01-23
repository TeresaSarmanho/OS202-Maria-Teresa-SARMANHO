
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
Do ponto de vista das operaçoes aritmeticas, o tempo deveria ser o mesmo. Porém, os acessos de memória mudam o tempo de retorno, e sua complexidade deve ser considerada para o cálculo da eficiência do código. Isso passa a importar com a multiplicação dos cores das máquinas e da utilização dos diferentes níveis de memória cache.

Buscar fazer as operaçoes com continuidade de memoria para não ter que buscar várias informações em lugares diferentes.
É mais rápido percorrer em colunas, ja que os dados estao salvos em colunas.
Neste caso, 


### OMP sur la meilleure boucle 

`make TestProduct.exe && OMP_NUM_THREADS=8 ./TestProduct.exe 1024`

  OMP_NUM         | MFlops  | MFlops(n=2048) | MFlops(n=512)  | MFlops(n=4096)
------------------|---------|----------------|----------------|---------------
1                 |  |
2                 |  |
3                 |  |
4                 |  |
5                 |  |
6                 |  |
7                 |  |
8                 |  |




### Produit par blocs

`make TestProduct.exe && ./TestProduct.exe 1024`

  szBlock         | MFlops  | MFlops(n=2048) | MFlops(n=512)  | MFlops(n=4096)
------------------|---------|----------------|----------------|---------------
origine (=max)    |  |
32                |  |
64                |  |
128               |  |
256               |  |
512               |  | 
1024              |  |




### Bloc + OMP



  szBlock      | OMP_NUM | MFlops  | MFlops(n=2048) | MFlops(n=512)  | MFlops(n=4096)|
---------------|---------|---------|-------------------------------------------------|
A.nbCols       |  1      |         |                |                |               |
512            |  8      |         |                |                |               |
---------------|---------|---------|-------------------------------------------------|
Speed-up       |         |         |                |                |               |
---------------|---------|---------|-------------------------------------------------|



### Comparaison with BLAS


# Tips 

```
	env 
	OMP_NUM_THREADS=4 ./produitMatriceMatrice.exe
```

```
    $ for i in $(seq 1 4); do elap=$(OMP_NUM_THREADS=$i ./TestProductOmp.exe|grep "Temps CPU"|cut -d " " -f 7); echo -e "$i\t$elap"; done > timers.out
```
