import numpy as np
from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot
import time

def same(a, b):
    return ((a[0] == b[0]).all() and (a[1] == b[1]).all()) or ((a[0] == b[1]).all() and (a[1] == b[0]).all())


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
print("Finish! // Shape: {0}".format(np.shape(teeth_mesh_v)))

print("Convert mesh file to Edges...")
edge = np.zeros((N_VERTICLE, 3, 2, 3))
for i in range(0, N_VERTICLE):
    edge[i] = [[teeth_mesh.v0[i], teeth_mesh.v1[i]], [teeth_mesh.v1[i], teeth_mesh.v2[i]], [teeth_mesh.v2[i], teeth_mesh.v0[i]]]
print("Finish! // Shape: {0}".format(np.shape(edge)))

print("Find Cycle 1...")
set_num = np.zeros(N_VERTICLE)
cycle = [edge[0][0], edge[0][1], edge[0][2]]

set_num[0] = 1
update = 0
before_size = 0
size = 1
while before_size != size:
    before_size = size
    for i in range(0, N_VERTICLE):
        if set_num[i] == 0:
            find = [False, False, False]
            cnt = 0
            j = 0
            while j < len(cycle):
                if same(cycle[j], edge[i][0]):
                    find[0] = True
                    del cycle[j]
                    j -= 1
                    cnt += 1
                if same(cycle[j], edge[i][1]):
                    find[1] = True
                    del cycle[j]
                    j -= 1
                    cnt += 1
                if same(cycle[j], edge[i][2]):
                    find[2] = True
                    del cycle[j]
                    j -= 1
                    cnt += 1
                j += 1
            if cnt != 0:
                set_num[i] = 1
                size += 1
                if not find[0]:
                    cycle.append(edge[i][0])
                if not find[1]:
                    cycle.append(edge[i][1])
                if not find[2]:
                    cycle.append(edge[i][2])
        # if update != len(cycle):
        #     update = len(cycle)
        #     print("Num of Edges in Cycle: {0}".format(update))
    end = time.time()
    print("Size of Cycle1: {0} // Num of Edges in Cycle1: {1} // Time: {2:.2f}sec".format(size, len(cycle), end-start))
print("Finish!")

# data = numpy.zeros(N_VERTICLE, dtype=mesh.Mesh.dtype)
# teeth_mesh = mesh.Mesh(data, remove_empty_areas=False)
#
# teeth_mesh.normals
# teeth_mesh.v0, teeth_mesh.v1, teeth_mesh.v2


# figure = pyplot.figure()
# axes = mplot3d.Axes3D(figure)
#
# axes.add_collection3d(mplot3d.art3d.Poly3DCollection(teeth_mesh.vectors))
#
# scale = teeth_mesh.points.flatten(-1)
# axes.auto_scale_xyz(scale, scale, scale)
#
# pyplot.show()
