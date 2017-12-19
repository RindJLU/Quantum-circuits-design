# coding: utf-8
# quantum circuits design
# step1: store quantum gates

import numpy as np
import torch
import matplotlib.pyplot as plt

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

# define kronecker operation
def kron(a, b):
    a = a.numpy()
    b = b.numpy()
    ans = torch.from_numpy(np.kron(a, b))
    return(ans)

# controled gate, which returns the matrix of the gate in its subspace
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


# tof1 = np.kron(gate['I'], controled_gate(gate['V'], 0, gate))
# tof2 = np.kron(np.kron(gate['P0'], gate['I']), gate['I']) + np.kron(np.kron(gate['P1'], gate['I']), gate['Z'])
# tof3 = np.kron(controled_gate(gate['S'], 0, gate), gate['I'])
# tof4 = np.kron(gate['I'], controled_gate(gate['V_dug'], 0, gate))
# tof5 = np.kron(np.kron(gate['I'], gate['I']), gate['P0']) + np.kron(np.kron(gate['Z'], gate['I']), gate['P1'])
# tup = (tof1, tof2, tof3, tof4, tof5)

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
            decode_result = np.kron(gate['I'], controled_gate(gate[index], 1, gate))
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
# define loss function

# define Hermite operation
def H(x):
    x1 = x.T
    x2 = np.conjugate(x1)
    return x2
# print(H(np.array([[1,2+1j],[3,4+5j]])))

# define loss function, the less the better.
def loss_fun(Ua, Ut):
    F = np.abs(np.trace(np.dot(Ua, H(Ut))))/(pow(2, 3))
    fidelity_error = 1 - pow(F, 2)
    return fidelity_error

# define the fidelity of quantum circuits, the bigger the better.
def fid(Ua, Ut):
    F = np.abs(np.trace(np.dot(Ua, H(Ut)))) / (pow(2, 3))
    return F
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
# Main
# print('=====================================================================')
# print('Please select a model: 1. Simulated Annealing(Press 1) 2. Geneatic Model()')
# -------------------------------------------------------------------------------------------------------------------
# Model one: Simulated Annealing
# tof_list = [] # 用列表存储数据
# for i in range(5):
#     tof_list.append(rand_generator())
# err = []
# T = 100
# alpha = 0.999
# T_min = pow(10, -3)
# iter_index = 0
# while T > T_min:
#     iter_index += 1
#     error = loss_fun(uni_matrix(tof_list), tof)
#     target_index = np.random.randint(0, 5)
#     target_list_temp = tof_list[target_index]
#     tof_list[target_index] = rand_generator()
#     error_temp = loss_fun(uni_matrix(tof_list), tof)
#     if error_temp < error:
#         pass
#     else:
#         if np.exp(-0.5*(error_temp - error)/T) > np.random.rand(1):
#             pass
#         else:
#             tof_list[target_index] = target_list_temp
#     T *= alpha
#     if iter_index % 10 == 0:
#         err.append([iter_index, error])
# print(uni_matrix(tof_list))
# print(tof_list)
# # 可视化
# import matplotlib.pyplot as plt
# err = np.array(err)
# plt.plot(err[:, 0], err[:, 1])
# plt.show()
# 第一次运行： 10000步
# [[1, 3, 2], [2, 3, 1], [3, 2, 1], [4, 3, 2], [2, 1, 3]] 标准Toffoli门
# [[2, 1, 3], [4, 3, 2], [2, 1, 3], [1, 3, 2], [3, 2, 1]]
# [[1, 3, 1], [2, 3, 2], [4, 3, 1], [3, 2, 1], [2, 3, 2]]
# [[3, 2, 1], [2, 3, 1], [4, 3, 2], [2, 1, 3], [1, 3, 2]]
# [[1, 3, 2], [2, 1, 3], [4, 3, 2], [2, 1, 3], [3, 2, 1]]
# print(uni_matrix([[4, 3, 2], [4, 3, 1], [2, 3, 1], [3, 1, 3], [3, 1, 3]]))
# ----------------------------------------------------------------------------------------------------------------------
# Main----Genetic Algorithm---------------------------------------------------------------------------------------------

def create_bin():
    bin_dict = {'0': ['00', '000'], '1': ['01', 'None'],  '2': ['10', '010'],
                '3': ['11', '011'], '4': ['None', '100'], '5': ['None', '101'], '7': ['None', '111']}
    bin_list = []
    for i in range(5):
        gate_bin = bin_dict[str(np.random.randint(0, 4))][0]
        ctrl_str = str(np.random.randint(0, 8))
        while ctrl_str == '1' or ctrl_str == '6':
            ctrl_str = str(np.random.randint(0, 8))
        ctrl_bin = bin_dict[ctrl_str][1]
        bin_list.append(gate_bin + ctrl_bin)
    return bin_list

