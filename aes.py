from ast import literal_eval

rounds = 4

next = 0
dummy =0 


def shiftrows(a):
    tmp = [0,0,0,0]
    for i in range (0,4):
        for j in range(0,4):
            tmp[j]= a[i][(j+i)%4]
        for j in range(0,4):
            a[i][j] = tmp[j]    

def mixcolumn(a):
    global next
    global dummy
    for j in range(0,4):
        for i in range(4):
            print("x"+ str(a[i][j])+" +", end = " ")
        for i in range(3):
            print("x"+str(next+i)+" +", end = " ")
        print("x"+str((next+3))+" - 5d"+str(dummy)+" >= 0")

        for i in range(4):
            print("d"+str(dummy)+"-x"+str(a[i][j])+" >= 0")
        for i in range(4):
            print("d"+str(dummy)+"-x"+str(next)+" >= 0")
            a[i][j]= next
            next= next+1
        dummy= dummy+1
        
    #for i in range(4):
    #    for j in range(4):
    #        print(a[i][j], end=" ")
    #    print("\n")


a = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]

for i in range(4):
    for j in range(4):
        a[i][j]=next
        next=next+1

print("minimize")
for i in range(rounds*16-1):
    print("x"+str(i)+" +", end=" ")
print("x"+str(rounds*16-1))

print("subject to")
for r in range(rounds):
    shiftrows(a)
    mixcolumn(a)

#for i in range(4,12):
#    print("d_{",i,"}\\\\")

stri4= """
x0 + x5 + x10 + x15 + x16 + x17 + x18 + x19 - 5d0 >= 0
d0-x0 >= 0
d0-x5 >= 0
d0-x10 >= 0
d0-x15 >= 0
d0-x16 >= 0
d0-x17 >= 0
d0-x18 >= 0
d0-x19 >= 0
x1 + x6 + x11 + x12 + x20 + x21 + x22 + x23 - 5d1 >= 0
d1-x1 >= 0
d1-x6 >= 0
d1-x11 >= 0
d1-x12 >= 0
d1-x20 >= 0
d1-x21 >= 0
d1-x22 >= 0
d1-x23 >= 0
x2 + x7 + x8 + x13 + x24 + x25 + x26 + x27 - 5d2 >= 0
d2-x2 >= 0
d2-x7 >= 0
d2-x8 >= 0
d2-x13 >= 0
d2-x24 >= 0
d2-x25 >= 0
d2-x26 >= 0
d2-x27 >= 0
x3 + x4 + x9 + x14 + x28 + x29 + x30 + x31 - 5d3 >= 0
d3-x3 >= 0
d3-x4 >= 0
d3-x9 >= 0
d3-x14 >= 0
d3-x28 >= 0
d3-x29 >= 0
d3-x30 >= 0
d3-x31 >= 0
x16 + x21 + x26 + x31 + x32 + x33 + x34 + x35 - 5d4 >= 0
d4-x16 >= 0
d4-x21 >= 0
d4-x26 >= 0
d4-x31 >= 0
d4-x32 >= 0
d4-x33 >= 0
d4-x34 >= 0
d4-x35 >= 0
x20 + x25 + x30 + x19 + x36 + x37 + x38 + x39 - 5d5 >= 0
d5-x20 >= 0
d5-x25 >= 0
d5-x30 >= 0
d5-x19 >= 0
d5-x36 >= 0
d5-x37 >= 0
d5-x38 >= 0
d5-x39 >= 0
x24 + x29 + x18 + x23 + x40 + x41 + x42 + x43 - 5d6 >= 0
d6-x24 >= 0
d6-x29 >= 0
d6-x18 >= 0
d6-x23 >= 0
d6-x40 >= 0
d6-x41 >= 0
d6-x42 >= 0
d6-x43 >= 0
x28 + x17 + x22 + x27 + x44 + x45 + x46 + x47 - 5d7 >= 0
d7-x28 >= 0
d7-x17 >= 0
d7-x22 >= 0
d7-x27 >= 0
d7-x44 >= 0
d7-x45 >= 0
d7-x46 >= 0
d7-x47 >= 0
x32 + x37 + x42 + x47 + x48 + x49 + x50 + x51 - 5d8 >= 0
d8-x32 >= 0
d8-x37 >= 0
d8-x42 >= 0
d8-x47 >= 0
d8-x48 >= 0
d8-x49 >= 0
d8-x50 >= 0
d8-x51 >= 0
x36 + x41 + x46 + x35 + x52 + x53 + x54 + x55 - 5d9 >= 0
d9-x36 >= 0
d9-x41 >= 0
d9-x46 >= 0
d9-x35 >= 0
d9-x52 >= 0
d9-x53 >= 0
d9-x54 >= 0
d9-x55 >= 0
x40 + x45 + x34 + x39 + x56 + x57 + x58 + x59 - 5d10 >= 0
d10-x40 >= 0
d10-x45 >= 0
d10-x34 >= 0
d10-x39 >= 0
d10-x56 >= 0
d10-x57 >= 0
d10-x58 >= 0
d10-x59 >= 0
x44 + x33 + x38 + x43 + x60 + x61 + x62 + x63 - 5d11 >= 0
d11-x44 >= 0
d11-x33 >= 0
d11-x38 >= 0
d11-x43 >= 0
d11-x60 >= 0
d11-x61 >= 0
d11-x62 >= 0
d11-x63 >= 0
x48 + x53 + x58 + x63 + x64 + x65 + x66 + x67 - 5d12 >= 0
d12-x48 >= 0
d12-x53 >= 0
d12-x58 >= 0
d12-x63 >= 0
d12-x64 >= 0
d12-x65 >= 0
d12-x66 >= 0
d12-x67 >= 0
x52 + x57 + x62 + x51 + x68 + x69 + x70 + x71 - 5d13 >= 0
d13-x52 >= 0
d13-x57 >= 0
d13-x62 >= 0
d13-x51 >= 0
d13-x68 >= 0
d13-x69 >= 0
d13-x70 >= 0
d13-x71 >= 0
x56 + x61 + x50 + x55 + x72 + x73 + x74 + x75 - 5d14 >= 0
d14-x56 >= 0
d14-x61 >= 0
d14-x50 >= 0
d14-x55 >= 0
d14-x72 >= 0
d14-x73 >= 0
d14-x74 >= 0
d14-x75 >= 0
x60 + x49 + x54 + x59 + x76 + x77 + x78 + x79 - 5d15 >= 0
d15-x60 >= 0
d15-x49 >= 0
d15-x54 >= 0
d15-x59 >= 0
d15-x76 >= 0
d15-x77 >= 0
d15-x78 >= 0
d15-x79 >= 0"""


