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
