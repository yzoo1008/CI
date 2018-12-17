import numpy as np

def read(path):
	size = 1000
	cnt = 0
	v_cnt = 0
	nv = np.zeros((size, 3), dtype='f8')
	node = np.zeros((size, 3, 3), dtype='f8')
	f = open(path, 'r')
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

	return nv[0:cnt], node[0:cnt]

def transform(nv, node, save_path):
	f = open(save_path, 'w')
	data = "solid\n"
	f.write(data)
	for num in range(np.shape(nv)[0]):
		data = "facet normal\n"
		for xyz in range(3):
			data += "" + str(nv[num][xyz]) + "\n"
		data += "outer loop\n"
		for i in range(np.shape(nv)[1]):
			data += "vertex\n"
			for xyz in range(3):
				data += "" + str(node[num][i][xyz]) + "\n"
		data += "endloop\n"
		data += "endfacet\n"
		f.write(data)
	data = "endsolid vcg\n"
	f.write(data)
	f.close()
