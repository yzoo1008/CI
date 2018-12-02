import numpy as np
import time
import math
import transform

PI = 3.141592653589793238462643383279502884197169


def angle(v1, v2):
    inner_product = round(np.dot(v1, v2), 4)
    size = round(np.linalg.norm(v1), 4) * round(np.linalg.norm(v2), 4)
    value = inner_product / size
    if value > 1:
        return 0
    if value < -1:
        return PI
    return np.arccos(value)


# 1.
start_1 = time.time()
f = open("./data/cube", 'r') #Model
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
# print(shape[0])
for r in range(0, shape[0]):
    for i in range(0, shape[0]):
        if r != i:
            dx = np_array[i, 0] - np_array[r, 0]
            dy = np_array[i, 1] - np_array[r, 1]
            dz = np_array[i, 2] - np_array[r, 2]
            # print(np_array[r, 3:6], np_array[i, 3:6], angle(np_array[r, 3:6], np_array[i, 3:6]))
            d = round(math.sqrt((dx*dx) + (dy*dy) + (dz*dz)), 1)
            # print(dx, dy, dz, d)
            a1 = int(180*angle((dx, dy, dz), np_array[r, 3:6])/PI * 10) / 10
            a2 = int(180*angle((-dx, -dy, -dz), np_array[i, 3:6])/PI * 10) / 10
            a3 = int(180*angle(np_array[r, 3:6], np_array[i, 3:6])/PI * 10) / 10

            hash_key = d, a1, a2, a3

            tmp = Hash_table.get(hash_key)
            if tmp:
                tmp.append([np_array[r], np_array[i]])
                Hash_table[hash_key] = tmp
            else:
                Hash_table[hash_key] = [[np_array[r], np_array[i]]]
print("Step 2: {:.3f}s".format(time.time() - start_2))


# 3. Find F(Mr, Mi) == F(Sr, Si)
start_3 = time.time()
f = open("./data/target_cube", 'r') #Scene
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

tg_np_array = np.array(tg_array)
shape = np.shape(tg_np_array)
r = 4

voting_table = dict()
transform_table = dict()

for i in range(0, np.shape(tg_np_array)[0]):
    if not i == r:
        dx = tg_np_array[i, 0] - tg_np_array[r, 0]
        dy = tg_np_array[i, 1] - tg_np_array[r, 1]
        dz = tg_np_array[i, 2] - tg_np_array[r, 2]
        d = round(math.sqrt((dx*dx) + (dy*dy) + (dz*dz)), 1)
        a1 = int(180*angle((dx, dy, dz), tg_np_array[r, 3:6])/PI * 10) / 10
        a2 = int(180*angle((-dx, -dy, -dz), tg_np_array[i, 3:6])/PI * 10) / 10
        a3 = int(180*angle(tg_np_array[r, 3:6], tg_np_array[i, 3:6])/PI * 10) / 10
        # a1 = round(180*angle((dx, dy, dz), tg_np_array[r, 3:6])/np.pi, 1)
        # a2 = round(180*angle((-dx, -dy, -dz), tg_np_array[i, 3:6])/np.pi, 1)
        # a3 = round(180*angle(tg_np_array[r, 3:6], tg_np_array[i, 3:6])/np.pi, 1)

        # hash_key = d, a1, a2, a3
        # if Hash_table.get(hash_key):
        #     print(np.shape(Hash_table.get(hash_key)))

        # for key in Hash_table.keys():
        #     print(key)

        hash_key = d, a1, a2, a3
        item_list = Hash_table.get(hash_key)
        # print(hash_key)
        for item in item_list:
            #print(item)
            Mr = item[0]
            Mi = item[1]
            Sr = tg_np_array[r]
            Si = tg_np_array[i]
            trans_matrix = transform.transformation(Sr, Mr)

            vector1 = Mi[0:3]-Mr[0:3]
            vector2 = Si[0:3]-Sr[0:3]
            vector2_trans = np.dot(trans_matrix, vector2)
            alpha = round(angle(vector1, vector2_trans)*180/PI, 0)

            count = voting_table.get(alpha)
            trans_dict_temp = transform_table.get(alpha)
            if count:
                count += 1
                voting_table[alpha] = count
                trans_dict_temp.append(trans_matrix)
                transform_table[alpha] = trans_dict_temp
            else:
                voting_table[alpha] = 1
                transform_table[alpha] = trans_matrix

print("Step 3: {:.3f}s".format(time.time() - start_3))


for key in voting_table.keys():
    print(key, voting_table.get(key), transform_table.get(key))




