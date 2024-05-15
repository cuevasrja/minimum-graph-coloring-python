def vertex_with_max_saturation(self):
    # Filtrar los vértices que tienen el atributo 'color' como una cadena vacía
    filtered_vertices = [v for v in self.vs if v['color'] == '']
    if not filtered_vertices:
        return -1  # Retorna None si no hay vértices con color como cadena vacía
    # Encontrar el vértice con la saturación máxima entre los filtrados
    max_saturation_vertex = max(filtered_vertices, key=lambda v: v['saturation'])
    # Obtener el índice del nodo con máxima saturación en la lista original
    return max_saturation_vertex["index"]

def adjacent_colors(self, node_index):
    adjacent_indices = self.neighbors(node_index, mode="ALL")
    colors = {self.vs[neighbor]['color'] for neighbor in adjacent_indices if self.vs[neighbor]['color']}
    return colors

# Definir el método como un método de instancia de la clase igraph.Graph
def change_color_and_increase_saturation(self, node_index, new_color):
    # Cambiar el color del nodo especificado
    self.vs[node_index]['color'] = new_color
    
    # Obtener los nodos adyacentes
    adjacent_indices = self.neighbors(node_index, mode="ALL")
    
    # Aumentar en 1 la saturación de los nodos adyacentes
    for neighbor in adjacent_indices:
        self.vs[neighbor]['saturation'] += 1
  
def group_nodes_by_color(self):
    # Crear un diccionario para almacenar los nodos agrupados por color
    nodes_by_color = {}
        
    # Iterar sobre todos los nodos
    for v in self.vs:
        color = v['color']
        if color in nodes_by_color:
            nodes_by_color[color].append(v.index)
        else:
            nodes_by_color[color] = [v.index]
        
    # Imprimir los nodos agrupados por color
    for color, nodes in nodes_by_color.items():
        print(f"Color {color}: {', '.join(map(str, nodes))}")
        
    # Imprimir el número total de colores
    total_colors = len(nodes_by_color)
    print(f"Número total de colores: {total_colors}")        
        