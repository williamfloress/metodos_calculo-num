import math


def newton_raphson(f, df, x0, er, n, mostrar_proceso=True):
    """Algoritmo de Newton-Raphson.

    Args:
        f (callable): función objetivo para la cual se busca la raíz.
        df (callable): derivada de la función objetivo.
        x0 (float): aproximación inicial a la raíz.
        er (float): cota máxima del error relativo permitido.
        n (int): número máximo de iteraciones para evitar bucles infinitos.
        mostrar_proceso (bool): si es True, muestra el proceso de cálculo paso a paso.

    Returns:
        tuple: par `(raiz_aproximada, error_final)`.
    """
    # Mostramos información inicial:
    if mostrar_proceso:
        print("\n" + "="*70)
        print("MÉTODO DE NEWTON-RAPHSON")
        print("="*70)
        print(f"Aproximación inicial (x0): {x0}")
        print(f"Error máximo permitido (er): {er}")
        print(f"Número máximo de iteraciones (n): {n}")
        print("-"*70)
        print("\nIteraciones:")
        print("-"*70)
        print(f"{'Iter':<6} {'x_actual':<15} {'f(x)':<15} {'f\'(x)':<15} {'x_nuevo':<15} {'Error':<15}")
        print("-"*70)
    
    # Inicialización de variables de control:
    # Definimos el error relativo inicial como 1.0 (100%):
    ei = 1.0
    # Iniciamos el contador de iteraciones:
    i = 0
    # Guardamos la estimación actual (comienza con el valor inicial x0):
    x_actual = x0

    # Bucle principal de iteración:
    while ei > er and i < n:
        fx = f(x_actual)
        # Si encontramos una raíz exacta, terminamos inmediatamente:
        if fx == 0:
            if mostrar_proceso:
                print(f"{i:<6} {x_actual:<15.7f} {fx:<15.7f} {'Raíz exacta':<15} {'-':<15} {'0.0000':<15}")
                print("-"*70)
                print(f"\n¡Raíz exacta encontrada en la iteración {i}!")
            return x_actual, 0.0

        dfx = df(x_actual)
        # Validamos que la derivada no sea cero para evitar divisiones no válidas:
        if dfx == 0:
            raise ValueError("La derivada se anuló; el método no puede continuar.")

        # Calculamos la nueva aproximación usando la fórmula de Newton-Raphson:
        x_nuevo = x_actual - fx / dfx

        # Actualizamos el error relativo si el nuevo valor no es cero:
        if x_nuevo != 0:
            ei = abs((x_nuevo - x_actual) / x_nuevo)
        else:
            ei = abs(x_nuevo - x_actual)

        # Mostramos la iteración actual:
        if mostrar_proceso:
            print(f"{i:<6} {x_actual:<15.7f} {fx:<15.7f} {dfx:<15.7f} {x_nuevo:<15.7f} {ei:<15.7f}")
            if i == 0:
                print(f"        Fórmula: x_{i+1} = x_{i} - f(x_{i})/f'(x_{i})")
                print(f"                 x_{i+1} = {x_actual:.7f} - {fx:.7f}/{dfx:.7f}")
                print(f"                 x_{i+1} = {x_nuevo:.7f}")

        # Preparamos la siguiente iteración:
        x_actual = x_nuevo
        i += 1

    # Mostramos resumen final:
    if mostrar_proceso:
        print("-"*70)
        if ei <= er:
            print(f"\n✓ Convergencia alcanzada en {i} iteraciones")
        else:
            print(f"\n⚠ Límite de iteraciones alcanzado ({n} iteraciones)")
        print(f"Raíz aproximada: {x_actual:.7f}")
        print(f"Error relativo final: {ei:.7f}")
        print("="*70)

    # Una vez terminado el bucle, devolvemos la mejor aproximación y el error alcanzado:
    return x_actual, ei


# Bloque de prueba:
if __name__ == "__main__":
    # Encabezado del programa:
    print("\n" + "="*70)
    print("MÉTODO: NEWTON-RAPHSON")
    print("="*70)
    print("Realizado por: William Flores")
    print("="*70)
    
    # Definimos la función objetivo y su derivada:
    f = lambda x: math.exp(-x) - math.log(x)
    df = lambda x: -math.exp(-x) - (1 / x)

    # Definimos la estimación inicial, error máximo y número máximo de iteraciones:
    x0 = 1.2
    er = 0.01
    n = 50

    # Ejecutamos el método de Newton-Raphson con los parámetros definidos:
    raiz, error = newton_raphson(f, df, x0, er, n, mostrar_proceso=True)

