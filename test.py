#!/usr/bin/env python3
"""
Test de efectividad de metodos numericos.
Lee EJERCICIOS_METODOS_NUMERICOS.md, resuelve los ejercicios y verifica si los
resultados son correctos.
"""

import math
import re
import sys
import os

# Permitir imports desde la carpeta metodos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import importlib.util

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

# Ruta al documento de ejercicios (en metodos/pruebas)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
EJERCICIOS_PATH = os.path.join(SCRIPT_DIR, "pruebas", "EJERCICIOS_METODOS_NUMERICOS.md")

# Tolerancias para considerar un resultado correcto
TOL_RAIZ = 0.02
TOL_INTEGRAL = 0.05  # Riemann: n>=50 para izquierdo/derecho da buen error
TOL_TAYLOR = 0.02  # Polinomio de Taylor

# Mapeo: expresion f(x) en el doc -> funcion Python
FUNCIONES = {
    "x² - 2": lambda x: x**2 - 2,
    "x^2 - 2": lambda x: x**2 - 2,
    "x³ - 2": lambda x: x**3 - 2,
    "x^3 - 2": lambda x: x**3 - 2,
    "e^(-x) - ln(x)": lambda x: math.exp(-x) - math.log(x),
    "x² - 4": lambda x: x**2 - 4,
    "x^2 - 4": lambda x: x**2 - 4,
    "cos(x) - x": lambda x: math.cos(x) - x,
    "x³ - x - 1": lambda x: x**3 - x - 1,
    "x^3 - x - 1": lambda x: x**3 - x - 1,
    "ln(x) - 1": lambda x: math.log(x) - 1,
    "sin(x)": lambda x: math.sin(x),
    "x² - 3": lambda x: x**2 - 3,
    "x^2 - 3": lambda x: x**2 - 3,
    "e^x - 2": lambda x: math.exp(x) - 2,
    "x²": lambda x: x**2,
    "x^2": lambda x: x**2,
    "x³": lambda x: x**3,
    "x^3": lambda x: x**3,
    "e^x": lambda x: math.exp(x),
    "1/(1+x)": lambda x: 1 / (1 + x),
    "1/x": lambda x: 1 / x if x != 0 else float("nan"),
    "x": lambda x: x,
    "2x": lambda x: 2 * x,
    "√x": lambda x: math.sqrt(x) if x >= 0 else float("nan"),
    "sqrt(x)": lambda x: math.sqrt(x) if x >= 0 else float("nan"),
    "x⁴": lambda x: x**4,
    "x^4": lambda x: x**4,
    "x² - 5": lambda x: x**2 - 5,
    "x^2 - 5": lambda x: x**2 - 5,
    "x² - 6": lambda x: x**2 - 6,
    "x^2 - 6": lambda x: x**2 - 6,
    "x³ - 10": lambda x: x**3 - 10,
    "x^3 - 10": lambda x: x**3 - 10,
    "x⁴ - 2": lambda x: x**4 - 2,
    "x^4 - 2": lambda x: x**4 - 2,
    "x² + x - 6": lambda x: x**2 + x - 6,
    "x^2 + x - 6": lambda x: x**2 + x - 6,
    "ln(x) + x - 2": lambda x: math.log(x) + x - 2 if x > 0 else float("nan"),
    "cos(x)": lambda x: math.cos(x),
}

# Mapeo: expresion f'(x) -> derivada
DERIVADAS = {
    "2x": lambda x: 2 * x,
    "3x²": lambda x: 3 * x**2,
    "3x^2": lambda x: 3 * x**2,
    "-e^(-x) - 1/x": lambda x: -math.exp(-x) - 1 / x if x != 0 else float("nan"),
    "-sin(x) - 1": lambda x: -math.sin(x) - 1,
    "3x² - 1": lambda x: 3 * x**2 - 1,
    "3x^2 - 1": lambda x: 3 * x**2 - 1,
    "1/x": lambda x: 1 / x if x != 0 else float("nan"),
    "e^x": lambda x: math.exp(x),
    "4x³": lambda x: 4 * x**3,
    "4x^3": lambda x: 4 * x**3,
    "2x + 1": lambda x: 2 * x + 1,
    "1/x + 1": lambda x: 1 / x + 1 if x != 0 else float("nan"),
}


