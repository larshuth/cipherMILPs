from distutils.command.build import build
from ast import literal_eval

constraintsstring = ""


def constraints(A, S, counter, dummy, M, dic):
    # wenn optimieren dann vllt dass die constraints als einzigen string returnt werden
    erstes = A[31], "+", A[32], "+ x" + str(counter), "-2d" + str(dummy), "=<0\n"
    "d" + str(dummy), "-", A[31], "=<0\n"
    "d" + str(dummy), "-", A[32], "=<0\n"
    "d" + str(dummy), "-x" + str(counter), "=<0\n"
    print(A[31], "+", A[32], "+ x" + str(counter), "-2d" + str(dummy), "=<0\n"
                                                                       "d" + str(dummy), "-", A[31], "=<0\n"
                                                                                                     "d" + str(dummy),
          "-", A[32], "=<0\n"
                      "d" + str(dummy), "-x" + str(counter), "=<0\n")
    A[31] = "x" + str(counter)
    counter += 1
    dummy += 1

    print(A[32], "+", A[2], "+ x" + str(counter), "-2d" + str(dummy), "=<0\n"
                                                                      "d" + str(dummy), "-", A[32], "=<0\n"
                                                                                                    "d" + str(dummy),
          "-", A[2], "=<0\n"
                     "d" + str(dummy), "-x" + str(counter), "=<0\n")
    S[0] = "x" + str(counter)
    counter += 1
    dummy += 1

    print(A[33], "+", A[7], "+ x" + str(counter), "-2d" + str(dummy), "=<0\n"
                                                                      "d" + str(dummy), "-", A[33], "=<0\n"
                                                                                                    "d" + str(dummy),
          "-", A[7], "=<0\n"
                     "d" + str(dummy), "-x" + str(counter), "=<0\n")
    S[1] = "x" + str(counter)
    counter += 1
    dummy += 1

    print(S[0], "+", S[1], "+ x" + str(counter), "+x" + str(counter + 1), "-3d" + str(dummy), "=<0\n"
                                                                                              "d" + str(dummy), "-",
          S[0], "=<0\n"
                "d" + str(dummy), "-", S[1], "=<0\n"
                                             "d" + str(dummy), "-x" + str(counter), "=<0\n"
                                                                                    "d" + str(dummy),
          "-x" + str(counter + 1), "=<0\n")
    S[2] = "x" + str(counter)
    counter += 1
    S[3] = "x" + str(counter)
    counter += 1
    dummy += 1

    print(A[16], "+", S[2], "+ x" + str(counter), "-2d" + str(dummy), "=<0\n"
                                                                      "d" + str(dummy), "-", A[16], "=<0\n"
                                                                                                    "d" + str(dummy),
          "-", S[2], "=<0\n"
                     "d" + str(dummy), "-x" + str(counter), "=<0\n")
    A[32] = "x" + str(counter)
    counter += 1
    dummy += 1

    print(A[29], "+", S[3], "+ x" + str(counter), "-2d" + str(dummy), "=<0\n"
                                                                      "d" + str(dummy), "-", A[29], "=<0\n"
                                                                                                    "d" + str(dummy),
          "-", S[3], "=<0\n"
                     "d" + str(dummy), "-x" + str(counter), "=<0\n")
    A[33] = "x" + str(counter)
    counter += 1
    dummy += 1

    print(A[2], "+", A[6], "+ x" + str(counter), "-2d" + str(dummy), "=<0\n"
                                                                     "d" + str(dummy), "-", A[2], "=<0\n"
                                                                                                  "d" + str(dummy), "-",
          A[6], "=<0\n"
                "d" + str(dummy), "-x" + str(counter), "=<0\n")
    A[2] = "x" + str(counter)
    counter += 1
    dummy += 1

    print(A[7], "+", A[15], "+ x" + str(counter), "-2d" + str(dummy), "=<0\n"
                                                                      "d" + str(dummy), "-", A[7], "=<0\n"
                                                                                                   "d" + str(dummy),
          "-", A[15], "=<0\n"
                      "d" + str(dummy), "-x" + str(counter), "=<0\n")
    A[7] = "x" + str(counter)
    counter += 1
    dummy += 1

    print(A[16], "+", A[28], "+ x" + str(counter), "-2d" + str(dummy), "=<0\n"
                                                                       "d" + str(dummy), "-", A[16], "=<0\n"
                                                                                                     "d" + str(dummy),
          "-", A[28], "=<0\n"
                      "d" + str(dummy), "-x" + str(counter), "=<0\n")
    A[16] = "x" + str(counter)
    counter += 1
    dummy += 1

    # Verschieben
    la = A[31]
    for i in range(30, -1, -1):
        temp = A[i]
        A[i + 1] = temp
    A[0] = la

    # print(A)
    return A, S, counter, dummy


