# coding: utf-8
import numpy as np
import copy
from projectq.ops import X, T, S, H, Rz, Measure
from projectq import MainEngine
from projectq.meta import Control


# ======================================================================================================================
# define truth table
input = ()
for i in range(8):
    a = i//4
    b = (i-a*4)//2
    c = (i-a*4-b*2)//1
    input = input + ([a, b, c],)

output = copy.deepcopy(input[0:6])
output = output + (input[7],)
output = output + (input[6],)
# print(input, output)
# ======================================================================================================================

# define gates:
I0 = Rz(0)
gate = (T, X, S, H)
def control(ctrl_list, q, eng):
    Gate = gate[ctrl_list[0]-1]
    q_trg = q[ctrl_list[1]-1]
    q_ctrl = q[ctrl_list[2]-1]
    with Control(eng, q_ctrl):
        Gate | q_trg
    return q

def rand_generator():
    tof_list = []  # 用列表存储数据
    for i in range(5):
        a = np.random.randint(1, 4)
        b = np.random.randint(1, 3)
        c = b
        while c == b:
            c = np.random.randint(1, 3)
        tof_list.append([a, b, c])
    return(tof_list)
# print(rand_generator())

tof_test = rand_generator()

def run(MainEngine, X):
    ans = ()
    for k in input:
        eng = MainEngine()
        q0, q1, q2 = eng.allocate_qureg(3)
        q = (q0, q1, q2)
        for m in k:
            if m == 1:
                X | q[m]
        for i in tof_test:
            control(i, q, eng)
        for n in q:
            Measure | n
        eng.flush()
        ans_ele = []
        for l in q:
            ans_ele.append(int(l))
        ans = ans + (ans_ele,)
    return(ans)

# define loss function: Mean Square
def loss_fun(ans, output):
    loss = 0
    for i in range(len(ans)):
        for j in range(len(ans[i])):
            loss += abs(ans[i][j]-output[i][j])
    return loss


loss_list = []
for i in range(100):
    ans = run(MainEngine, X)
    loss = loss_fun(ans, output)
    loss_list.append(loss)
print(min(loss_list))
