# coding: utf-8
# quantum circuits design
# step1: store quantum gates
# 1. 张量积操作
import numpy as np
import torch

def kron(a, b):
    a = a.numpy()
    b = b.numpy()
    ans = torch.from_numpy(np.kron(a, b))
    return(ans)
# ======================================================================================================================
# gate database 
I = np.array([[1, 0], [0, 1]])
X = np.array([[0, 1], [1, 0]])
Y = np.array([[0, -1j], [1j, 0]])
Z = np.array([[1, 0], [0, -1]])
V = np.array([[(1 + 1j)/2, (1 - 1j)/2], [(1 - 1j)/2, (1 + 1j)/2]])
V_dug = np.array([[(1 - 1j)/2, (1 + 1j)/2], [(1 + 1j)/2, (1 - 1j)/2]])
S = np.array([[1, 0], [0, 1j]])
T = np.array([[1, 0], [0, np.exp(1j*np.pi/4)]])
P0 = np.array([[1, 0], [0, 0]])
P1 = np.array([[0, 0], [0, 1]])
H = np.sqrt(0.5)*(np.array([[1, 1], [1, -1]]))
gate = {'I': I, 'X': X, 'Y': Y, 'Z': Z, 'T': T, 'V': V, 'V_dug': V_dug, 'S': S, 'P0': P0, 'P1': P1, 'H': H}
# ======================================================================================================================
# 定义受控gate
def controled_gate(x, m, gate):
    # x is a unitary gate defined in gate
    # m is the index of the controled gate: if 0: control the latter one; if 1, control the first one.
    if m == 0:
        ans = np.kron(gate['P0'], gate['I']) + np.kron(gate['P1'], x)
    elif m == 1:
        ans = np.kron(gate['P1'], gate['I']) + np.kron(gate['P0'], x)
    else:
        print('Error, m can only be 0 or 1!')
    return ans
# test
# ans = controled_gate(gate['X'], 1, gate)
# print(ans)
# [[0 1 0 0]
# [1 0 0 0]
# [0 0 1 0]
# [0 0 0 1]]

# test controled_x gate (type C)

# a = np.kron(gate['H'], gate['H'])
# b = controled_gate(gate['X'], 0, gate)
# c = np.kron(gate['H'], gate['H'])
# res1 = np.dot(b, a)
# res = np.dot(c, res1)
# print(res)


tof1 = np.kron(gate['I'], controled_gate(gate['V'], 0, gate))
tof2 = np.kron(np.kron(gate['P0'], gate['I']), gate['I']) + np.kron(np.kron(gate['P1'], gate['I']), gate['Z'])
tof3 = np.kron(controled_gate(gate['S'], 0, gate), gate['I'])
tof4 = np.kron(gate['I'], controled_gate(gate['V_dug'], 0, gate))
tof5 = np.kron(np.kron(gate['I'], gate['I']), gate['P0']) + np.kron(np.kron(gate['Z'], gate['I']), gate['P1'])
tup = (tof1, tof2, tof3, tof4, tof5)

# ans = np.eye(8)
# for i in tup: # 此处用tuple存储数据
#     ans = np.dot(ans, i)
# # print(ans)

# 关于tuple，增加元素： tup = tup + (XXXX, )
# ======================================================================================================================
# 编码和解码

