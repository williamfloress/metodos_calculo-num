# Calculo Numerico

Proyecto Universitario de Calculo Numerico
Universidad de Oriente - 2026
Realizado por:
Br. William Flores
CI: 24.107.343

---

Proyecto de metodos numericos en Python. Implementa tecnicas para aproximar raices de ecuaciones y calcular integrales definidas cuando no existen soluciones analiticas.

---

## Que hace el proyecto

El proyecto ofrece cuatro metodos numericos principales:

1. **Metodo de Biseccion**: Encuentra raices de una ecuacion f(x) = 0 dividiendo sucesivamente el intervalo [a, b] en mitades hasta que el error sea aceptable. Requiere que f(a) y f(b) tengan signos opuestos.

2. **Metodo de Newton-Raphson**: Aproxima raices usando iteraciones de la forma x_nuevo = x - f(x)/f'(x). Necesita la funcion y su derivada. Suele converger mas rapido que la biseccion.

3. **Integracion por Riemann**: Aproxima integrales definidas sumando areas de rectangulos. Incluye tres variantes: extremo izquierdo, extremo derecho y punto medio (este ultimo suele dar mejor precision).

4. **Polinomio de Taylor**: Aproxima una funcion mediante un polinomio expandido alrededor de un punto. Permite evaluar funciones en puntos cercanos al centro de expansion. Requiere la libreria `sympy`.

Ademas hay un **controlador** (`calculo-numerico.py`) con menu interactivo que permite elegir metodo y ejercicio para resolver, y un **sistema de pruebas** (`test.py`) que lee ejercicios desde un documento y verifica si los metodos producen resultados correctos.

---

## Estructura del proyecto

```
calculo-num/
  metodos/
    biseccion.py           Metodo de biseccion
    newton_raphson.py      Metodo de Newton-Raphson
    integracion.py         Integracion numerica (Riemann)
    polinomio-de-taylor.py Polinomio de Taylor (requiere sympy)
    calculo-numerico.py    Controlador con menu interactivo
    test.py                Pruebas automaticas de efectividad
    pruebas/
      EJERCICIOS_METODOS_NUMERICOS.md  Ejercicios con entradas y soluciones esperadas
```

---

## Como funciona test.py

`test.py` comprueba que los metodos funcionen bien haciendo lo siguiente:

1. **Lee el documento** `metodos/pruebas/EJERCICIOS_METODOS_NUMERICOS.md`, que contiene tablas con ejercicios para cada metodo.

2. **Interpreta las tablas**: Extrae funcion, parametros (intervalo, x0, n, etc.) y solucion esperada de cada fila.

3. **Ejecuta el metodo correspondiente**:
   - Biseccion: usa la funcion, el intervalo [a, b], error maximo y numero maximo de iteraciones.
   - Newton-Raphson: usa la funcion, su derivada, valor inicial x0, error maximo y numero maximo de iteraciones.
   - Riemann: usa la funcion, limites de integracion [a, b], numero de subintervalos y variante (izquierdo, derecho, punto_medio).
   - Taylor: usa la funcion, centro de expansion (a), grado (n) y punto de evaluacion (x_eval).

4. **Compara el resultado** obtenido con la solucion esperada. Si el error esta dentro de la tolerancia, marca el ejercicio como OK; si no, como FALLO.

5. **Muestra un resumen** con cuantos ejercicios pasaron por cada metodo y el total.

Para ver el detalle de cada iteracion durante las pruebas, ejecuta:

```
python test.py --verbose
```

o

```
python test.py -v
```

---

## Como probar los metodos

### Opcion 1: Ejecutar las pruebas automaticas

Desde la carpeta `metodos`:

```
cd metodos
python test.py
```

Se leen los ejercicios del documento, se resuelven y se indica si cada uno paso o fallo.

### Opcion 2: Usar el controlador calculo-numerico.py (menu interactivo)

El archivo `calculo-numerico.py` ofrece un menu interactivo. Ejecutalo desde la carpeta `metodos`:

```
cd metodos
python calculo-numerico.py
```

Se mostrara un menu principal con cinco opciones:

1. **Metodo de Biseccion** - Al elegirlo, aparecera un submenu con 5 ejercicios integrados (x^2-2, x^3-2, e^(-x)-ln(x), cos(x)-x, x^2-5). Elige uno para ver el proceso paso a paso y el resultado.

2. **Metodo de Newton-Raphson** - Submenu con 5 ejercicios equivalentes para Newton-Raphson.

3. **Integracion Riemann** - Submenu con 5 ejercicios (x^2 en [0,1], e^x en [0,1], sin(x) en [0,pi], x en [0,2], sqrt(x) en [0,1]).

4. **Polinomio de Taylor** - Submenu con 5 ejercicios (e^x, sin(x), cos(x), x^2, e^x en distintos centros y puntos de evaluacion). Requiere instalar sympy.

5. **Salir** - Finaliza el programa.

Puedes resolver varios ejercicios seguidos. Tras cada resultado, volveras al submenu del metodo para elegir otro ejercicio o volver al menu principal. El script se mantiene en ejecucion hasta que elijas Salir.

**Nota sobre funciones predefinidas**: el menu interactivo solo ejecuta ejercicios incluidos en el script. No permite escribir funciones personalizadas desde la consola.

### Opcion 3: Usar los modulos directamente

Puedes importar cada modulo y llamar a sus funciones:

```python
import sys
sys.path.insert(0, "metodos")

import biseccion
import newton_raphson
import integracion

# Biseccion
raiz, err = biseccion.biseccion(lambda x: x**2 - 4, 0, 3, er=0.0001, n=100)

# Newton-Raphson
raiz, err = newton_raphson.newton_raphson(
    lambda x: x**2 - 4,
    lambda x: 2*x,
    x0=2.5, er=0.0001, n=50
)

# Riemann (cualquier variante: izquierdo, derecho, punto_medio)
resultado = integracion.integrar(lambda x: x**2, 0, 1, n=50, metodo="punto_medio")

# Polinomio de Taylor (requiere sympy; usar importlib por el guion en el nombre del archivo)
```

**Aqui si puedes definir tus propias funciones** en Python y pasarlas como `lambda` o como funciones normales, segun el metodo.

### Opcion 4: Agregar o modificar ejercicios

Edita `metodos/pruebas/EJERCICIOS_METODOS_NUMERICOS.md` para anadir nuevos ejercicios o cambiar los existentes. Las tablas deben mantener el mismo formato (columnas separadas por |) y usar expresiones que el `test.py` pueda interpretar. Si usas una funcion nueva, debes registrarla en los diccionarios `FUNCIONES` y `DERIVADAS` dentro de `metodos/test.py`.

---

## Requisitos

- Python 3.8 o superior
- Modulo estandar `math` (incluido en Python)

Para **biseccion, Newton-Raphson e integracion Riemann** no se requieren librerias externas.

Para el **polinomio de Taylor** se necesita instalar `sympy`:

```
pip install sympy
```

---

MVP adicional (calculadora virtual con frontend):
Actualmente solo funciona con los metodos de biseccion y Newton-Raphson.
Se encuentra en trabajo de implementacion para incluir los nuevos metodos aprendidos en clase.
Repositorio: https://github.com/williamfloress/numeric-calculator
Demo: https://numeric-calculator-eight.vercel.app/
