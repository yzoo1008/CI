import numpy as np

def read():
	size = 349
	cnt = 0
	v_cnt = 0
	nv = np.zeros((size, 3), dtype='f8')
	node = np.zeros((size, 3, 3), dtype='f8')
	f = open("./scene_deci.stl", 'r')
	while True:
		line = f.readline()
		if not line:
			break

		if 'facet normal' in line:
			xyz = line.split()
			nv[cnt] = [float(xyz[2]), float(xyz[3]), float(xyz[4])]
			cnt += 1
			v_cnt = 0

		if 'vertex' in line:
			xyz = line.split()
			node[cnt-1][v_cnt] = [float(xyz[1]), float(xyz[2]), float(xyz[3])]
			v_cnt += 1
	f.close()

	return nv, node

def transform(nv, node):
	f = open("./scene_deci_trans.stl", 'w')
	data = "solid STL "
	f.write(data)
	for num in range(np.shape(nv)[0]):
		data = " facet normal"
		for xyz in range(3):
			data += " " + str(nv[num][xyz]) + " "
		data += " outer loop"
		for i in range(np.shape(nv)[1]):
			data += " vertex"
			for xyz in range(3):
				data += " " + str(node[num][i][xyz]) + " "
		data += " endloop"
		data += " endfacet"
		f.write(data)
	data = "endsolid vcg"
	f.write(data)
	f.close()