counter = 0
# Array mit den Bits die momentan in der Cipher sind
A = []
for e in range(34):
    A.append("x" + str(counter))
    counter += 1

S = [0, 0, 0, 0]

dummy = 0

rounds = 3
M = []
dic = {}

# initialisieren der Matrix
for i in range(37 * rounds):
    M.append([])
    for e in range(34 + 19 * rounds):
        M[i].append(0)

# In dem dictionary wird für jede Variable deren Position gespeichert
c = 0
for a in range(34 + 19 * rounds):
    if a < 9 * rounds:
        dic["d" + str(a)] = a
    else:
        dic["x" + str(c)] = a
        c += 1

# hier wird das Array durch die Cipher gejagt für die jeweilige Anzahl an Runden
for a in range(rounds):
    A, S, counter, dummy = constraints(A, S, counter, dummy, M, dic)


# FROM HERE ON THE CODE IS (ALMOST) THE SAME AS FOR AES

# takes string of constraints and fills in the matrix
# input: string of the constraints, dictionary of order of the variables, and the Matrix
def buildmat(lala, dic, M):
    lal = lala.splitlines()
    for a in lal:
        if a == "":
            lal.remove(a)
    print(lal)
    o = 0
    for i in lal:
        for key in dic.keys():
            if "- " + key + " " in i or "-" + key + " " in i:
                M[o][dic[key]] = -1
            elif "-2" + key + " " in i:
                M[o][dic[key]] = -2
            elif "-3" + key + " " in i:
                M[o][dic[key]] = -3
            elif key + " " in i:
                M[o][dic[key]] = 1

        o += 1
    return M


# i am lowkey embarrassed by this mess, these are the sorted strings
# TO DO: function that sorts the constraints by itself (hier nur lange constraints nach oben)
# for 1 round
stri = """x31 + x32 + x34 -2d0 =<0
x32 + x2 + x35 -2d1 =<0
x33 + x7 + x36 -2d2 =<0
x35 + x36 + x37 +x38 -3d3 =<0
x16 + x37 + x39 -2d4 =<0
x29 + x38 + x40 -2d5 =<0
x2 + x6 + x41 -2d6 =<0
x7 + x15 + x42 -2d7 =<0
x16 + x28 + x43 -2d8 =<0
d0 - x31 =<0
d0 - x32 =<0
d0 -x34 =<0

d1 - x32 =<0
d1 - x2 =<0
d1 -x35 =<0

d2 - x33 =<0
d2 - x7 =<0
d2 -x36 =<0

d3 - x35 =<0
d3 - x36 =<0
d3 -x37 =<0
d3 -x38 =<0

d4 - x16 =<0
d4 - x37 =<0
d4 -x39 =<0

d5 - x29 =<0
d5 - x38 =<0
d5 -x40 =<0

d6 - x2 =<0
d6 - x6 =<0
d6 -x41 =<0

d7 - x7 =<0
d7 - x15 =<0
d7 -x42 =<0

d8 - x16 =<0
d8 - x28 =<0
d8 -x43 =<0"""

