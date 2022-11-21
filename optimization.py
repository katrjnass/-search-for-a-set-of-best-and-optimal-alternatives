with open('matrix.txt') as f:
    matrix = [list(map(int, row.split())) for row in f.readlines()]


def dfs(vertex):  # перевірка на ациклічність
    color[vertex] = "grey"
    for j in range(len(matrix)):
        if matrix[vertex][j] == 1:
            if color[j] == "white":
                dfs(j)
            if color[j] == "grey":
                return True
    color[vertex] = "black"


def append_elements(array1, array2):  # додавання елементів масиву в масив
    for k in array2:
        if k not in array1:
            array1.append(k)
    return array1


def find_Q(s1_s0, Q):  # знаходження послідовності множини Q
    q_temp = []
    for k in s1_s0:
        flag = False
        for j in range(len(matrix)):
            if matrix[j][k] == 1:
                if j in Q:  # верхній переріз не має мати одиниць в рядках з Q на попередньому кроці
                    flag = True
                    break
        if not flag:
            q_temp.append(k)
    append_elements(Q, q_temp)
    return Q


def neyman_morgenstern():  # знаходження множини Неймана-Моргенштерна
    S = []
    Q = []
    for k in range(len(matrix)):
        flag = False
        for j in range(len(matrix)):
            if matrix[j][k] == 1:
                flag = True
                break
        if not flag:  # обираємо перерізи в яких всі елементи=0
            S.append(k)
    append_elements(Q, S)
    while len(S) < len(matrix):
        s_temp = []
        for k in range(len(matrix)):
            flag = False
            for j in range(len(matrix)):
                if matrix[j][k] == 1:
                    if j not in S:  # одиниці можуть бути лише в рядках, які є в S
                        flag = True
                        break
            if not flag:
                if k not in S:
                    s_temp.append(k)
        find_Q(s_temp, Q)
        append_elements(S, s_temp)
    return Q


def vnutrishnya_stiykist():  # перевірка чи відповідає розв’язок властивості внутрішньої стійкості
    flag = False
    for k in X:
        gen = (l for l in X if l != k)  # перевіряємо чи є у кожному рядку з X одиниці на позиціях елементів з множини X
        for j in gen:
            if matrix[k][j] == 1 or matrix[j][k] == 1:
                flag = True
                break
    if not flag:
        return True


def zovnishna_stiykist():  # перевірка чи відповідає розв’язок властивості зовнішньої стійкості
    mnoshina = []
    for j in range(len(matrix)):
        if j not in X:
            mnoshina.append(j)  # множина усіх елементів, що не входять в X
    for k in mnoshina:
        flag = False
        for j in range(len(matrix)):
            if matrix[j][k] == 1 and j in X:  # якщо є хоча б одна одиниця в рядках з множини X
                flag = True
        if not flag:
            return False
    return True


def fill_matrix():  # представляємо усі відношення на одній матриці
    for k in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix[k][j] == 1 and matrix[j][k] == 1:
                matrix[k][j] = "I"
                matrix[j][k] = "I"
            if matrix[k][j] == 1 and matrix[j][k] == 0:
                matrix[k][j] = "P"
            if matrix[k][j] == 0 and matrix[j][k] == 0:
                matrix[k][j] = "N"
                matrix[j][k] = "N"


def check_kmax(sx):  # знаходимо множину k-максимальних елементів
    array_kmax = []
    array_pretend = []
    for k in range(len(matrix)):
        array_pretend.clear()
        for j in range(len(matrix)):
            if sx[k][j] == 1:
                array_pretend.append(j)  # масив з усіма позиціями одиниць, які стосуються цього рядка
        flag = True
        for l in range(len(matrix)):
            for p in range(len(matrix)):
                if sx[l][p] == 1 and p not in array_pretend:  # якщо є хоча б одна одиниця не на позиції з масиву, значить рядок, який перевіряємо не є k-максимальним
                    flag = False
                    break
        if flag:
            array_kmax.append(k)
    for k in range(len(array_kmax)):
        array_kmax[k] = array_kmax[k] + 1
    return array_kmax


def check_kopt(sx):  # знаходимо множину k-оптимальних елементів
    array_kopt = []
    for k in range(len(matrix)):
        counter = 0
        for j in range(len(matrix)):
            if sx[k][j] == 1:
                counter += 1  # підраховуємо кількість одиниць в рядку
        if counter == len(sx):
            array_kopt.append(k)
    for k in range(len(array_kopt)):
        array_kopt[k] = array_kopt[k] + 1
    return array_kopt


def k1optimization():  # k-оптимізація при k=1
    s = [[0] * len(matrix) for k in range(len(matrix))]
    for k in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix[k][j] == "N" or matrix[k][j] == "P" or matrix[k][j] == "I":
                s[k][j] = 1
    print("Множина 1-opt елементів", check_kopt(s))
    print("Множина 1-max елементів", check_kmax(s))


def k2_k3optimization(vidnoshennya, number_k):  # k-оптимізація при k=2 і k=3
    s = [[0] * len(matrix) for k in range(len(matrix))]
    for k in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix[k][j] == vidnoshennya or matrix[k][j] == "P":
                s[k][j] = 1
    print(f'Множина {number_k}-opt елементів', check_kopt(s))
    print(f'Множина {number_k}-max елементів', check_kmax(s))


def k4optimization():  # k-оптимізація при k=4
    s = [[0] * len(matrix) for k in range(len(matrix))]
    for k in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix[k][j] == "P":
                s[k][j] = 1
    print("Множина 4-opt елементів", check_kopt(s))
    print("Множина 4-max елементів", check_kmax(s))


def koptimization():  # k-оптимізація
    fill_matrix()
    k1optimization()
    k2_k3optimization("N", 2)
    k2_k3optimization("I", 3)
    k4optimization()


color = [0] * len(matrix[0])
X = []
cycle = False
for i in range(len(matrix)):
    color[i] = "white"
for i in range(len(matrix)):
    if dfs(i):
        cycle = True
        break
if not cycle:
    print("Відношення ациклічне")
    X = neyman_morgenstern()
    X.sort()
    print_X = []
    for m in range(len(X)):
        print_X.append(X[m] + 1)
    print(f'{print_X}-множина Неймана-Моргенштерна')
    if vnutrishnya_stiykist() and zovnishna_stiykist():
        print(
            f'{print_X}-розв’язок рівняння Неймана-Моргенштерна, так як він має властивості внутрішньої і зовнішньої стійкості')
else:
    print("Відношення неациклічне")
    koptimization()