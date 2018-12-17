import numpy as np
import math


def R_x(x):
	x = math.pi*x/180
	return [[1, 0, 0],
	       [0, np.cos(x), -np.sin(x)],
	       [0, np.sin(x), np.cos(x)]]
def R_y(y):
	y = math.pi * y / 180
	return [[np.cos(y), 0, np.sin(y)],
	       [0, 1, 0],
	       [-np.sin(y), 0, np.cos(y)]]
def R_z(z):
	z = math.pi * z / 180
	return [[np.cos(z), -np.sin(z), 0],
	       [np.sin(z), np.cos(z), 0],
	       [0, 0, 1]]

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

	trans = [[round(cos + (x**2 * (1-cos)), 4), round(x*y*(1-cos) - z*sin, 4), round(x*z*(1-cos) + y*sin, 4)],
	         [round(x*y*(1-cos) + z*sin, 4), round(cos + y**2*(1-cos), 4), round(y*z*(1-cos) - x*sin, 4)],
	         [round(x*z*(1-cos) - y*sin, 4), round(y*z*(1-cos) + x*sin, 4), round(cos + z**2*(1-cos), 4)]]
	return trans

def merge(mat1, alpha, mat2):
	#T_mtog = np.matrix(mat1)
	#T_mtog_I = T_mtog.I
	T_alpha = [[1, 0, 0],
	           [0, np.cos(-alpha), -np.sin(-alpha)],
	           [0, np.sin(-alpha), np.cos(-alpha)]]

	matrix = np.matmul(np.linalg.inv(mat1), T_alpha)
	T = np.matmul(matrix, mat2)
	return T

def solution():
	R_1 = R_x(90)
	R_2 = R_z(146)
	R_3 = R_x(-19)
	R_4 = R_y(-1)
	t1 = np.matmul(R_4, R_3)
	t2 = np.matmul(t1, R_2)
	T = np.matmul(t2, R_1)
	return T

	# R_1 = R_x(20)
	# R_2 = R_y(40)
	# R_3 = R_z(60)
	# t1 = np.matmul(R_3, R_2)
	# T = np.matmul(t1, R_1)
	# return T
	#
