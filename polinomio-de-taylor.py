import math
import sympy as sp


def polinomio_taylor(f, a, n, x_eval=None, mostrar_proceso=True):
    """Algoritmo para calcular el polinomio de Taylor.

    Args:
        f (callable o sympy.Expr): función objetivo para la cual se calcula el polinomio.
            Puede ser una función lambda o una expresión simbólica de sympy.
        a (float): punto alrededor del cual se expande el polinomio (centro de expansión).
        n (int): grado del polinomio de Taylor (número de términos - 1).
        x_eval (float, optional): punto donde se desea evaluar el polinomio.
            Si es None, se retorna la expresión simbólica del polinomio.
        mostrar_proceso (bool): si es True, muestra el proceso de cálculo paso a paso.

    Returns:
        tuple: par `(polinomio, error_resto)` donde:
            - polinomio: expresión simbólica del polinomio o valor numérico si x_eval está definido.
            - error_resto: estimación del error del resto (término de Lagrange).
    """
    # Definimos la variable simbólica x:
    x = sp.Symbol('x')
    
    # Mostramos información inicial:
    if mostrar_proceso:
        print("\n" + "="*70)
        print("CÁLCULO DEL POLINOMIO DE TAYLOR")
        print("="*70)
        print(f"Función: f(x) = {f}")
        print(f"Centro de expansión (a): {a}")
        print(f"Grado del polinomio (n): {n}")
        if x_eval is not None:
            print(f"Punto de evaluación (x): {x_eval}")
        print("-"*70)
    
    # Convertimos la función a expresión simbólica si es necesario:
    # Si f es una función lambda, la convertimos a expresión simbólica:
    if callable(f) and not isinstance(f, sp.Basic):
        # Creamos una expresión simbólica evaluando f(x):
        try:
            # Intentamos evaluar f con la variable simbólica:
            f_simbolica = f(x)
            # Si f no puede trabajar con símbolos, usamos lambdify:
            if not isinstance(f_simbolica, sp.Basic):
                # Necesitamos crear una función numérica y luego convertirla:
                # Para esto, evaluamos en puntos y construimos el polinomio numéricamente:
                f_simbolica = sp.lambdify(x, f(x), 'numpy')
                # Si llegamos aquí, necesitamos un enfoque diferente:
                # Usaremos derivadas numéricas aproximadas:
                return polinomio_taylor_numerico(f, a, n, x_eval, mostrar_proceso)
        except:
            # Si falla, usamos el método numérico:
            return polinomio_taylor_numerico(f, a, n, x_eval, mostrar_proceso)
    else:
        # Si ya es una expresión simbólica:
        f_simbolica = f
    
    # Inicializamos el polinomio como cero:
    polinomio = 0
    
    if mostrar_proceso:
        print("\nCálculo de términos del polinomio:")
        print("-"*70)
    
    # Calculamos cada término del polinomio de Taylor:
    # P_n(x) = Σ(k=0 to n) [f^(k)(a) / k!] * (x - a)^k
    for k in range(n + 1):
        if mostrar_proceso:
            print(f"\nTérmino k = {k}:")
        
        # Calculamos la k-ésima derivada de f:
        f_derivada_k = f_simbolica
        for _ in range(k):
            f_derivada_k = sp.diff(f_derivada_k, x)
        
        if mostrar_proceso:
            if k == 0:
                print(f"  f^({k})(x) = {f_derivada_k}")
            else:
                print(f"  f^({k})(x) = {sp.simplify(f_derivada_k)}")
        
        # Evaluamos la derivada en el punto a:
        f_derivada_k_en_a = f_derivada_k.subs(x, a)
        
        if mostrar_proceso:
            print(f"  f^({k})({a}) = {f_derivada_k_en_a}")
            print(f"  {k}! = {math.factorial(k)}")
        
        # Calculamos el término: [f^(k)(a) / k!] * (x - a)^k
        coeficiente = f_derivada_k_en_a / math.factorial(k)
        termino = coeficiente * (x - a)**k
        
        if mostrar_proceso:
            termino_simplificado = sp.simplify(termino)
            print(f"  Término {k}: [{f_derivada_k_en_a} / {math.factorial(k)}] * (x - {a})^{k}")
            print(f"            = {termino_simplificado}")
        
        # Sumamos el término al polinomio:
        polinomio += termino
        
        if mostrar_proceso:
            polinomio_actual = sp.simplify(polinomio)
            print(f"  Polinomio acumulado: P_{k}(x) = {polinomio_actual}")
    
    # Simplificamos el polinomio:
    polinomio = sp.simplify(polinomio)
    
    if mostrar_proceso:
        print("\n" + "-"*70)
        print(f"POLINOMIO DE TAYLOR FINAL (grado {n}):")
        print(f"P_{n}(x) = {polinomio}")
        print("-"*70)
    
    # Calculamos el error del resto (término de Lagrange):
    # R_n(x) = [f^(n+1)(ξ) / (n+1)!] * (x - a)^(n+1)
    # Para estimar, usamos la derivada (n+1)-ésima evaluada en un punto intermedio:
    if x_eval is not None:
        if mostrar_proceso:
            print(f"\nEVALUACIÓN DEL POLINOMIO EN x = {x_eval}:")
            print("-"*70)
        
        # Evaluamos el polinomio en x_eval:
        polinomio_evaluado = float(polinomio.subs(x, x_eval))
        
        if mostrar_proceso:
            print(f"P_{n}({x_eval}) = {polinomio_evaluado:.7f}")
        
        # Calculamos la derivada (n+1)-ésima:
        if mostrar_proceso:
            print(f"\nCálculo del error del resto (término de Lagrange):")
        
        f_derivada_n1 = f_simbolica
        for _ in range(n + 1):
            f_derivada_n1 = sp.diff(f_derivada_n1, x)
        
        if mostrar_proceso:
            print(f"  f^({n+1})(x) = {sp.simplify(f_derivada_n1)}")
        
        # Estimamos el error usando el valor máximo posible de la derivada:
        # (simplificación: usamos el valor en a como aproximación)
        try:
            max_derivada = abs(float(f_derivada_n1.subs(x, a)))
            if mostrar_proceso:
                print(f"  |f^({n+1})({a})| = {max_derivada:.7f}")
        except:
            max_derivada = abs(float(f_derivada_n1.subs(x, x_eval)))
            if mostrar_proceso:
                print(f"  |f^({n+1})({x_eval})| = {max_derivada:.7f}")
        
        error_resto = (max_derivada / math.factorial(n + 1)) * abs((x_eval - a)**(n + 1))
        
        if mostrar_proceso:
            print(f"  ({n+1})! = {math.factorial(n + 1)}")
            print(f"  |x - a|^{n+1} = |{x_eval} - {a}|^{n+1} = {abs((x_eval - a)**(n + 1)):.7f}")
            print(f"  Error estimado: R_{n}({x_eval}) = {error_resto:.7f}")
        
        return polinomio_evaluado, error_resto
    else:
        # Si no se especifica x_eval, retornamos el polinomio simbólico:
        return polinomio, None


