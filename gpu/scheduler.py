# gpu/scheduler.py — Warp Scheduler: decide qué warp ejecuta en cada ciclo
#
# TAREAS:
#   1. Clase WarpScheduler con:
#        - warps (lista de warps asignados al SM)
#        - policy (str: "round_robin" | "greedy")
#
#   2. Metodo next_warp() -> Warp | None
#      Retorna el proximo warp listo para ejecutar segun la politica.
#
#   POLITICAS A IMPLEMENTAR:
#     round_robin: rotar entre warps en orden circular, saltar los WAITING/DONE
#     greedy:      siempre ejecutar el primer warp READY disponible
#
#   CONCEPTO CLAVE — LATENCY HIDING:
#     Cuando un warp hace LOAD de memoria (latencia alta), el scheduler
#     cambia a otro warp listo. Esto es como los GPUs "esconden" la latencia
#     de memoria — ocupan los cores con otros warps mientras esperan datos.
#     Para simular: cuando un warp hace LOAD, marcarlo como WAITING por N ciclos.

from enum import Enum
from .warp import Warp, WarpState


class Policy(Enum):
    GREEDY = "greedy"
    ROUND_ROBIN = "round_robin"


class WarpScheduler:
    def __init__(self, warps: list[Warp], policy: Policy = Policy.GREEDY):
        self.warps = warps
        self.policy: str = policy
        self.current_warp = 0

    def next_warp(self) -> Warp | None:
        if self.policy == Policy.ROUND_ROBIN:
            return self._round_robin_next()

        return self._greedy_next()

    def _round_robin_next(self):
        for idx in range(self.current_warp, len(self.warps)):
            if self.warps[idx % len(self.warps)].state == WarpState.READY:
                self.current_warp = (idx + 1) % len(self.warps)
                return self.warps[idx % len(self.warps)]
        return None

    def _greedy_next(self):
        for warp in self.warps:
            if warp.state == WarpState.READY and not warp.is_done():
                return warp
        return None
