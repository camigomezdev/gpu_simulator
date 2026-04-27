# gpu/gpu.py — El GPU completo: coleccion de SMs + memoria global
#
# TAREAS:
#   1. Clase GPU con:
#        - num_sms        (cuantos SMs tiene el GPU)
#        - sms            (lista de objetos SM)
#        - global_memory  (objeto GlobalMemory compartido por todos los SMs)
#        - config         (dict con parametros: warp_size, max_blocks_per_sm, etc.)
#
#   2. Metodo launch_kernel(kernel, grid_dim, block_dim) -> None
#      Simula el lanzamiento de un kernel:
#        a. Calcular total de bloques = grid_dim_x * grid_dim_y
#        b. Distribuir bloques entre SMs (round-robin o greedy)
#        c. Cada SM recibe sus bloques via assign_block()
#
#   3. Metodo run() -> SimStats
#      Ejecutar todos los SMs hasta que terminen todos los warps:
#        - Loop: llamar sm.step() en cada SM activo
#        - Contar ciclos totales
#        - Retornar estadisticas (ciclos, instrucciones ejecutadas, etc.)
#
#   EJEMPLO DE CONFIGURACION (tipo RTX 3080 simplificado):
#     num_sms = 68
#     cores_per_sm = 128
#     warp_size = 32
#     max_warps_per_sm = 48
#     shared_memory_per_sm = 100 * 1024  # 100 KB

from .memory import GlobalMemory
from .sm import SM
from .thread import Thread


class GPU:
    def __init__(
            self, num_sms: int = 68,
            cores_per_sm: int = 68,
            warp_size: int = 32,
            max_warps_per_sm: int = 48,
            shared_memory_per_sm: int = (100 * 1024)
    ):
        self.global_memory = GlobalMemory()
        self.sms = [SM(idx,
                       cores_per_sm,
                       self.global_memory)
                    for idx in range(num_sms)]
        self.config = {
            "num_sms": num_sms,
            "cores_per_sm": cores_per_sm,
            "warp_size": warp_size,
            "max_blocks_per_sm": max_warps_per_sm,
            "shared_memory_per_sm": shared_memory_per_sm
        }

    def launch_kernel(self, kernel, grid_dim, block_dim: list) -> None:
        blocks = []
        self.instructions = kernel
        for blockIdx in range(grid_dim):
            blocks.append([Thread(threadIdx + (blockIdx * block_dim))
                          for threadIdx in range(block_dim)])

        for i, block in enumerate(blocks):
            self.sms[i % len(self.sms)].assign_block(block)
            self.sms[i % len(self.sms)].assign_instructions(kernel)

    def run(self):
        results = [sm.step() for sm in self.sms]
        cycles = 1
        while any(results):
            results = [sm.step() for sm in self.sms]
            cycles += 1

        return {
            "cycles": cycles,
            "warps_completed": len(self.sms) * self.config["warp_size"],
        }
