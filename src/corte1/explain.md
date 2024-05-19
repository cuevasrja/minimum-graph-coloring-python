# Corte 1 - Minimum Graph Coloring

**Realizado Por:**
- Joao Pinto. (17-10490)
- Jhonaiker Blanco. (18-10784)
- Juan Cuevas. (19-10056)

En este corte se implementaron soluciones para el problema de coloración mínima de grafos. Se implementaron 3 algoritmos diferentes para resolver este problema, los cuales son:
- Algoritmo de Búsqueda Local con vecindad de Kempe.
- Algoritmo de D Satur.
- Algoritmo de Búsqueda Exacta (Backtracking).

Para la implementación de estos algoritmos se utilizó el lenguaje de programación Python, y se utilizó la librería iGraph para la representación de grafos y algunas operaciones sobre estos.

## Algoritmos usados

### D Satur

El algoritmo de D Satur se basa en la técnica de coloreo de nodos por saturación. La saturación de un nodo es la cantidad de colores diferentes que tiene en sus vecinos. El algoritmo selecciona el nodo con mayor saturación y le asigna el color que minimice la cantidad de conflictos. 

### Búsqueda Exacta (Backtracking)

El algoritmo de Búsqueda Exacta se basa en la técnica de backtracking, donde se prueban todas las posibles combinaciones de colores para los nodos del grafo. Para este algoritmo, se implementó una variante que premite podar el árbol de búsqueda, seleccionando los nodos de forma determinística. La poda se realiza cuando se llega a un nodo que no tiene solución, es decir, cuando se llega a un nodo que no se puede colorear con los colores disponibles, o cuando se llega a una solución que no es mejor que la mejor solución encontrada hasta el momento.

### Búsqueda Local con vecindad de Kempe

El algoritmo de Búsqueda Local con vecindad de Kempe se basa en la técnica de búsqueda local, donde se intercambian los colores de dos nodos vecinos. La vecindad de Kempe se define como el conjunto de nodos que comparten un color con el nodo seleccionado. Para empezar la búsqueda local, se toma un grafo con una coloración válida usando el algoritmo de D Satur. Luego, se seleccionan dos nodos de forma determinística y se intercambian sus colores. Si la solución resultante es mejor que la solución actual, se actualiza la solución actual con la nueva solución. Este proceso se repite hasta que no se puedan encontrar soluciones mejores.



## Pruebas

## Resultados

## Conclusiones