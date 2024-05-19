# Minimum Graph Coloring Python

**Realizado Por:**
- Joao Pinto. (17-10490)
- Jhonaiker Blanco. (18-10784)
- Juan Cuevas. (19-10056)

Este proyecto fue realizado para la materia de Diseño de Algoritmos 2 de la Universidad Simón Bolívar. El objetivo de este proyecto es resolver el problema de coloración mínima de grafos. Para esto se implementaron diversas técnicas de resolución, las cuales se describen a continuación.

## Configuración de entorno

Para ejecutar le proyecto, se debe tener instalado Python 3.8 o superior. 

Para instalar las librerías necesarias, se recomienda crear un entorno virtual. Para esto, se puede utilizar el siguiente comando:

```bash
python -m venv venv
```

Luego, se debe activar el entorno virtual con el siguiente comando:

```bash
source venv/bin/activate
```

Finalmente, se deben instalar las librerías necesarias con el siguiente comando:

```bash
pip install -r requirements.txt
```

Para desactivar el entorno virtual, se debe ejecutar el siguiente comando:

```bash
deactivate
```

Es **importante** tener en cuenta que **el entorno virtual debe estar activado** para poder ejecutar el programa.

## Uso

Para ejecutar el programa, se debe correr el archivo `main.py` con el siguiente comando:

```bash
python main.py <archivo>
```

> El archivo debe estar en el formato DIMACS y su extensión debe ser `.col`. En la carpeta `/data` se encuentran algunos ejemplos de archivos que se pueden utilizar. Para más información sobre el formato DIMACS, se puede consultar [aquí](http://mat.tepper.cmu.edu/COLOR/instances.html).

## Entrega 1

Para la primera entrega, se implementaron los siguientes algoritmos:

- **Busqueda Local con vecindad de Kempe**: El algoritmo de búsqueda local explora el espacio de soluciones a partir de una solución inicial, moviéndose a soluciones vecinas que mejoren la solución actual. Para esta implementación, se utilizó la vecindad de Kempe, la cual consiste en intercambiar los colores de las componentes conexas de los subgrafos inducidos por los nodos que tienen dos colores fijos, para todos los pares de colores diferentes presentes en la solución.

- **D-Satur**: Este algoritmo es una heurística especializada para el problema de coloración de grafos, y su componente principal es el coloreado de nodos según su grado de saturación. El grado de saturación de un nodo es la cantidad de colores diferentes que tiene en sus vecinos. El algoritmo selecciona el nodo con mayor grado de saturación y le asigna el color que minimice la cantidad de conflictos.

- **Busqueda Exacta (Backtracking)**: Este algoritmo se basa en el algoritmo de backtracking, donde se prueban todas las posibles combinaciones de colores para los nodos del grafo. Para este algoritmo, se implementó una variante que permite podar el árbol de búsqueda, podando aquellas coloraciones parciales que no sean válidas ó que produzcan soluciones con mayor numero de colores que la mejor solucion hasta el momento.

Además, se realizaron pruebas para evaluar el desempeño de los algoritmos implementados. Para más información sobre los algoritmos y las pruebas realizadas, se puede consultar el archivo `explain.md` en la carpeta de este corte. Puede acceder a este archivo [aquí](src/corte1/explain.md).