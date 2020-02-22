import random
import time
# import numpy as np
# import matplotlib.pyplot as plt

def show(x, y):
    x_even = np.arange(x[0][0] - 0.1, x[0][len(x[0]) - 1] + 0.1 , 100)
    x_odd = np.arange(x[1][0] - 0.1, x[1][len(x[1]) - 1] + 0.1 , 100)

    y_b_odd = np.array(y[0][1])
    y_b_even = np.array(y[0][0])
    y_v_odd = np.array(y[1][1])
    y_v_even = np.array(y[1][0])
    y_vo_odd = np.array(y[2][1])
    y_vo_even = np.array(y[2][0])

    plt.figure(1)
    plt.ylabel("Время вычисления")
    plt.xlabel("Размер матрицы")
    plt.plot(x_even, y_b_even, 'k', label = 'based for even')
    plt.plot(x_even, y_v_even, 'g', label = 'vinograd for even')
    plt.plot(x_even, y_vo_even, 'b', label = 'optimized vinograd for even')

    plt.plot(x_odd, y_b_odd, 'k--', label = 'based for odd')
    plt.plot(x_odd, y_v_odd, 'g--', label = 'vinograd for odd')
    plt.plot(x_odd, y_vo_odd, 'b--', label = 'optimized vinograd for odd')

    plt.legend(loc = 'upper left')

    for i in range(len(x[0])):
        plt.plot(x[0][i], y_b_even[i], 'ko', markersize = 3)
        plt.plot(x[0][i], y_v_even[i], 'go', markersize = 3)
        plt.plot(x[0][i], y_vo_even[i], 'bo', markersize = 3)

        plt.plot(x[1][i], y_b_odd[i], 'kv', markersize = 3)
        plt.plot(x[1][i], y_v_odd[i], 'gv', markersize = 3)
        plt.plot(x[1][i], y_vo_odd[i], 'bv', markersize = 3)
    plt.show()

def test_time(points_b, points_v, points_vo):
    odd_b = []
    even_b = []
    odd_v = []
    even_v = []
    odd_vo = []
    even_vo = []


    for i in [x*100 for x in range (1, 11)]:
        mat1 = mat2 = generate_mat([i, i])

        start = time.process_time()
        based(mat1, mat2)
        end = time.process_time()
        even_b.append(end - start)

        start = time.process_time()
        vinograd(mat1, mat2)
        end = time.process_time()
        even_v.append(end - start)

        start = time.process_time()
        vinograd_optimized(mat1, mat2)
        end = time.process_time()
        even_vo.append(end - start)

    for i in [x*100+1 for x in range (1, 11)]:
        mat1 = mat2 = generate_mat([i, i])

        start = time.process_time()
        based(mat1, mat2)
        end = time.process_time()
        odd_b.append(end - start)

        start = time.process_time()
        vinograd(mat1, mat2)
        end = time.process_time()
        odd_v.append(end - start)

        start = time.process_time()
        vinograd_optimized(mat1, mat2)
        end = time.process_time()
        odd_vo.append(end - start)

    points_b.append(even_b)
    points_b.append(odd_b)
    points_v.append(even_v)
    points_v.append(odd_v)
    points_vo.append(even_vo)
    points_vo.append(odd_vo)
    return points_b, points_v, points_vo

def print_matrix(mat):
    if mat:
        print("")
        for i in range (len(mat)):
            print(mat[i])

def create_mat(size):
    width = size[0]
    height = size[1]

    res = []
    for i in range (width):
        res.append([0]*(height))

    return res

def generate_mat(size):
    mat = create_mat(size)
    random.seed()

    for i in range (size[0]):
        for j in range (size[1]):
            mat[i][j] = random.randint(0, 10)

    return mat