def obtener_funcion(expr):
    """Obtiene la funcion callable a partir de la expresion del documento."""
    expr = expr.strip()
    return FUNCIONES.get(expr)


def obtener_derivada(expr):
    """Obtiene la derivada callable a partir de la expresion del documento."""
    expr = expr.strip()
    return DERIVADAS.get(expr)


def parsear_solucion_esperada(texto):
    """Extrae el valor numerico de la solucion esperada (ej: '≈ 1.414 (√2)' -> 1.414)."""
    if not texto or not isinstance(texto, str):
        return None
    texto = texto.strip()
    # Buscar patron "≈ X.XXX" o "X.XXX"
    m = re.search(r"≈?\s*([\d.]+)", texto)
    if m:
        try:
            return float(m.group(1))
        except ValueError:
            pass
    # Valores exactos conocidos por referencia
    if "√2" in texto or "sqrt(2)" in texto.lower():
        return math.sqrt(2)
    if "∛2" in texto or "2^(1/3)" in texto:
        return 2 ** (1/3)
    if "√3" in texto or "sqrt(3)" in texto.lower():
        return math.sqrt(3)
    if "√5" in texto or "sqrt(5)" in texto.lower():
        return math.sqrt(5)
    if "√6" in texto or "sqrt(6)" in texto.lower():
        return math.sqrt(6)
    if "∛10" in texto or "10^(1/3)" in texto:
        return 10 ** (1/3)
    if "1/3" in texto:
        return 1 / 3
    if "1/4" in texto:
        return 0.25
    if "1/5" in texto:
        return 0.2
    if "2/3" in texto:
        return 2 / 3
    if "e - 1" in texto or "e-1" in texto:
        return math.e - 1
    if "ln 2" in texto or "ln2" in texto.lower():
        return math.log(2)
    if "e)" in texto and "2.718" in texto:
        return math.e
    if "ln 2" in texto.lower():
        return math.log(2)
    if "e^0.5" in texto or "e^0,5" in texto:
        return math.exp(0.5)
    if "e^0.2" in texto or "e^0,2" in texto:
        return math.exp(0.2)
    if "sin 0.5" in texto.lower():
        return math.sin(0.5)
    if "cos 0.3" in texto.lower():
        return math.cos(0.3)
    return None


def parsear_tabla_md(contenido, inicio_marker, fin_marker=None):
    """Extrae filas de una tabla markdown entre dos secciones."""
    try:
        idx = contenido.find(inicio_marker)
        if idx < 0:
            return []
        texto = contenido[idx:]
        if fin_marker:
            fin = texto.find(fin_marker, len(inicio_marker))
            if fin > 0:
                texto = texto[:fin]
        lineas = texto.split("\n")
        filas = []
        for i, ln in enumerate(lineas):
            if "|" in ln and not ln.strip().startswith("|---"):
                partes = [p.strip() for p in ln.split("|")[1:-1]]
                if len(partes) >= 2 and not partes[0].startswith("#"):
                    filas.append(partes)
        return filas
    except Exception:
        return []


def cargar_ejercicios_biseccion(contenido):
    """Carga ejercicios de biseccion desde el contenido del MD."""
    filas = parsear_tabla_md(contenido, "## Método de Bisección", "## Método de Newton-Raphson")
    ejercicios = []
    for row in filas:
        if len(row) < 6:
            continue
        try:
            num, fx, a, b, er, n, esperado_str = row[0], row[1], row[2], row[3], row[4], row[5], row[6]
            f = obtener_funcion(fx)
            if f is None:
                continue
            esperado = parsear_solucion_esperada(esperado_str)
            if esperado is None:
                continue
            ejercicios.append({
                "num": num, "fx": fx, "f": f,
                "a": float(a), "b": float(b),
                "er": float(er), "n": int(n),
                "esperado": esperado,
            })
        except (ValueError, IndexError):
            continue
    return ejercicios