stri3= """
x0 + x5 + x10 + x15 + x16 + x17 + x18 + x19 - 5d0 >= 0
x1 + x6 + x11 + x12 + x20 + x21 + x22 + x23 - 5d1 >= 0
x2 + x7 + x8 + x13 + x24 + x25 + x26 + x27 - 5d2 >= 0
x3 + x4 + x9 + x14 + x28 + x29 + x30 + x31 - 5d3 >= 0
x16 + x21 + x26 + x31 + x32 + x33 + x34 + x35 - 5d4 >= 0
x20 + x25 + x30 + x19 + x36 + x37 + x38 + x39 - 5d5 >= 0
x24 + x29 + x18 + x23 + x40 + x41 + x42 + x43 - 5d6 >= 0
x28 + x17 + x22 + x27 + x44 + x45 + x46 + x47 - 5d7 >= 0
x32 + x37 + x42 + x47 + x48 + x49 + x50 + x51 - 5d8 >= 0
x36 + x41 + x46 + x35 + x52 + x53 + x54 + x55 - 5d9 >= 0
x40 + x45 + x34 + x39 + x56 + x57 + x58 + x59 - 5d10 >= 0
x44 + x33 + x38 + x43 + x60 + x61 + x62 + x63 - 5d11 >= 0

d0-x0 >= 0
d0-x5 >= 0
d0-x10 >= 0
d0-x15 >= 0
d0-x16 >= 0
d0-x17 >= 0
d0-x18 >= 0
d0-x19 >= 0

d1-x1 >= 0
d1-x6 >= 0
d1-x11 >= 0
d1-x12 >= 0
d1-x20 >= 0
d1-x21 >= 0
d1-x22 >= 0
d1-x23 >= 0
d2-x2 >= 0
d2-x7 >= 0
d2-x8 >= 0
d2-x13 >= 0
d2-x24 >= 0
d2-x25 >= 0
d2-x26 >= 0
d2-x27 >= 0
d3-x3 >= 0
d3-x4 >= 0
d3-x9 >= 0
d3-x14 >= 0
d3-x28 >= 0
d3-x29 >= 0
d3-x30 >= 0
d3-x31 >= 0
d4-x16 >= 0
d4-x21 >= 0
d4-x26 >= 0
d4-x31 >= 0
d4-x32 >= 0
d4-x33 >= 0
d4-x34 >= 0
d4-x35 >= 0
d5-x20 >= 0
d5-x25 >= 0
d5-x30 >= 0
d5-x19 >= 0
d5-x36 >= 0
d5-x37 >= 0
d5-x38 >= 0
d5-x39 >= 0
d6-x24 >= 0
d6-x29 >= 0
d6-x18 >= 0
d6-x23 >= 0
d6-x40 >= 0
d6-x41 >= 0
d6-x42 >= 0
d6-x43 >= 0
d7-x28 >= 0
d7-x17 >= 0
d7-x22 >= 0
d7-x27 >= 0
d7-x44 >= 0
d7-x45 >= 0
d7-x46 >= 0
d7-x47 >= 0
d8-x32 >= 0
d8-x37 >= 0
d8-x42 >= 0
d8-x47 >= 0
d8-x48 >= 0
d8-x49 >= 0
d8-x50 >= 0
d8-x51 >= 0
d9-x36 >= 0
d9-x41 >= 0
d9-x46 >= 0
d9-x35 >= 0
d9-x52 >= 0
d9-x53 >= 0
d9-x54 >= 0
d9-x55 >= 0
d10-x40 >= 0
d10-x45 >= 0
d10-x34 >= 0
d10-x39 >= 0
d10-x56 >= 0
d10-x57 >= 0
d10-x58 >= 0
d10-x59 >= 0
d11-x44 >= 0
d11-x33 >= 0
d11-x38 >= 0
d11-x43 >= 0
d11-x60 >= 0
d11-x61 >= 0
d11-x62 >= 0
d11-x63 >= 0
"""

