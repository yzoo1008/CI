import numpy as np
import math


def transformation(mat1, mat2): #need to add translation now only rotation
	# print(mat1[3:6], mat2[3:6], np.dot(mat1[3:6], mat2[3:6]))
	cos = np.dot(mat1[3:6], mat2[3:6])
	sin = math.sqrt(1 - cos*cos)

	a1, a2, a3 = mat1[3], mat1[4], mat1[5]
	b1, b2, b3 = mat2[3], mat2[4], mat2[5]
	out_prod = np.array([a2*b3 - a3*b2, a3*b1 - a1*b3, a1*b2 - a2*b1])
	#translate = mat2[3:6] - mat1[3:6]

	if round(np.linalg.norm(out_prod),8) == 0. :
		v = [0. ,0. ,0.]
	else:
		v = out_prod / np.linalg.norm(out_prod)

	x = v[0]
	y = v[1]
	z = v[2]

	trans = [[round(cos + (x**2 * (1-cos)), 4), round(x*y*(1-cos) - z*sin, 4), round(x*z*(1-cos) + y*sin, 4)],
	         [round(x*y*(1-cos) + z*sin, 4), round(cos + y**2*(1-cos), 4), round(y*z*(1-cos) - x*sin, 4)],
	         [round(x*z*(1-cos) - y*sin, 4), round(y*z*(1-cos) + x*sin, 4), round(cos + z**2*(1-cos), 4)]]
	return trans