def cargar_ejercicios_newton(contenido):
    """Carga ejercicios de Newton-Raphson desde el contenido del MD."""
    filas = parsear_tabla_md(contenido, "## Método de Newton-Raphson", "## Integración numérica")
    ejercicios = []
    for row in filas:
        if len(row) < 6:
            continue
        try:
            num, fx, dfx, x0, er, n, esperado_str = row[0], row[1], row[2], row[3], row[4], row[5], row[6]
            f = obtener_funcion(fx)
            df = obtener_derivada(dfx)
            if f is None or df is None:
                continue
            esperado = parsear_solucion_esperada(esperado_str)
            if esperado is None:
                continue
            ejercicios.append({
                "num": num, "fx": fx, "f": f, "df": df,
                "x0": float(x0), "er": float(er), "n": int(n),
                "esperado": esperado,
            })
        except (ValueError, IndexError):
            continue
    return ejercicios


def cargar_ejercicios_riemann(contenido):
    """Carga ejercicios de integracion Riemann desde el contenido del MD."""
    filas = parsear_tabla_md(contenido, "## Integración numérica", "## Polinomio de Taylor")
    ejercicios = []
    for row in filas:
        if len(row) < 6:
            continue
        try:
            num, fx, a, b, n, metodo, esperado_str = row[0], row[1], row[2], row[3], row[4], row[5], row[6]
            f = obtener_funcion(fx)
            if f is None:
                continue
            esperado = parsear_solucion_esperada(esperado_str)
            if esperado is None:
                continue
            # Tratar limite b=π
            b_str = str(b).strip()
            if "π" in b_str or b_str.lower() == "pi":
                b_val = math.pi
            else:
                b_val = float(b)
            ejercicios.append({
                "num": num, "fx": fx, "f": f,
                "a": float(a), "b": b_val,
                "n": int(n), "metodo": metodo.strip(),
                "esperado": esperado,
            })
        except (ValueError, IndexError):
            continue
    return ejercicios


def cargar_ejercicios_taylor(contenido):
    """Carga ejercicios de polinomio de Taylor desde el contenido del MD."""
    filas = parsear_tabla_md(contenido, "## Polinomio de Taylor", "## Valores exactos")
    ejercicios = []
    for row in filas:
        if len(row) < 6:
            continue
        try:
            num, fx, a, n, x_eval, esperado_str = row[0], row[1], row[2], row[3], row[4], row[5]
            f = obtener_funcion(fx)
            if f is None:
                continue
            esperado = parsear_solucion_esperada(esperado_str)
            if esperado is None:
                continue
            ejercicios.append({
                "num": num, "fx": fx, "f": f,
                "a": float(a), "n": int(n), "x_eval": float(x_eval),
                "esperado": esperado,
            })
        except (ValueError, IndexError):
            continue
    return ejercicios


def evaluar_raiz(resultado, esperado, tolerancia=TOL_RAIZ):
    """Verifica si la raiz aproximada esta dentro de la tolerancia."""
    raiz, _ = resultado
    error = abs(raiz - esperado)
    ok = error <= tolerancia
    return ok, error


def evaluar_integral(resultado, esperado, tolerancia=TOL_INTEGRAL):
    """Verifica si la integral aproximada esta dentro de la tolerancia."""
    error = abs(resultado - esperado)
    ok = error <= tolerancia
    return ok, error


def evaluar_taylor(resultado, esperado, tolerancia=TOL_TAYLOR):
    """Verifica si la aproximacion de Taylor esta dentro de la tolerancia."""
    valor_aprox = resultado[0] if isinstance(resultado, tuple) else resultado
    error = abs(valor_aprox - esperado)
    ok = error <= tolerancia
    return ok, error


def run_tests_biseccion(ejercicios, mostrar_proceso=False):
    """Ejecuta los ejercicios de biseccion cargados del documento."""
    print("\n" + "=" * 60)
    print("TESTS - METODO DE BISECCION")
    print("=" * 60)

    aprobados = 0
    for ej in ejercicios:
        try:
            resultado = biseccion.biseccion(
                ej["f"], ej["a"], ej["b"],
                er=ej["er"], n=ej["n"],
                mostrar_proceso=mostrar_proceso
            )
            ok, error = evaluar_raiz(resultado, ej["esperado"])
            simbolo = "OK" if ok else "FALLO"
            fx_safe = _safe_fx(ej['fx'])
            print(f"  [{simbolo}] #{ej['num']} f(x)={fx_safe} | raiz={resultado[0]:.6f} | esperado~{ej['esperado']:.4f} | error={error:.2e}")
            if ok:
                aprobados += 1
        except Exception as e:
            print(f"  [FALLO] #{ej['num']} f(x)={_safe_fx(ej['fx'])} - Excepcion: {str(e)[:50]}")

    return aprobados, len(ejercicios)