def bin2code(group):
    # In genetic algorithm, it is important to use Gary code to reduce the variance of every change made.
    # The relationship is as follows.
    # use five
    ctrl_dict = {'000': [1, 2], '010': [2, 1], '011': [2, 3], '111': [3, 2], '101': [3, 1], '100': [1, 3]}
    group_code =
    for member in group:
        code = []
        for bin in member:
            gate_index = int(bin[0:2], 2) + 1
            ctrl_index = ctrl_dict[bin[2:5]]
            code.append([gate_index] + ctrl_index)

# print(bin2code(create_bin()))


# define a function that calculate the prob of the member being selected:
def fid_prob(group):
    m_fid = [] # Stories the fidelity of the member in group
    for g in group:
        m_fid.append(fid(uni_matrix(g), tof))
    sum_fid = sum(m_fid)
    m_prob = [0]
    for m in range(len(m_fid)):
        m_prob.append(m_fid[m]/sum_fid + m_prob[m-1])
    rand_number = np.random.uniform(0, 1)
    for i in range(0, len(m_prob)-1):
        if rand_number >= m_prob[i] and rand_number <= m_prob[i+1]:
            break
    return i
# print(fid_prob(member_fidelity))

def var(new_group, m):
    # create new gate
    a = np.random.randint(1, 5)
    b = np.random.randint(1, 4)
    c = b
    while c == b:
        c = np.random.randint(1, 4)
    # replacing gate:
    rand_gate_index = np.random.randint(0, 5)
    ind = len(new_group[rand_gate_index])
    rand_index2 = np.random.randint(0, 3)  # the position of the variation in the gate
    new_group[m][rand_gate_index][0:int(ind)-1] = [a, b, c]
    # if rand_index2 == 0:
    #     new_group[m][i][0] = np.random.randint(1, 5)
    # elif rand_index2 == 1:
    #     trg_index = new_group[m][i][2]
    #     while trg_index == new_group[m][i][2]:
    #         trg_index = np.random.randint(1, 3)
    #     new_group[m][i][1] = trg_index
    # elif rand_index2 == 2:
    #     trg_index = new_group[m][i][1]
    #     while trg_index == new_group[m][i][1]:
    #         trg_index = np.random.randint(1, 3)
    #     new_group[m][i][2] = trg_index
    return new_group

def cross_select(member_number):
    # Assume the number of the members in a group is even.
    CrossPair_list = []
    for i in range(len(member_number)):
        CrossPair_list.append(np.random.randint(0, len(member_number)-1))
    return CrossPair_list


# Main:
# Initial the group

group_bin = ()
m_num = 10
for i in range(m_num):
    tof_list = []  # 用列表存储数据,数据为2进制字符串
    new_member = create_bin()
    group_bin = group_bin + (new_member,)

print(group_bin)



FID_iter = []
stop_index = 0
iters = 0
while iters <= 1000 and stop_index == 0:
    iters = iters + 1
    new_group = ()
    # Select New Generation
    for m1 in range(m_num):
        rand_index = fid_prob(group)
        new_group = new_group + (group[rand_index],)

    # Cross according the order that they are selected:
    pair_num = m_num/2
    for m2 in range(int(pair_num)):
        exchange_index = np.random.randint(0, 5)
        exchange_temp = new_group[2*m2][0:exchange_index] # Only exchange the first number of the list ----- exchange the gate
        new_group[2*m2][0:exchange_index] = new_group[2*m2+1][0:exchange_index]
        new_group[2*m2+1][0:exchange_index] = exchange_temp
        # Variation:
        new_group = var(new_group, 2*m2)
        new_group = var(new_group, 2*m2+1)
    group = new_group
    del new_group

    m_fid = []
    for m in group:
        m_fid.append(fid(uni_matrix(m), tof))
    FID_iter.append(max(m_fid))
print(group)
print(FID_iter)
print(max(FID_iter))

# ======================================================================================================================
# GLOA

