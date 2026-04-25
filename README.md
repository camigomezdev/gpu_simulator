# Simulador de GPU en Python

Simulacion educativa de un GPU con su jerarquia de componentes: Threads, Warps, Cores, SMs y memoria. Incluye un ISA (Instruction Set Architecture) propio y un assembler para escribir kernels.

## Arquitectura simulada

```
GPU
└── SMs (Streaming Multiprocessors)
     ├── Warp Scheduler
     ├── Cores (ejecutan instrucciones)
     ├── Shared Memory (por bloque)
     └── Warps
          └── 32 Threads (cada uno con sus propios registros)

Memoria
├── Global Memory  (compartida por todo el GPU, lenta)
└── Shared Memory  (por bloque, rapida)
```

**SIMT** — Single Instruction, Multiple Threads: un warp ejecuta la misma instruccion en sus 32 threads simultaneamente, pero cada thread opera sobre sus propios datos.

---

## Estructura del proyecto

```
modelo-gpu/
├── main.py
├── gpu/
│   ├── thread.py
│   ├── warp.py
│   ├── core.py
│   ├── scheduler.py
│   ├── memory.py
│   ├── sm.py
│   └── gpu.py
├── isa/
│   ├── opcodes.py
│   ├── instruction.py
│   └── assembler.py
├── kernels/
│   └── vector_add.asm
└── sim/
    └── runner.py
```

---

## Tareas en orden

### Fase 1 — ISA (el lenguaje del GPU)

**Tarea 1 — `isa/opcodes.py`**
Definir el conjunto de instrucciones del GPU.

- Crear un enum `Opcode` con las instrucciones soportadas:
  - Aritmetica: `ADD`, `SUB`, `MUL`, `DIV`, `ADDI` (con inmediato)
  - Memoria: `LOAD`, `STORE`
  - Control: `JMP`, `BEQ`, `BNE`
  - Especiales: `MOV`, `NOP`, `RET`, `GETID`
- `GETID` es la instruccion clave: le dice a cada thread cual es su indice

**Como probar:**
```python
from isa.opcodes import Opcode

print(Opcode.ADD)          # Opcode.ADD
print(Opcode.ADD.value)    # el valor asignado
print(list(Opcode))        # lista todos los opcodes
# Verificar que existen los 13 opcodes esperados
assert hasattr(Opcode, 'GETID')
assert hasattr(Opcode, 'BEQ')
```

---

**Tarea 2 — `isa/instruction.py`**
Representar una instruccion como objeto.

- Clase `Instruction` con campos: `opcode`, `dest`, `src1`, `src2`, `label`
- Metodo `__repr__` para debug: `"ADD R1 R2 R3"`
- Soportar operandos inmediatos (numeros literales) ademas de registros

**Como probar:**
```python
from isa.opcodes import Opcode
from isa.instruction import Instruction

i = Instruction(Opcode.ADD, dest='R1', src1='R2', src2='R3')
print(i)          # ADD R1 R2 R3

# Con inmediato
i2 = Instruction(Opcode.ADDI, dest='R1', src1='R2', src2=5)
print(i2)         # ADDI R1 R2 5

# Con label (para saltos)
i3 = Instruction(Opcode.JMP, label='loop')
print(i3)         # JMP loop
```

---

### Fase 2 — Componentes de hardware

**Tarea 3 — `gpu/thread.py`**
La unidad minima de ejecucion.

- Clase `Thread` con: `thread_id`, `registers` (dict), `pc`, `state`, `active`
- Estado posible: `READY | RUNNING | FINISHED | STALLED`
- Metodos `read_register(name)` y `write_register(name, value)`

**Como probar:**
```python
from gpu.thread import Thread

t = Thread(thread_id=7)
print(t.thread_id)   # 7
print(t.pc)          # 0
print(t.state)       # READY
print(t.active)      # True

t.write_register('R1', 42)
print(t.read_register('R1'))   # 42

# Leer registro que no existe debe retornar 0 (o lanzar error claro)
print(t.read_register('R99'))  # 0
```

---

**Tarea 4 — `gpu/warp.py`**
Grupo de 32 threads que ejecutan en lockstep.

- Clase `Warp` con: `warp_id`, `threads` (lista de 32), `active_mask`, `pc`, `state`
- Metodo `get_active_threads()` — retorna solo los threads activos
- Metodo `is_done()` — True si todos los threads terminaron
- Manejar **warp divergence**: cuando un branch divide los threads, ejecutar ambos caminos con mascaras distintas

**Como probar:**
```python
from gpu.warp import Warp

w = Warp(warp_id=0, start_thread_id=0)
print(len(w.threads))          # 32
print(w.is_done())             # False
print(len(w.get_active_threads()))  # 32

# Simular que la mitad de los threads terminan
for t in w.threads[:16]:
    t.active = False
print(len(w.get_active_threads()))  # 16
print(w.is_done())             # False

# Terminar todos
for t in w.threads:
    t.active = False
print(w.is_done())             # True
```

---

**Tarea 5 — `gpu/memory.py`**
Subsistema de memoria.

