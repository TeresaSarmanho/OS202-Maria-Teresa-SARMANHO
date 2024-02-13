
# TD2

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


## 1.1 Questions du cours


### 1.1.1. Un premier scénario où il n’y a pas d’interblocage
Si on exécute le rank dans l'ordre 0 1 2, le rank 0 envoie un message vers 2 et 1, puis est mis en attente, ce qui assure la réception du message.

### 1.1.2. Un deuxième scénario où il y a interblocage.
Si on exécute le rank dans l'ordre 0 2 1, le rank 1 envoie un message vers 2 qui est reçu au même instant, ce qui n'assure pas la réception du message.

Parmi les six cas possibles, on peut constater que 50% correspondent à des interblocages.

## 1.1 Questions du nº2

D'après la loi d'Amdahl, on sait que l'accélération maximale pour un processus ayant une partie non parallélisée correspondant à 10% est :

$$ S = \frac{1}{f} = \frac{1}{0,10} = 10 $$

L'utilisation de 3 nœuds de calcul semble raisonnable pour éviter de gaspiller trop de ressources CPU, car cela permet d'accélérer le code de plus de trois fois et de diviser en parties égales la partie parallèle du code.

Selon la loi de Gustafson, l'accélération maximale peut être déterminée à partir de l'accélération déjà obtenue et du nombre de nœuds. Ainsi :

$$ S(n) = \frac{t_s+nt_p}{t_s+t_p} $$

En utilisant l'accélération déjà obtenue de 4 fois et la loi d'Amdahl, on obtient :

$$ 4 = t_s + 6t_p $$

$$ 5t_p = 3 $$

En doublant la quantité de données, on trouve l'accélération maximale :

$$ S(6) = \frac{0,4+6x1,2}{0,4+1,2}= 4,75$$

## 1.3 Ensemble de mandelbrot
### Partition équitable par ligne
tp(n) correspond au plus grand temps mésuré.
  n coeurs        | tp(n)    	         | temps de constitution de l'image
------------------|--------------------|----------------------------------
1                 |  4.1611488         | 0.053988
2                 |  2.1148117	      | 0.028347
4                 |  2.0546007	      | 0.064010
5                 |  2.6449451	      | 0.045917
6                 |  2.5818762	      | 0.050048
7                 |  2.2956218	      | 0.099091


$$ speedup = 1.967621 $$


### Stratégie maître–esclave
  n coeurs        | tp(n)    	         
------------------|--------------------
0                 |  -                 
2                 |  0.0740649         



