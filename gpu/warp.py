# gpu/warp.py — Grupo de 32 threads que ejecutan en lockstep (SIMT)
#
# TAREAS:
#   1. Clase Warp con:
#        - warp_id
#        - threads     (lista de 32 objetos Thread)
#        - active_mask (bitmask o lista de bool — qué threads están activos)
#        - pc          (todos los threads del warp comparten el mismo PC)
#        - state       (READY | RUNNING | WAITING | DONE)
#
#   2. Metodo get_active_threads() -> lista de threads activos
#
#   3. Metodo is_done() -> True si todos los threads terminaron
#
#   CONCEPTO CLAVE — WARP DIVERGENCE:
#     Si hay un IF/ELSE y algunos threads toman el IF y otros el ELSE,
#     el warp debe ejecutar AMBOS caminos (enmascarando threads inactivos).
#     Esto se llama divergencia y es el mayor costo de rendimiento en GPUs.
#     Para el modelo educativo: al llegar a un BEQ/BNE, calcular el active_mask
#     para cada camino y ejecutar ambos secuencialmente.
#
#   WARP SIZE = 32 (constante de hardware en NVIDIA — no cambia entre generaciones)

from enum import Enum
from .thread import Thread, ThreadState


WARP_SIZE = 32


class WarpState(Enum):
    READY = "READY"
    RUNNING = "RUNNING"
    FINISHED = "FINISHED"
    STALLED = "STALLED"


class Warp:
    def __init__(self, warp_id):
        self.warp_id = warp_id
        self.threads = [Thread(i) for i in range(WARP_SIZE)]
        self.active_mask = [thread.active for thread in self.threads]
        self.pc: int = 0
        self.state = WarpState.READY

    def get_active_threads(self):
        return [
            thread
            for thread in self.threads
            if thread.state != ThreadState.FINISHED
        ]

    def is_done(self):
        for thread in self.threads:
            if thread.state != ThreadState.FINISHED:
                return False

        return True
