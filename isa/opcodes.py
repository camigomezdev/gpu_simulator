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
