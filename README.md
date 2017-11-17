# Quantum circuits design. by yufeng(11/17/2017)
## 1. Encode the quantum circuits.<br>

The method of encoding the quantum circuits empersis on the one qubits gate and two qubits gate(universal quantum gates: actually single qubit gates and CNOT gate is already universal\[Quantum computation and quantum information]).<br>

The detail of encoding mathods can be found in the paper \[Decomposition of unitary matrices for ﬁnding quantum circuits: Application to molecular Hamiltonians] by Prof.Kais, Purdue.https://www.chem.purdue.edu/kais/paper/Anmer-JCP-2011.pdf<br>

__The represtation of quantum gates:__<br>
Four element list: \[a, b, c, d], where a, b and c are intergers, and d is the value of the angle(for non-rotation gates the value is 0). Creating a list store different gates, like\{V, Z, S, V+}, and a represents the index of the gate. For example, a = 1 means the gate is V. And b and c is the index of qubits, where b is the controled qubit, and c is the controled qubit.<br>

__Example__<br>