# for 3 rounds:
stri3 = """x31 + x32 + x34 -2d0 =<0
x32 + x2 + x35 -2d1 =<0
x33 + x7 + x36 -2d2 =<0
x35 + x36 + x37 +x38 -3d3 =<0
x16 + x37 + x39 -2d4 =<0
x29 + x38 + x40 -2d5 =<0
x2 + x6 + x41 -2d6 =<0
x7 + x15 + x42 -2d7 =<0
x16 + x28 + x43 -2d8 =<0
x30 + x39 + x44 -2d9 =<0
x39 + x1 + x45 -2d10 =<0
x40 + x6 + x46 -2d11 =<0
x45 + x46 + x47 +x48 -3d12 =<0
x15 + x47 + x49 -2d13 =<0
x28 + x48 + x50 -2d14 =<0
x1 + x5 + x51 -2d15 =<0
x6 + x14 + x52 -2d16 =<0
x15 + x27 + x53 -2d17 =<0
x29 + x49 + x54 -2d18 =<0
x49 + x0 + x55 -2d19 =<0
x50 + x5 + x56 -2d20 =<0
x55 + x56 + x57 +x58 -3d21 =<0
x14 + x57 + x59 -2d22 =<0
x27 + x58 + x60 -2d23 =<0
x0 + x4 + x61 -2d24 =<0
x5 + x13 + x62 -2d25 =<0
x14 + x26 + x63 -2d26 =<0

d0 - x31 =<0
d0 - x32 =<0
d0 -x34 =<0

d1 - x32 =<0
d1 - x2 =<0
d1 -x35 =<0

d2 - x33 =<0
d2 - x7 =<0
d2 -x36 =<0

d3 - x35 =<0
d3 - x36 =<0
d3 -x37 =<0
d3 -x38 =<0

d4 - x16 =<0
d4 - x37 =<0
d4 -x39 =<0

d5 - x29 =<0
d5 - x38 =<0
d5 -x40 =<0

d6 - x2 =<0
d6 - x6 =<0
d6 -x41 =<0

d7 - x7 =<0
d7 - x15 =<0
d7 -x42 =<0

d8 - x16 =<0
d8 - x28 =<0
d8 -x43 =<0

d9 - x30 =<0
d9 - x39 =<0
d9 -x44 =<0

d10 - x39 =<0
d10 - x1 =<0
d10 -x45 =<0

d11 - x40 =<0
d11 - x6 =<0
d11 -x46 =<0

d12 - x45 =<0
d12 - x46 =<0
d12 -x47 =<0
d12 -x48 =<0

d13 - x15 =<0
d13 - x47 =<0
d13 -x49 =<0

d14 - x28 =<0
d14 - x48 =<0
d14 -x50 =<0

d15 - x1 =<0
d15 - x5 =<0
d15 -x51 =<0

d16 - x6 =<0
d16 - x14 =<0
d16 -x52 =<0

d17 - x15 =<0
d17 - x27 =<0
d17 -x53 =<0

d18 - x29 =<0
d18 - x49 =<0
d18 -x54 =<0

d19 - x49 =<0
d19 - x0 =<0
d19 -x55 =<0

d20 - x50 =<0
d20 - x5 =<0
d20 -x56 =<0

d21 - x55 =<0
d21 - x56 =<0
d21 -x57 =<0
d21 -x58 =<0

d22 - x14 =<0
d22 - x57 =<0
d22 -x59 =<0

d23 - x27 =<0
d23 - x58 =<0
d23 -x60 =<0

d24 - x0 =<0
d24 - x4 =<0
d24 -x61 =<0

d25 - x5 =<0
d25 - x13 =<0
d25 -x62 =<0

d26 - x14 =<0
d26 - x26 =<0
d26 -x63 =<0"""

