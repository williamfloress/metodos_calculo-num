#!/usr/bin/env python3
"""
Controlador de metodos numericos con menu interactivo.
Importa biseccion, Newton-Raphson, integracion (Riemann) y polinomio de Taylor.
Permite al usuario elegir metodo y ejercicio para resolver.
"""

import importlib.util
import math
import os

import biseccion
import newton_raphson
import integracion

# Cargar polinomio-de-taylor (nombre con guion)
_taylor_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "polinomio-de-taylor.py")
if os.path.isfile(_taylor_path):
    _spec = importlib.util.spec_from_file_location("polinomio_taylor", _taylor_path)
    polinomio_taylor = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(polinomio_taylor)
else:
    polinomio_taylor = None


def resolver_raiz_biseccion(f, a, b, er=0.01, n=100, mostrar_proceso=True):
    """Resuelve la ecuacion f(x)=0 usando el metodo de biseccion."""
    return biseccion.biseccion(f, a, b, er, n, mostrar_proceso)


def resolver_raiz_newton(f, df, x0, er=0.01, n=100, mostrar_proceso=True):
    """Resuelve la ecuacion f(x)=0 usando Newton-Raphson."""
    return newton_raphson.newton_raphson(f, df, x0, er, n, mostrar_proceso)


def resolver_integral(f, a, b, n=100, metodo="punto_medio"):
    """Aproxima la integral de f en [a, b] usando Riemann."""
    return integracion.integrar(f, a, b, n, metodo)


def resolver_taylor(f, a, n, x_eval=None, mostrar_proceso=True):
    """Calcula el polinomio de Taylor de f alrededor de a y lo evalua en x_eval."""
    if polinomio_taylor is None:
        raise ImportError("Modulo polinomio-de-taylor no disponible (requiere sympy).")
    return polinomio_taylor.polinomio_taylor(f, a, n, x_eval=x_eval, mostrar_proceso=mostrar_proceso)


# 5 ejercicios por metodo, integrados en el script
EJERCICIOS_BISECCION = [
    {
        "nombre": "x^2 - 2 = 0 (raiz sqrt(2))",
        "f": lambda x: x**2 - 2,
        "a": 0, "b": 2, "er": 0.01, "n": 100,
    },
    {
        "nombre": "x^3 - 2 = 0 (raiz 2^(1/3))",
        "f": lambda x: x**3 - 2,
        "a": 0, "b": 2, "er": 0.001, "n": 100,
    },
    {
        "nombre": "e^(-x) - ln(x) = 0",
        "f": lambda x: math.exp(-x) - math.log(x),
        "a": 1, "b": 1.5, "er": 0.01, "n": 100,
    },
    {
        "nombre": "cos(x) - x = 0",
        "f": lambda x: math.cos(x) - x,
        "a": 0, "b": 1, "er": 0.01, "n": 100,
    },
    {
        "nombre": "x^2 - 5 = 0 (raiz sqrt(5))",
        "f": lambda x: x**2 - 5,
        "a": 2, "b": 3, "er": 0.01, "n": 100,
    },
]

EJERCICIOS_NEWTON = [
    {
        "nombre": "x^2 - 2 = 0 (raiz sqrt(2))",
        "f": lambda x: x**2 - 2,
        "df": lambda x: 2 * x,
        "x0": 1.5, "er": 0.01, "n": 50,
    },
    {
        "nombre": "x^3 - 2 = 0 (raiz 2^(1/3))",
        "f": lambda x: x**3 - 2,
        "df": lambda x: 3 * x**2,
        "x0": 1.2, "er": 0.001, "n": 50,
    },
    {
        "nombre": "e^(-x) - ln(x) = 0",
        "f": lambda x: math.exp(-x) - math.log(x),
        "df": lambda x: -math.exp(-x) - 1 / x,
        "x0": 1.2, "er": 0.01, "n": 50,
    },
    {
        "nombre": "cos(x) - x = 0",
        "f": lambda x: math.cos(x) - x,
        "df": lambda x: -math.sin(x) - 1,
        "x0": 0.5, "er": 0.01, "n": 50,
    },
    {
        "nombre": "x^2 - 5 = 0 (raiz sqrt(5))",
        "f": lambda x: x**2 - 5,
        "df": lambda x: 2 * x,
        "x0": 2.5, "er": 0.01, "n": 50,
    },
]

