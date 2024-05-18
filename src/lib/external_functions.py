from typing import List, Set, Any

def first_element_not_in_set(array: List[Any], set_b: Set[Any]) -> Any|None:
    """
    Retorna el primer elemento de la lista que no está en el conjunto especificado.
    """

    for element in array:
        if element not in set_b:
            return element
    return None
