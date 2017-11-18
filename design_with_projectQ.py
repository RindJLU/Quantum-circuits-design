# coding: utf-8
import numpy as np
import projectq.setups.default
from projectq.ops import Z, X, S, Measure
from projectq import MainEngine
from projectq.backends import CircuitDrawer
from projectq.meta import Dagger, Control


def control(Gate, q_trg, q_ctrl):
    with Control(eng, q_ctrl):
        Gate | q_trg
    return q_trg

drawing_engine = CircuitDrawer()
eng = MainEngine()

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

