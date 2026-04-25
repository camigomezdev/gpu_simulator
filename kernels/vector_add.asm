# kernels/vector_add.asm — Kernel de suma de vectores escrito en el ISA custom
#
# LOGICA DEL KERNEL (equivalente en CUDA):
#   int i = threadIdx.x + blockIdx.x * blockDim.x;
#   C[i] = A[i] + B[i];
#
# TAREAS:
#   1. Escribir las instrucciones del ISA cuando ya este definido
#   2. Asumir que en memoria global:
#        addr 0..N-1    -> array A
#        addr N..2N-1   -> array B
#        addr 2N..3N-1  -> array C (resultado)
#   3. Cada thread calcula su indice con GETID y accede a su posicion
#
# PSEUDOCODIGO EN EL ISA:
#   GETID R0          # R0 = thread_id (= indice i)
#   LOAD  R1 R0       # R1 = A[i]
#   ADD   R2 R0 IMM_N # R2 = i + N  (offset para B)   <- necesitas ADDI
#   LOAD  R3 R2       # R3 = B[i]
#   ADD   R4 R1 R3    # R4 = A[i] + B[i]
#   ADD   R5 R0 IMM_2N# R5 = i + 2N (offset para C)
#   STORE R4 R5       # C[i] = R4
#   RET
