# isa/instruction.py — Representa una instruccion del ISA
#
# TAREAS:
#   1. Definir una clase Instruction con campos:
#        - opcode  (cual operacion)
#        - dest    (registro destino, e.g. "R1")
#        - src1    (primer operando — registro o literal)
#        - src2    (segundo operando — registro, literal, o None)
#        - label   (opcional, para saltos: "loop_start")
#
#   2. Metodo __repr__ util para debug: "ADD R1 R2 R3"
#
#   DECISION DE DISEÑO:
#     ¿Los operandos son solo registros o también inmediatos (numeros literales)?
#     ADDI R1 R2 5  ->  R1 = R2 + 5  (instruccion con inmediato)
#     Mas simple al inicio: soporte para literales enteros como src.
