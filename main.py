import sys
import igraph as ig
from src.lib.read_graph import read_graph
import time
import threading


def run_with_timeout(func, timeout):
    """
    Ejecuta una función con un límite de tiempo y devuelve True si se completó a tiempo, False si se excedió el tiempo.
    """

    def wrapper(stop_event):
        try:
            func()
        except Exception as e:
            print(f"Ocurrió un error al ejecutar la función: {e}")
        stop_event.set()  # Señalar que la función ha terminado

    stop_event = threading.Event()
    thread = threading.Thread(target=wrapper, args=(stop_event,))
    thread.start()

    thread.join(timeout)
    if thread.is_alive():
        print("El tiempo de ejecución excede los 5 minutos, saltando esta parte del código")
        stop_event.set()  # Señalar que el hilo debe detenerse
        thread.join()  # Esperar a que el hilo termine

        return False

    return True


def main():
    # Se leen los argumentos de la línea de comandos
    file_path: str = sys.argv[1]
    g: ig.Graph = read_graph(file_path)

    # Se muestran la cantidad de lados
    print("\033[103;1mCantidad de lados:\033[0m \033[93m",
          len(g.es), "\033[0m")
    # Se muestran la cantidad de nodos
    print("\033[103;1mCantidad de nodos:\033[0m \033[93m",
          len(g.vs), "\033[0m")

    # Invocando D-Satur
    print("\n\033[100;1mInvocando D-Satur...\033[0m")

    g.reset_colors()
    start_time = time.time()

    if run_with_timeout(g.d_satur, 300):
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Tiempo de ejecución: {execution_time} segundos")

        g.group_nodes_by_color()

        is_valid: str = "\033[92;1mTrue" if g.is_valid_coloring(
        ) else "\033[91mFalse"
        print(f"Coloración válida: {is_valid}\033[0m")

    g.reset_colors()

    # Invocando Ave Cleptomana
    print("\n\033[100;1mInvocando a Jhonaiker...\033[0m")

    g.reset_colors()
    start_time = time.time()

    if run_with_timeout(g.kleptom_bird, 1200):
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Tiempo de ejecución: {execution_time} segundos")

        g.group_nodes_by_color()

        is_valid: str = "\033[92;1mTrue" if g.is_valid_coloring(
        ) else "\033[91mFalse"
        print(f"Coloración válida: {is_valid}\033[0m")

    g.reset_colors()


if __name__ == "__main__":
    main()
