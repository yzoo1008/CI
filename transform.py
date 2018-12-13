import numpy as np
import math


def transformation(mat1, mat2): #need to add translation now only rotation
	# print(mat1[3:6], mat2[3:6], np.dot(mat1[3:6], mat2[3:6]))
	cos = np.dot(mat1[3:6], mat2[3:6])
	sin = math.sqrt(1 - cos*cos)

	a1, a2, a3 = mat1[3], mat1[4], mat1[5]
	b1, b2, b3 = mat2[3], mat2[4], mat2[5]
	out_prod = np.array([a2*b3 - a3*b2, a3*b1 - a1*b3, a1*b2 - a2*b1])

	if round(np.linalg.norm(out_prod), 6) == 0. :
		v = [0. ,0. ,0.]
	else:
		v = out_prod / np.linalg.norm(out_prod)

	x = v[0]
	y = v[1]
	z = v[2]

	T = [[round(cos + (x**2 * (1-cos)), 4), round(x*y*(1-cos) - z*sin, 4), round(x*z*(1-cos) + y*sin, 4)],
	         [round(x*y*(1-cos) + z*sin, 4), round(cos + y**2*(1-cos), 4), round(y*z*(1-cos) - x*sin, 4)],
	         [round(x*z*(1-cos) - y*sin, 4), round(y*z*(1-cos) + x*sin, 4), round(cos + z**2*(1-cos), 4)]]
	return T

def merge(mat1, alpha, mat2):
	T_mtog = np.matrix(mat1)
	T_stog = np.matrix(mat2)
	T_mtog_I = T_mtog.I
	T_alpha = [[1, 0, 0],
	           [0, np.cos(-alpha), -np.sin(-alpha)],
	           [0, np.sin(-alpha), np.cos(-alpha)]]
	# T_alpha_I = np.matrix(T_alpha).I

	mat1 = np.matmul(T_mtog_I, T_alpha)
	T = np.matmul(mat1, T_stog)
	return T

def solution(a, b, c):
	x = math.pi*a/180
	y = math.pi*b/180
	z = math.pi*c/180
	R_x = [[1, 0, 0],
	       [0, np.cos(x), -np.sin(x)],
	       [0, np.sin(x), np.cos(x)]]
	R_y = [[np.cos(y), 0, np.sin(y)],
	       [0, 1, 0],
	       [-np.sin(y), 0, np.cos(y)]]
	R_z = [[np.cos(z), -np.sin(z), 0],
	       [np.sin(z), np.cos(z), 0],
	       [0, 0, 1]]
	mat1 = np.matmul(R_z, R_y)
	mat2 = np.matmul(mat1, R_x)
	mat3 = np.matrix(mat2)
	T = mat3.I
	return mat3