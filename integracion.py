#!/usr/bin/env python3

import math


def riemann_izquierdo(f, a, b, n):
    """Aproximación por sumas de Riemann usando el extremo izquierdo.

    Args:
        f (callable): función a integrar.
        a (float): límite inferior.
        b (float): límite superior.
        n (int): número de subintervalos.

    Returns:
        float: aproximación de la integral.
    """
    h = (b - a) / n  # Paso entre subintervalos
    suma = 0
    for i in range(n):
        x_i = a + i * h  # Extremo izquierdo del subintervalo i
        suma += f(x_i) * h
    return suma


def riemann_derecho(f, a, b, n):
    """Aproximación por sumas de Riemann usando el extremo derecho.

    Args:
        f (callable): función a integrar.
        a (float): límite inferior.
        b (float): límite superior.
        n (int): número de subintervalos.

    Returns:
        float: aproximación de la integral.
    """
    h = (b - a) / n  # Paso entre subintervalos
    suma = 0
    for i in range(1, n + 1):
        x_i = a + i * h  # Extremo derecho del subintervalo i
        suma += f(x_i) * h
    return suma


def riemann_punto_medio(f, a, b, n):
    """Aproximación por sumas de Riemann usando el punto medio.

    Args:
        f (callable): función a integrar.
        a (float): límite inferior.
        b (float): límite superior.
        n (int): número de subintervalos.

    Returns:
        float: aproximación de la integral.
    """
    h = (b - a) / n  # Paso entre subintervalos
    suma = 0
    for i in range(n):
        x_i = a + (i + 0.5) * h  # Punto medio del subintervalo i
        suma += f(x_i) * h
    return suma


def integrar(f, a, b, n=100, metodo="punto_medio"):
    """Integración numérica por el método de Riemann.

    Args:
        f (callable): función a integrar.
        a (float): límite inferior.
        b (float): límite superior.
        n (int): número de subintervalos.
        metodo (str): "izquierdo", "derecho" o "punto_medio".

    Returns:
        float: aproximación de la integral.
    """
    if metodo == "izquierdo":
        return riemann_izquierdo(f, a, b, n)
    elif metodo == "derecho":
        return riemann_derecho(f, a, b, n)
    elif metodo == "punto_medio":
        return riemann_punto_medio(f, a, b, n)
    else:
        raise ValueError("Método no reconocido. Use: 'izquierdo', 'derecho' o 'punto_medio'.")


if __name__ == "__main__":
    f = lambda x: x ** 2
    a, b = 0, 1
    n = 10

    valor_exacto = 1 / 3
    print("Integral de f(x) = x² en [0, 1] - Método de Riemann")
    print(f"Valor exacto: {valor_exacto:.10f}\n")

    izq = riemann_izquierdo(f, a, b, n)
    print(f"Riemann izquierdo (n={n}): {izq:.10f}")
    print(f"Error: {abs(izq - valor_exacto):.2e}\n")

    der = riemann_derecho(f, a, b, n)
    print(f"Riemann derecho (n={n}): {der:.10f}")
    print(f"Error: {abs(der - valor_exacto):.2e}\n")

    medio = riemann_punto_medio(f, a, b, n)
    print(f"Riemann punto medio (n={n}): {medio:.10f}")
    print(f"Error: {abs(medio - valor_exacto):.2e}")
