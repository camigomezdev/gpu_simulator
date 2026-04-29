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


class Memory:
    LATANCY = 0

    def __init__(self):
        self.storage = {}

    def read(self, addr):
        return self.storage.get(addr, 0), self.LATANCY

    def write(self, addr, value):
        self.storage[addr] = value
        return addr


class GlobalMemory(Memory):
    LATANCY = 100


class SharedMemory(Memory):
    def __init__(self, max_size):
        super().__init__()
        self.max_size = max_size

    def write(self, addr, value) -> None:
        
        if addr < self.max_size:
            print(len(self.storage), self.max_size)
            self.storage[addr] = value
            return addr
        raise MemoryError


class RegisterFile:
    def __init__(self):
        self.regs = {}

    def read(self, reg_name):
        return self.regs.get(reg_name, 0)

    def write(self, reg_name, value):
        self.regs[reg_name] = value
    
    def __str__(self):
        return str(self.regs)