# gate_index = ['V', 'Z', 'S', 'V_dug']
# initial the circuits: eight gates in a circuits, include 2 single qubit gate
# def inital_circuits(n):
#     circuits_list = []
#     for i in range(n):
#         gate_index = np.random.randint(1, 5)
#         gate_tar = np.random.randint(1, 4) # refers to the target index of a controlled gate
#         gate_ctrl = gate_tar
#         while gate_ctrl == gate_tar:
#             gate_ctrl = np.random.randint(1, 4)
#         circuits_list.append([gate_index, gate_tar, gate_ctrl])
#     return(circuits_list)
#
# def exc(Group, g1, g2, m):
#     for i in range(len(Group[g1][m])): # exchange the mth member in group1 and group2
#         temp = Group[g1][m][i]
#         Group[g1][m][i] = Group[g2][m][i]
#         Group[g2][m][i] = temp
#     return Group
#
# def fid_sort(vec): # vec contains the fid a member of a group;
#     vec = np.array(vec)
#     index_list = np.argsort(vec) # this gives the index of member in a group accroding to the fideility.
#     return index_list
#
# def Group_del(Group):
#     Group_del = () # contains member index, the first one is the leader of the group.
#     NewGroup = ()
#     for group in Group:
#         mem_sorted = ()
#         mem_fid_sorted = []
#         mem_fid = []
#         for mem in group:
#             mem_fid.append(loss_fun(uni_matrix(mem), tof))
#         fid_list = fid_sort(mem_fid)
#         for i in range(len(fid_list)):
#             mem_sorted = mem_sorted + (group[fid_list[i]],)
#             mem_fid_sorted.append(mem_fid[fid_list[i]])
#         NewGroup = NewGroup + (mem_sorted,)
#         Group_del = Group_del + (mem_fid_sorted,)
#     return NewGroup, Group_del
# # print(Group_del(Group))
#
# # Main:
# # define 25 groups with 15 population in each group.
# Group = ()
# for group_index in range(6):
#     single_group = ()
#     for i in range(6):
#         single_group = single_group + (inital_circuits(5),)
#     Group = Group + (single_group,)
# # print(Group)
#
# min_fed = [1]
# iter = 0
# stop_index = 1
# while stop_index == 1 and iter <= 1000:
#     Group, Group_fed = Group_del(Group)
#     # first check the group, is there any member in the group reaches minimize loss.
#     fid = []
#     for g in range(len(Group)):
#         for m in range(len(Group[g])):
#             if Group_fed[g][m] <= 0.00001:
#                 print('Find a solution!')
#                 print(Group[g][m])
#                 stop_index = 0
#             else:
#                 fid.append(min(Group_fed[g]))
#     min_fed.append(min(fid))
#
#     for grp in Group:
#         for num in range(len(Group[0])-1):
#             mem_index = num + 1
#             mem_temp = grp[mem_index] # store the old member
#             # create new member
#             leader_part_index = np.random.randint(0, 5)
#             # choose one gate to be changed, simply replace it by the
#             # corresponding part in the leader to it.
#             grp[mem_index][leader_part_index] = grp[0][leader_part_index]
#             # randomly choose one gate to be a new gate
#             new_gate_index = np.random.randint(0, 5)
#             grp[mem_index][new_gate_index] = inital_circuits(1)[0]
#
#             # check
#             if loss_fun(uni_matrix(grp[mem_index]), tof) >= loss_fun(uni_matrix(mem_temp), tof):
#                 for i in range(len(mem_temp)):
#                     grp[mem_index][i] = mem_temp[i]
#     # cross different groups, also follows the replacement criteria???
#     # Here I only exchange the last two member
#     if iter % 20 == 0:
#         a = [0, 1, 2, 3, 4, 5]
#         np.random.shuffle(a) # disorder the list, and exchange every pair.
#         for i in range(int(len(a)/2)):
#             for j in range(2):
#                 changed_mem_index = np.random.randint(1, 5)
#                 Group = exc(Group, a[2 * i], a[2 * i + 1], changed_mem_index)
#
# # Visualization
# plt.plot(min_fed)
# plt.title('Fidelity Error vs. Number of Iterations')
# plt.xlabel('Number of Iterations')
# plt.ylabel('Fidelity Error')
# print(Group_fed)
# plt.show()

# Solutions found:
# [[2, 3, 1], [4, 3, 2], [2, 3, 1], [3, 2, 1], [1, 3, 2]]
# [[2, 3, 1], [4, 3, 2], [2, 3, 1], [1, 3, 2], [3, 2, 1]]
# [[3, 2, 1], [1, 3, 2], [2, 1, 3], [4, 3, 2], [2, 3, 1]]
# [[2, 3, 2], [4, 3, 1], [3, 2, 1], [2, 3, 2], [1, 3, 1]]
# [[2, 1, 3], [4, 3, 2], [2, 1, 3], [3, 2, 1], [1, 3, 2]]
# [[3, 2, 1], [2, 1, 3], [4, 3, 2], [2, 1, 3], [1, 3, 2]]
# [[3, 2, 1], [1, 3, 2], [2, 3, 1], [4, 3, 2], [2, 1, 3]]
# [[3, 2, 1], [2, 3, 2], [4, 3, 1], [2, 3, 2], [1, 3, 1]]
# [[2, 1, 3], [4, 3, 2], [2, 3, 1], [1, 3, 2], [3, 2, 1]]
