# coding: utf-8
import numpy as np

# define Three qubits quantum teleportation(sender part):
QT_matrix = np.zeros([8,8])
for i in range(len(QT_matrix[1])):
    if (i//2 + i%2)//2 == 0:
        pos_index = 0
    else:
        pos_index = 1