EJERCICIOS_RIEMANN = [
    {
        "nombre": "Integral x^2 en [0, 1] (valor exacto 1/3)",
        "f": lambda x: x**2,
        "a": 0, "b": 1, "n": 20, "metodo": "punto_medio",
    },
    {
        "nombre": "Integral e^x en [0, 1] (valor exacto e - 1)",
        "f": lambda x: math.exp(x),
        "a": 0, "b": 1, "n": 30, "metodo": "punto_medio",
    },
    {
        "nombre": "Integral sin(x) en [0, pi] (valor exacto 2)",
        "f": lambda x: math.sin(x),
        "a": 0, "b": math.pi, "n": 30, "metodo": "punto_medio",
    },
    {
        "nombre": "Integral x en [0, 2] con Riemann izquierdo",
        "f": lambda x: x,
        "a": 0, "b": 2, "n": 50, "metodo": "izquierdo",
    },
    {
        "nombre": "Integral sqrt(x) en [0, 1] (valor exacto 2/3)",
        "f": lambda x: math.sqrt(x),
        "a": 0, "b": 1, "n": 30, "metodo": "punto_medio",
    },
]

EJERCICIOS_TAYLOR = [
    {"nombre": "e^x en a=0, n=4, evaluar en x=0.5", "f": lambda x: math.exp(x), "a": 0, "n": 4, "x_eval": 0.5},
    {"nombre": "sin(x) en a=0, n=5, evaluar en x=0.5", "f": lambda x: math.sin(x), "a": 0, "n": 5, "x_eval": 0.5},
    {"nombre": "cos(x) en a=0, n=4, evaluar en x=0.3", "f": lambda x: math.cos(x), "a": 0, "n": 4, "x_eval": 0.3},
    {"nombre": "x^2 en a=1, n=2, evaluar en x=1.2", "f": lambda x: x**2, "a": 1, "n": 2, "x_eval": 1.2},
    {"nombre": "e^x en a=0, n=3, evaluar en x=0.2", "f": lambda x: math.exp(x), "a": 0, "n": 3, "x_eval": 0.2},
]


def menu_principal():
    """Muestra el menu principal y retorna la opcion elegida."""
    print("\n" + "=" * 50)
    print("  CONTROLADOR DE CALCULO NUMERICO")
    print("=" * 50)
    print("  1. Metodo de Biseccion")
    print("  2. Metodo de Newton-Raphson")
    print("  3. Integracion Riemann")
    print("  4. Polinomio de Taylor")
    print("  5. Salir")
    print("=" * 50)
    return input("  Elija opcion (1-5): ").strip()


def menu_biseccion():
    """Submenu de ejercicios de biseccion."""
    print("\n--- Ejercicios de Biseccion ---")
    for i, ej in enumerate(EJERCICIOS_BISECCION, 1):
        print(f"  {i}. {ej['nombre']}")
    print(f"  {len(EJERCICIOS_BISECCION) + 1}. Volver al menu principal")
    return input(f"  Elija ejercicio (1-{len(EJERCICIOS_BISECCION) + 1}): ").strip()


def menu_newton():
    """Submenu de ejercicios de Newton-Raphson."""
    print("\n--- Ejercicios de Newton-Raphson ---")
    for i, ej in enumerate(EJERCICIOS_NEWTON, 1):
        print(f"  {i}. {ej['nombre']}")
    print(f"  {len(EJERCICIOS_NEWTON) + 1}. Volver al menu principal")
    return input(f"  Elija ejercicio (1-{len(EJERCICIOS_NEWTON) + 1}): ").strip()


def menu_riemann():
    """Submenu de ejercicios de integracion Riemann."""
    print("\n--- Ejercicios de Integracion Riemann ---")
    for i, ej in enumerate(EJERCICIOS_RIEMANN, 1):
        print(f"  {i}. {ej['nombre']}")
    print(f"  {len(EJERCICIOS_RIEMANN) + 1}. Volver al menu principal")
    return input(f"  Elija ejercicio (1-{len(EJERCICIOS_RIEMANN) + 1}): ").strip()


def menu_taylor():
    """Submenu de ejercicios de polinomio de Taylor."""
    print("\n--- Ejercicios de Polinomio de Taylor ---")
    for i, ej in enumerate(EJERCICIOS_TAYLOR, 1):
        print(f"  {i}. {ej['nombre']}")
    print(f"  {len(EJERCICIOS_TAYLOR) + 1}. Volver al menu principal")
    return input(f"  Elija ejercicio (1-{len(EJERCICIOS_TAYLOR) + 1}): ").strip()