def vinograd(mat1, mat2):
    try:
        width1 = len(mat1)
        width2 = len(mat2)

        height1 = len(mat1[0])
        height2 = len(mat2[0])
    except:
        return

    if height1 != width2:
        print("\nCan't multiplex given matrixes")
        return

    mulh = [0] * (width1)
    mulv = [0] * (height2)

    res = create_mat([width1, height2])
    for i in range (width1):
        for j in range (height1//2):
            mulh[i] = mulh[i] + mat1[i][2*j] * mat1[i][2*j+1]

    for i in range (height2):
        for j in range (height1//2):
            mulv[i] = mulv[i] + mat2[2*j][i] * mat2[2*j+1][i]

    for i in range (width1):
        for j in range (height2):
            res[i][j] = -mulh[i] -mulv[j]
            for k in range (height1//2):
                res[i][j] = res[i][j] + (mat1[i][2*k]+mat2[2*k+1][j])*(mat1[i][2*k+1]+mat2[2*k][j])

    if height1%2:
        for i in range (width1):
            for j in range (height2):
                res[i][j] = res[i][j] + mat1[i][height1-1] * mat2[height1-1][j]

    return res

def vinograd_optimized(mat1, mat2):
    try:
        width1 = len(mat1)
        width2 = len(mat2)

        height1 = len(mat1[0])
        height2 = len(mat2[0])
    except:
        return

    if height1 != width2:
        print("\nCan't multiplex given matrixes")
        return

    mulh = [0] * (width1)
    mulv = [0] * (height2)
    high_value = (height1//2)*2

    res = create_mat([width1, height2])
    for i in range (width1):
        for j in range (0, high_value, 2):
            mulh[i] -= mat1[i][j]*mat1[i][j+1]

    for i in range (height2):
        for j in range (0, high_value, 2):
            mulv[i] -= mat2[j][i]*mat2[j+1][i]

    for i in range (width1):
        for j in range (height2):
            res[i][j] = mulh[i] + mulv[j]

            buffer = 0
            for k in range (0, high_value, 2):
                buffer += (mat1[i][k]+mat2[k+1][j])*(mat1[i][k+1]+mat2[k][j])
            res[i][j] += buffer

            if height1 % 2:
                res[i][j] += mat1[i][height1-1]*mat2[height1-1][j]

    return res

def based(mat1, mat2):
    try:
        width1 = len(mat1)
        width2 = len(mat2)

        height1 = len(mat1[0])
        height2 = len(mat2[0])
    except:
        return

    if height1 != width2:
        print("\nCan't multiplex given matrixes")
        return

    res = create_mat([width1, height2])
    for i in range (width1):
        for j in range (height2):
            for k in range (height1):
                res[i][j] = res[i][j] + mat1[i][k]*mat2[k][j]

    return res

# n1 = int(input('rows1: '))
# m1 = int(input('columns1: '))
#
# n2 = int(input('rows2: '))
# m2 = int(input('columns2: '))
#
# mat1 = generate_mat([n1,m1])
# mat2 = generate_mat([n2,m2])
#
# print_matrix(mat1)
# print('first matrix')
# print_matrix(mat2)
# print('second matrix')
#
# res1 = based(mat1, mat2)
# print_matrix(res1)
# print('based result')
#
# res2 = vinograd(mat1, mat2)
# print_matrix(res2)
# print('vinograd result')
#
# res3 = vinograd_optimized(mat1, mat2)
# print_matrix(res3)
# print('vinograd optimized result')

mas = [[1,0,0,0,0],[0,1,0,0,0],[0,0,1,0,0],[0,0,0,1,0],[0,0,0,0,1]]
mas1 = [[1,2,3,4,5],[7,8,9,10,11],[12,13,14,15,16],[0,0,0,1,0],[0,0,0,0,1]]

print(vinograd(mas, mas1))

# y_b = []
# y_v = []
# y_vo = []
#
# y_b, y_v, y_vo = test_time(y_b, y_v, y_vo)
#
# p_x_even = [x*100 for x in range (1, 11)]
# p_x_odd = [x*100+1 for x in range (1, 11)]
# print(y_b, y_v, y_vo)
# show([p_x_even, p_x_odd], [y_b, y_v, y_vo])