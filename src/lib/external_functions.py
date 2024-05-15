def first_element_not_in_set(array, set_b):
    for element in array:
        if element not in set_b:
            return element
    return None 