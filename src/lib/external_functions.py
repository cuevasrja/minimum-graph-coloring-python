def first_element_not_in_set(array, set_b):
    """
    Retorna el primer elemento de la lista que no está en el conjunto especificado.
    """

    for element in array:
        if element not in set_b:
            return element
    return None