def polinomio_taylor_numerico(f, a, n, x_eval=None, mostrar_proceso=True):
    """Versión numérica del polinomio de Taylor para funciones lambda.

    Args:
        f (callable): función objetivo (función lambda o función Python).
        a (float): punto alrededor del cual se expande el polinomio.
        n (int): grado del polinomio de Taylor.
        x_eval (float, optional): punto donde se desea evaluar el polinomio.
        mostrar_proceso (bool): si es True, muestra el proceso de cálculo paso a paso.

    Returns:
        tuple: par `(polinomio_func, error_resto)` donde polinomio_func es una función lambda.
    """
    # Usamos diferencias finitas para aproximar las derivadas:
    h = 1e-5  # Paso pequeño para la aproximación numérica
    
    if mostrar_proceso:
        print("\n" + "="*70)
        print("CÁLCULO DEL POLINOMIO DE TAYLOR (MÉTODO NUMÉRICO)")
        print("="*70)
        print(f"Centro de expansión (a): {a}")
        print(f"Grado del polinomio (n): {n}")
        print(f"Paso para diferencias finitas (h): {h}")
        if x_eval is not None:
            print(f"Punto de evaluación (x): {x_eval}")
        print("-"*70)
        print("\nCálculo de términos del polinomio:")
        print("-"*70)
    
    # Construimos el polinomio término por término:
    def polinomio_func(x_val):
        resultado = 0.0
        for k in range(n + 1):
            # Aproximamos la k-ésima derivada usando diferencias finitas:
            if k == 0:
                derivada_k = f(a)
            else:
                # Aproximación de la derivada k-ésima usando diferencias finitas centrales:
                derivada_k = aproximar_derivada_k(f, a, k, h)
            
            if mostrar_proceso:
                print(f"\nTérmino k = {k}:")
                print(f"  f^({k})({a}) ≈ {derivada_k:.7f}")
                print(f"  {k}! = {math.factorial(k)}")
            
            # Calculamos el término del polinomio:
            coeficiente = derivada_k / math.factorial(k)
            termino = coeficiente * ((x_val - a)**k)
            resultado += termino
            
            if mostrar_proceso:
                print(f"  Término {k}: [{derivada_k:.7f} / {math.factorial(k)}] * ({x_val} - {a})^{k}")
                print(f"            = {coeficiente:.7f} * {((x_val - a)**k):.7f} = {termino:.7f}")
                print(f"  Polinomio acumulado: P_{k}({x_val}) = {resultado:.7f}")
        
        return resultado
    
    # Calculamos el error del resto:
    if x_eval is not None:
        if mostrar_proceso:
            print("\n" + "-"*70)
            print(f"EVALUACIÓN DEL POLINOMIO EN x = {x_eval}:")
            print("-"*70)
        
        valor_aprox = polinomio_func(x_eval)
        
        if mostrar_proceso:
            print(f"\nP_{n}({x_eval}) = {valor_aprox:.7f}")
            print(f"\nCálculo del error del resto:")
        
        # Aproximamos la derivada (n+1)-ésima:
        derivada_n1 = aproximar_derivada_k(f, a, n + 1, h)
        
        if mostrar_proceso:
            print(f"  f^({n+1})({a}) ≈ {derivada_n1:.7f}")
            print(f"  ({n+1})! = {math.factorial(n + 1)}")
            print(f"  |x - a|^{n+1} = |{x_eval} - {a}|^{n+1} = {abs((x_eval - a)**(n + 1)):.7f}")
        
        error_resto = (abs(derivada_n1) / math.factorial(n + 1)) * abs((x_eval - a)**(n + 1))
        
        if mostrar_proceso:
            print(f"  Error estimado: R_{n}({x_eval}) = {error_resto:.7f}")
        
        return valor_aprox, error_resto
    else:
        return polinomio_func, None


