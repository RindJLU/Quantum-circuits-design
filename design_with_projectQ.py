# coding: utf-8
from projectq.ops import H, Measure
from projectq import MainEngine
from Quantum\ circuits\ design.py import kron
eng = MainEngine()
q1 = eng.allocate_qubit()
q2 = eng.allocate_qubit()

H | q1
H | q2
Measure | q1
Measure | q2

eng.flush()

print('Measured q1: {}'.format(int(q1)))
print('Measured q2: {}'.format(int(q2)))