def _safe_fx(s):
    """Convierte caracteres Unicode a ASCII para imprimir en Windows."""
    return (s or "").replace('\u2248', '~').replace('\u221a', 'sqrt').replace('\u00b2', '^2').replace('\u00b3', '^3').replace('\u2074', '^4')


def run_tests_newton(ejercicios, mostrar_proceso=False):
    """Ejecuta los ejercicios de Newton-Raphson cargados del documento."""
    print("\n" + "=" * 60)
    print("TESTS - METODO DE NEWTON-RAPHSON")
    print("=" * 60)

    aprobados = 0
    for ej in ejercicios:
        try:
            resultado = newton_raphson.newton_raphson(
                ej["f"], ej["df"], ej["x0"],
                er=ej["er"], n=ej["n"],
                mostrar_proceso=mostrar_proceso
            )
            ok, error = evaluar_raiz(resultado, ej["esperado"])
            simbolo = "OK" if ok else "FALLO"
            fx_safe = _safe_fx(ej['fx'])
            print(f"  [{simbolo}] #{ej['num']} f(x)={fx_safe} | raiz={resultado[0]:.6f} | esperado~{ej['esperado']:.4f} | error={error:.2e}")
            if ok:
                aprobados += 1
        except Exception as e:
            print(f"  [FALLO] #{ej['num']} f(x)={_safe_fx(ej['fx'])} - Excepcion: {str(e)[:50]}")

    return aprobados, len(ejercicios)


def run_tests_riemann(ejercicios, mostrar_proceso=False):
    """Ejecuta los ejercicios de integracion Riemann cargados del documento."""
    print("\n" + "=" * 60)
    print("TESTS - INTEGRACION RIEMANN")
    print("=" * 60)

    aprobados = 0
    for ej in ejercicios:
        try:
            resultado = integracion.integrar(
                ej["f"], ej["a"], ej["b"],
                n=ej["n"], metodo=ej["metodo"]
            )
            ok, error = evaluar_integral(resultado, ej["esperado"])
            simbolo = "OK" if ok else "FALLO"
            fx_safe = _safe_fx(ej['fx'])
            b_str = f"{ej['b']:.2f}" if isinstance(ej['b'], float) and ej['b'] == math.pi else str(ej['b'])
            print(f"  [{simbolo}] #{ej['num']} f(x)={fx_safe} [{ej['a']},{b_str}] metodo={ej['metodo']} | obt={resultado:.6f} | esp~{ej['esperado']:.4f} | error={error:.2e}")
            if ok:
                aprobados += 1
        except Exception as e:
            print(f"  [FALLO] #{ej['num']} f(x)={_safe_fx(ej['fx'])} - Excepcion: {str(e)[:50]}")

    return aprobados, len(ejercicios)


def _taylor_func_sympy(fx_str):
    """Devuelve expresion sympy para Taylor si esta disponible."""
    try:
        import sympy as sp
        x = sp.Symbol("x")
        fx = (fx_str or "").strip().lower()
        if "e^x" in fx or "e^" in fx:
            return sp.exp(x)
        if "sin" in fx:
            return sp.sin(x)
        if "cos" in fx:
            return sp.cos(x)
        if "x²" in fx or "x^2" in fx:
            return x**2
        return None
    except ImportError:
        return None


