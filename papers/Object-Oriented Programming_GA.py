# def create_bin():
#     bin_dict = {'0': ['00', '000'], '1': ['01', 'None'], '2': ['10', '010'],
#                 '3': ['11', '011'], '4': ['None', '100'], '5': ['None', '101'], '7': ['None', '111']}
#     bin_list = []
#     for i in range(5):
#         gate_bin = bin_dict[str(np.random.randint(0, 4))][0]
#         ctrl_str = str(np.random.randint(0, 8))
#         while ctrl_str == '1' or ctrl_str == '6':
#             ctrl_str = str(np.random.randint(0, 8))
#         ctrl_bin = bin_dict[ctrl_str][1]
#         bin_list.append(gate_bin + ctrl_bin)
#     return bin_list
#
#
# def bin2code(group):
#     # In genetic algorithm, it is important to use Gary code to reduce the variance of every change made.
#     # The relationship is as follows.
#     # use five
#     ctrl_dict = {'000': [1, 2], '010': [2, 1], '011': [2, 3], '111': [3, 2], '101': [3, 1], '100': [1, 3]}
#     group_code =
#     for member in group:
#         code = []
#         for bin in member:
#             gate_index = int(bin[0:2], 2) + 1
#             ctrl_index = ctrl_dict[bin[2:5]]
#             code.append([gate_index] + ctrl_index)
#
#
# # print(bin2code(create_bin()))
#
#
# # define a function that calculate the prob of the member being selected:
# def fid_prob(group):
#     m_fid = []  # Stories the fidelity of the member in group
#     for g in group:
#         m_fid.append(fid(uni_matrix(g), tof))
#     sum_fid = sum(m_fid)
#     m_prob = [0]
#     for m in range(len(m_fid)):
#         m_prob.append(m_fid[m] / sum_fid + m_prob[m - 1])
#     rand_number = np.random.uniform(0, 1)
#     for i in range(0, len(m_prob) - 1):
#         if rand_number >= m_prob[i] and rand_number <= m_prob[i + 1]:
#             break
#     return i
#
#
# # print(fid_prob(member_fidelity))
#
# def var(new_group, m):
#     # create new gate
#     a = np.random.randint(1, 5)
#     b = np.random.randint(1, 4)
#     c = b
#     while c == b:
#         c = np.random.randint(1, 4)
#     # replacing gate:
#     rand_gate_index = np.random.randint(0, 5)
#     ind = len(new_group[rand_gate_index])
#     rand_index2 = np.random.randint(0, 3)  # the position of the variation in the gate
#     new_group[m][rand_gate_index][0:int(ind) - 1] = [a, b, c]
#     # if rand_index2 == 0:
#     #     new_group[m][i][0] = np.random.randint(1, 5)
#     # elif rand_index2 == 1:
#     #     trg_index = new_group[m][i][2]
#     #     while trg_index == new_group[m][i][2]:
#     #         trg_index = np.random.randint(1, 3)
#     #     new_group[m][i][1] = trg_index
#     # elif rand_index2 == 2:
#     #     trg_index = new_group[m][i][1]
#     #     while trg_index == new_group[m][i][1]:
#     #         trg_index = np.random.randint(1, 3)
#     #     new_group[m][i][2] = trg_index
#     return new_group
#
#
# def cross_select(member_number):
#     # Assume the number of the members in a group is even.
#     CrossPair_list = []
#     for i in range(len(member_number)):
#         CrossPair_list.append(np.random.randint(0, len(member_number) - 1))
#     return CrossPair_list
#
#
# # Main:
# # Initial the group
#
# group_bin = ()
# m_num = 10
# for i in range(m_num):
#     tof_list = []  # 用列表存储数据,数据为2进制字符串
#     new_member = create_bin()
#     group_bin = group_bin + (new_member,)
#
# print(group_bin)
#
# FID_iter = []
# stop_index = 0
# iters = 0
# while iters <= 1000 and stop_index == 0:
#     iters = iters + 1
#     new_group = ()
#     # Select New Generation
#     for m1 in range(m_num):
#         rand_index = fid_prob(group)
#         new_group = new_group + (group[rand_index],)
#
#     # Cross according the order that they are selected:
#     pair_num = m_num / 2
#     for m2 in range(int(pair_num)):
#         exchange_index = np.random.randint(0, 5)
#         exchange_temp = new_group[2 * m2][
#                         0:exchange_index]  # Only exchange the first number of the list ----- exchange the gate
#         new_group[2 * m2][0:exchange_index] = new_group[2 * m2 + 1][0:exchange_index]
#         new_group[2 * m2 + 1][0:exchange_index] = exchange_temp
#         # Variation:
#         new_group = var(new_group, 2 * m2)
#         new_group = var(new_group, 2 * m2 + 1)
#     group = new_group
#     del new_group
#
#     m_fid = []
#     for m in group:
#         m_fid.append(fid(uni_matrix(m), tof))
#     FID_iter.append(max(m_fid))
# print(group)
# print(FID_iter)
# print(max(FID_iter))


