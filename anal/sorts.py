import time
import random
from copy import deepcopy

def test_time2():
    g_ord = open("gnome_ord.txt", "w")
    g_rev = open("gnome_rev.txt", "w")
    g_ran = open("gnome_ran.txt", "w")

    c_ord = open("choice_ord.txt", "w")
    c_rev = open("choice_rev.txt", "w")
    c_ran = open("choice_ran.txt", "w")

    k_ord = open("cocktail_ord.txt", "w")
    k_rev = open("cocktail_rev.txt", "w")
    k_ran = open("cocktail_ran.txt", "w")
    for i in ([a for a in range(100, 1001, 100)]):
        start, end = 0, 0
        for j in range(100):
            sorted = generate_sorted(i)
            start += time.process_time()
            gnome(sorted)
            end += time.process_time()

        g_ord.write(str(i) + " " + str((end - start)/100) + "\n")

        #-------------------------------------------------

        start, end = 0, 0
        for j in range(100):
            reverse = generate_reverse(i)
            start += time.process_time()
            gnome(reverse)
            end += time.process_time()

        g_rev.write(str(i) + " " + str((end - start)/100) + "\n")

        #------------------------------------------------

        start, end = 0, 0
        for j in range(100):
            randomed = generate_random(i)
            start += time.process_time()
            gnome(randomed)
            end += time.process_time()

        g_ran.write(str(i) + " " + str((end - start)/100) + "\n")

        #------------------------------------------------
        #------------------------------------------------

        start, end = 0, 0
        for j in range(100):
            sorted = generate_sorted(i)
            start += time.process_time()
            cocktail(sorted)
            end += time.process_time()

        k_ord.write(str(i) + " " + str((end - start)/100) + "\n")

        # -------------------------------------------------

        start, end = 0, 0
        for j in range(100):
            reverse = generate_reverse(i)
            start += time.process_time()
            cocktail(reverse)
            end += time.process_time()

        k_rev.write(str(i) + " " + str((end - start)/100) + "\n")

        # ------------------------------------------------

        start, end = 0, 0
        for j in range(100):
            randomed = generate_random(i)
            start += time.process_time()
            cocktail(randomed)
            end += time.process_time()

        k_ran.write(str(i) + " " + str((end - start)/100) + "\n")

        # ------------------------------------------------
        # ------------------------------------------------

        start, end = 0, 0
        for j in range(100):
            sorted = generate_sorted(i)
            start += time.process_time()
            choice(sorted)
            end += time.process_time()

        c_ord.write(str(i) + " " + str((end - start)/100) + "\n")

        # -------------------------------------------------

        start, end = 0, 0
        for j in range(100):
            reverse = generate_reverse(i)
            start += time.process_time()
            choice(reverse)
            end += time.process_time()

        c_rev.write(str(i) + " " + str((end - start)/100) + "\n")

        # ------------------------------------------------

        start, end = 0, 0
        for j in range(100):
            randomed = generate_random(i)
            start += time.process_time()
            choice(randomed)
            end += time.process_time()

        c_ran.write(str(i) + " " + str((end - start)/100) + "\n")

        # ------------------------------------------------
        # ------------------------------------------------

    g_ord.close()
    g_rev.close()
    g_ran.close()

    c_ord.close()
    c_rev.close()
    c_ran.close()

    k_ord.close()
    k_rev.close()
    k_ran.close()

def test_time():
    compare_3_sorts_time = []
    for i in ([a for a in range (100, 1001, 100)]):
        time_cocktail = []
        time_choice = []
        time_gnome = []

        start, end = 0, 0
        sorted = generate_sorted(i)
        for j in range (100):
            start += time.process_time()
            cocktail(sorted)
            end += time.process_time()

        time_cocktail.append((end - start)/100)
        #-------------------------------------
        start, end = 0, 0
        for j in range(100):
            start += time.process_time()
            choice(sorted)
            end += time.process_time()

        time_choice.append((end - start) / 100)
        #---------------------------------------
        start, end = 0, 0
        for j in range(100):
            start += time.process_time()
            gnome(sorted)
            end += time.process_time()

        time_gnome.append((end - start) / 100)
        #---------------------------------------
        #---------------------------------------
        start, end = 0, 0
        reverse = generate_reverse(i)
        for j in range(100):
            start += time.process_time()
            cocktail(reverse)
            end += time.process_time()

        time_cocktail.append((end - start) / 100)
        # -------------------------------------
        start, end = 0, 0
        for j in range(100):
            start += time.process_time()
            choice(reverse)
            end += time.process_time()

        time_choice.append((end - start) / 100)
        # ---------------------------------------
        start, end = 0, 0
        for j in range(100):
            start += time.process_time()
            gnome(reverse)
            end += time.process_time()

        time_gnome.append((end - start) / 100)
        # ---------------------------------------
        # ---------------------------------------
        start, end = 0, 0
        rand = generate_random(i)
        for j in range(100):
            start += time.process_time()
            cocktail(rand)
            end += time.process_time()

        time_cocktail.append((end - start) / 100)
        # -------------------------------------
        start, end = 0, 0
        for j in range(100):
            start += time.process_time()
            choice(rand)
            end += time.process_time()

        time_choice.append((end - start) / 100)
        # ---------------------------------------
        start, end = 0, 0
        for j in range(100):
            start += time.process_time()
            gnome(rand)
            end += time.process_time()

        time_gnome.append((end - start) / 100)

        #---------------------------------------
        #---------------------------------------
        #---------------------------------------
        compare_3_sorts_time.append((time_cocktail, time_choice, time_gnome))

    return compare_3_sorts_time

def generate_random(len):
    random.seed()
    arr = []

    for i in range (len):
        arr.append(random.randint(-1000, 1000))

    return arr

def generate_reverse(len):
    random.seed()

    k = random.randint(1, 47)
    return [k*i for i in range (len, 0, -1)]

def generate_sorted(len):
    random.seed()

    k = random.randint(1, 47)
    return [k*i for i in range (1, len + 1)]

def cocktail(array):
    left = 0
    right = len(array)-1

    while left <= right:
        for i in range(left, right):
            if array[i] > array[i+1]:
                array[i], array[i+1] = array[i+1], array[i]
        right -= 1

        for i in range(right, left, -1):
            if array[i-1] > array[i]:
                array[i-1], array[i] = array[i], array[i-1]
        left += 1

    return array

def gnome(array):
    i = 1
    size = len(array)

    while i < size:
        if not i or array[i - 1] <= array[i]:
            i += 1
        else:
            array[i], array[i - 1] = array[i - 1], array[i]
            i -= 1

    return array

def choice(array):
    size = len(array)

    for i in range (size - 1):
        min = i

        for j in range (i + 1, size):
            if array[j] < array[min]:
                min = j

        array[i], array[min] = array[min], array[i]

    return array

# mas = test_time()
# f = 100
# l = 1
# for i in mas:
#     print(f*l)
#     for j in i:
#         print(j)
#     print('\n')
#     l += 1
##test_time2()

# arr = generate_random(10)
arr = [random.randint(0, 2) for i in range (1000)]
arr2 = deepcopy(arr)
arr3 = deepcopy(arr)

# print("original array :", arr)
t1 = time.time()
print("gnome sort: ", gnome(arr))
t2 = time.time()
print(t2-t1)

t1 = time.time()
print("choise sort: ", choice(arr))
t2 = time.time()
print(t2-t1)

t1 = time.time()
print("coctail sort: ", cocktail(arr))
t2 = time.time()
print(t2-t1)