M=[]
dic={}

for i in range(36*3):
    M.append([])
    for e in range(16+20*3):
        M[i].append(0)

c=0
for a in range(16+20*3):
    if a<4*3:
        dic["d"+str(a)]=a
    else:
        dic["x"+str(c)]=a
        c+=1

def buildmat(lala,dic,M):
    print("tst")
    items=dic.keys()
    print(items)
    lal= lala.splitlines()
    for a in lal:
        if a=="":
            lal.remove(a)
    print(lal)
    print(len(lal))
    o=0
    for i in lal:
        for key in dic.keys():
            if "- "+key+" " in i or "-"+key+" " in i:
                M[o][dic[key]]=-1
            elif "-2"+key+" " in i:
                M[o][dic[key]]=-2
            elif "- 5"+key+" " in i:
                M[o][dic[key]]=-5
            
            elif key+" " in i or key+"-" in i:
                #print(dic[key])
                M[o][dic[key]]=1
            
        o+=1
    #print(M)
    return M

def sortcon(ma):
    order={}
    for li in ma:
        indices = [i for i, x in enumerate(li) if x != 0]
        #print(indices)
        order[str(li)]=indices[1]
    dic2=dict(sorted(order.items(),key= lambda x:x[1]))
    print(dic2)
    mat= list(dic2.keys())
    for i in range(len(mat)):
        mat[i] = literal_eval(mat[i])
    #print(mat)
    return mat
  
ma= buildmat(stri3,dic,M)
#print(ma)
#wenn 1 runde dann 9
malast=ma[(4*3):]

malast= sortcon(malast)

mat=ma[:(4*3)]+malast

def latex(matrix):
    input=""
    for i in matrix:
        zahl= 0
        for j in i:
            if zahl!=0:
                input+=" & "
            if j!=0:
                input= input+str(j)
            zahl+=1
        input+="\\\ \n"
    return input
    
#print(mat)

print(latex(mat))
