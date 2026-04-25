# gpu/core.py — CUDA Core: ejecuta una instruccion para un thread
#
# TAREAS:
#   1. Clase Core con:
#        - core_id
#        - busy (bool — esta ejecutando algo ahora)
#
#   2. Metodo execute(instruction, thread, memory) -> None
#      Implementa cada opcode:
#        ADD:    thread.registers[dest] = src1_val + src2_val
#        SUB:    ...
#        MUL:    ...
#        LOAD:   thread.registers[dest] = memory.read(addr)
#        STORE:  memory.write(addr, src_val)
#        GETID:  thread.registers[dest] = thread.thread_id
#        MOV:    thread.registers[dest] = src1_val
#        NOP:    no hace nada
#        RET:    thread.state = FINISHED
#        JMP:    thread.pc = target
#        BEQ:    if src1 == src2: thread.pc = target
#        BNE:    if src1 != src2: thread.pc = target
#
#   NOTA: En un GPU real, hay cores especializados (FP32, INT, LD/ST, SFU).
#   Para la simulacion educativa, un Core generico que maneja todo es suficiente.
