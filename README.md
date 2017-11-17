# Quantum circuits design. by yufeng(11/17/2017)
## 1. Encode the quantum circuits.<br>

The method of encoding the quantum circuits empersis on the one qubits gate and two qubits gate(universal quantum gates: actually single qubit gates and CNOT gate is already universal\[Quantum computation and quantum information]).<br>

The detail of encoding mathods can be found in the paper \[Decomposition of unitary matrices for ﬁnding quantum circuits: Application to molecular Hamiltonians] by Prof.Kais, Purdue.https://www.chem.purdue.edu/kais/paper/Anmer-JCP-2011.pdf<br>

__The represtation of quantum gates:__<br>
Four element list: \[a, b, c, d], where a, b and c are intergers, and d is the value of the angle(for non-rotation gates the value is 0). Creating a list store different gates, like\{V, Z, S, V+}, and a represents the index of the gate. For example, a = 1 means the gate is V. And b and c is the index of qubits, where b is the controled qubit, and c is the controled qubit.<br>

__Example__<br>
![example_Toffoli](https://github.com/RindJLU/Quantum-circuits-design/blob/master/pictures/Toffoli.png)<br>
The code here is \[1 3 2 0.0]; \[2 3 1 0.0]; \[3 2 1 0.0]; \[4 3 2 0.0]; \[2 1 3 0.0].<br>

__MY CODE TO GENERATE TOFFOLI GATE__<br>
See Quantum circuits design.py<br>
__Problem:__ Mainly use Annealing methods to generate search the new circuits, although it can generate new Toffoli gate, but it is too slow and wastes many resouses.<br>
__Some solutions of Toffoli gate:__<br>
\[[2, 1, 3], [4, 3, 2], [2, 1, 3], [1, 3, 2], [3, 2, 1]]<br>
\[[1, 3, 1], [2, 3, 2], [4, 3, 1], [3, 2, 1], [2, 3, 2]]<br>
\[[3, 2, 1], [2, 3, 1], [4, 3, 2], [2, 1, 3], [1, 3, 2]]<br>

