from typing import Set, List
import igraph as ig
from src.lib.external_functions import first_element_not_in_set
import math
import random

def calculate_rounded_percentages(number: int) -> List[int]:
    """
    Calcula los porcentajes de un número en incrementos de 0.05 desde 0.05 hasta 0.50 y redondea hacia arriba.
    """
    percentages = []
    # Iterar sobre los valores de porcentaje en incrementos de 0.05 desde 0.05 hasta 0.5
    for percent in range(5,50, 5):
        # Calcular el porcentaje correspondiente y redondear hacia arriba
        percentage_value = math.ceil(number * percent / 100)
        percentages.append(percentage_value)
        
    return percentages

def get_random_values(array, n):
    # Verificar que n no sea mas grande que el tamaño del array
    n = min(n, len(array))
    # Obtener n valores random del array
    random_values = random.sample(array, n)
    return random_values

def ils(self: ig.Graph):
    
    self.random_color_graph()
    amount_of_colors = self.number_of_colors()

    current_colors_in_graph = self.colors_used()
    iterations_percentage = calculate_rounded_percentages(amount_of_colors)
    current_vertex_state = self.save_vertex_state()    
    i = 0
    
    while i < len(iterations_percentage):
        
        list_of_colors_to_eliminate = get_random_values(current_colors_in_graph, i)
        
        for color_of_node in list_of_colors_to_eliminate:
            self.uncolor(color_of_node)
            
        self.d_satur()        
    
        new_amount_of_colors_used = self.get_amount_of_colors()
    
        if new_amount_of_colors_used < amount_of_colors:
            amount_of_colors = new_amount_of_colors_used
            current_colors_in_graph = self.colors_used()
            current_vertex_state = self.save_vertex_state()
            print("Number ", amount_of_colors)
            i = 0  # Reiniciar el contador
        elif i == len(iterations_percentage) - 1:
            self.local_search()
            new_amount_of_colors_used = self.get_amount_of_colors()
            if(new_amount_of_colors_used < amount_of_colors):
                amount_of_colors = new_amount_of_colors_used
                current_colors_in_graph = self.colors_used()
                current_vertex_state = self.save_vertex_state()
                print("Number ", amount_of_colors)
                i = 0  # Reiniciar el contador                
         
        else:
            self.load_vertex_state(current_vertex_state)
            i += 1       
    