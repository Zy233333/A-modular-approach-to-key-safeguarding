# author:Zy233333
# date:2022/3/5
# 本例中r = 3, n = 5

import random


# 最大公约数
def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)


# 求模逆
def ex_eucd(a, m):
    if gcd(a, m) != 1:
        return None
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m


# 产生p和m1,m2,....mn
def is_coprime(m, len):
    for i in range(0, len):
        for j in range(i + 1, len):
            if gcd(m[i], m[j]) != 1:
                return False
    return True


def create():
    m = [0, 0, 0, 0, 0, 0]  # m[0]存放p

    m[0] = random.randint(pow(10, 50), pow(10, 51))
    i = 1
    while i < len(m):
        temp = random.randint(pow(10, 50), pow(10, 51))
        m[i] = temp
        if is_coprime(m, i + 1):
            i = i + 1

    i = 1
    while i < len(m):  # 排序
        j = 1
        while j < len(m) - i:
            if m[j] > m[j + 1]:
                temp = m[j]
                m[j] = m[j + 1]
                m[j + 1] = temp
            j = j + 1
        i = i + 1
    return m


def create_p_m():
    m = create()
    while True:
        if m[1] * m[2] * m[3] > m[0] * m[4] * m[5]:
            return m
        m = create()


# 产生y1,y2,....yn
def create_yn(m, Y):
    y = [0, 0, 0, 0, 0, 0]
    for i in range(1, len(m)):
        y[i] = Y % m[i]
    return y


# 产生w1,w2,..wr-1及其逆元
def create_w(m, ir):
    w = [1, 0, 0]  # w[0]不存放
    for i in range(1, 3):
        w[i] = m[ir[i]]
        w[i] = w[i - 1] * w[i]
    return w


def create_inverse_w(m, ir, w):
    inverse_w = [0, 0, 0]  # inverse_w[0]不存放
    for i in range(1, 3):
        inverse_w[i] = ex_eucd(w[i], m[ir[i + 1]])
    return inverse_w


# 恢复密文
def recover(yr, m, ir, w, inverse_w):
    z = yr[1]
    a = [0, 0, 0]  # a[0]不存放
    for i in range(1, 3):
        a[i] = (yr[i + 1] - z) * inverse_w[i] % m[ir[i + 1]]
        z = z + a[i] * w[i]

    return z


# step1:生成符合条件的p,m1,m2,....mn
m = create_p_m()

# step2:秘密X及其对应的Y, y1,y2,....yn
X = random.randint(0, m[0])
M = m[1] * m[2] * m[3]
A = random.randint(0, M / m[0])
Y = X + A * m[0]
yn = create_yn(m, Y)

# step3:生成y(i1),y(i2),...,y(ir)（本例中r=3）
print("输入3份参与者1~5：")
ir = [0, 0, 0, 0]  # 存放参与者，ir[0]不存放
yr = [0, 0, 0, 0]  # yr[0]不存放
for i in range(1, 4):
    ir[i] = int(input())
ir.sort()
for i in range(1, 4):
    yr[i] = yn[ir[i]]

# step4:生成w1,w2,...,wr及其其逆元（本例中r=2）
w = create_w(m, ir)
inverse_w = create_inverse_w(m, ir, w)

# step5:恢复秘密
z = recover(yr, m, ir, w, inverse_w)
recover_x = z % m[0]
print("原来的明文为:")
print(X)
print("最后恢复的明文为:")
print(recover_x)

# 输出相关参数
print("p,m1,m2,....mn分别为:")
for i in range(len(m)):
    print(m[i])

print("秘密X为：")
print(X)
print("A为：")
print(A)
print("Y为：")
print(Y)
print("M为：")
print(M)
print("y1,y2,...yn分别为:")
for i in range(1, len(yn)):
    print(yn[i])

print("选择的yi1,yi2,..yir为：")
for i in range(1, len(yr)):
    print(yr[i])

print("选择的w1,w2,..wr-1为：")
for i in range(1, len(w)):
    print(w[i])
print("选择的w1,w2,..wr-1的逆为：")
for i in range(1, len(inverse_w)):
    print(inverse_w[i])