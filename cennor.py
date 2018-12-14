import numpy as np
import time
import math
import transform
import random


def angle(v1, v2):
    inner_product = np.dot(v1, v2)
    size = np.linalg.norm(v1) * np.linalg.norm(v2)
    value = inner_product / size
    if value >= 1:
        return 0
    if value <= -1:
        return math.pi
    return np.arccos(value)


def cal_alpha(v):
    if v[1]==0 and v[2]==0:
        return 0 # No angle between x-y plane
    v_innerP = np.dot([v[1], v[2]],[1,0])
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

def rotating_mat(a, b, c):
    rx = [[1,0,0], [0, np.cos(a), (-1)*np.sin(a)], [0, np.sin(a), np.cos(a)]]
    ry = [[np.cos(b), 0, np.sin(b)], [0, 1, 0], [(-1)*np.sin(b), 0, np.cos(b)]]
    rz = [[np.cos(c), (-1)*np.sin(c), 0], [np.sin(c), np.cos(c), 0], [0, 0, 1]]
    rm_temp = np.matmul(rz, ry)
    return np.matmul(rm_temp, rx)
# 1.
start_1 = time.time()
f = open("./data/ds_model", 'r') #Model
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
    print(r)
    for i in range(0, shape[0]):
        if r != i:
            dx = np_array[i, 0] - np_array[r, 0]
            dy = np_array[i, 1] - np_array[r, 1]
            dz = np_array[i, 2] - np_array[r, 2]
            # print(np_array[r, 3:6], np_array[i, 3:6], angle(np_array[r, 3:6], np_array[i, 3:6]))
            d = int(math.sqrt((dx*dx) + (dy*dy) + (dz*dz))*10)
            a1 = int(angle((dx, dy, dz), np_array[r, 3:6])*1000)
            a2 = int(angle((-dx, -dy, -dz), np_array[i, 3:6])*1000)
            a3 = int(angle(np_array[r, 3:6], np_array[i, 3:6])*1000)

            #hash_key = str(d)+str(a1)+str(a2)+str(a3)
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
f = open("./data/ds_scene", 'r') #Scene
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
tg_shape = np.shape(tg_np_array)
voting_table = dict()
transform_table = dict()
r_set = set()
#r = 4  # temporary value. should do change r repeatedly
while True :
    r_set.add(random.randrange(0, tg_shape[0]))  # make r_set
    if len(r_set)==10 :
        break

print(r_set)
print("tg_shape number is : ", tg_shape[0])
for r in r_set :
    for i in range(0,tg_shape[0]):
        if r != i:
            dx = tg_np_array[i, 0] - tg_np_array[r, 0]
            dy = tg_np_array[i, 1] - tg_np_array[r, 1]
            dz = tg_np_array[i, 2] - tg_np_array[r, 2]
            d = int(math.sqrt((dx * dx) + (dy * dy) + (dz * dz))*10)
            a1 = int(angle((dx, dy, dz), tg_np_array[r, 3:6])*1000)
            a2 = int(angle((-dx, -dy, -dz), tg_np_array[i, 3:6])*1000)
            a3 = int(angle(tg_np_array[r, 3:6], tg_np_array[i, 3:6])*1000)
            # for key in Hash_table.keys():
            #     print(key)
            hash_key = d, a1, a2, a3
            item_list = Hash_table.get(hash_key)
            #print("this is hash_key :")
            #print(hash_key)
            #print("item num:")
            #print(len(item_list))
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

                    #print("----------------------")
                    #print(np.matmul(T_mtog, Mr[3:6]))
                    #print(np.matmul(T_stog, Sr[3:6]))

                    alpha = cal_alpha(Svector_transformed) - cal_alpha(Mvector_transformed)
                    if alpha < 0 :
                        alpha = 2*math.pi + alpha

                    alpha = int(alpha*1000)
                    #print("alph value is ", alpha)
                    #print("S alpha is ", cal_alpha(Svector_transformed), "M alpha is ", cal_alpha(Mvector_transformed))
                    #alpha = round(angle(vector1, vector2_trans)*180/PI, 0) # cannot make 0~2pi
                    count = voting_table.get(alpha)
                    trans_dict_temp = transform_table.get(alpha)
                    if count:
                        count += 1
                        voting_table[alpha] = count
                        num_check = False
                        for index in range(0, len(trans_dict_temp)):
                            if np.array_equal(trans_dict_temp[index], [T_mtog, T_stog]) :
                                num_check = True
                                break
                        if not num_check :
                            trans_dict_temp.append([T_mtog, T_stog])

                        transform_table[alpha] = trans_dict_temp

                    else:
                        voting_table[alpha] = 1
                        transform_table[alpha] = [[T_mtog, T_stog]]

            else:
                print("No item list. hash_key : ", hash_key)



print("Step 3: {:.3f}s".format(time.time() - start_3))

vote_num = -1
winner = 0

print("key numbers : ", len(voting_table.keys()))
for key in voting_table.keys():
    temp = voting_table.get(key)
    print(key, temp)  #, transform_table.get(key)
    if (vote_num < temp) :
        winner = key
        vote_num = temp

print("winner is :", winner/1000.0)
print("transform matrix as a tuple : ", transform_table.get(winner))

transform_mats = transform_table.get(winner)
sudo_rotating = rotating_mat(30*math.pi/180, 45*math.pi/180, 60*math.pi/180)
print("30, 45, 60 rotating matrix is : \n", sudo_rotating)
Rx_alpha = [[1,0,0],[0,np.cos(winner/1000.0), (-1)*np.sin(winner/1000.0)], [0,np.sin(winner/1000.0), np.cos(winner/1000.0)]]
for i in range(0, len(transform_mats)):
    Rotation_mat_temp = np.matmul(np.linalg.inv(transform_mats[i][0]), np.linalg.inv(Rx_alpha))
    Rotation_mat = np.matmul(Rotation_mat_temp, transform_mats[i][1])
    print("rotation matrix[", i, "] is : \n", Rotation_mat)
    print("this should be identity : \n", np.matmul(sudo_rotating, np.linalg.inv(Rotation_mat)))
