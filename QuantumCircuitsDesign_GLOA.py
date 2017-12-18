# coding: utf-8

import numpy as np
import matplotlib.pyplot as plt

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

tof = np.array([[1, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 1, 0]])

# define rotate gates---------------------------------------------------------------------------------------------------
def Rx(theta):
    return (np.array([[np.cos(theta / 2), 1j*np.sin(theta / 2)],
                      [1j*np.sin(theta / 2), np.cos(theta / 2)]]))

def Ry(theta):
    return (np.array([[np.cos(theta / 2), np.sin(theta / 2)],
                      [-np.sin(theta / 2), np.cos(theta / 2)]]))

def Rz(theta):
    return(np.array([[1, 0],
                     [0, np.exp(1j*theta)]]))

def Rzz(theta):
    return(np.array([[np.exp(1j*theta), 0],
                     [0, np.exp(1j*theta)]]))

# define a tuple to store these gates:
rotate_gate = (Rx, Ry, Rz, Rzz, X, Y, Z, H, V, V_dug)
# ----------------------------------------------------------------------------------------------------------------------
# ======================================================================================================================
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

def decode(code_list, gate, rotate_gate):
    gate_index = code_list[0]
    theta = code_list[3]
    if code_list[1] == 3:
        if code_list[2] == 1:
            decode_result = np.kron(np.kron(gate['P0'], gate['I']), gate['I']) + np.kron(np.kron(gate['P1'], gate['I']), rotate_gate[gate_index](theta))
        elif code_list[2] == 2:
            decode_result = np.kron(gate['I'], controled_gate(rotate_gate[gate_index](theta), 0, gate))
        elif code_list[2] == 3:
            decode_result = np.kron(np.kron(gate['I'], gate['I']), rotate_gate[gate_index](theta))
        else:
            print('Index Error!')
    elif code_list[1] == 2:
        if code_list[2] == 1:
            decode_result = np.kron(controled_gate(rotate_gate[gate_index](theta), 0, gate), gate['I'])
        elif code_list[2] == 3:
            decode_result = np.kron(gate['I'], controled_gate(rotate_gate[gate_index](theta), 1, gate))
        elif code_list[2] == 2:
            decode_result = np.kron(np.kron(gate['I'], rotate_gate[gate_index](theta)), gate['I'])
        else:
            print('Index Error!')
    elif code_list[1] == 1:
        if code_list[2] == 2:
            decode_result = np.kron(controled_gate(rotate_gate[gate_index](theta), 1, gate), gate['I'])
        elif code_list[2] == 3:
            decode_result = np.kron(np.kron(gate['I'], gate['I']), gate['P0']) + np.kron(np.kron(rotate_gate[gate_index](theta), gate['I']), gate['P1'])

        elif code_list[1] == 1:
            decode_result = np.kron(np.kron(rotate_gate[gate_index](theta), gate['I']), gate['I'])
        else:
            print('Index Error!')
    else:
        print('Index Error!')
    return decode_result


def code2matrix(circuits_list, gate, rotate_gate):
    mat = np.eye(8)
    for cir_ele in circuits_list: # cir_ele refers to the element in the circuit list([x x x], [y y y]...)
        mat = np.dot(decode(cir_ele, gate, rotate_gate), mat)
    return(mat)

# define the loss function

def H(x):
    x1 = x.T
    x2 = np.conjugate(x1)
    return x2

def loss_fun(Ua, Ut):
    F = np.abs(np.trace(np.dot(Ua, H(Ut))))/(pow(2, 3))
    fidelity_error = 1 - pow(F, 2)
    return fidelity_error
#=======================================================================================================================
# main
print('==============================================')
print('Running QuantumCircuitsDesign.py:')
# initial the circuits: eight gates in a circuits, include 2 single qubit gate
def inital_circuits():
    circuits_tuple = ()
    for i in range(6):
        gate_index = np.random.randint(0, 4)
        gate_tar = np.random.randint(1, 4) # refers to the target index of a controlled gate
        gate_ctrl = np.random.randint(1, 4)
        gate_rotate_angle = np.random.uniform(0, 2*np.pi)
        circuits_tuple = circuits_tuple + ([gate_index, gate_tar, gate_ctrl, gate_rotate_angle],)
    return(circuits_tuple)

# ======================================================================================================================
# print(code2matrix(circuits_tuple, gate, rotate_gate))
# print(circuits_tuple)
# optimize the angle

# Machine learning methods

# delta_theta = 0.1
# eps = 0.00001
# loss = []
# for iter in range(1000):
#     grad = []
#     for g in circuits_tuple:
#         g[3] += eps # calculate the loss function after a small positive disturbance
#         loss_pos = loss_fun(code2matrix(circuits_tuple, gate, rotate_gate), tof)
#         g[3] += -2*eps # calculate the loss function after a small negative disturbance
#         loss_neg =loss_fun(code2matrix(circuits_tuple, gate, rotate_gate), tof)
#         g[3] += eps # reset the theta to its origin value
#         grad.append((loss_pos - loss_neg)/(2*eps))
#     for j in range(len(grad)):
#         circuits_tuple[j][3] += -delta_theta*grad[j]
#     loss_temp = loss_fun(code2matrix(circuits_tuple, gate, rotate_gate), tof)
#     loss.append(loss_temp)
#
# # print image
# plt.plot(range(len(loss)), loss)
# plt.show()
#
# print('----------------------------------------------')
# print('Circuits list:')
# print(circuits_tuple)
# print('----------------------------------------------')
#
# print('Done')
# print('==============================================')
# ======================================================================================================================

# GLOA


# define 25 groups with 15 population in each group.
Group = ()
for group_index in range(1):
    single_group = ()
    for i in range(10):
        single_group = single_group + (inital_circuits(),)
    Group = Group + (single_group,)
# print(Group)

def fid_sort(vec): # vec contains the fid a member of a group;
    vec = np.array(vec)
    index_list = np.argsort(vec) # this gives the index of member in a group accroding to the fideility.
    return index_list

def Group_information(Group):
    Group_info = () # contains member index, the first one is the leader of the group.
    for group in Group:
        mem_sorted = ()
        mem_fid_sorted = []
        mem_fid = []
        for mem in group:
            mem_fid.append(loss_fun(code2matrix(mem, gate, rotate_gate), tof))
        fid_list = fid_sort(mem_fid)
        for i in range(len(fid_list)):
            mem_sorted = mem_sorted + (group[fid_list[i]])
            mem_fid_sorted.append(mem_fid[fid_list[i]])
        group_info = (mem_sorted, mem_fid_sorted)
        Group_info = Group_info + (group_info,)
    return(Group_info)
print(Group_information(Group))

