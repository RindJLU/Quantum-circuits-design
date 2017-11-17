# Learning projectQ

## 1. projectq.ops:<br>
DATA:<br>
    Allocate = <projectq.ops._gates.AllocateQubitGate object><br>
    AllocateDirty = <projectq.ops._gates.AllocateDirtyQubitGate object><br>
    Barrier = <projectq.ops._gates.BarrierGate object><br>
    CNOT = <projectq.ops._metagates.ControlledGate object><br>
    CX = <projectq.ops._metagates.ControlledGate object><br>
    Deallocate = <projectq.ops._gates.DeallocateQubitGate object><br>
   __Entangle(?)__ = <projectq.ops._gates.EntangleGate object><br>
    H = <projectq.ops._gates.HGate object><br>
    Measure = <projectq.ops._gates.MeasureGate object><br>
    NOT = <projectq.ops._gates.XGate object><br>
   __QFT(?)__ = <projectq.ops._qftgate.QFTGate object><br>
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