import numpy as np
import torch

class Group:
    def __init__(self, group_bin, group_code, group_num, group_fid):
        self.bin = group_bin
        self.code = group_code
        self.num = group_num
        self.fid = group_fid
        bin_dict = {'0': ['00', '000'], '1': ['01', 'None'], '2': ['10', '010'],
                    '3': ['11', '011'], '4': ['None', '100'], '5': ['None', '101'], '7': ['None', '111']}

        for m in range(self.num):
            bin_list = []
            for i in range(5):
                gate_bin = bin_dict[str(np.random.randint(0, 4))][0]
                ctrl_str = str(np.random.randint(0, 8))
                while ctrl_str == '1' or ctrl_str == '6':
                    ctrl_str = str(np.random.randint(0, 8))
                ctrl_bin = bin_dict[ctrl_str][1]
                bin_list.append(gate_bin + ctrl_bin)
            self.bin = self.bin + (bin_list,)

    def refresh_code(self):
        self.code = []
        # In genetic algorithm, it is important to use Gary code to reduce the variance of every change made.
        # The relationship is as follows.
        # use five
        ctrl_dict = {'000': [1, 2], '010': [2, 1], '011': [2, 3], '111': [3, 2], '101': [3, 1], '100': [1, 3]}
        for member in self.bin:
            code = []
            for bin in member:
                gate_index = int(bin[0:2], 2) + 1
                ctrl_index = ctrl_dict[bin[2:5]]
                code.append([gate_index] + ctrl_index)
            self.code.append(code)

    def refresh_fid(self):
        self.fid = []

        # define kronecker operation
        def kron(a, b):
            a = a.numpy()
            b = b.numpy()
            ans = torch.from_numpy(np.kron(a, b))
            return (ans)

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

        def decode(code_list, gate, gate_index):
            a = code_list[0] - 1
            index = gate_index[a]
            if code_list[1] == 3:
                if code_list[2] == 1:
                    decode_result = np.kron(np.kron(gate['P0'], gate['I']), gate['I']) + np.kron(
                        np.kron(gate['P1'], gate['I']), gate[index])
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
                    decode_result = np.kron(np.kron(gate['I'], gate['I']), gate['P0']) + np.kron(
                        np.kron(gate[index], gate['I']), gate['P1'])
                else:
                    print('Index Error!')
            else:
                print('Index Error!')
            return decode_result

        # define Hermite operation
        def H(x):
            x1 = x.T
            x2 = np.conjugate(x1)
            return x2

        def fid(Ua, Ut):
            F = np.abs(np.trace(np.dot(Ua, H(Ut)))) / (pow(2, 3))
            return F

        tof = np.array([[1, 0, 0, 0, 0, 0, 0, 0],
                        [0, 1, 0, 0, 0, 0, 0, 0],
                        [0, 0, 1, 0, 0, 0, 0, 0],
                        [0, 0, 0, 1, 0, 0, 0, 0],
                        [0, 0, 0, 0, 1, 0, 0, 0],
                        [0, 0, 0, 0, 0, 1, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 1],
                        [0, 0, 0, 0, 0, 0, 1, 0]])
        # ======================================================================================================================
        # gate database
        I = np.array([[1, 0], [0, 1]])
        X = np.array([[0, 1], [1, 0]])
        Y = np.array([[0, -1j], [1j, 0]])
        Z = np.array([[1, 0], [0, -1]])
        V = np.array([[(1 + 1j) / 2, (1 - 1j) / 2], [(1 - 1j) / 2, (1 + 1j) / 2]])
        V_dug = np.array([[(1 - 1j) / 2, (1 + 1j) / 2], [(1 + 1j) / 2, (1 - 1j) / 2]])
        S = np.array([[1, 0], [0, 1j]])
        T = np.array([[1, 0], [0, np.exp(1j * np.pi / 4)]])
        P0 = np.array([[1, 0], [0, 0]])
        P1 = np.array([[0, 0], [0, 1]])
        H = np.sqrt(0.5) * (np.array([[1, 1], [1, -1]]))
        for c in self.code:
            self.fid.append(fid(decode(c, gate={'I': I, 'X': X, 'Y': Y, 'Z': Z, 'T': T, 'V': V, 'V_dug': V_dug, 'S': S, 'P0': P0, 'P1': P1, 'H': H}
                                       , gate_index=['V', 'Z', 'S', 'V_dug']), tof))


    def next_generation(self):
        # first define the probability of a member being selected
        # define a function that calculate the prob of the member being selected:
        # Stories the fidelity of the member in group
        def fid_prob(group):
            m_fid = self.fid
            sum_fid = sum(m_fid)
            m_prob = [0]
            for m in range(len(m_fid)):
                m_prob.append(m_fid[m] / sum_fid + m_prob[m - 1])
            rand_number = np.random.uniform(0, 1)
            for i in range(0, len(m_prob) - 1):
                if rand_number >= m_prob[i] and rand_number <= m_prob[i + 1]:
                    break
            return i

        new_group_bin = ()
        for b in self.bin:
            new_group_bin = new_group_bin + self.bin[fid_prob(self.code)]
        self.bin = new_group_bin

    def cross(self):


        # def var(new_group, m):
        #     # create new gate
        #     a = np.random.randint(1, 5)
        #     b = np.random.randint(1, 4)
        #     c = b
        #     while c == b:
        #         c = np.random.randint(1, 4)
        #     # replacing gate:
        #     rand_gate_index = np.random.randint(0, 5)
        #     ind = len(new_group[rand_gate_index])
        #     rand_index2 = np.random.randint(0, 3)  # the position of the variation in the gate
        #     new_group[m][rand_gate_index][0:int(ind) - 1] = [a, b, c]
        #     # if rand_index2 == 0:
        #     #     new_group[m][i][0] = np.random.randint(1, 5)
        #     # elif rand_index2 == 1:
        #     #     trg_index = new_group[m][i][2]
        #     #     while trg_index == new_group[m][i][2]:
        #     #         trg_index = np.random.randint(1, 3)
        #     #     new_group[m][i][1] = trg_index
        #     # elif rand_index2 == 2:
        #     #     trg_index = new_group[m][i][1]
        #     #     while trg_index == new_group[m][i][1]:
        #     #         trg_index = np.random.randint(1, 3)
        #     #     new_group[m][i][2] = trg_index
        #     return new_group
        #
        # # Cross according the order that they are selected:
        # m_num = len(self.bin)
        # pair_num = m_num / 2
        # for m2 in range(int(pair_num)):
        #     exchange_index = np.random.randint(0, 5)
        #     exchange_temp = new_group[2 * m2][
        #                     0:exchange_index]  # Only exchange the first number of the list ----- exchange the gate
        #     new_group[2 * m2][0:exchange_index] = new_group[2 * m2 + 1][0:exchange_index]
        #     new_group[2 * m2 + 1][0:exchange_index] = exchange_temp
        #     # Variation:
        #     new_group = var(new_group, 2 * m2)
        #     new_group = var(new_group, 2 * m2 + 1)
        # group = new_group
        # del new_group




grp = Group((), [], 5, [])
grp.refresh_code()
print(grp.bin)