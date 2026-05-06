# gpu/sm.py — Streaming Multiprocessor (SM): unidad principal de computo
#
# TAREAS:
#   1. Clase SM con:
#        - sm_id
#        - cores          (lista de N objetos Core — tipico: 32-128 por SM)
#        - warps           (lista de warps asignados a este SM)
#        - scheduler       (objeto WarpScheduler)
#        - shared_memory   (objeto SharedMemory — una por bloque activo)
#        - global_memory   (referencia a la memoria global del GPU)
#
#   2. Metodo assign_block(block) -> None
#      Recibe un bloque de threads, crea los Warps (grupos de 32), los agrega
#      al pool del scheduler.
#
#   3. Metodo step() -> bool
#      Ejecuta un "ciclo" de simulacion:
#        a. Pedir al scheduler el siguiente warp listo
#        b. Fetch de la instruccion en warp.pc
#        c. Ejecutar esa instruccion en todos los threads activos del warp
#           (un Core por thread — en paralelo, en Python: iterar la lista)
#        d. Avanzar warp.pc
#        e. Retornar True si quedan warps sin terminar
#
#   CONCEPTO: Un SM puede tener multiples bloques activos a la vez.
#   El maximo depende de recursos: registros usados, shared memory usada.
#   Para la sim: limitar a M bloques activos (configurable).

from .warp import Warp, WarpState
from .thread import Thread, ThreadState
from .core import Core
from .scheduler import WarpScheduler
from .memory import MemoryHierarchy
from isa.instruction import Instruction


class SM:
    def __init__(self, sm_id, n_cores, memory):
        self.sm_id = sm_id
        self.cores: list[Core] = [Core(idx, False) for idx in range(n_cores)]
        self.scheduler: WarpScheduler = WarpScheduler([])
        self.memory: MemoryHierarchy = memory
        self.instructions: list[Instruction] = []

    def assign_instructions(self, instructions):
        self.instructions = instructions

    def assign_block(self, block: list[Thread]):
        warp_id = 0
        for i in range(0, len(block), 32):
            threads = block[i: i+32]
            new_warp = Warp(warp_id)
            new_warp.threads = threads
            warp_id += 1
            self.scheduler.warps.append(new_warp)

        print(f"Cantidad de Warps: {len(self.scheduler.warps)}")
        print(f"Block Size: {len(block)}")

    def step(self) -> bool:
        if self.scheduler.check_and_release_sync():
            for warp in self.scheduler.warps:
                if warp.state == WarpState.SYNCING:
                    warp.state = WarpState.READY

        next_warp = self.scheduler.next_warp()
        if next_warp is None:
            return False

        if next_warp.pc < len(self.instructions):
            instruction = self.instructions[next_warp.pc]

            threads = next_warp.get_active_threads()

            for core, thread in zip(self.cores, threads):
                core.execute(instruction, thread, self.memory)

            if any(thread.state == ThreadState.SYNC for thread in next_warp.threads):
                next_warp.state = WarpState.SYNCING

            if next_warp.is_done():
                next_warp.state = WarpState.FINISHED

            next_warp.pc += 1

            for warp in self.scheduler.warps:

                if not warp.is_done():
                    return True

        return False
