from annoy import AnnoyIndex
import random
import annoy


f = 2
t = AnnoyIndex(f, "angular")
for i in range(20):
    v = [random.gauss(0,1) for z in range(f)]
    t.add_item(i, v)

t.build(2) # 10 trees
t.save('test.ann')


u = AnnoyIndex(f, 'angular')
u.load('test.ann') # super fast, will just mmap the file
print(u.get_nns_by_item(0, 100))