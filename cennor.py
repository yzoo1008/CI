import numpy as np
import time


def angle(v1, v2):
    value = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    return np.arccos(value)


# 1.
start_1 = time.time()
f = open("./data/cube", 'r')
array = []
while True:
    line = f.readline()
    if not line:
        break
    line = line.split('  ')
    line = line[1:]
    line[5] = line[5].split('\n')[0]
    tmp = []
    for i in range(0, 6):
        tmp.append(float(line[i]))
    array.append(tmp)
f.close()

np_array = np.array(array)
shape = np.shape(np_array)

print("Step 1: {:.3f}s".format(time.time() - start_1))

# 2. Make point pair feature hash table
start_2 = time.time()
Hash_table = dict()
for r in range(0, shape[0]):
    for i in range(0, shape[0]):
        if r != i:
            dx = np_array[i, 0] - np_array[r, 0]
            dy = np_array[i, 1] - np_array[r, 1]
            dz = np_array[i, 2] - np_array[r, 2]
            d = round(pow((dx*dx) + (dy*dy) + (dz*dz), 1/2), 1)
            a1 = round(180*angle((dx, dy, dz), np_array[r, 3:6])/np.pi, 1)
            a2 = round(180*angle((-dx, -dy, -dz), np_array[i, 3:6])/np.pi, 1)
            a3 = round(180*angle(np_array[r, 3:6], np_array[i, 3:6])/np.pi, 1)

            hash_key = d, a1, a2, a3
            tmp = Hash_table.get(hash_key)
            if tmp:
                tmp.append(np_array[r, 3:6])
                tmp.append(np_array[i, 3:6])
                Hash_table[hash_key] = tmp
            else:
                Hash_table[hash_key] = [np_array[r, 3:6], np_array[i, 3:6]]
print("Step 2: {:.3f}s".format(time.time() - start_2))


# 3. Find F(Mr, Mi) == F(Sr, Si)
start_3 = time.time()
f = open("./data/target_cube", 'r')
tg_array = []
while True:
    line = f.readline()
    if not line:
        break
    line = line.split('  ')
    line = line[1:]
    line[5] = line[5].split('\n')[0]
    tg_tmp = []
    for i in range(0, 6):
        tg_tmp.append(float(line[i]))
    tg_array.append(tg_tmp)
f.close()

tg_np_array = np.array(array)
shape = np.shape(tg_np_array)
r = 4
i = 6
dx = tg_np_array[i, 0] - tg_np_array[r, 0]
dy = tg_np_array[i, 1] - tg_np_array[r, 1]
dz = tg_np_array[i, 2] - tg_np_array[r, 2]
d = round(pow((dx*dx) + (dy*dy) + (dz*dz), 1/2), 1)
a1 = round(180*angle((dx, dy, dz), tg_np_array[r, 3:6])/np.pi, 1)
a2 = round(180*angle((-dx, -dy, -dz), tg_np_array[i, 3:6])/np.pi, 1)
a3 = round(180*angle(tg_np_array[r, 3:6], tg_np_array[i, 3:6])/np.pi, 1)

hash_key = d, a1, a2, a3
if Hash_table.get(hash_key):
    print(np.shape(Hash_table.get(hash_key)))

print("Step 3: {:.3f}s".format(time.time() - start_3))





