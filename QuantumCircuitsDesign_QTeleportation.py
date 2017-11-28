# coding: utf-8
import numpy as np

# define Three qubits quantum teleportation(sender part):
# QT_matrix = np.zeros([8, 8])
# for i in range(len(QT_matrix[1])):
#     if (i//2 + i%2)//2 == 0:
#         pos_index = 0
#     else:
#         pos_index = 1

I = np.array([[1, 0], [0, 1]])
X = np.array([[0, 1], [1, 0]])
P0 = np.array([[1, 0], [0, 0]])
P1 = np.array([[0, 0], [0, 1]])
gate = {'I': I, 'X': X, 'P0': P0, 'P1': P1}
# define rotate gate(y)
def Ry(theta):
    return(np.array([[np.cos(theta/2), np.sin(theta/2)], [-np.sin(theta/2), np.cos(theta/2)]]))

def H(x):
    x1 = x.T
    x2 = np.conjugate(x1)
    return x2

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

def loss_fun(Ua, Ut):
    F = np.abs(np.trace(np.dot(Ua, H(Ut))))/(pow(2, 3))
    fidelity_error = 1 - pow(F, 2)
    return fidelity_error

# def QT_gate(theta1, theta2):
#     QT_gate = np.kron((np.kron(np.kron(Ry(theta2), I), I)), np.kron((np.kron(controled_gate(X, 0, gate), I)), np.kron((np.kron(I, controled_gate(X, 0, gate))), (np.kron(I, np.kron(I, Ry(theta1)))))))
#     return(QT_gate)

def QT_gate(theta1, theta2):
    QT_gate = np.dot((np.kron(np.kron(Ry(theta2), I), I)), np.dot((np.kron(controled_gate(X, 0, gate), I)), np.dot((np.kron(I, controled_gate(X, 0, gate))), (np.kron(I, np.kron(I, Ry(theta1)))))))
    return(QT_gate)
# ----------------------------------------------------------------------------------------------------------------------
# define quantum teleportation matrix
QT3 = QT_gate(1.565, 1.565)
# print(QT3)
# Machine Learning Methods:

# Initializing theta1, theta2:
theta1 = np.random.uniform(0, 2*np.pi)
theta2 = np.random.uniform(0, 2*np.pi)


delta_theta = 0.01
eps = 0.00001
for i in range(1000):
    loss = loss_fun(QT_gate(theta1, theta2), QT3)
    grad_theta1 = (loss_fun(QT_gate(theta1+eps, theta2), QT3) - loss_fun(QT_gate(theta1-eps, theta2), QT3))/(2*eps)
    grad_theta2 = (loss_fun(QT_gate(theta1, theta2 + eps), QT3) - loss_fun(QT_gate(theta1, theta2 - eps), QT3))/(2 * eps)
    theta1 += -grad_theta1*delta_theta
    theta2 += -grad_theta2*delta_theta

print(loss, QT_gate(theta1, theta2))
print(theta1, theta2)