# for 4 rounds:
stri4 = """x31 + x32 + x34 -2d0 =<0
x32 + x2 + x35 -2d1 =<0
x33 + x7 + x36 -2d2 =<0
x35 + x36 + x37 +x38 -3d3 =<0
x16 + x37 + x39 -2d4 =<0
x29 + x38 + x40 -2d5 =<0
x2 + x6 + x41 -2d6 =<0
x7 + x15 + x42 -2d7 =<0
x16 + x28 + x43 -2d8 =<0
x30 + x39 + x44 -2d9 =<0
x39 + x1 + x45 -2d10 =<0
x40 + x6 + x46 -2d11 =<0
x45 + x46 + x47 +x48 -3d12 =<0
x15 + x47 + x49 -2d13 =<0
x28 + x48 + x50 -2d14 =<0
x1 + x5 + x51 -2d15 =<0
x6 + x14 + x52 -2d16 =<0
x15 + x27 + x53 -2d17 =<0
x29 + x49 + x54 -2d18 =<0
x49 + x0 + x55 -2d19 =<0
x50 + x5 + x56 -2d20 =<0
x55 + x56 + x57 +x58 -3d21 =<0
x14 + x57 + x59 -2d22 =<0
x27 + x58 + x60 -2d23 =<0
x0 + x4 + x61 -2d24 =<0
x5 + x13 + x62 -2d25 =<0
x14 + x26 + x63 -2d26 =<0
x28 + x59 + x64 -2d27 =<0
x59 + x34 + x65 -2d28 =<0
x60 + x4 + x66 -2d29 =<0
x65 + x66 + x67 +x68 -3d30 =<0
x13 + x67 + x69 -2d31 =<0
x26 + x68 + x70 -2d32 =<0
x34 + x3 + x71 -2d33 =<0
x4 + x12 + x72 -2d34 =<0
x13 + x25 + x73 -2d35 =<0

d0 - x31 =<0
d0 - x32 =<0
d0 -x34 =<0

d1 - x32 =<0
d1 - x2 =<0
d1 -x35 =<0

d2 - x33 =<0
d2 - x7 =<0
d2 -x36 =<0

d3 - x35 =<0
d3 - x36 =<0
d3 -x37 =<0
d3 -x38 =<0

d4 - x16 =<0
d4 - x37 =<0
d4 -x39 =<0

d5 - x29 =<0
d5 - x38 =<0
d5 -x40 =<0

d6 - x2 =<0
d6 - x6 =<0
d6 -x41 =<0

d7 - x7 =<0
d7 - x15 =<0
d7 -x42 =<0

d8 - x16 =<0
d8 - x28 =<0
d8 -x43 =<0

d9 - x30 =<0
d9 - x39 =<0
d9 -x44 =<0

d10 - x39 =<0
d10 - x1 =<0
d10 -x45 =<0

d11 - x40 =<0
d11 - x6 =<0
d11 -x46 =<0

d12 - x45 =<0
d12 - x46 =<0
d12 -x47 =<0
d12 -x48 =<0

d13 - x15 =<0
d13 - x47 =<0
d13 -x49 =<0

d14 - x28 =<0
d14 - x48 =<0
d14 -x50 =<0

d15 - x1 =<0
d15 - x5 =<0
d15 -x51 =<0

d16 - x6 =<0
d16 - x14 =<0
d16 -x52 =<0

d17 - x15 =<0
d17 - x27 =<0
d17 -x53 =<0

d18 - x29 =<0
d18 - x49 =<0
d18 -x54 =<0

d19 - x49 =<0
d19 - x0 =<0
d19 -x55 =<0

d20 - x50 =<0
d20 - x5 =<0
d20 -x56 =<0

d21 - x55 =<0
d21 - x56 =<0
d21 -x57 =<0
d21 -x58 =<0

d22 - x14 =<0
d22 - x57 =<0
d22 -x59 =<0

d23 - x27 =<0
d23 - x58 =<0
d23 -x60 =<0

d24 - x0 =<0
d24 - x4 =<0
d24 -x61 =<0

d25 - x5 =<0
d25 - x13 =<0
d25 -x62 =<0

d26 - x14 =<0
d26 - x26 =<0
d26 -x63 =<0

d27 - x28 =<0
d27 - x59 =<0
d27 -x64 =<0

d28 - x59 =<0
d28 - x34 =<0
d28 -x65 =<0

d29 - x60 =<0
d29 - x4 =<0
d29 -x66 =<0

d30 - x65 =<0
d30 - x66 =<0
d30 -x67 =<0
d30 -x68 =<0

d31 - x13 =<0
d31 - x67 =<0
d31 -x69 =<0

d32 - x26 =<0
d32 - x68 =<0
d32 -x70 =<0

d33 - x34 =<0
d33 - x3 =<0
d33 -x71 =<0

d34 - x4 =<0
d34 - x12 =<0
d34 -x72 =<0

d35 - x13 =<0
d35 - x25 =<0
d35 -x73 =<0
"""


# print(ma)

# this function takes the the last part of the matrix (with 2 variables in a row, not more)
# and takes the position of their second variable, puts it in a dictionary
# then we sort the dictionary and turn the sorted rows into a matrix again
def sortcon(ma):
    order = {}
    for li in ma:
        indices = [i for i, x in enumerate(li) if x != 0]
        order[str(li)] = indices[1]
    dic2 = dict(sorted(order.items(), key=lambda x: x[1]))
    # print(dic2)
    mat = list(dic2.keys())
    for i in range(len(mat)):
        mat[i] = literal_eval(mat[i])
    return mat


ma = buildmat(stri3, dic, M)
# print(ma)

# we sort only the last constraints, not the long ones
malast = ma[(9 * rounds):]
malast = sortcon(malast)

# now we add them together and get the sorted matrix (which has a diagonal now)
mat = ma[:(9 * rounds)] + malast


# this function just turns the Matrix into an output that can be used for latex
def latex(matrix):
    input = ""
    for i in matrix:
        zahl = 0
        for j in i:
            if zahl != 0:
                input += " & "
            if j != 0:
                input = input + str(j)
            zahl += 1
        input += "\\\ \n"
    return input


# print(mat)

print(latex(mat))
