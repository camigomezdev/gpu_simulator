# sim/runner.py — Orquesta el lanzamiento de un kernel y reporta resultados
#
# TAREAS:
#   1. Clase SimRunner con:
#        - gpu      (objeto GPU)
#        - memory   (referencia a global_memory para cargar datos iniciales)
#
#   2. Metodo load_data(array_a, array_b, n) -> None
#      Escribe los arrays de entrada en global_memory antes de correr el kernel
#
#   3. Metodo run_kernel(program, grid_dim, block_dim) -> dict
#      a. Ensamblar el programa (assembler.assemble(program))
#      b. Lanzar gpu.launch_kernel(...)
#      c. Correr gpu.run()
#      d. Leer resultados de global_memory
#      e. Retornar {"result": [...], "cycles": N, "instructions": M}
#
#   4. Metodo print_stats(stats) -> None
#      Imprimir un resumen legible de la simulacion:
#        Ciclos totales: 42
#        Instrucciones ejecutadas: 1024
#        Warps completados: 32
#        Throughput: X instrucciones/ciclo
