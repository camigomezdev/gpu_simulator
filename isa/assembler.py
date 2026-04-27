# isa/assembler.py — Convierte texto plano a lista de objetos Instruction
#
# TAREAS:
#   1. Funcion assemble(source: str) -> list[Instruction]
#      Parsea linea por linea:
#        - Ignorar comentarios (#) y lineas vacias
#        - Detectar labels (terminan en ":")
#        - Crear objetos Instruction para cada linea de codigo
#
#   2. Resolver labels a indices numericos (para saber a que linea saltar)
#      Ejemplo:
#        loop:        <- label en linea 0
#          ADD R1 R1 R2
#          BNE R1 R3 loop   <- saltar a linea 0
#
#   EJEMPLO DE FORMATO DE TEXTO:
#     # vector add kernel
#     GETID R0        # R0 = thread index
#     LOAD  R1 R0     # R1 = A[R0]
#     LOAD  R2 R0     # R2 = B[R0]  (necesita offset — ver TAREAS de memoria)
#     ADD   R3 R1 R2  # R3 = A[R0] + B[R0]
#     STORE R3 R0     # C[R0] = R3
#     RET

from .instruction import Instruction
from .opcodes import Opcode


def assemble(source: str) -> list[Instruction]:
    lines = source.split("\n")
    labels = {}
    instruction_index = 0
    instructions = []
    for line in lines:
        line = line.split("#")[0]
        line = " ".join(line.split())

        if ":" in line:
            label, rest = line.split(":", 1)
            labels[label.strip().upper()] = instruction_index
            line = rest.strip()

        if line:
            inst_list = line.replace(",", "").split(" ")
            opcode: Opcode = Opcode[inst_list[0].strip()]
            sig = opcode.operands
            operands = iter(inst_list[1:])

            dest = next(operands).strip() if sig.dest else None
            src1 = next(operands).strip() if sig.src1 else None
            src2 = next(operands).strip() if sig.src2 else None
            label = next(operands).strip() if sig.label else None

            new_inst = Instruction(
                opcode=opcode, dest=dest, src1=src1, src2=src2, label=label)

            instructions.append(new_inst)
            instruction_index += 1
    for inst in instructions:
        if inst.label is not None:
            inst.label = labels[inst.label.upper()]
    return instructions


if __name__ == "__main__":
    instructions = assemble(
        "MOV   R0 R0\n"
        "loop:\n"
        "  ADD R1 R1 R2\n"
        "  BNE R1 R3 loop\n"
        "RET\n")
    print(instructions)
