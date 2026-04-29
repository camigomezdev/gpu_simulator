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

from sim.runner import SimRunner


# Resultado esperado calculado en CPU (ground truth)
N = 128
A = [i for i in range(N)]
B = [i*10 for i in range(N)]
expected = [a + b for a, b in zip(A, B)]  # [11, 22, 33, 44]

sim = SimRunner()


program = open('kernels/vector_add.asm')
instructions = program.read()
program.close()

for grid_dim, block_dim in [(8, 16), (4, 32), (2, 64), (1, 128)]:
    print("-------")
    sim.reset()
    sim.load_data(A, B, N)
    stats = sim.run_kernel(instructions, grid_dim, block_dim)
    sim.print_stats(stats)
    

print("-------")
# sim.print_stats(stats)
# Resultado del GPU simulado
gpu_result = stats["results"]


# Verificación
assert gpu_result == expected, f"Error: {gpu_result} != {expected}"
print("OK")
