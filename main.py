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

    # Invocando Local Search
    print("\n\033[100;1mInvocando Local Search...\033[0m")
    start_time = time.time()

    if run_with_timeout(g.local_search, 300):
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Tiempo de ejecución: {execution_time} segundos")

        g.group_nodes_by_color()

        is_valid: str = "\033[92;1mTrue" if g.is_valid_coloring(
        ) else "\033[91mFalse"
        print(f"Coloración válida: {is_valid}\033[0m")

    # # Invocando Backtracking
    # print("\n\033[100;1mInvocando Backtracking...\033[0m")

    # g.reset_colors()

    # if len(g.vs) == 0:
    #     print("\033[91;1mError:\033[0m Backtracking no pudo colorear el grafo")
    # else:
    #     start_time = time.time()

    #     if run_with_timeout(g.backtracking, 120):
    #         end_time = time.time()
    #         execution_time = end_time - start_time
    #         print(f"Tiempo de ejecución: {execution_time} segundos")

    #         g.group_nodes_by_color()

    #         is_valid: str = "\033[92;1mTrue" if g.is_valid_coloring(
    #         ) else "\033[91mFalse"
    #         print(f"Coloración válida: {is_valid}\033[0m")

    # Invocando GRASP
    print("\n\033[100;1mInvocando GRASP...\033[0m")

    g.reset_colors()

    if len(g.vs) == 0:
        print("\033[91;1mError:\033[0m GRASP no pudo colorear el grafo")
    else:
        start_time = time.time()

        if run_with_timeout(g.grasp, 300):
            end_time = time.time()
            execution_time = end_time - start_time
            print(f"Tiempo de ejecución: {execution_time} segundos")

            g.group_nodes_by_color()

            is_valid: str = "\033[92;1mTrue" if g.is_valid_coloring(
            ) else "\033[91mFalse"
            print(f"Coloración válida: {is_valid}\033[0m")

    # Invocando Tabu Search
    print("\n\033[100;1mInvocando Tabu Search...\033[0m")

    g.reset_colors()

    if len(g.vs) == 0:
        print("\033[91;1mError:\033[0m Tabu Search no pudo colorear el grafo")
    else:
        start_time = time.time()

        if run_with_timeout(g.tabu_search, 300):
            end_time = time.time()
            execution_time = end_time - start_time
            print(f"Tiempo de ejecución: {execution_time} segundos")

            g.group_nodes_by_color()

            is_valid: str = "\033[92;1mTrue" if g.is_valid_coloring(
            ) else "\033[91mFalse"
            print(f"Coloración válida: {is_valid}\033[0m")

    # Invocando Algoritmo Genético
    print("\n\033[100;1mInvocando Algoritmo Genético...\033[0m")

    g.reset_colors()

    if len(g.vs) == 0:
        print(
            "\033[91;1mError:\033[0m Algoritmo Genético no pudo colorear el grafo")
    else:
        start_time = time.time()

        if run_with_timeout(g.genetic_algorithm, 300):
            end_time = time.time()
            execution_time = end_time - start_time
            print(f"Tiempo de ejecución: {execution_time} segundos")

            g.group_nodes_by_color()

            is_valid: str = "\033[92;1mTrue" if g.is_valid_coloring(
            ) else "\033[91mFalse"
            print(f"Coloración válida: {is_valid}\033[0m")

    g.reset_colors()

    # Invocando Simulated Annealing
    print("\n\033[100;1mInvocando Simulated Annealing...\033[0m")

    if len(g.vs) == 0:
        print(
            "\033[91;1mError:\033[0m Simulated Annealing no pudo colorear el grafo")
    else:
        start_time = time.time()

        if run_with_timeout(g.simulated_annealing, 300):
            end_time = time.time()
            execution_time = end_time - start_time
            print(f"Tiempo de ejecución: {execution_time} segundos")

            g.group_nodes_by_color()

            is_valid: str = "\033[92;1mTrue" if g.is_valid_coloring(
            ) else "\033[91mFalse"
            print(f"Coloración válida: {is_valid}\033[0m")

    # Invocando Iterated Local Search
    print("\n\033[100;1mInvocando Iterated Local Search...\033[0m")

    g.reset_colors()

    if len(g.vs) == 0:
        print(
            "\033[91;1mError:\033[0m Iterated Local Search no pudo colorear el grafo")
    else:
        start_time = time.time()

        if run_with_timeout(g.ils, 300):
            end_time = time.time()
            execution_time = end_time - start_time
            print(f"Tiempo de ejecución: {execution_time} segundos")

            g.group_nodes_by_color()

            is_valid: str = "\033[92;1mTrue" if g.is_valid_coloring(
            ) else "\033[91mFalse"
            print(f"Coloración válida: {is_valid}\033[0m")


if __name__ == "__main__":
    main()
