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
