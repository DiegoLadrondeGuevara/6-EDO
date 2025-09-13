# Generaré las gráficas y algunos números clave (valores finales) para los casos pedidos.
import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import matplotlib.pyplot as plt

# Parámetros propuestos (puedes cambiarlos si quieres)
K = 100.0     # capacidad de carga
N0 = 5.0      # condición inicial N(0)
r = 0.5       # tasa inicial
r_prime = 0.2 # tasa tras terapia (r' < r)

# Funciones Gompertz
def N_no_therapy(t, K, N0, r):
    return K * np.exp(np.log(N0 / K) * np.exp(-r * t))

def N_with_therapy(t, K, N0, r, r_prime, t0):
    # Para t < t0 regresamos la solución sin terapia.
    t = np.array(t)
    N = np.empty_like(t, dtype=float)
    mask_before = t < t0
    mask_after = ~mask_before
    # antes de t0
    N[mask_before] = N_no_therapy(t[mask_before], K, N0, r)
    # valor en t0
    N_t0 = N_no_therapy(t0, K, N0, r)
    # después de t0, usar N(t0) como condición inicial con r' y tiempo desplazado
    # N(t) = K * exp( ln(N_t0/K) * exp(-r'*(t-t0)) )
    N[mask_after] = K * np.exp(np.log(N_t0 / K) * np.exp(-r_prime * (t[mask_after] - t0)))
    return N

# Tiempo de evaluación
t_max = 40
t = np.linspace(0, t_max, 400)

# (a) Comparación con y sin terapia para t0 = 5
t0_a = 5.0
N_no = N_no_therapy(t, K, N0, r)
N_ther = N_with_therapy(t, K, N0, r, r_prime, t0_a)

plt.figure(figsize=(8,5))
plt.plot(t, N_no, label='Sin terapia')
plt.plot(t, N_ther, label=f'Con terapia (t0={t0_a})')
plt.xlabel('t')
plt.ylabel('N(t)')
plt.title('Comparación: sin terapia vs con terapia (t0=5)')
plt.legend()
plt.grid(alpha=0.3)
plt.show()

# (b) Comparación para 3 valores de t0 (2, 5, 8)
t0_vals = [2.0, 5.0, 8.0]
plt.figure(figsize=(8,5))
for tt0 in t0_vals:
    Ntmp = N_with_therapy(t, K, N0, r, r_prime, tt0)
    plt.plot(t, Ntmp, label=f't0={tt0}')
# también mostramos la curva sin terapia como referencia
plt.plot(t, N_no, label='Sin terapia', linestyle='--')
plt.xlabel('t')
plt.ylabel('N(t)')
plt.title('Comparación: terapia aplicada en distintos tiempos t0')
plt.legend()
plt.grid(alpha=0.3)
plt.show()

# Imprimir valores finales (t = 40) y valores en t0
t_eval = [t0_a, 30, 40]
print("Valores clave para el caso t0 = 5 (ejemplo elegido):")
print(f"N(0) = {N_no_therapy(0, K, N0, r):.4f}")
print(f"N({t0_a}) sin terapia = {N_no_therapy(t0_a, K, N0, r):.4f}")
print(f"N({t0_a}) con terapia (valor inicial para fase r') = {N_with_therapy(t0_a, K, N0, r, r_prime, t0_a):.4f}")
print(f"N(30) sin terapia = {N_no_therapy(30, K, N0, r):.4f}")
print(f"N(30) con terapia (t0={t0_a}) = {N_with_therapy(30, K, N0, r, r_prime, t0_a):.4f}")
print(f"N(40) sin terapia = {N_no_therapy(40, K, N0, r):.4f}")
print(f"N(40) con terapia (t0={t0_a}) = {N_with_therapy(40, K, N0, r, r_prime, t0_a):.4f}")

# Valores finales para los 3 t0
print("\nComparación de N(40) para distintos t0:")
for tt0 in t0_vals:
    print(f"t0={tt0}: N(40) = {N_with_therapy(40, K, N0, r, r_prime, tt0):.4f}")
print(f"Sin terapia: N(40) = {N_no_therapy(40, K, N0, r):.4f}")
