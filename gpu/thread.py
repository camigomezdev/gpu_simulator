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
