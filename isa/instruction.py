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


class Instruction:
    def __init__(self, opcode, dest, src1, src2, label=""):
        self.opcode = opcode
        self.dest = dest
        self.src1 = src1
        self.src2 = src2
        self.label = label

    def __repr__(self):
        sig = self.opcode.operands
        parts = [self.opcode.name]
        for field in sig._fields:
            if getattr(sig, field):
                value = getattr(self, field)
                if value is not None:
                    parts.append(str(value))
        return " ".join(parts)

    def __str__(self):
        return f"Instruction {self.opcode} - Values {self.dest} {self.src1} {self.src2} {self.label}"
