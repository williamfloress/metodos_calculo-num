#importar la libreria math para usar funciones matemáticas:

import math

def biseccion(f, a, b, er, n, mostrar_proceso=True):
    """Algoritmo de biseccion
    #Declaramos la funcion con los parametros siguientes:
    #f: funcion objetivo (recibe un numero y retorna otro)
    #a, b: extremos iniciales del intervalo donde se cree que hay una raiz
    #er: error maximo permitido (por ejemplo, 0.01)
    #n: numero maximo de iteraciones para evitar bucles infinitos
    #mostrar_proceso (bool): si es True, muestra el proceso de cálculo paso a paso
    
    returns: 
    tuple: par `(raiz_aproximada, error_final)`
    """
    # Mostramos información inicial:
    if mostrar_proceso:
        print("\n" + "="*70)
        print("MÉTODO DE BISECCIÓN")
        print("="*70)
        print(f"Intervalo inicial: [a, b] = [{a}, {b}]")
        print(f"Error máximo permitido (er): {er}")
        print(f"Número máximo de iteraciones (n): {n}")
        print(f"f(a) = {f(a):.7f}")
        print(f"f(b) = {f(b):.7f}")
        print("-"*70)
        print("\nIteraciones:")
        print("-"*70)
        print(f"{'Iter':<6} {'a':<15} {'b':<15} {'m':<15} {'f(a)':<15} {'f(m)':<15} {'f(b)':<15} {'Error':<15}")
        print("-"*70)
    
    #Inicializacion de variables de control:
    #Declaramos el error inicial como 1.0 (100%):
    ei = 1.0
    #Iniciamos un contador de iteraciones en cero:
    i = 0
    #Variable de reserva de punto medio de la iteracion anterior:
    m_anterior = None

    #Validacion que exista cambio de signo en el intervalo:
    #Si no hay cambio de signo, el metodo no garantiza convergencia:
    if f(a) * f(b) > 0:
        raise ValueError("La funcion no cambia de signo en el intervalo dado.")
    
    #Bucle principal de iteración:

    #Crear un ciclo que continue mientras el error sea mayor que el "er" y no supere el limite de iteraciones "n":
    while ei > er and i < n:
        #calculamos el punto medio del intervalo:
        m_actual = (a + b) / 2

        #Si ya existe un "m_anterior", procedemos a calcular el error relativo utilizando el valor nuevo:
        if m_anterior is not None:
            ei = abs((m_actual - m_anterior) / m_actual)

        #Debemos decidir ahora que subintervalo conservar:
        #Considerando que:
        #Si f(a) y f(m_actual) tienen signos opuestos, la raiz estará entre (a) y (m_actual), por lo que actualizamos "b= m_actual"
        #Si no, entonces la raiz estará entre (m_actual) y (b), por lo que actualizamos "a= m_actual"
        #Si ninguno cambia de signo (valor exactamente cero), retornamos la raiz encontrada:

        fa = f(a)
        fm = f(m_actual)  # Corregido: faltaba f()
        fb = f(b)
        
        # Mostramos la iteración actual:
        if mostrar_proceso:
            error_str = f"{ei:.7f}" if m_anterior is not None else "-"
            print(f"{i:<6} {a:<15.7f} {b:<15.7f} {m_actual:<15.7f} {fa:<15.7f} {fm:<15.7f} {fb:<15.7f} {error_str:<15}")
            if i == 0:
                print(f"        Cálculo: m = (a + b) / 2 = ({a} + {b}) / 2 = {m_actual:.7f}")
        
        if fa * fm < 0:
            if mostrar_proceso:
                print(f"        f(a) * f(m) < 0 → La raíz está en [a, m] → b = m")
            b = m_actual
        elif fm * fb < 0:
            if mostrar_proceso:
                print(f"        f(m) * f(b) < 0 → La raíz está en [m, b] → a = m")
            a = m_actual
        else:
            if mostrar_proceso:
                print(f"        ¡Raíz exacta encontrada! f(m) = 0")
                print("-"*70)
            return m_actual, 0.0
        
        #Ahora debemos guardar el m_actual para la siguiente iteración y sumar 1 al contador:
        m_anterior = m_actual
        i += 1
    
    # Mostramos resumen final:
    if mostrar_proceso:
        print("-"*70)
        if ei <= er:
            print(f"\n✓ Convergencia alcanzada en {i} iteraciones")
        else:
            print(f"\n⚠ Límite de iteraciones alcanzado ({n} iteraciones)")
        print(f"Raíz aproximada: {m_actual:.7f}")
        print(f"Error relativo final: {ei:.7f}")
        print("="*70)
    
    #Si el bucle termina, retornaremos la mejor aproximación y el error alcanzado:
    return m_actual, ei

#Bloque de prueba:
if __name__ == "__main__":
    # Encabezado del programa:
    print("\n" + "="*70)
    print("MÉTODO: BISECCIÓN")
    print("="*70)
    print("Realizado por: William Flores")
    print("="*70)
    
    #Definimos funcion objetivo:
    f = lambda x: math.exp(-x) - math.log(x)
    #Definimos los valores iniciales del intervalo:
    a = 1
    b = 1.5
    #Definimos el error máximo permitido:
    er = 0.01
    #Definimos el numero máximo de iteraciones:
    n = 50

    #Llamamos a la funcion biseccion con los parametros definidos anteriormente:
    raiz, error = biseccion(f, a, b, er, n, mostrar_proceso=True)




    
