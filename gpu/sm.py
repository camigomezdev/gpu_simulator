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
