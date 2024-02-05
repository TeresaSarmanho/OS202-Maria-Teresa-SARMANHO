
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

## 1.1 Questions du nº2

## 1.3 Ensemble de mandelbrot
### Partition équitable par ligne

  n coeurs        | tp(n)    	         | temps de constitution de l'image
------------------|--------------------|----------------------------------
1                 |  4.1611488         | 0.053988
2                 |  2.1148117	      | 0.028347

speedup = sequential_time / parallel_time = 1.967621

*Comment interpréter les résultats obtenus ?*

### Stratégie maître–esclave

