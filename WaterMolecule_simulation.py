# coding: utf-8

import numpy as np

# define some gates:
I = np.array([[1, 0], [0, 1]])
X = np.array([[0, 1], [1, 0]])
P0 = np.array([[1, 0], [0, 0]])
P1 = np.array([[0, 0], [0, 1]])
gate = {'I': I, 'X': X, 'P0': P0, 'P1': P1}



# define the hamiltoniam of the water molecule
H_H2 = np.array([[0.264, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, -1.1607, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, -1.1607, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, -1.8305, 0, 0, 0, 0, 0, 0, 0, 0, 0.1813, 0, 0, 0],
                  [0, 0, 0, 0, -0.3613, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, -1.2462, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, -1.0649, 0, 0, -0.1813, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, -1.2525, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, -0.3613, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, -0.1813, 0, 0, -1.0649, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1.2462, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1.2525, 0, 0, 0, 0],
                  [0, 0, 0, 0.1813, 0, 0, 0, 0, 0, 0, 0, 0, -0.2545, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -0.4759, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -0.4759, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])

def Rz(theta):
    return(np.array([[1, 0],
                     [0, np.exp(1j*theta)]]))

def Rzz(theta):
    return(np.array([[np.exp(1j*theta), 0],
                     [0, np.exp(1j*theta)]]))
# print(Rz(1), Rzz(2))

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

theta = []
for i in range(14):
    theta.append(np.random.uniform(0, 2*np.pi))

def H_H2_all(theta):
    H_H2O_test = ()
    H_H2O_test = H_H2O_test+ (np.kron(np.kron(I, Rz(theta[0])), controled_gate(Rz(theta[1]), 1, gate)),)
    H_H2O_test = H_H2O_test+ (np.kron(np.kron(controled_gate(Rzz(theta[2]), 0, gate), Rz(theta[3])), Rzz(theta[4])),)
    H_H2O_test = H_H2O_test+ (np.kron(np.kron(controled_gate(Rz(theta[5]), 0, gate), I), I),)
    H_H2O_test = H_H2O_test+ (np.kron(np.kron(I, controled_gate(Rz(theta[6]), 0, gate)), I),)
    H_H2O_test = H_H2O_test+ (np.kron(np.kron(np.kron(gate['P0'], I), I), I) + np.kron(gate['P1'], np.kron(I, np.kron(I, Rz(theta[7])))),)
    H_H2O_test = H_H2O_test+ (np.kron(I, (np.kron(np.kron(gate['P0'], I), I) + np.kron(np.kron(gate['P1'], I), Rz(theta[8])))),)
    H_H2O_test = H_H2O_test+ (np.kron(np.kron(I, np.kron(Rzz(theta[9]), I)), Rz(theta[10])),)
    H_H2O_test = H_H2O_test+ (np.kron(np.kron(np.kron(Rzz(theta[11]), Rz(theta[12])), I), Rz(theta[13])),)
    return(H_H2O_test)
# print(H_H2O_test)

def H_H2_mat(theta):
    H_H2_m = np.eye(16)
    H_H2_test = H_H2_all(theta)
    for i in H_H2_test:
        H_H2_m = np.dot(H_H2_m, i)
    return(H_H2_m)
# print(H_H2O_mat(H_H2O_test))

def H(x):
    x1 = x.T
    x2 = np.conjugate(x1)
    return x2

def loss_fun(Ua, Ut):
    F = np.abs(np.trace(np.dot(Ua, H(Ut))))/(pow(2, 4))
    fidelity_error = 1 - pow(F, 2)
    return fidelity_error

# print(loss_fun(H_H2O_mat(H_H2O_test), H_H2O))


# Main
# eps = 0.0001
# delta_theta = 0.1
# loss = []
# for i in range(3000):
#     loss.append(loss_fun(H_H2_mat(theta), H_H2))
#     grad = []
#     for j in range(len(theta)):
#         theta[j] += eps
#         loss_delta_pos = loss_fun(H_H2_mat(theta), H_H2)
#         theta[j] += -2*eps
#         loss_delta_neg = loss_fun(H_H2_mat(theta), H_H2)
#         grad.append ((loss_delta_pos-loss_delta_neg)/(2*eps))
#         theta[j] += eps
#     for k in range(len(grad)):
#         theta[k] += -grad[k]*delta_theta
#     del grad
# print(theta, H_H2_mat(theta))
#
#
# import matplotlib.pyplot as plt
# plt.plot(range(len(loss)), loss)
# plt.show()


theta1 = [4.0563, 5.5655, 0.1664, 1.0825, 5.5785, 5.7717, 5.6850, 5.7165, 5.6422, 4.2983, 1.3661, 3.2498, 2.7562, 4.3102]
print(loss_fun(H_H2_mat(theta1), H_H2))