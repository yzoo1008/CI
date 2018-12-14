import numpy as np
import time
import math
import transform
import module
import random
import datetime

Model_path = "./demo/demo_model"
Scene_path = "./demo/scene_deci"

def angle(v1, v2):
    inner_product = np.dot(v1, v2)
    size = np.linalg.norm(v1) * np.linalg.norm(v2)
    if size == 0:
        print(v1, v2)
    value = inner_product / size
    if value >= 1:
        return 0
    if value <= -1:
        return math.pi
    return np.arccos(value)

def cal_alpha(v):
    if v[1]==0 and v[2]==0:
        return 0 # No angle between x-y plane
    v_innerP = np.dot([v[1], v[2]], [1, 0])
    v_size = np.linalg.norm([v[1], v[2]])
    v_value = v_innerP / v_size
    if v_value >= 1:
        theta = 0
    elif v_value <= -1:
        theta = math.pi
    else:
        theta = np.arccos(v_value)
        if v[2] < 0:
            theta = 2*math.pi - theta
    return theta

def read(filename):
    f = open(filename, 'r')  # Model
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
    return np.array(array)

print("Start Time: {}".format(datetime.datetime.now()))

# 1.
start_1 = time.time()

np_array = read(Model_path)
shape = np.shape(np_array)

print("Step 1: {:.3f}s".format(time.time() - start_1))

# 2. Make point pair feature hash table
start_2 = time.time()
Hash_table = dict()
for r in range(0, shape[0]):
    print(r)
    for i in range(0, shape[0]):
        if r != i:
            dx = np_array[i, 0] - np_array[r, 0]
            dy = np_array[i, 1] - np_array[r, 1]
            dz = np_array[i, 2] - np_array[r, 2]

            d = int(math.sqrt((dx*dx) + (dy*dy) + (dz*dz))*10)
            a1 = int(angle((dx, dy, dz), np_array[r, 3:6])*10)
            a2 = int(angle(np_array[i, 3:6], (-dx, -dy, -dz))*10)
            a3 = int(angle(np_array[r, 3:6], np_array[i, 3:6])*10)

            hash_key = d, a1, a2, a3
            tmp = Hash_table.get(hash_key)
            if tmp:
                tmp.append([np_array[r], np_array[i]])
                Hash_table[hash_key] = tmp
            else:
                Hash_table[hash_key] = [[np_array[r], np_array[i]]]
print("Step 2: {:.3f}s".format(time.time() - start_2))

# 3. Find F(Mr, Mi) == F(Sr, Si) & Voting
start_3 = time.time()

tg_np_array = read(Scene_path)
tg_shape = np.shape(tg_np_array)

voting_table = dict()
transform_table = dict()
r_set = set()

while True :
    r_set.add(random.randrange(0, tg_shape[0]))  # make r_set
    if len(r_set) == 5:
        break
print(r_set)

num_miss = 0
for r in r_set :
    for i in range(0, tg_shape[0]):
        if r != i:
            dx = tg_np_array[i, 0] - tg_np_array[r, 0]
            dy = tg_np_array[i, 1] - tg_np_array[r, 1]
            dz = tg_np_array[i, 2] - tg_np_array[r, 2]

            d = int(math.sqrt((dx * dx) + (dy * dy) + (dz * dz)) * 10)
            a1 = int(angle((dx, dy, dz), tg_np_array[r, 3:6]) * 10)
            a2 = int(angle(tg_np_array[i, 3:6], (-dx, -dy, -dz)) * 10)
            a3 = int(angle(tg_np_array[r, 3:6], tg_np_array[i, 3:6]) * 10)

            hash_key = d, a1, a2, a3
            item_list = Hash_table.get(hash_key)
            if item_list:
                for item in item_list:
                    Mr = item[0]
                    Mi = item[1]
                    Sr = tg_np_array[r]
                    Si = tg_np_array[i]
                    T_mtog = transform.transformation(Mr, [0,0,0,1,0,0])
                    T_stog = transform.transformation(Sr, [0,0,0,1,0,0])
                    Mvector = Mi[0:3]-Mr[0:3]
                    Svector = Si[0:3]-Sr[0:3]
                    Mvector_transformed = np.matmul(T_mtog, Mvector)
                    Svector_transformed = np.matmul(T_stog, Svector)

                    alpha = cal_alpha(Svector_transformed) - cal_alpha(Mvector_transformed)
                    if alpha < 0 :
                        alpha = 2*math.pi + alpha
                    alpha = int(alpha*10000.0)

                    count = voting_table.get(alpha)
                    trans_dict_temp = transform_table.get(alpha)
                    p_tuple = [Mr[0:3], Sr[0:3]]
                    if count:
                        count += 1
                        voting_table[alpha] = count
                        num_check = False
                        for index in range(0, len(trans_dict_temp)):
                            # if np.sum(np.abs(np.array(trans_dict_temp[index]) - np.array([T_mtog, T_stog]))) < (1.0/1000.0):
                            if np.array_equal(trans_dict_temp[index][0:2], [T_mtog, T_stog]):
                                trans_dict_temp[index][3] += 1
                                num_check = True
                                break
                        if not num_check :
                            trans_dict_temp.append([T_mtog, T_stog, p_tuple, 1])
                        transform_table[alpha] = trans_dict_temp
                    else:
                        voting_table[alpha] = 1
                        transform_table[alpha] = [[T_mtog, T_stog, p_tuple, 1]]
            else:
                num_miss += 1

print("Miss: {}".format(num_miss))
print("Step 3: {:.3f}s".format(time.time() - start_3))

# 4. Find Winner
start_4 = time.time()
vote_num = -1
winner = 0
print("Numbers of keys : {}".format(len(voting_table.keys())))
for key in voting_table.keys():
    temp = voting_table.get(key)
    if vote_num < temp:
        winner = key
        vote_num = temp
print("Winner is : {} with {}".format(winner/10000.0, vote_num))
Transform_matrix_list = transform_table.get(winner)
#print("Transform matrix as a tuple : {}".format(Transform_matrix_list))
print("Shape of Transform matrix: {}".format(np.shape(Transform_matrix_list)))

print("Step 4: {:.3f}s".format(time.time() - start_4))

# 5. Choose Solution
start_5 = time.time()
real_count = -1
mat_index = -1
for number in range(np.shape(Transform_matrix_list)[0]):
    if real_count < transform_table.get(winner)[number][3] :
        real_count = transform_table.get(winner)[number][3]
        mat_index = number
#print("#### Number of different matrix : ", number+1)
T = transform.merge(transform_table.get(winner)[mat_index][0], float(winner)/10000.0, transform_table.get(winner)[mat_index][1])
P = transform_table.get(winner)[mat_index][2]
Pos = P[0] - np.matmul(T, P[1])
print(P[0] - np.matmul(T, P[1]))
print("Actual counted is : ", real_count)
Real_T = transform.solution()
print("Our T Solution: ")
print(T)
print("Real T Value: ")
print(Real_T)
print("this should identity matrix")
print(np.matmul(T, np.linalg.inv(Real_T)))

print("Step 5: {:.3f}s".format(time.time() - start_5))


# 6. Read & Transform Scene
start_6 = time.time()
NV, Node = module.read()

for num in range(np.shape(Node)[0]):
    NV[num] = np.matmul(T, NV[num]) + Pos
    for xyz in range(np.shape(Node)[1]):
        Node[num][xyz] = np.matmul(T, Node[num][xyz]) + Pos

module.transform(NV, Node)

print("Step 6: {:.3f}s".format(time.time() - start_6))
