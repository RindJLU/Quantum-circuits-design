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
### 2.1 What is the difficulty to use projectQ?<br>
Firstly, projectQ is not a simulation mathod, but more like a experiment way. This is 
because projectQ is based on IBM Quantum Experience, and the error of 
quantum devices provided by IBM(also see IBM Q: https://quantumexperience.ng.bluemix.net/qx/community) can make it hard to apply machine learning since 
the output itself is not precise.

Secondly, in the Simulated Annealing method, we use __unitary gate__ 
as optimization target. But here we cannot use unitary gate, 
since projectQ is based on experimental result, which means we can only analysis
the data to attain the state of qubits. In this case, use**Truth Table** could be better.



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
Like the picture below, by comparing the final emperimental and theorical output, it is possible to define the __loss function__

### 2.3 What if the input qubits are in superposition?
To train quantum circuits using projectQ, it is nature to use truth table 
as optimizing goal. Based on our knowledge about quantum states, the difference
between qubits with classical bits is that qubits can be in state of superposition.
In light of this, there will be infinity number of training data. Can we find a complete data that can guarantee the validity 
for any input state?

__Yes, we can.__To make this clear, let's consider the operation of quantum circuits-unitary operatin, which is also linear
operation. In linear space, if we can guarantee the validity for any of its complete base spaces, the quantum circuits will
be valid for any input.

Based on this, I will train qubits in their computational basis(2^n).

__problem__: how to get the state of a quantum qubit without measure in projectq?

## 3. Other optimization method:
### 3.1 Genetic Algorithm
The idea of genetic algorithm is to find the fittest individuals in a group. The fitness is defined as the result of
loss function. The higher the fitness a member in the group has, the more likely this gene of this member be inherent
to next generation. In addition to inheritance, the genovariation is another approach to change the gene in the group and therefore, 
keep away the local minimum.

However, for this problem, the GA may not be effective. The reason is in this question, while we search the possible solution of 
circuits, it is not discontinuous. Changing the gate or the target and controlled qubut can make a big disturbance to the whole system.

### 3.2 Group Leader Optimization Algorithm
This is was inspired by the importance of the leader in a group. 
Members in the group would like to learn from the leader and therefore, become more and more like the leader.
Once the a member of a group is 'better' than the leader, this member will replace the current learder and become the new one.
To guarantee this will not trapped in a local minimum, creating many groups and crossing the members of these group.

For more information, please view the paper 'Group Leader Optimization Algorithm.'http://www.tandfonline.com/doi/abs/10.1080/00268976.2011.552444

#### IMPLEMENTATION
Here I apply the GLOA algrithm to a simple problem-designing Toffoli gate:

__Preparation:__\
In the first place, I created six groups, each of which contains six members(here, every member refers to a possible solution). 
Next, I defined a function that could calculate the fidelity of all groups and sort the member of a group according to its fidelity.
and the first member of one group, which has the biggest fidelity(least loss), would be the leader of the group.

__Optimization Process__\
The Group Leader Optimization Algorithm, as the name implies, is a model that make advantages of the influence of leaders in 
social groups, where the members of the group are influenced by the leader, and therefore, their behavior is increasingly similar to the leaders'.
Hence, while optimization, the effect of a leader must be considered.

1. creating new members:\
For every member in a group(including the leader), creating a new version of it, and replace the old member according to the __Replacement Criteria__.
The new member follows: __New member = r1 portion of old member + r2 portion of the leader + r3 portion of random__

__Replacement Criteria__\
If the loss of new member is less than the old member, then replace the old member.\
Once the change for all the members(except the leader) is done, then use the function I designed in __Preparation__ to sort
the new group. Here the leader may be changed if one of its member has less loss than itself.

2. Crossover different groups:\
Every 10 iterations, make a cross of different groups. Randomly select two index of the member(not the leader) in a group, and randomly choose 
groups do the crossover. 

### Result
![GLOA_examples](https://github.com/RindJLU/Quantum-circuits-design/blob/master/pictures/GLOA_example.png)\
From the picture above, we can see that the GLOA is much faster than the Simulated Annealing, although it is not very stable(iterations rangeing
from 150 to 700).

Solutions found:\
\[[2, 3, 1], [4, 3, 2], [2, 3, 1], [3, 2, 1], [1, 3, 2]]\
\[[2, 3, 1], [4, 3, 2], [2, 3, 1], [1, 3, 2], [3, 2, 1]]\
\[[3, 2, 1], [1, 3, 2], [2, 1, 3], [4, 3, 2], [2, 3, 1]]\
\[[2, 3, 2], [4, 3, 1], [3, 2, 1], [2, 3, 2], [1, 3, 1]]\
\[[2, 1, 3], [4, 3, 2], [2, 1, 3], [3, 2, 1], [1, 3, 2]]\
\[[3, 2, 1], [2, 1, 3], [4, 3, 2], [2, 1, 3], [1, 3, 2]]\
\[[3, 2, 1], [1, 3, 2], [2, 3, 1], [4, 3, 2], [2, 1, 3]]\
\[[3, 2, 1], [2, 3, 2], [4, 3, 1], [2, 3, 2], [1, 3, 1]]\
\[[2, 1, 3], [4, 3, 2], [2, 3, 1], [1, 3, 2], [3, 2, 1]]




## 4 Machine learning method:
### 4.1 Gradient Decent
Gradient decent is a effective way dealing with continuous problem. Here I use this method to optimize the angle of the rotate gate.

Although this is effective way, the result can easily be trapped to local minimum.


## 5. Matrix Decomposing:

# Problem existed:
## 1. INPUT?
The core problem is that the input of qubit is two dimention(2 by 1), and if the two element is not 0 at the same time, this is __superposition__. This is different from classical nueral network where the input can only be 0 or 1. 

## 2. Controled gate.
How to represnt controled gate in correspoding nueral network? This may equal to the problem of __entanglement state__.

Currently, my though for this problem is to find a function linking control qubit and target qubit, which can generate the result of correspoding controled gate operation.<br>
__There are several papers that discuss this problems, see fold 'papers'.__
![paper](https://github.com/RindJLU/Quantum-circuits-design/blob/master/papers/%E5%9F%BA%E4%BA%8E%E9%87%8F%E5%AD%90%E9%97%A8%E7%BA%BF%E8%B7%AF%E7%9A%84%E9%87%8F%E5%AD%90%E7%A5%9E%E7%BB%8F%E7%BD%91%E7%BB%9C%E6%A8%A1%E5%9E%8B%E5%8F%8A%E7%AE%97%E6%B3%95.pdf)



