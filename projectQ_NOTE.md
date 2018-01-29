# Learning projectQ

## 1. projectq.ops:<br>
DATA:<br>
```
    Allocate = <projectq.ops._gates.AllocateQubitGate object><br>
    AllocateDirty = <projectq.ops._gates.AllocateDirtyQubitGate object><br>
    Barrier = <projectq.ops._gates.BarrierGate object><br>
    CNOT = <projectq.ops._metagates.ControlledGate object><br>
    CX = <projectq.ops._metagates.ControlledGate object><br>
    Deallocate = <projectq.ops._gates.DeallocateQubitGate object><br>
    Entangle(?) = <projectq.ops._gates.EntangleGate object><br>
    H = <projectq.ops._gates.HGate object><br>
    Measure = <projectq.ops._gates.MeasureGate object><br>
    NOT = <projectq.ops._gates.XGate object><br>
    QFT(?) = <projectq.ops._qftgate.QFTGate object><br>
    S = <projectq.ops._gates.SGate object><br>
    Sdag = <projectq.ops._metagates.DaggeredGate object><br>
    Sdagger = <projectq.ops._metagates.DaggeredGate object><br>
    Swap = <projectq.ops._gates.SwapGate object><br>
    T = <projectq.ops._gates.TGate object><br>
    Tdag = <projectq.ops._metagates.DaggeredGate object><br>
    Tdagger = <projectq.ops._metagates.DaggeredGate object><br>
    Toffoli = <projectq.ops._metagates.ControlledGate object><br>
   __X__ = <projectq.ops._gates.XGate object><br>
   __Y__ = <projectq.ops._gates.YGate object><br>
   __Z__ = <projectq.ops._gates.ZGate object<br>
```
__Introduce the gates:__ 
```
from project.ops import H, X, Y, Measure......
```

## 2. MainEngine<br>
```
from projectq import MainEngine
eng = MainEngine()
q1 = eng.allocate_qubit() # Create new qubits
```

## 3. Unitary operation:<br>
```
H | q1
Measure |q1
```

This is just one measurement. To understand what is the state of q1, we need do many measurement to determine the norm of the quantum state of a qubit.<br>
```
from projectq import MainEngine
from projectq.ops import H, Measure
import matplotlib.pyplot as plt

eng = MainEngine()
q1 = eng.allocate_qubit()

q1_1 = 0
q1_0 = 0
for i in range(1024):
    H | q1
    Measure | q1
    eng.flush()
    if int(q1) == 1:
        q1_1 += 1
    elif int(q1) == 0:
        q1_0 += 1
print('Totally Measured {} times'.format(1024))
print('Measured 0 {} times'.format(q1_0))
print('Measured 1 {} times'.format(q1_1))
plt.bar([0, 1], [q1_1, q1_0], width=0.4, color="green")
plt.show()
```
## 4. Control operation
To realize control operation, it is important to import __Control__ from projectq.meta<br>
```
from projectq import MainEngine
from projectq.meta import Control
from prodectq import H, X, Measure

eng = MainEngine()

\# Genrating two qubits
q_ctrl = eng.allocate_qubit()
q_trg = eng.allocate_qubit()

H | q_ctrl
\# control operation
with Control(eng, q_ctrl):
    X | q_trg

Measure | q_ctrl
Measure | q_trg

eng.flush()

print('Measured q1: {}'.format(int(q1)))
print('Measured q2: {}'.format(int(q2)))
```
## 5. Print picture of quantum circuits:<br>
Use CircuitDrawer in projectq.backends<br>
```
def Draw(eng, code_list):
    # code_list contains the code of a quantum circuits, more details see Quantumcircuits_design.py
    # Store gates using tuble
    gate_list = (X, Z, S, X)
    # Store qubits using tuble
    q = ('',)
    q += (eng.allocate_qubit(),)
    q += (eng.allocate_qubit(),)
    q += (eng.allocate_qubit(),)
    for i in code_list:
        gate_index = i[0]
        gate = gate_list[gate_index - 1]
        q_trg_index = i[1]
        q_trg = q[q_trg_index]
        q_ctrl_index = i[2]
        q_ctrl = q[q_ctrl_index]
        q_trg = control(gate, q_trg, q_ctrl)
    eng.flush()
    print(drawing_engine.get_latex())
Draw(eng, ([3, 2, 1],))
```

