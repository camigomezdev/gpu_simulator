# isa/opcodes.py — Define los opcodes (nombres de instrucciones) del ISA custom
#
# TAREAS:
#   1. Definir un enum o dict con los opcodes disponibles.
#      Ejemplo de categorias:
#        - Aritmetica:   ADD, SUB, MUL, DIV
#        - Memoria:      LOAD, STORE        (leer/escribir global memory)
#        - Control:      JMP, BEQ, BNE      (saltos — cuidado con warp divergence)
#        - Especiales:   MOV, NOP, RET
#        - Thread ID:    GETID              (obtiene el threadIdx del thread actual)
#
#   2. Pensar en el formato de instruccion:
#      opcode  dest  src1  src2   (similar a RISC)
#      Ejemplo: ADD R1 R2 R3  ->  R1 = R2 + R3
#
#   CONCEPTO CLAVE:
#     GETID es fundamental — permite que cada thread sepa cuál es su índice
#     para acceder a posiciones distintas del array (el paralelismo real).

import enum
from collections import namedtuple

Signature = namedtuple('Signature', ['dest', 'src1', 'src2', 'label'])


class Opcode(enum.Enum):
    def __new__(cls, value, operands):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.operands = operands
        return obj

    ADD = 1, Signature(dest=True, src1=True, src2=True, label=False)
    SUB = 2, Signature(dest=True, src1=True, src2=True, label=False)
    MUL = 3, Signature(dest=True, src1=True, src2=True, label=False)
    DIV = 4, Signature(dest=True, src1=True, src2=True, label=False)
    LOAD = 5, Signature(dest=True, src1=True, src2=True, label=False)
    STORE = 6, Signature(dest=True, src1=True, src2=True, label=False)
    JMP = 7, Signature(dest=False, src1=False, src2=False, label=True)
    BEQ = 8, Signature(dest=False, src1=True, src2=True, label=True)
    BNE = 9, Signature(dest=False, src1=True, src2=True, label=True)
    MOV = 10, Signature(dest=True, src1=True, src2=False, label=False)
    NOP = 11, Signature(dest=False, src1=False, src2=False, label=False)
    RET = 12, Signature(dest=False, src1=False, src2=False, label=False)
    GETID = 13, Signature(dest=True, src1=False, src2=False, label=False)