# 编码：
# 用一个list表示一个操作； list有3个元素， 第一个元素表示2bit门操作。 第二和第三个元素表示受控bit和控制bit
gate_index = ['V', 'Z', 'S', 'V_dug']
# 解码：
def decode(code_list, gate, gate_index):
    a = code_list[0]-1
    index = gate_index[a]
    if code_list[1] == 3:
        if code_list[2] == 1:
            decode_result = np.kron(np.kron(gate['P0'], gate['I']), gate['I']) + np.kron(np.kron(gate['P1'], gate['I']), gate[index])
        elif code_list[2] == 2:
            decode_result = np.kron(gate['I'], controled_gate(gate[index], 0, gate))
        else:
            print('Index Error!')
    elif code_list[1] == 2:
        if code_list[2] == 1:
            decode_result = np.kron(controled_gate(gate[index], 0, gate), gate['I'])
        elif code_list[2] == 3:
            decode_result = np.kron(gate['I'], controled_gate(gate['S'], 1, gate))
        else:
            print('Index Error!')
    elif code_list[1] == 1:
        if code_list[2] == 2:
            decode_result = np.kron(controled_gate(gate[index], 1, gate), gate['I'])
        elif code_list[2] == 3:
            decode_result = np.kron(np.kron(gate['I'], gate['I']), gate['P0']) + np.kron(np.kron(gate[index], gate['I']), gate['P1'])
        else:
            print('Index Error!')
    else:
        print('Index Error!')
    return decode_result

# test
toffoli_list = ([1, 3, 2], [2, 3, 1], [3, 2, 1], [4, 3, 2], [2, 1, 3])
tof = np.eye(8)
for i in toffoli_list:
    tof = np.dot(tof, decode(i, gate, gate_index))
# print(tof_test)

# ======================================================================================================================
# 定义loss function

# 先定义共轭转置
def H(x):
    x1 = x.T
    x2 = np.conjugate(x1)
    return x2
# print(H(np.array([[1,2+1j],[3,4+5j]])))

def loss_fun(Ua, Ut):
    F = np.abs(np.trace(np.dot(Ua, H(Ut))))/(pow(2, 3))
    fidelity_error = 1 - pow(F, 2)
    return fidelity_error
# test
# print(loss_fun(tof_test, tof_test))
# ======================================================================================================================
# 定义优化方案：
# 1. Toffoli gate 设计：
def rand_generator():
    a = np.random.randint(1, 5)
    b = np.random.randint(1, 4)
    c = b
    while c == b:
        c = np.random.randint(1, 4)
    return([a, b, c])

def uni_matrix(tof_list):
    tof_test = np.eye(8)
    for j in tof_list:
        tof_test = np.dot(tof_test, decode(j, gate, gate_index))
    return tof_test
# test
# print(rand_generator())

# ======================================================================================================================
# 主程序
# 退火-------------------------------------------------------------------------------------------------------------------
tof_list = [] # 用列表存储数据
for i in range(5):
    tof_list.append(rand_generator())
err = []
T = 100
alpha = 0.999
T_min = pow(10, -3)
iter_index = 0
while T > T_min:
    iter_index += 1
    error = loss_fun(uni_matrix(tof_list), tof)
    target_index = np.random.randint(0, 5)
    target_list_temp = tof_list[target_index]
    tof_list[target_index] = rand_generator()
    error_temp = loss_fun(uni_matrix(tof_list), tof)
    if error_temp < error:
        pass
    else:
        if np.exp(-0.5*(error_temp - error)/T) > np.random.rand(1):
            pass
        else:
            tof_list[target_index] = target_list_temp
    T *= alpha
    if iter_index % 10 == 0:
        err.append([iter_index, error])
print(uni_matrix(tof_list))
print(tof_list)
# 可视化
import matplotlib.pyplot as plt
err = np.array(err)
plt.plot(err[:, 0], err[:, 1])
plt.show()
# 第一次运行： 10000步
# [[1, 3, 2], [2, 3, 1], [3, 2, 1], [4, 3, 2], [2, 1, 3]] 标准Toffoli门
# [[2, 1, 3], [4, 3, 2], [2, 1, 3], [1, 3, 2], [3, 2, 1]]
# [[1, 3, 1], [2, 3, 2], [4, 3, 1], [3, 2, 1], [2, 3, 2]]
# [[3, 2, 1], [2, 3, 1], [4, 3, 2], [2, 1, 3], [1, 3, 2]]
# print(uni_matrix([[4, 3, 2], [4, 3, 1], [2, 3, 1], [3, 1, 3], [3, 1, 3]]))
# ----------------------------------------------------------------------------------------------------------------------
# machine learning method-----------------------------------------------------------------------------------------------
