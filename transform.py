import numpy as np
import math


def transformation(mat1, mat2):
	# print(mat1[3:6], mat2[3:6], np.dot(mat1[3:6], mat2[3:6]))
	cos = np.dot(mat1[3:6], mat2[3:6])
	sin = math.sqrt(1 - cos*cos)

	a1 = mat1[3]
	a2 = mat1[4]
	a3 = mat1[5]
	b1 = mat2[3]
	b2 = mat2[4]
	b3 = mat2[5]
	out_prod = np.array([a2*b3 - a3*b2, a3*b1 - a1-b3, a1*b2 - a2*b1])

	v = out_prod / np.linalg.norm(out_prod)
	x = v[0]
	y = v[1]
	z = v[2]

	trans = [[cos + (x**2 * (1-cos)), x*y*(1-cos) - z*sin, x*z*(1-cos) + y*sin],
	         [x*y*(1-cos) + z*sin, cos + y**2*(1-cos), y*z*(1-cos) - x*sin],
	         [x*z*(1-cos) - y*sin, y*z*(1-cos) + x*sin, cos + z**2*(1-cos)]]

	return trans