- Clase `GlobalMemory`: dict o lista como storage, metodos `read(addr)` y `write(addr, value)`, simular latencia con ciclos de espera
- Clase `SharedMemory`: una instancia por bloque, sin latencia, tamanio maximo configurable

**Como probar:**
```python
from gpu.memory import GlobalMemory, SharedMemory

gm = GlobalMemory()
gm.write(0, 99)
print(gm.read(0))    # 99
print(gm.latency)    # ciclos de espera (ej: 100)

# Shared memory — rapida, tamanio limitado
sm = SharedMemory(size=1024)
sm.write(0, 42)
print(sm.read(0))    # 42

# Verificar que SharedMemory no tiene latencia
# y que GlobalMemory si la tiene
```

---

**Tarea 6 — `gpu/core.py`**
El motor de ejecucion: aplica una instruccion a un thread.

- Clase `Core` con `core_id` y `busy`
- Metodo `execute(instruction, thread, memory)` que implementa cada opcode:
  - `ADD/SUB/MUL/DIV`: operaciones aritmeticas entre registros
  - `ADDI`: aritmetica con inmediato
  - `LOAD/STORE`: leer y escribir en memoria
  - `GETID`: escribir `thread.thread_id` en el registro destino
  - `MOV/NOP/RET`: utilidades
  - `JMP/BEQ/BNE`: modificar `thread.pc`

**Como probar:**
```python
from gpu.core import Core
from gpu.thread import Thread
from gpu.memory import GlobalMemory
from isa.opcodes import Opcode
from isa.instruction import Instruction

core = Core(core_id=0)
t = Thread(thread_id=5)
mem = GlobalMemory()

t.write_register('R1', 10)
t.write_register('R2', 3)

# ADD
core.execute(Instruction(Opcode.ADD, 'R3', 'R1', 'R2'), t, mem)
print(t.read_register('R3'))   # 13

# GETID
core.execute(Instruction(Opcode.GETID, 'R0'), t, mem)
print(t.read_register('R0'))   # 5

# LOAD / STORE
mem.write(0, 777)
core.execute(Instruction(Opcode.LOAD, 'R4', src1=0), t, mem)
print(t.read_register('R4'))   # 777
```

---

**Tarea 7 — `gpu/scheduler.py`**
Decide que warp ejecuta en cada ciclo.

- Clase `WarpScheduler` con lista de warps y politica (`round_robin` o `greedy`)
- Metodo `next_warp()` — retorna el proximo warp `READY`, saltando `WAITING` y `DONE`
- `round_robin`: rotar en orden circular
- `greedy`: siempre el primero disponible
- Cuando un warp hace `LOAD`, marcarlo `WAITING` por N ciclos (simula latencia de memoria y **latency hiding**)

**Como probar:**
```python
from gpu.warp import Warp
from gpu.scheduler import WarpScheduler

warps = [Warp(warp_id=i, start_thread_id=i*32) for i in range(4)]
sched = WarpScheduler(warps, policy='round_robin')

# Round robin: debe rotar entre warps
print(sched.next_warp().warp_id)   # 0
print(sched.next_warp().warp_id)   # 1
print(sched.next_warp().warp_id)   # 2

# Marcar warp 3 como WAITING, debe saltarlo
warps[3].state = 'WAITING'
sched2 = WarpScheduler(warps, policy='round_robin')
ids = [sched2.next_warp().warp_id for _ in range(6)]
print(ids)   # nunca debe aparecer 3
```

---

**Tarea 8 — `gpu/sm.py`**
El SM integra cores, warps, scheduler y memoria compartida.

- Clase `SM` con: `sm_id`, `cores`, `warps`, `scheduler`, `shared_memory`, referencia a `global_memory`
- Metodo `assign_block(block)` — crea los warps a partir de un bloque de threads
- Metodo `step()` — ejecuta un ciclo de simulacion:
  1. Pedir al scheduler el siguiente warp
  2. Fetch de la instruccion en `warp.pc`
  3. Ejecutar en todos los threads activos del warp (un core por thread)
  4. Avanzar `warp.pc`
  5. Retornar `True` si quedan warps sin terminar

**Como probar:**
```python
from gpu.sm import SM
from gpu.memory import GlobalMemory
from isa.opcodes import Opcode
from isa.instruction import Instruction

program = [
    Instruction(Opcode.GETID, 'R0'),
    Instruction(Opcode.RET),
]
gm = GlobalMemory()
sm = SM(sm_id=0, num_cores=32, global_memory=gm)

block = {'block_id': 0, 'threads': list(range(32))}
sm.assign_block(block, program)

# Ejecutar ciclos hasta terminar
while sm.step():
    pass

# Verificar que cada thread tiene su ID en R0
for warp in sm.warps:
    for t in warp.threads:
        print(t.thread_id, t.read_register('R0'))  # deben coincidir
```

---

**Tarea 9 — `gpu/gpu.py`**
El GPU completo: coordina los SMs y lanza kernels.

- Clase `GPU` con: `num_sms`, `sms`, `global_memory`, `config`
- Metodo `launch_kernel(program, grid_dim, block_dim)`:
  1. Calcular total de bloques
  2. Distribuir bloques entre SMs (round-robin)
  3. Cada SM recibe sus bloques via `assign_block()`