def ejecutar_biseccion(opt):
    """Ejecuta el ejercicio de biseccion elegido."""
    idx = int(opt)
    if idx < 1 or idx > len(EJERCICIOS_BISECCION):
        return False
    ej = EJERCICIOS_BISECCION[idx - 1]
    try:
        raiz, error = resolver_raiz_biseccion(
            ej["f"], ej["a"], ej["b"],
            er=ej["er"], n=ej["n"],
            mostrar_proceso=True
        )
        print(f"\n  Resultado: raiz ~ {raiz:.8f}, error = {error:.6f}")
    except Exception as e:
        print(f"\n  Error: {e}")
    return True


def ejecutar_newton(opt):
    """Ejecuta el ejercicio de Newton-Raphson elegido."""
    idx = int(opt)
    if idx < 1 or idx > len(EJERCICIOS_NEWTON):
        return False
    ej = EJERCICIOS_NEWTON[idx - 1]
    try:
        raiz, error = resolver_raiz_newton(
            ej["f"], ej["df"], ej["x0"],
            er=ej["er"], n=ej["n"],
            mostrar_proceso=True
        )
        print(f"\n  Resultado: raiz ~ {raiz:.8f}, error = {error:.6f}")
    except Exception as e:
        print(f"\n  Error: {e}")
    return True


def ejecutar_riemann(opt):
    """Ejecuta el ejercicio de Riemann elegido."""
    idx = int(opt)
    if idx < 1 or idx > len(EJERCICIOS_RIEMANN):
        return False
    ej = EJERCICIOS_RIEMANN[idx - 1]
    try:
        resultado = resolver_integral(
            ej["f"], ej["a"], ej["b"],
            n=ej["n"], metodo=ej["metodo"]
        )
        print(f"\n  Resultado: integral ~ {resultado:.8f}")
    except Exception as e:
        print(f"\n  Error: {e}")
    return True


def ejecutar_taylor(opt):
    """Ejecuta el ejercicio de Taylor elegido."""
    idx = int(opt)
    if idx < 1 or idx > len(EJERCICIOS_TAYLOR):
        return False
    ej = EJERCICIOS_TAYLOR[idx - 1]
    try:
        resultado = resolver_taylor(
            ej["f"], ej["a"], ej["n"],
            x_eval=ej["x_eval"],
            mostrar_proceso=True
        )
        valor = resultado[0] if isinstance(resultado, tuple) else resultado
        print(f"\n  Resultado: P_n({ej['x_eval']}) ~ {valor:.8f}")
    except Exception as e:
        print(f"\n  Error: {e}")
    return True


def main():
    """Bucle principal del menu interactivo."""
    print("""
Proyecto Universitario de Calculo Numerico
Universidad de Oriente - 2026
Realizado por:
Br. William Flores
CI: 24.107.343
""")
    print("  Bienvenido al controlador de calculo numerico.")
    print("  Seleccione el metodo y el ejercicio que desea resolver.")

    while True:
        opcion = menu_principal()

        if opcion == "5":
            print("\n  Hasta luego.\n")
            break

        if opcion == "1":
            while True:
                sub = menu_biseccion()
                if sub == str(len(EJERCICIOS_BISECCION) + 1):
                    break
                if sub.isdigit() and 1 <= int(sub) <= len(EJERCICIOS_BISECCION):
                    ejecutar_biseccion(sub)
                else:
                    print("  Opcion no valida.")

        elif opcion == "2":
            while True:
                sub = menu_newton()
                if sub == str(len(EJERCICIOS_NEWTON) + 1):
                    break
                if sub.isdigit() and 1 <= int(sub) <= len(EJERCICIOS_NEWTON):
                    ejecutar_newton(sub)
                else:
                    print("  Opcion no valida.")

        elif opcion == "3":
            while True:
                sub = menu_riemann()
                if sub == str(len(EJERCICIOS_RIEMANN) + 1):
                    break
                if sub.isdigit() and 1 <= int(sub) <= len(EJERCICIOS_RIEMANN):
                    ejecutar_riemann(sub)
                else:
                    print("  Opcion no valida.")

        elif opcion == "4":
            if polinomio_taylor is None:
                print("\n  El modulo polinomio-de-taylor no esta disponible (requiere sympy).")
                continue
            while True:
                sub = menu_taylor()
                if sub == str(len(EJERCICIOS_TAYLOR) + 1):
                    break
                if sub.isdigit() and 1 <= int(sub) <= len(EJERCICIOS_TAYLOR):
                    ejecutar_taylor(sub)
                else:
                    print("  Opcion no valida.")

        else:
            print("  Opcion no valida. Elija 1, 2, 3, 4 o 5.")


# Referencias a modulos para uso avanzado
biseccion_mod = biseccion
newton_raphson_mod = newton_raphson
integracion_mod = integracion
taylor_mod = polinomio_taylor


if __name__ == "__main__":
    main()
