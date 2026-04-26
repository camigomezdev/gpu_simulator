# Contexto del proyecto para Claude

Simulador educativo de GPU en Python. El usuario es nuevo en arquitectura GPU y esta aprendiendo los conceptos implementandolos desde cero. **No implementar codigo por el — solo orientar, explicar y evaluar con `/evaluar`.**

## Estado de las tareas

### Fase 1 — ISA
- [x] `isa/opcodes.py` — enum de opcodes (ADD, SUB, MUL, DIV, LOAD, STORE, JMP, BEQ, BNE, MOV, NOP, RET, GETID)
- [x] `isa/instruction.py` — clase Instruction con opcode, dest, src1, src2, label

### Fase 2 — Hardware
- [x] `gpu/thread.py` — Thread: registers (dict), pc, state, active
- [x] `gpu/warp.py` — Warp: 32 threads, active_mask, SIMT, divergencia
- [x] `gpu/memory.py` — GlobalMemory + SharedMemory
- [x] `gpu/core.py` — execute(instruction, thread, memory) con todos los opcodes
- [x] `gpu/scheduler.py` — WarpScheduler: round_robin y greedy, latency hiding
- [ ] `gpu/sm.py` — SM: assign_block(), step()
- [ ] `gpu/gpu.py` — GPU: launch_kernel(), run()

### Fase 3 — Assembler y kernels
- [ ] `isa/assembler.py` — parser texto → list[Instruction], resolver labels
- [ ] `kernels/vector_add.asm` — kernel de suma de vectores en ISA propio

### Fase 4 — Integracion
- [ ] `sim/runner.py` — load_data(), run_kernel(), print_stats()
- [ ] `main.py` — demo y validacion end-to-end

## Como actualizar este archivo

Cuando el usuario complete una tarea, cambiar `[ ]` por `[x]`. Ejemplo:
```
- [x] `isa/opcodes.py` — completado
```

## Perfil del usuario
- Nuevo en arquitectura GPU (no conoce warps, SMs, SIMT de antes)
- Quiere aprender haciendo, no que le den el codigo
- Nivel educativo / conceptual — sin cycle-accuracy
- Quiere ejecutar kernels simples y definir su propio ISA

## Skill disponible
- `/evaluar` — evalua lo implementado como un profesor: puntos positivos, problemas y pistas. No da soluciones directas.

## Orden de dependencias
```
opcodes → instruction → thread → warp → memory → core → scheduler → sm → gpu → assembler → vector_add.asm → runner → main
```
Cada componente depende de los anteriores. Si algo no funciona, revisar la cadena hacia atras.
