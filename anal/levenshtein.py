import random, time, sys

def create_random_line(size):
    str1 = ""
    str2 = ""

    random.seed()
    size1 = size2 = size

    for i in range (size1):
        str1 += chr(random.randint(32, 126))

    for i in range (size2):
        str2 += chr(random.randint(32, 126))

    return str1, str2

def print_matrix(mat):
    print("")
    for i in range (len(mat)):
        print(mat[i])

def create_matrix(weight, height):
    res = []
    for i in range (len(height) + 1):
        res.append([0]*(len(weight) + 1))

    return res

def compare():
    for i in range(2, 11):
        print(i)
        str1, str2 = create_random_line(i)
        #---------------------------
        time_start = time.process_time()

        for i in range(1000):
            lev_mat(str1, str2)

        time_end = time.process_time()
        print('{:.7f}'.format((time_end - time_start)/1000))
        #---------------------------
        time_start = time.process_time()

        for i in range(1000):
            d_lev_mat(str1, str2)

        time_end = time.process_time()
        print('{:.7f}'.format((time_end - time_start)/1000))
        # ---------------------------
        time_start = time.process_time()

        for i in range(1000):
            d_lev_rec(str1, str2)

        time_end = time.process_time()
        print('{:.7f}'.format((time_end - time_start)/1000))

def lev_mat(str1, str2, output = False):
    if len(str1) and len(str2):
        matrix = create_matrix(str1, str2)

        for i in range (1, len(matrix)):
            matrix[i][0] = matrix[i-1][0] + 1

        for i in range (1, len(matrix[0])):
            matrix[0][i] = matrix[0][i-1] + 1

        for i in range (1, len(str2) + 1):
            for j in range (1, len(str1) + 1):
                penalty = matrix[i-1][j-1]
                if str1[j-1] != str2[i-1]:
                    penalty += 1
                penalty = min(penalty, matrix[i][j-1] + 1, matrix[i-1][j] + 1)

                matrix[i][j] = penalty

        d = matrix[len(matrix) - 1][len(matrix[0]) - 1]
        if output:
            print_matrix(matrix)
    elif not len(str1) and not len(str2):
        d = 0
    else:
        if len(str1):
            d = len(str1)
        else:
            d = len(str2)

    return d

def d_lev_rec(str1, str2):
    # global mem_rec
    # global count
    #
    # count +=1

    if not (len(str1) or len(str2)):
        return 0
    elif not (len(str1) and len(str2)):
        if len(str1):
            return len(str1)
        else:
            return len(str2)

    # mem_rec += 2*sys.getsizeof(str1[:-1])
    # mem_rec += 2*sys.getsizeof(str2[:-1])
    d1 = d_lev_rec(str1, str2[:-1]) + 1
    d2 = d_lev_rec(str1[:-1], str2) + 1
    d3 = d_lev_rec(str1[:-1], str2[:-1])
    if str1[-1] != str2[-1]:
        d3 += 1

    d4 = 0
    if len(str1) > 1 and len(str2) > 1:
        if str1[-1] == str2[-2] and str1[-2] == str2[-1]:
            # mem_rec += sys.getsizeof(str1[:-2])
            # mem_rec += sys.getsizeof(str2[:-2])
            d4 = d_lev_rec(str1[:-2], str2[:-2]) + 1

    if not d4:
        res = min(d1, d2, d3)
    else:
        res = min(d1, d2, d3, d4)

    return res

def d_lev_mat(str1, str2, output = False):
    # global mem_mat

    if len(str1) and len(str2):
        matrix = create_matrix(str1, str2)

        for i in range (1, len(matrix)):
            matrix[i][0] = matrix[i-1][0] + 1

        for i in range (1, len(matrix[0])):
            matrix[0][i] = matrix[0][i-1] + 1

        for i in range (1, len(str2) + 1):
            for j in range (1, len(str1) + 1):
                penalty = matrix[i-1][j-1]
                if str1[j-1] != str2[i-1]:
                    penalty += 1
                penalty = min(penalty, matrix[i][j-1] + 1, matrix[i-1][j] + 1)
                if i > 1 and j > 1:
                    if str1[j-1] == str2[i-2] and str2[i-1] == str1[j-2]:
                        penalty = min(penalty, matrix[i-2][j-2] + 1)

                matrix[i][j] = penalty

        d = matrix[len(matrix) - 1][len(matrix[0]) - 1]
        # mem_mat += len(matrix)*len(matrix[0])*sys.getsizeof(matrix[0][0])
        # mem_mat += 2*sys.getsizeof(d)
        if output:
            print_matrix(matrix)
    elif not len(str1) and not len(str2):
        d = 0
    else:
        if len(str1):
            d = len(str1)
        else:
            d = len(str2)

    return d

string1 = input("first string to compare: ")
string2 = input("second string to compare: ")

print("string1: (", string1, ") ", len(string1))
print("string2: (", string2, ") ", len(string2))

mem_rec = 0
mem_mat = 0
count = 0

d_mat = lev_mat(string1, string2, True)
print("levenstein matrix ", d_mat)

d_d_l_mat = d_lev_mat(string1, string2, True)
print("damerau-levenstein matrix ", d_d_l_mat)

d_d_l_rec = d_lev_rec(string1, string2)
print("damerau-levenstein recurent ", d_d_l_rec)

# print("\nMemory recurse: {0} + (memory in stack for 1 call)*{1}".format(mem_rec, count))
# print("Memory not recurse: {0} + (memory in stack for 1 call)*1".format(mem_mat + sys.getsizeof(string1) + sys.getsizeof(string2)))

# compare()

