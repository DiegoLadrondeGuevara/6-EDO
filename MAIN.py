import matplotlib
matplotlib.use('TkAgg')

import numpy as np
import matplotlib.pyplot as plt

# Parámetros del modelo
K = 100.0     # capacidad de carga
N0 = 5.0      # población inicial
r = 0.5       # tasa de crecimiento inicial
r_prime = 0.2 # tasa de crecimiento después de terapia (más baja)

# Solución de Gompertz sin terapia
def N_no_therapy(t, K, N0, r):
    return K * np.exp(np.log(N0 / K) * np.exp(-r * t))

# Solución con cambio de tasa en t0 (aplicación de terapia)
def N_with_therapy(t, K, N0, r, r_prime, t0):
    t = np.array(t)
    N = np.empty_like(t, dtype=float)

    antes = t < t0
    despues = ~antes

    N[antes] = N_no_therapy(t[antes], K, N0, r)
    N_t0 = N_no_therapy(t0, K, N0, r)

    N[despues] = K * np.exp(np.log(N_t0 / K) * np.exp(-r_prime * (t[despues] - t0)))
    return N

# Rango de tiempo
t_max = 40
t = np.linspace(0, t_max, 400)

# (a) Comparación con y sin terapia, con t0 = 5
t0_a = 5.0
N_no = N_no_therapy(t, K, N0, r)
N_ther = N_with_therapy(t, K, N0, r, r_prime, t0_a)

plt.figure(figsize=(8, 5))
plt.plot(t, N_no, label='Sin terapia', color='steelblue')
plt.plot(t, N_ther, label=f'Con terapia (t0={t0_a})', color='crimson')
plt.xlabel('t')
plt.ylabel('N(t)')
plt.title('Comparación: sin terapia vs con terapia (t0 = 5)')
plt.legend()
plt.grid(alpha=0.3)
plt.show()

# (b) Comparación para distintos t0 (2, 5, 8)
t0_vals = [2.0, 5.0, 8.0]
plt.figure(figsize=(8, 5))

colores = ['darkorange', 'green', 'purple']
for i, tt0 in enumerate(t0_vals):
    N_tmp = N_with_therapy(t, K, N0, r, r_prime, tt0)
    plt.plot(t, N_tmp, label=f't0 = {tt0}', color=colores[i])

plt.plot(t, N_no, label='Sin terapia', linestyle='--', color='gray')
plt.xlabel('t')
plt.ylabel('N(t)')
plt.title('Terapia aplicada en distintos tiempos')
plt.legend()
plt.grid(alpha=0.3)
plt.show()

# Valores numéricos clave
print("Valores clave para el caso t0 = 5:")
print(f"N(0) = {N_no_therapy(0, K, N0, r):.4f}")
print(f"N({t0_a}) sin terapia = {N_no_therapy(t0_a, K, N0, r):.4f}")
print(f"N({t0_a}) con terapia = {N_with_therapy(t0_a, K, N0, r, r_prime, t0_a):.4f}")
print(f"N(30) sin terapia = {N_no_therapy(30, K, N0, r):.4f}")
print(f"N(30) con terapia = {N_with_therapy(30, K, N0, r, r_prime, t0_a):.4f}")
print(f"N(40) sin terapia = {N_no_therapy(40, K, N0, r):.4f}")
print(f"N(40) con terapia = {N_with_therapy(40, K, N0, r, r_prime, t0_a):.4f}")

print("\nComparación de N(40) para distintos t0:")
for tt0 in t0_vals:
    print(f"t0 = {tt0}: N(40) = {N_with_therapy(40, K, N0, r, r_prime, tt0):.4f}")
print(f"Sin terapia: N(40) = {N_no_therapy(40, K, N0, r):.4f}")
