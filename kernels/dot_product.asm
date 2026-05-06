

GETID R0                # id = Thread ID
LOAD  R1 R0             # x = Load A[id]
LOAD  R2 R0 R7          # y = Load B[id]
MUL R3 R1 R2            # z = x*y
STORES R3 R0         # Save z
SYNC
SUB R4 R0 R0        # acc = 0
SUB R5 R0 R0        # acc = 0
SUB R6 R0 R0        # idx = 0
BNE R0 R5 ENDLOOP
LOOP:
    LOADS R3 R6
    ADD R4 R4 R3
    ADD R6 R6 R9
    BNE R6 R7 LOOP
ADD R8 R7 R7
STORE R4 R5 R8
ENDLOOP:
RET