import pymesh
from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot


my_mesh = mesh.Mesh.from_file('C:\Users\KYJ\Desktop/test1.stl')

figure = pyplot.figure()
axes = mplot3d.Axes3D(figure)

# Load the STL files and add the vectors to the plot
axes.add_collection3d(mplot3d.art3d.Poly3DCollection(my_mesh.vectors))

# Auto scale to the mesh size
axes.set_xlim3d(-60, 60)
axes.set_ylim3d(-80, 0)
axes.set_zlim3d(45, 100)

axes.view_init(azim=120)
pyplot.show()

print(my_mesh.data)



