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

from time import sleep

from isa.instruction import Instruction
from .thread import Thread, ThreadState
from .memory import MemoryHierarchy, Memory
from isa.opcodes import Opcode


class Core:
    def __init__(self, core_id: int, busy: bool):
        self.core_id = core_id
        self.busy = busy

    def execute(self, instruction: Instruction, thread: Thread, memory: MemoryHierarchy):
        opcode = instruction.opcode

        if opcode == Opcode.ADD:
            self._add(instruction, thread)
        elif opcode == Opcode.SUB:
            self._sub(instruction, thread)
        elif opcode == Opcode.MUL:
            self._mult(instruction, thread)
        elif opcode == Opcode.DIV:
            self._div(instruction, thread)
        elif opcode == Opcode.LOAD:
            self._load(instruction, thread, memory.global_memory)
        elif opcode == Opcode.STORE:
            self._store(instruction, thread, memory.global_memory)
        elif opcode == Opcode.GETID:
            self._get_id(instruction, thread)
        elif opcode == Opcode.MOV:
            self._mov(instruction, thread)
        elif opcode == Opcode.NOP:
            self._nop(thread)
        elif opcode == Opcode.RET:
            self._ret(thread)
        elif opcode == Opcode.JMP:
            self._jmp(instruction, thread)
        elif opcode == Opcode.BEQ:
            self._beq(instruction, thread)
        elif opcode == Opcode.BNE:
            self._bne(instruction, thread)
        elif opcode == Opcode.LOADS:
            self._load(instruction, thread, memory.shared_memory)
        elif opcode == Opcode.STORES:
            self._store(instruction, thread, memory.shared_memory)
        elif opcode == Opcode.SYNC:
            self._sync(thread)

    def _add(self, instruction: Instruction, thread: Thread):
        src1 = thread.read_register(instruction.src1)
        src2 = thread.read_register(instruction.src2)
        thread.write_register(instruction.dest, src1 + src2)
        thread.pc += 1

    def _sub(self, instruction: Instruction, thread: Thread):
        src1 = thread.read_register(instruction.src1)
        src2 = thread.read_register(instruction.src2)
        thread.write_register(instruction.dest, src1 - src2)
        thread.pc += 1

    def _mult(self, instruction: Instruction, thread: Thread):
        src1 = thread.read_register(instruction.src1)
        src2 = thread.read_register(instruction.src2)
        thread.write_register(instruction.dest, src1 * src2)
        thread.pc += 1

    def _div(self, instruction: Instruction, thread: Thread):
        src1 = thread.read_register(instruction.src1)
        src2 = thread.read_register(instruction.src2)

        if src2 == 0:
            raise ZeroDivisionError

        thread.write_register(instruction.dest, src1 / src2)
        thread.pc += 1

    def _load(self, instruction: Instruction, thread: Thread, memory: Memory):
        addr = thread.read_register(instruction.src1)
        offset = thread.read_register(instruction.src2)
        value, latency = memory.read(addr+offset)
        thread.stall_cycles += latency
        thread.write_register(instruction.dest, value)
        thread.pc += 1

    def _store(self, instruction: Instruction, thread: Thread, memory: Memory):
        addr = thread.read_register(instruction.src1)
        offset = thread.read_register(instruction.src2)
        value = thread.read_register(instruction.dest)

        memory.write(addr+offset, value)
        thread.pc += 1

    def _get_id(self, instruction: Instruction, thread: Thread):
        thread.write_register(instruction.dest, thread.thread_id)
        thread.pc += 1

    def _jmp(self, instruction: Instruction, thread: Thread):
        thread.pc = instruction.label

    def _beq(self, instruction: Instruction, thread: Thread):
        src1 = thread.read_register(instruction.src1)
        src2 = thread.read_register(instruction.src2)
        if src1 == src2:
            thread.pc = instruction.label
            return
        thread.pc += 1

    def _bne(self, instruction: Instruction, thread: Thread):
        src1 = thread.read_register(instruction.src1)
        src2 = thread.read_register(instruction.src2)
        if src1 != src2:
            thread.pc = instruction.label
            return
        thread.pc += 1

    def _mov(self, instruction: Instruction, thread: Thread):
        value = thread.read_register(instruction.src1)
        thread.write_register(instruction.dest, value)
        thread.pc += 1

    def _ret(self, thread: Thread):
        thread.state = ThreadState.FINISHED
        thread.pc += 1

    def _nop(self, thread: Thread):
        thread.pc += 1

    def _sync(self, thread: Thread):
        thread.state = ThreadState.SYNC
        thread.pc += 1