def run_tests_taylor(ejercicios, mostrar_proceso=False):
    """Ejecuta los ejercicios de polinomio de Taylor cargados del documento."""
    if polinomio_taylor is None:
        print("\n  [SALTADO] Polinomio de Taylor: modulo no encontrado o sympy no instalado.")
        return 0, 0

    print("\n" + "=" * 60)
    print("TESTS - POLINOMIO DE TAYLOR")
    print("=" * 60)

    aprobados = 0
    for ej in ejercicios:
        try:
            f_sym = _taylor_func_sympy(ej.get("fx", ""))
            f = f_sym if f_sym is not None else ej["f"]
            resultado = polinomio_taylor.polinomio_taylor(
                f, ej["a"], ej["n"],
                x_eval=ej["x_eval"],
                mostrar_proceso=mostrar_proceso
            )
            valor_aprox = resultado[0] if isinstance(resultado, tuple) else resultado
            ok, error = evaluar_taylor(resultado, ej["esperado"])
            simbolo = "OK" if ok else "FALLO"
            fx_safe = _safe_fx(ej['fx'])
            print(f"  [{simbolo}] #{ej['num']} f(x)={fx_safe} a={ej['a']} n={ej['n']} x={ej['x_eval']} | obt={valor_aprox:.6f} | esp~{ej['esperado']:.4f} | error={error:.2e}")
            if ok:
                aprobados += 1
        except Exception as e:
            print(f"  [FALLO] #{ej['num']} f(x)={_safe_fx(ej['fx'])} - Excepcion: {str(e)[:80]}")

    return aprobados, len(ejercicios)


def main():
    mostrar = "--verbose" in sys.argv or "-v" in sys.argv

    if not os.path.isfile(EJERCICIOS_PATH):
        print(f"Error: No se encuentra el archivo de ejercicios: {EJERCICIOS_PATH}")
        return 1

    with open(EJERCICIOS_PATH, "r", encoding="utf-8") as f:
        contenido = f.read()

    ej_biseccion = cargar_ejercicios_biseccion(contenido)
    ej_newton = cargar_ejercicios_newton(contenido)
    ej_riemann = cargar_ejercicios_riemann(contenido)
    ej_taylor = cargar_ejercicios_taylor(contenido)

    print("\n*** EVALUACION DE EFECTIVIDAD - METODOS NUMERICOS ***")
    print(f"(Ejercicios cargados desde: {EJERCICIOS_PATH})")
    print(f"  Biseccion: {len(ej_biseccion)} | Newton-Raphson: {len(ej_newton)} | Riemann: {len(ej_riemann)} | Taylor: {len(ej_taylor)}")

    total_ok = 0
    total_tests = 0
    b_ok, b_tot, n_ok, n_tot, r_ok, r_tot, t_ok, t_tot = 0, 0, 0, 0, 0, 0, 0, 0

    if ej_biseccion:
        b_ok, b_tot = run_tests_biseccion(ej_biseccion, mostrar_proceso=mostrar)
        total_ok += b_ok
        total_tests += b_tot
    else:
        print("\n  No se cargaron ejercicios de Biseccion.")

    if ej_newton:
        n_ok, n_tot = run_tests_newton(ej_newton, mostrar_proceso=mostrar)
        total_ok += n_ok
        total_tests += n_tot
    else:
        print("\n  No se cargaron ejercicios de Newton-Raphson.")

    if ej_riemann:
        r_ok, r_tot = run_tests_riemann(ej_riemann, mostrar_proceso=mostrar)
        total_ok += r_ok
        total_tests += r_tot
    else:
        print("\n  No se cargaron ejercicios de Riemann.")

    if ej_taylor:
        t_ok, t_tot = run_tests_taylor(ej_taylor, mostrar_proceso=mostrar)
        total_ok += t_ok
        total_tests += t_tot
    else:
        print("\n  No se cargaron ejercicios de Taylor.")

    print("\n" + "=" * 60)
    print("RESUMEN")
    print("=" * 60)
    if ej_biseccion:
        print(f"  Biseccion:      {b_ok}/{b_tot} aprobados")
    if ej_newton:
        print(f"  Newton-Raphson: {n_ok}/{n_tot} aprobados")
    if ej_riemann:
        print(f"  Riemann:        {r_ok}/{r_tot} aprobados")
    if ej_taylor and polinomio_taylor:
        print(f"  Taylor:         {t_ok}/{t_tot} aprobados")
    print(f"  TOTAL:          {total_ok}/{total_tests} aprobados")
    print("=" * 60)

    if total_ok == total_tests and total_tests > 0:
        print("  RESULTADO: Todos los metodos fueron efectivos.")
    elif total_tests > 0:
        print(f"  RESULTADO: {total_tests - total_ok} ejercicio(s) fuera de tolerancia.")
    else:
        print("  RESULTADO: No se pudieron cargar ejercicios.")

    return 0 if total_ok == total_tests and total_tests > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
