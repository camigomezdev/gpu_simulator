# gpu/memory.py — Subsistema de memoria del GPU
#
# TAREAS:
#   1. Clase GlobalMemory:
#        - storage (dict o lista — el "DRAM" del GPU, compartido por todos)
#        - Metodos: read(addr) y write(addr, value)
#        - Simular latencia: read retorna el valor pero marca N ciclos de espera
#
#   2. Clase SharedMemory:
#        - Una instancia por bloque (no por SM — importante)
#        - Mucho mas rapida que global memory (sin latencia en la sim educativa)
#        - Metodos: read(addr) y write(addr, value)
#        - Tamaño maximo configurable (en hardware real: 48KB o 96KB por SM)
#
#   3. Clase RegisterFile:
#        - Una instancia por thread (o representarla directamente en Thread)
#        - En hardware real: 65536 registros de 32-bit por SM, particionados
#          entre todos los threads activos — esto limita la occupancy
#
#   CONCEPTO: MEMORY HIERARCHY (de rapida a lenta)
#     Registros > Shared Memory > L1 Cache > L2 Cache > Global Memory (DRAM)
#     Para la sim educativa modelar solo: Registros + Shared + Global
