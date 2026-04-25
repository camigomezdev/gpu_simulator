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
