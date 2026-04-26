# gpu/thread.py — Unidad minima de ejecucion
#
# TAREAS:
#   1. Clase Thread con:
#        - thread_id   (indice global: blockIdx * blockDim + threadIdx)
#        - registers   (dict: {"R0": 0, "R1": 0, ...} — emular N registros)
#        - pc          (program counter — indice de la instruccion actual)
#        - state       (READY | RUNNING | FINISHED | STALLED)
#        - active      (bool — para el active mask del warp, ver warp.py)
#
#   2. Metodo read_register(name) y write_register(name, value)
#
#   CONCEPTO CLAVE:
#     Cada thread tiene sus PROPIOS registros — esto es lo que permite
#     que 32 threads ejecuten "ADD R1 R2 R3" pero con datos distintos.
#     El thread 0 suma A[0]+B[0], el thread 1 suma A[1]+B[1], etc.

from enum import Enum
from .memory import RegisterFile


class ThreadState(Enum):
    READY = "READY"
    RUNNING = "RUNNING"
    FINISHED = "FINISHED"
    STALLED = "STALLED"


class Thread:
    def __init__(self, thread_id: int, n_registers: int = 8):
        self.thread_id: int = thread_id

        self.registers: dict[str, int] = RegisterFile()
        for n in range(n_registers):
            self.registers.write(f"R{n}", 0)
        self.stall_cycles = 0

        self.pc: int = 0
        self.state: ThreadState = ThreadState.READY
        self.active: bool = True

    def read_register(self, name: str) -> int:
        return self.registers.read(name)

    def write_register(self, name: str, value: int) -> None:
        self.registers.write(name, value)


if __name__ == "__main__":
    threads = [Thread(i) for i in range(10)]

    for i, t in enumerate(threads):
        t.write_register("R2", i * 10)
        t.write_register("R3", 1)

    # Misma instruccion, resultados distintos (SIMT)
    for t in threads:
        result = t.read_register("R2") + t.read_register("R3")
        t.write_register("R1", result)
        print(t.thread_id, t.registers)