## 6. Draw Pictures of Quantum Circuits
```
def Draw(eng, code_list):
    # code_list contains the code of a quantum circuits, more details see Quantumcircuits_design.py
    # Store gates using tuble
    gate_list = (X, Z, S, X)
    # Store qubits using tuble
    q = ('',)
    q += (eng.allocate_qubit(),)
    q += (eng.allocate_qubit(),)
    q += (eng.allocate_qubit(),)
    for i in code_list:
        gate_index = i[0]
        gate = gate_list[gate_index - 1]
        q_trg_index = i[1]
        q_trg = q[q_trg_index]
        q_ctrl_index = i[2]
        q_ctrl = q[q_ctrl_index]
        q_trg = control(gate, q_trg, q_ctrl)
    eng.flush()
    print(drawing_engine.get_latex())
Draw(eng, ([3, 2, 1],))
```
__Result:__<br>
```
LaTex code:
\documentclass{standalone}
\usepackage[margin=1in]{geometry}
\usepackage[hang,small,bf]{caption}
\usepackage{tikz}
\usepackage{braket}
\usetikzlibrary{backgrounds,shadows.blur,fit,decorations.pathreplacing,shapes}

\begin{document}
\begin{tikzpicture}[scale=0.8, transform shape]

\tikzstyle{basicshadow}=[blur shadow={shadow blur steps=8, shadow xshift=0.7pt, shadow yshift=-0.7pt, shadow scale=1.02}]\tikzstyle{basic}=[draw,fill=white,basicshadow]
\tikzstyle{operator}=[basic,minimum size=1.5em]
\tikzstyle{phase}=[fill=black,shape=circle,minimum size=0.1cm,inner sep=0pt,outer sep=0pt,draw=black]
\tikzstyle{none}=[inner sep=0pt,outer sep=-.5pt,minimum height=0.5cm+1pt]
\tikzstyle{measure}=[operator,inner sep=0pt,minimum height=0.5cm, minimum width=0.75cm]
\tikzstyle{xstyle}=[circle,basic,minimum height=0.35cm,minimum width=0.35cm,inner sep=0pt,very thin]
\tikzset{
shadowed/.style={preaction={transform canvas={shift={(0.5pt,-0.5pt)}}, draw=gray, opacity=0.4}},
}
\tikzstyle{swapstyle}=[inner sep=-1pt, outer sep=-1pt, minimum width=0pt]
\tikzstyle{edgestyle}=[very thin]


\end{tikzpicture}
\end{document}
```

## 7. Quantum register and corresponding quantum state.
When apply 
````
a = MainEngine().allocate_qubit()
````
This will create a quantum register which stores a qubit. if use 
````
a.__str__()
````
This will return the register index of a(form 0 on)

## 8. Create new unitary gate.
```
# act on sigle qubit
0.5 * ‘X0 X5’ + 0.3 * ‘Z1 Z2’.
```
```angular2html
# act on n qubits:
coefficent * local_operator[0] x ... x local_operator[n-1]
# x is tensor operation
```
 Example: 
```angular2html
hamiltonian = 0.5 * QubitOperator('X0 X5') + 0.3 * QubitOperator('Z0')
```

## 9. Excute multi-qubits operation
```
from projectq.ops import All

All(H) | qubits
Measure | qubits  % unecessary for Measure to use 'All'
```

## 10. Amplitude & Probability
```
amp = eng.backend.get_amplitude('00', qubit + qubit2)
prob11 = eng.backend.get_probability('11', qureg)
```

## 11. Set wavefunction to a specific state
```
eng.backend.set_wavefunction([1/math.sqrt(2), 1/math.sqrt(2), 0, 0], qureg)  # where the list index represent the                                                                                          corresponding state.
```

## 12. Get the wavefunction
```
import copy
mapping, wavefunction = copy.deepcopy(eng.backend.cheat())
print("The full wavefunction is: {}".format(wavefunction))
Measure | qubit1 + qubit2  # In order to not deallocate a qubit in a superposition state
```
