from typing import List, Set, Any
import random

def first_element_not_in_set(array: List[Any], set_b: Set[Any]) -> Any|None:
    """
    Retorna el primer elemento de la lista que no está en el conjunto especificado.
    """

    for element in array:
        if element not in set_b:
            return element
    return None

def filter_elements_of_array(array: List[Any], conjunto: Set[Any]) -> List[Any]:
    # Utilizar una lista por comprensión para filtrar los elementos
    return [elemento for elemento in array if elemento not in conjunto]

def delete_random_value_from_list(lst: List[int]) -> int:
    # Seleccionar un valor aleatorio de la lista
    valor_aleatorio = random.choice(lst)
    # Eliminar el valor aleatorio de la lista
    lst.remove(valor_aleatorio)
    # Devolver el valor aleatorio eliminado
    return valor_aleatorio