def aproximar_derivada_k(f, a, k, h):
    """Aproxima la k-ésima derivada de f en el punto a usando diferencias finitas.

    Args:
        f (callable): función objetivo.
        a (float): punto donde se evalúa la derivada.
        k (int): orden de la derivada.
        h (float): paso para la aproximación.

    Returns:
        float: aproximación de la k-ésima derivada.
    """
    if k == 0:
        return f(a)
    elif k == 1:
        # Primera derivada: diferencia central:
        return (f(a + h) - f(a - h)) / (2 * h)
    else:
        # Derivadas de orden superior: recursivamente:
        # f^(k)(a) ≈ [f^(k-1)(a+h) - f^(k-1)(a-h)] / (2h)
        derivada_anterior_plus = aproximar_derivada_k(f, a + h, k - 1, h)
        derivada_anterior_minus = aproximar_derivada_k(f, a - h, k - 1, h)
        return (derivada_anterior_plus - derivada_anterior_minus) / (2 * h)


# Bloque de prueba:
if __name__ == "__main__":
    # Encabezado del programa:
    print("\n" + "="*70)
    print("MÉTODO: POLINOMIO DE TAYLOR")
    print("="*70)
    print("Realizado por: William Flores")
    print("="*70)
    
    # Ejemplo 1: Polinomio de Taylor usando sympy (expresión simbólica):
    print("\n" + "="*70)
    print("EJEMPLO 1: Polinomio de Taylor de e^x alrededor de x=0")
    print("="*70)
    x = sp.Symbol('x')
    f_simbolica = sp.exp(x)
    
    # Calculamos el polinomio de grado 5:
    polinomio, _ = polinomio_taylor(f_simbolica, 0, 5, None, mostrar_proceso=True)
    
    # Evaluamos en x=1:
    print("\n" + "="*70)
    print("EVALUACIÓN EN x = 1")
    print("="*70)
    valor_aprox, error = polinomio_taylor(f_simbolica, 0, 5, 1.0, mostrar_proceso=True)
    valor_exacto = math.exp(1)
    print("\n" + "-"*70)
    print("RESUMEN DE RESULTADOS:")
    print("-"*70)
    print(f"Valor aproximado P_5(1): {valor_aprox:.7f}")
    print(f"Valor exacto e^1:         {valor_exacto:.7f}")
    print(f"Error absoluto:           {abs(valor_exacto - valor_aprox):.7f}")
    print(f"Error estimado del resto: {error:.7f}")
    
    # Ejemplo 2: Polinomio de Taylor usando función lambda:
    print("\n\n" + "="*70)
    print("EJEMPLO 2: Polinomio de Taylor de sin(x) alrededor de x=0")
    print("="*70)
    f_lambda = lambda x: math.sin(x)
    
    # Calculamos el polinomio de grado 7:
    valor_aprox2, error2 = polinomio_taylor(f_lambda, 0, 7, math.pi / 4, mostrar_proceso=True)
    valor_exacto2 = math.sin(math.pi / 4)
    print("\n" + "-"*70)
    print("RESUMEN DE RESULTADOS:")
    print("-"*70)
    print(f"Valor aproximado P_7(π/4): {valor_aprox2:.7f}")
    print(f"Valor exacto sin(π/4):     {valor_exacto2:.7f}")
    print(f"Error absoluto:            {abs(valor_exacto2 - valor_aprox2):.7f}")
    print(f"Error estimado del resto:  {error2:.7f}")
    
    # Ejemplo 3: Polinomio de Taylor usando sympy con función más compleja:
    print("\n\n" + "="*70)
    print("EJEMPLO 3: Polinomio de Taylor de ln(1+x) alrededor de x=0")
    print("="*70)
    f_simbolica2 = sp.log(1 + x)
    
    polinomio2, _ = polinomio_taylor(f_simbolica2, 0, 4, None, mostrar_proceso=True)
    
    print("\n" + "="*70)
    print("EVALUACIÓN EN x = 0.5")
    print("="*70)
    valor_aprox3, error3 = polinomio_taylor(f_simbolica2, 0, 4, 0.5, mostrar_proceso=True)
    valor_exacto3 = math.log(1.5)
    print("\n" + "-"*70)
    print("RESUMEN DE RESULTADOS:")
    print("-"*70)
    print(f"Valor aproximado P_4(0.5): {valor_aprox3:.7f}")
    print(f"Valor exacto ln(1.5):      {valor_exacto3:.7f}")
    print(f"Error absoluto:            {abs(valor_exacto3 - valor_aprox3):.7f}")
    print(f"Error estimado del resto:  {error3:.7f}")
    print("\n" + "="*70)

