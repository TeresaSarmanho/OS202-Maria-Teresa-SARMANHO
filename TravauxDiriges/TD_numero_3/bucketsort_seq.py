def bucket_sort(l):
    bucket = []
    for i in range(len(l)):
        bucket.append(i) #scatters element
    for j in l:
        index = int(10*j)
        bucket[index].append(j)  #scatters into the bucket of their own range
    for k in range(len(l)): 
        bucket[k] = sorted(bucket[k]) #sorts the buckets
    
    a = 0
    for b in range(len(l)):
        for c in range(len(bucket[b])):
            #merges the bukets into the list again
           l[a]=bucket[b][c]
           a += 1
    return l

l1 = [0.42, 0.32, 0.23, 0.52, 0.25, 0.47, 0.51]

res = bucket_sort(l1)
print(res)
