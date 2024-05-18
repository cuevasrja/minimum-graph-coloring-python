# Minimum Graph Coloring Python

**Realizado Por:**
- Joao Pinto. (17-10490)
- Jhonaiker Blanco. (18-10784)
- Juan Cuevas. (19-10056)

Este proyecto fue realizado para la materia de Diseño de Algoritmos 2 de la Universidad Simón Bolívar. El objetivo de este proyecto es resolver el problema de coloración mínima de grafos. Para esto se implementaron diversas técnicas de resolución, las cuales se describen a continuación.

## Uso

Para ejecutar el programa, se debe correr el archivo `main.py` con el siguiente comando:

```bash
python main.py <archivo>
```

> [!WARNING] Advertencia
> En caso de no tener las librerias de Python necesarias, se puede instalar con el siguiente comando:
> ```bash
> pip install -r requirements.txt
> ```

> [!NOTE] Nota
> El archivo debe estar en el formato DIMACS y su extensión debe ser `.col`. En la carpeta `/data` se encuentran algunos ejemplos de archivos que se pueden utilizar. Para más información sobre el formato DIMACS, se puede consultar [aquí](http://mat.tepper.cmu.edu/COLOR/instances.html).

## Entrega 1

Para la primera entrega, se implementaron los siguientes algoritmos:

- **Busqueda Local con vecindad Kempe**: Este algoritmo se basa en la técnica de búsqueda local, donde se intercambian los colores de dos nodos vecinos. La vecindad de Kempe se define como el conjunto de nodos que comparten un color con el nodo seleccionado. Para este algoritmo, se implementaron dos variantes: una que selecciona los nodos de forma aleatoria y otra que selecciona los nodos de forma determinística.
- **D Satur**: Este algoritmo se basa en la técnica de coloreo de nodos por saturación. La saturación de un nodo es la cantidad de colores diferentes que tiene en sus vecinos. El algoritmo selecciona el nodo con mayor saturación y le asigna el color que minimice la cantidad de conflictos.
- **Busqueda Exacta (Backtracking)**: Este algoritmo se basa en la técnica de backtracking, donde se prueban todas las posibles combinaciones de colores para los nodos del grafo. Para este algoritmo, se implementaron dos variantes: una que selecciona los nodos de forma aleatoria y otra que selecciona los nodos de forma determinística.

Además, se realizaron pruebas para evaluar el desempeño de los algoritmos implementados. Para más información sobre los algoritmos y las pruebas realizadas, se puede consultar el archivo `explain.md` en la carpeta de este corte. Puede acceder a este archivo [aquí](src/corte1/explain.md).