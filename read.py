import numpy as np

size = 267845
cnt = 0
v_cnt = 0
nv = np.zeros((size, 3), dtype='f8')
node = np.zeros((size, 3, 3), dtype='f8')
f = open("./ascii.stl", 'r')
while True:
    line = f.readline()

    if not line:
        break

    if 'facet normal' in line:
        xyz = line.split()
        nv[cnt] = [xyz[2], xyz[3], xyz[4]]
        cnt += 1
        v_cnt = 0

    if 'vertex' in line:
        xyz = line.split()
        node[cnt-1][v_cnt] = [xyz[1], xyz[2], xyz[3]]
        v_cnt += 1
f.close()

cyc1 = []
cyc1.append(node[0])
node = np.delete(node, 0, 0)
match_all = 1

while match_all != 0:
    match_all = 0
    queue = []
    for i in range(len(node)):
        for j in range(len(cyc1)):
            match = 0
            for n in range(3):
                for m in range(3):
                    if np.all(node[i][n] == cyc1[j][m]):
                        match += 1
            if match == 2:
                queue.append(i)
                match_all += 1
    print(match_all)
    queue.sort(reverse=True)
    for i in queue:
        cyc1.append(node[i])
        node = np.delete(node, i, 0)

