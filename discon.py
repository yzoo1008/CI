import numpy as np
from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot
import time
import Queue


def same(a, b):
	return  round(a[0], 6) == round(b[0], 6) and round(a[1], 6) == round(b[1], 6) and round(a[2], 6) == round(b[2], 6)


data_dir = './data/'
teeth_file = 'Teeth_Lower.stl'
gingiva_file = 'Gingiva_Lower.stl'

start = time.time()
print("Read mesh file...")
data_path = data_dir + teeth_file
teeth_mesh = mesh.Mesh.from_file(data_dir + gingiva_file)
teeth_mesh_nm = teeth_mesh.normals
teeth_mesh_v = teeth_mesh.v0, teeth_mesh.v1, teeth_mesh.v2
N_VERTICLE = np.shape(teeth_mesh_v)[1]

# q = Queue.Queue()
# q.put(teeth_mesh_v[0][0])
list = [(teeth_mesh_v[0]).tolist(), (teeth_mesh_v[1]).tolist(), (teeth_mesh_v[2]).tolist()]

set = {tuple(teeth_mesh_v[0][0])}
visited = np.zeros(N_VERTICLE)
cnt = 0
t = 0
while len(set):
	comp = set.pop()
	for i in range(0, 3):
		indexes = [k for k, x in enumerate(list[i]) if same(x, comp)]
		for j in indexes:
			if visited[j] == 0:
				if i == 0:
					set.add(tuple(teeth_mesh_v[1][j]))
					set.add(tuple(teeth_mesh_v[2][j]))
				elif i == 1:
					set.add(tuple(teeth_mesh_v[0][j]))
					set.add(tuple(teeth_mesh_v[2][j]))
				else:
					set.add(tuple(teeth_mesh_v[0][j]))
					set.add(tuple(teeth_mesh_v[1][j]))
				visited[j] = 1
				j -= t
				list[0].remove(list[0][j])
				list[1].remove(list[1][j])
				list[2].remove(list[2][j])
				t += 1



	# for i in range(0, N_VERTICLE):
	# 	if visited[i] == 0:
	# 		for j in range(0, 3):
	# 			if (comp == teeth_mesh_v[j][i]).all():
	# 				if j == 0:
	# 					set.add(tuple(teeth_mesh_v[1][i]))
	# 					set.add(tuple(teeth_mesh_v[2][i]))
	# 				elif j == 1:
	# 					set.add(tuple(teeth_mesh_v[0][i]))
	# 					set.add(tuple(teeth_mesh_v[2][i]))
	# 				else:
	# 					set.add(tuple(teeth_mesh_v[0][i]))
	# 					set.add(tuple(teeth_mesh_v[1][i]))
	# 				visited[i] = 1
	# 				t += 1
	# 				break
	cnt += 1
	print(cnt, len(set), t)
print("Finish! // Shape: {0}".format(np.shape(teeth_mesh_v)))
print("Time: {0:.2f}sec".format(time.time()-start))


# print("Convert mesh file to Edges...")
# edge = np.zeros((N_VERTICLE, 3, 2, 3))
# for i in range(0, N_VERTICLE):
#     edge[i] = [[teeth_mesh.v0[i], teeth_mesh.v1[i]], [teeth_mesh.v1[i], teeth_mesh.v2[i]], [teeth_mesh.v2[i], teeth_mesh.v0[i]]]
# print("Finish! // Shape: {0}".format(np.shape(edge)))
#
# print("Find Cycle 1...")
# set_num = np.zeros(N_VERTICLE)
# cycle = [edge[0][0], edge[0][1], edge[0][2]]
#
# set_num[0] = 1
# update = 0
# before_size = 0
# size = 1
# while before_size != size:
#     before_size = size
#     for i in range(0, N_VERTICLE):
#         if set_num[i] == 0:
#             find = [False, False, False]
#             cnt = 0
#             j = 0
#             while j < len(cycle):
#                 if same(cycle[j], edge[i][0]):
#                     find[0] = True
#                     del cycle[j]
#                     j -= 1
#                     cnt += 1
#                 if same(cycle[j], edge[i][1]):
#                     find[1] = True
#                     del cycle[j]
#                     j -= 1
#                     cnt += 1
#                 if same(cycle[j], edge[i][2]):
#                     find[2] = True
#                     del cycle[j]
#                     j -= 1
#                     cnt += 1
#                 j += 1
#             if cnt != 0:
#                 set_num[i] = 1
#                 size += 1
#                 if not find[0]:
#                     cycle.append(edge[i][0])
#                 if not find[1]:
#                     cycle.append(edge[i][1])
#                 if not find[2]:
#                     cycle.append(edge[i][2])
#         # if update != len(cycle):
#         #     update = len(cycle)
#         #     print("Num of Edges in Cycle: {0}".format(update))
#     end = time.time()
#     print("Size of Cycle1: {0} // Num of Edges in Cycle1: {1} // Time: {2:.2f}sec".format(size, len(cycle), end-start))
# print("Finish!")
