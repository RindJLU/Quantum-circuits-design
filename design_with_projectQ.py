# coding: utf-8
import numpy as np
import copy
import projectq
from projectq.ops import X, T, S, H, Rz, Rx, Measure, All
from projectq import MainEngine
from projectq.meta import Control


# ======================================================================================================================
# define truth table
# qubits_in = []
# for i in range(8):
#     a = i//4
#     b = (i-a*4)//2
#     c = (i-a*4-b*2)//1
#     qubits_in.append([a, b, c])
#
# tof_out = copy.deepcopy(qubits_in[0:6])
# tof_out.append(qubits_in[7])
# tof_out.append(qubits_in[6])
#
# tof_truth_list = (qubits_in, tof_out)
# print()
#
# # ======================================================================================================================
# #
# # define gates:
# I0 = Rz(0)
# gate = (T, X, S, H)
# def control(ctrl_list, q, eng):
#     Gate = gate[ctrl_list[0]-1]
#     q_trg = q[ctrl_list[1]-1]
#     q_ctrl = q[ctrl_list[2]-1]
#     with Control(eng, q_ctrl):
#         Gate | q_trg
#     return q
#
#
# def rand_generator():
#     tof_list = []  # 用列表存储数据
#     for i in range(5):
#         a = np.random.randint(1, 4)
#         b = np.random.randint(1, 3)
#         c = b
#         while c == b:
#             c = np.random.randint(1, 3)
#         tof_list.append([a, b, c])
#     return(tof_list)
# # print(rand_generator())
#
#
# def run(MainEngine, X, tof_test):
#     qubit_out_bit = []
#     for k in qubits_in:
#         state = []
#         eng = MainEngine()
#         qubit0, qubit1, qubit2 = eng.allocate_qureg(3)
#         q = (qubit0, qubit1, qubit2)
#         for m in k:
#             if m == 1:
#                 X | q[m]
#         for i in tof_test:
#             control(i, q, eng)
#         eng.flush()
#         mapping, wavefunction = copy.deepcopy(eng.backend.cheat())
#
#         state.append(mapping[qubit0[0].id])
#         b = mapping[qubit1.id]
#         c = mapping[qubit2.id]
#         qubit_out_bit.append(state)
#     return(qubit_out_bit)
# #
# # # define loss function: Mean Square
# # def loss_fun(output):
# #     loss = 0
# #     for i in range(len(ans)):
# #         for j in range(len(ans[i])):
# #             loss += abs(ans[i][j]-output[i][j])
# #     return loss
#
#
# tof_test = rand_generator()
# ans = run(MainEngine, X, tof_test)
# print('This is the input qubits states: {}'.format(qubits_in))
# print('This is the output qubits states:'.format(ans))





eng = projectq.MainEngine()
qubit1 = eng.allocate_qubit()
qubit2 = eng.allocate_qubit()
Rx(0.2) | qubit1
Rx(0.4) | qubit2
eng.flush() # In order to have all the above gates sent to the simulator and executed

# We save a copy of the wavefunction at this point in the algorithm. In order to make sure we get a copy
# also if the Python simulator is used, one should make a deepcopy:
mapping, wavefunction = copy.deepcopy(eng.backend.cheat())

print("The full wavefunction is: {}".format(wavefunction))
# Note: qubit1 is a qureg of length 1, i.e. a list containing one qubit objects, therefore the
#       unique qubit id can be accessed via qubit1[0].id
print("qubit1 has bit-location {}".format(mapping[qubit1[0].id]))
print("qubit2 has bit-location {}".format(mapping[qubit2[0].id]))

# Suppose we want to know the amplitude of the qubit1 in state 0 and qubit2 in state 1:
state = 0 + (1 << mapping[qubit2[0].id])
print("Amplitude of state qubit1 in state 0 and qubit2 in state 1: {}".format(wavefunction[state]))
# If one only wants to access one (or a few) amplitudes, get_amplitude provides an easier interface:
amplitude  = eng.backend.get_amplitude('01', qubit1 + qubit2)
print("Accessing same amplitude but using get_amplitude instead: {}".format(amplitude))

Measure | qubit1 + qubit2 # In order to not deallocate a qubit in a superposition state
