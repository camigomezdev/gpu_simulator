# main.py — Punto de entrada y demo del GPU simulado
#
# TAREAS:
#   1. Configurar el GPU (num_sms, cores_per_sm, etc.)
#   2. Crear arrays de prueba A y B de tamaño N
#   3. Cargarlos en memoria global
#   4. Ejecutar el kernel vector_add con grid_dim y block_dim apropiados
#   5. Verificar que C[i] == A[i] + B[i] para todo i
#   6. Imprimir estadisticas de la simulacion
#
# EJEMPLO DE USO ESPERADO (cuando todo este implementado):
#
#   gpu = GPU(num_sms=4, cores_per_sm=32)
#   runner = SimRunner(gpu)
#
#   N = 128
#   A = list(range(N))
#   B = list(range(N, 2*N))
#
#   runner.load_data(A, B, N)
#
#   with open("kernels/vector_add.asm") as f:
#       program = f.read()
#
#   stats = runner.run_kernel(program, grid_dim=4, block_dim=32)
#   runner.print_stats(stats)
#
#   assert stats["result"] == [A[i] + B[i] for i in range(N)], "ERROR"
#   print("Resultado correcto!")

from random import randint
from sim.runner import SimRunner


# Resultado esperado calculado en CPU (ground truth)
N = 128
A = [randint(0, N) for _ in range(N)]
B = [randint(0, N) for _ in range(N)]
mul = [a * b for a, b in zip(A, B)]  # [11, 22, 33, 44]
expected = sum(i for i in mul)
sim = SimRunner()


program = open('kernels/dot_product.asm')
instructions = program.read()
program.close()


print("-------")
sim.reset()
sim.load_data(A, B, N)
stats = sim.run_kernel(instructions, 4, 32, registers={
                       "R7": N, "R9": 1}, result_count=1)
sim.print_stats(stats)


print("-------")
# sim.print_stats(stats)
# Resultado del GPU simulado
gpu_result = stats["results"]

print(gpu_result)


# Verificación
assert gpu_result == expected, f"Error: {gpu_result} != {expected}"
print("OK")
