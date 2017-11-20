# __Quantum circuits design. By yufeng__
## 1. Optimization Method.<br>
### 1.1 Representation method.

The method of encoding the quantum circuits emphasize on the one qubits gate and two qubits gate(universal quantum gates: actually single qubit gates and CNOT gate is already universal\[Quantum computation and quantum information]).<br>

The detail of encoding methods can be found in the paper \[Decomposition of unitary matrices for ﬁnding quantum circuits: Application to molecular Hamiltonians] by Prof.Kais, Purdue.https://www.chem.purdue.edu/kais/paper/Anmer-JCP-2011.pdf<br>

__The representation of quantum gates:__<br>
Four element list: \[a, b, c, d], where a, b and c are intergers, and d is the value of the angle(for non-rotation gates the value is 0). Creating a list store different gates, like\{V, Z, S, V+}, and a represents the index of the gate. For example, a = 1 means the gate is V. And b and c is the index of qubits, where b represents the target qubit, and c is the index of controled qubit.<br>

__Example__<br>
![example_Toffoli](https://github.com/RindJLU/Quantum-circuits-design/blob/master/pictures/Toffoli.png)<br>
The code here is \[1 3 2 0.0]; \[2 3 1 0.0]; \[3 2 1 0.0]; \[4 3 2 0.0]; \[2 1 3 0.0].<br>

## 1.2 My code(based on simulated annealing) to generate TOFFOLI gate<br>
See __Quantum circuits design.py__<br>
__Problem Existed:__ Mainly use Simulated Annealing methods to generate search the new circuits, although it can generate new Toffoli gate, but it is too slow and wastes many resources.<br>
__Some solutions of Toffoli gate:__<br>
**(Here ignore the last element of code list, since all the gates are
non-rotation gates)<br>**
\[[2, 1, 3], [4, 3, 2], [2, 1, 3], [1, 3, 2], [3, 2, 1]]<br>
\[[1, 3, 1], [2, 3, 2], [4, 3, 1], [3, 2, 1], [2, 3, 2]]<br>
\[[3, 2, 1], [2, 3, 1], [4, 3, 2], [2, 1, 3], [1, 3, 2]]<br>
\[[1, 3, 2], [2, 1, 3], [4, 3, 2], [2, 1, 3], [3, 2, 1]]<br>
Fidelity with step:
![Fidelity with step](https://github.com/RindJLU/Quantum-circuits-design/blob/master/pictures/Figure_1.png)

## 2. Design circuits with projectQ<br>
### 2.1 What is the difficulty of using projectQ?<br>
Firstly, projectQ is not a simulation mathod, but more like a experiment way. This is 
because projectQ is based on IBM Quantum Experience, and the error of 
quantum devices provided by IBM(also see IBM Q: https://quantumexperience.ng.bluemix.net/qx/community) can make it hard to apply machine learning since 
the output itself is not precise.

Secondly, in the Simulated Annealing method, we use __unitary gate__ 
as optimization target. But here we cannot use unitary gate, 
since projectQ is based on experiment, which only give output of
qubits. In this case, use**Truth Table** could be better.



### 2.2 Link projectQ with the representation listed above. <br>
__Realizing Controled gate :__(see projectQ_NOTE.md)<br>
```
with Control(eng, q_ctrl): 
    Gate | q_trg
```
__Obtaining the unitary matrix of the quantum circuits based on 
 multimetering.__
 Because qubits can be in superposition, the amplitude is important 
  if ignoring the phase. To obtain the amplitude that qubit in state
   |0> and |1>, it is useful to measure many times(say 1024 times) to get the relative
   probability.

__Example and visualize__
![CNOT gate](https://github.com/RindJLU/Quantum-circuits-design/blob/master/pictures/TIM%E6%88%AA%E5%9B%BE20171119215034.png)
(From https://arxiv.org/pdf/0905.2103.pdf)
Like the picture below, by comparing the final emperimental and theorical output, it is possible to define the __loss function__.


# Problem existed:
## 1. INPUT?
The core problem is that the input of qubit is two dimention(2 by 1), and if the two element is not 0 at the same time, this is __superposition__. This is different from classical nueral network where the input can only be 0 or 1. 

## 2. Controled gate.
How to represnt controled gate in correspoding nueral network? This may equal to the problem of __entanglement state__.

Currently, my though for this problem is to find a function linking control qubit and target qubit, which can generate the result of correspoding controled gate operation.




