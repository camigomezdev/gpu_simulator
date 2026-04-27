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

from gpu.gpu import GPU
from gpu.memory import GlobalMemory
from isa.assembler import assemble


class SimRunner:
    def __init__(self):
        self.gpu = GPU()
        self.n = 0

    def load_data(self, array_a, array_b, n):
        self.n = n

        for i in range(n):
            self.gpu.global_memory.write(i, array_a[i])
            self.gpu.global_memory.write(i + n, array_b[i])

    def run_kernel(self, program, grid_dim, block_dim):
        instructions = assemble(program)
        self.gpu.launch_kernel(instructions, grid_dim, block_dim)

        for sm in self.gpu.sms:
            for warp in sm.scheduler.warps:
                for thread in warp.threads:
                    thread.write_register("R7", self.n)

        stats = self.gpu.run()

        results = [self.gpu.global_memory.read(
            idx + self.n * 2)[0] for idx in range(self.n)]
        stats["results"] = results
        stats["excecuted_instructions"] = len(instructions)
        return stats

    def print_stats(self, stats):
        print(f"Cycles: {stats['cycles']}")
        print(f"Instrucciones ejecutadas: {stats['excecuted_instructions']}")
        print(f"Warps completados: {stats['warps_completed']}")
        print(
            f"Throughput: {stats['excecuted_instructions'] / stats['cycles']}")