- Metodo `run()` — loop hasta que todos los SMs terminen, contar ciclos

**Como probar:**
```python
from gpu.gpu import GPU
from isa.opcodes import Opcode
from isa.instruction import Instruction

program = [
    Instruction(Opcode.GETID, 'R0'),
    Instruction(Opcode.RET),
]
gpu = GPU(num_sms=2, cores_per_sm=32)
gpu.launch_kernel(program, grid_dim=4, block_dim=32)
stats = gpu.run()

print(stats['cycles'])        # numero de ciclos totales
print(stats['instructions'])  # instrucciones ejecutadas
# Con 4 bloques en 2 SMs, cada SM debe haber procesado 2 bloques
```

---

### Fase 3 — Assembler y kernels

**Tarea 10 — `isa/assembler.py`**
Convierte texto plano a lista de instrucciones.

- Funcion `assemble(source: str) -> list[Instruction]`
- Parsear linea por linea: ignorar comentarios (`#`) y lineas vacias
- Detectar labels (terminan en `:`) y resolver saltos a indices numericos
- Retornar lista de objetos `Instruction` lista para ejecutar

**Como probar:**
```python
from isa.assembler import assemble

source = """
# Suma simple
    GETID R0
    ADDI  R1 R0 10
loop:
    NOP
    BNE   R0 R1 loop
    RET
"""
program = assemble(source)
print(len(program))       # 5 instrucciones (sin comentarios ni vacias)
print(program[0])         # GETID R0
print(program[3])         # BNE R0 R1 2  <- label resuelta a indice
```

---

**Tarea 11 — `kernels/vector_add.asm`**
Primer kernel real escrito en el ISA propio.

- Suma de dos vectores A y B, resultado en C
- Cada thread calcula `C[i] = A[i] + B[i]` usando `GETID` para obtener su indice
- Asumir layout en memoria: `A` en `[0..N)`, `B` en `[N..2N)`, `C` en `[2N..3N)`

**Como probar:**
```python
from isa.assembler import assemble

with open("kernels/vector_add.asm") as f:
    program = assemble(f.read())

# Verificar que ensambla sin errores
print(len(program), "instrucciones")

# Inspeccion manual: la primera instruccion debe ser GETID
print(program[0])   # GETID Rx

# La ultima debe ser RET
print(program[-1])  # RET
```
La prueba real es correrlo con el GPU completo en la Tarea 13.

---

### Fase 4 — Integracion

**Tarea 12 — `sim/runner.py`**
Orquesta la ejecucion completa.

- Clase `SimRunner` con metodos:
  - `load_data(array_a, array_b, n)` — escribe inputs en global memory
  - `run_kernel(program, grid_dim, block_dim)` — ensambla, lanza, corre y lee resultados
  - `print_stats(stats)` — imprime ciclos, instrucciones, throughput

**Como probar:**
```python
from gpu.gpu import GPU
from sim.runner import SimRunner

gpu = GPU(num_sms=2, cores_per_sm=32)
runner = SimRunner(gpu)

N = 32
A = list(range(N))
B = list(range(N, 2*N))
runner.load_data(A, B, N)

# Verificar que la memoria global tiene los datos correctos
print(gpu.global_memory.read(0))    # 0  (A[0])
print(gpu.global_memory.read(N))    # 32 (B[0])
```

---

**Tarea 13 — `main.py`**
Demo y validacion end-to-end.

- Configurar el GPU
- Crear arrays de prueba, cargarlos, ejecutar `vector_add`
- Verificar que `C[i] == A[i] + B[i]` para todo `i`
- Imprimir estadisticas

**Como probar:**
```bash
python main.py
```
Salida esperada:
```
Ciclos totales: <N>
Instrucciones ejecutadas: <N>
Resultado correcto: True
```
Si `Resultado correcto` es `False`, revisar la cadena hacia atras: primero `core.py` (ejecuta bien ADD/LOAD/STORE?), luego `assembler.py` (resuelve bien las direcciones?), luego `vector_add.asm` (el layout de memoria es correcto?).

---

## Conceptos clave

| Concepto | Descripcion |
|----------|-------------|
| **SIMT** | 32 threads ejecutan la misma instruccion, datos distintos |
| **Warp divergence** | Un branch divide el warp — se ejecutan ambos caminos con mascara |
| **Latency hiding** | Mientras un warp espera memoria, el scheduler corre otro |
| **Occupancy** | Cuantos warps activos caben en un SM (limitado por registros y shared memory) |
| **Active mask** | Bitmask que indica que threads del warp estan activos en este ciclo |

## Ejemplo de uso (objetivo final)

```python
gpu = GPU(num_sms=4, cores_per_sm=32)
runner = SimRunner(gpu)

N = 128
runner.load_data(A=list(range(N)), B=list(range(N, 2*N)), n=N)

with open("kernels/vector_add.asm") as f:
    stats = runner.run_kernel(f.read(), grid_dim=4, block_dim=32)

runner.print_stats(stats)
# Ciclos totales: 42
# Instrucciones ejecutadas: 1024
# Resultado correcto: True
```
