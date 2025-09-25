class Graph:
    
    # конструкторы
    def __init__(self): # конструктор по умолчанию
        self.name = "G" # по умолчанию имя графа G (имя может быть любой строкой)
        self.is_directed = False # по умолчанию граф неориентированный
        self.is_weighted = False # по умолчанию граф невзвешенный
        self.adj_list = {} # по умолчанию список (словарь) смежности пустой

    def __init__(self, name, is_directed, is_weighted, adj_list): # основной констуктор
        self.name = name
        self.is_directed = is_directed
        self.is_weighted = is_weighted
        self.adj_list = adj_list

    def copy_constuctor(self, original): # констуктор копии
        self.name = original.name
        self.is_directed = original.is_directed
        self.is_weighted = original.is_weighted
        self.adj_list = original.adj_list


    def add_vertex(self, new_vertex): # добавить вершину
        if not isinstance(new_vertex, str):
            print("Некорректный формат данных\n")
        elif new_vertex in self.adj_list:
            print("Данная вершина уже есть в графе\n")
        else:
            self.adj_list[new_vertex] = []
            print(f"Вершина {new_vertex} успешно добавлена!\n")

    def file_constuctor(self, file_path): # конструктор из файла
        graphs = []
        current_graph = None
        
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.readlines()
        
        i = 0
        for i in range(0, len(text)):
            line = text[i].strip()
            if line == "":
                i += 1
                continue
            if line.startswith("Граф "):
                if current_graph is not None:
                    graphs.append(current_graph)
                graph_name = line[5:].strip()
                current_graph = self.name(graph_name)
            elif current_graph is not None:
                if line.startswith("Граф "):
                    self.name = line[6:]
                elif line.startswith("Вид: "):
                    if line[5:line.rfind(" ")].lower() == "неориентированный": self.is_directed = False
                    elif line[5:line.rfind(" ")].lower() == "ориентированный": self.is_directed = True
                    elif line[line.rfind(" "):].lower() == "взвешенный": self.is_weighted = True
                    elif line[line.rfind(" "):].lower() in ("невзвешенный", ""): self.is_weighted = False
                    else:
                        print(f"Ошибка считывания графа с файла: неверный тип\n")
                        break
                elif ":" in line:
                    parts = line.split(":")
                    if len(parts) >= 2:
                        vertex = parts[0].strip()
                        current_graph.add_vertex(vertex)
                        
                        edges_str = parts[1].strip()
                        if edges_str:
                            edges = [edge.strip() for edge in edges_str.split(",")]
                            
                            for edge in edges:
                                if current_graph.is_weighted:
                                    if "(" in edge and ")" in edge:
                                        end_vertex = edge.split("(")[0].strip()
                                        weight_str = edge.split("(")[1].split(")")[0]
                                        try:
                                            weight = float(weight_str)
                                            current_graph.add_edge((vertex, end_vertex, weight))
                                        except ValueError:
                                            print(f"Ошибка: некорректный вес '{weight_str}' для ребра {vertex}-{end_vertex}")
                                    else:
                                        current_graph.add_edge((vertex, edge, 0.0))
                                else:
                                    current_graph.add_edge((vertex, edge))
            
            i += 1
        if current_graph is not None:
            graphs.append(current_graph)
        return graphs
    
    # методы
    def transform_adjlist(self): # превратить список смежности в список рёбер
        print (f"Превращение списка смежности графа {self.name} в список ребёр\n")
        edge_list = []
        for k, v in self.adjlist:
            for vs in v:
                edge = k + vs
                if not self.isDirected:
                    if edge not in edge_list and edge.reverse() not in edge_list:
                        edge_list.append(edge, edge.reverse())
                else:
                    if edge not in edge_list:
                        edge_list.append(edge)

    def write_adjlist(self, file_path): # записать список смежности в файл
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"Граф {self.name}\n")
            directed_str = "ориентированный" if self.is_directed else "неориентированный"
            weighted_str = "взвешенный" if self.is_weighted else "невзвешенный"
            f.write(f"Вид: {directed_str} {weighted_str}\n")
            
            for vertex, neighbors in self.adj_list.items():
                f.write(f"{vertex}: ")
                neighbor_strs = []
                for neighbor in neighbors:
                    if self.is_weighted:
                        end_vertex, weight = neighbor
                        neighbor_strs.append(f"{end_vertex}({weight})")
                    else:
                        neighbor_strs.append(neighbor)
                f.write(", ".join(neighbor_strs))
                f.write("\n")
            f.write("\n")  # Пустая строка между графами

    def add_edge(self, new_edge): # добавить ребро (дугу)
        if len(new_edge) == 2:
            start_vertex, end_vertex = new_edge
            weight = 0.0  # вес по умолчанию для невзвешенных графов
        elif len(new_edge) == 3:
            start_vertex, end_vertex, weight = new_edge
        else:
            print("Некорректный формат данных\n")
        
        if start_vertex not in self.adj_list:
            self.add_vertex(start_vertex)
        if end_vertex not in self.adj_list:
            self.add_vertex(end_vertex)
        
        if self.is_weighted:
            self.adj_list[start_vertex].append((end_vertex, weight))
            if not self.is_directed:
                self.adj_list[end_vertex].append((start_vertex, weight))
        else:
            self.adj_list[start_vertex].append(end_vertex)
            if not self.is_directed:
                self.adj_list[end_vertex].append(start_vertex)
        
        print(f"Ребро {start_vertex}-{end_vertex} успешно добавлено!\n")
        if self.is_weighted:
            print(f"Вес: {weight}\n")

    def del_vertex(self, unnecessary_vertex):  # удалить вершину
        if unnecessary_vertex not in self.adj_list:
            print("Вершины нет в графе\n")
        
        for vertex in self.adj_list:
            if self.is_weighted:
                self.adj_list[vertex] = [neighbor for neighbor in self.adj_list[vertex] 
                                       if neighbor[0] != unnecessary_vertex]
            else:
                self.adj_list[vertex] = [neighbor for neighbor in self.adj_list[vertex] 
                                       if neighbor != unnecessary_vertex]
        
        del self.adj_list[unnecessary_vertex]
        print(f"Вершина {unnecessary_vertex} успешно удалена!\n")

    def del_edge(self, unnecessary_edge): # удалить ребро (дугу)
        if len(unnecessary_edge) < 2:
            print("Некорректный формат ребра\n")
            return False
        
        start_vertex, end_vertex = unnecessary_edge[0], unnecessary_edge[1]
        
        if start_vertex not in self.adj_list or end_vertex not in self.adj_list:
            print("Одна или обе вершины не найдены в графе\n")
            return False
        3
        # Удаляем ребро
        if self.is_weighted:
            self.adj_list[start_vertex] = [neighbor for neighbor in self.adj_list[start_vertex] 
                                         if neighbor[0] != end_vertex]
            if not self.is_directed:
                self.adj_list[end_vertex] = [neighbor for neighbor in self.adj_list[end_vertex] 
                                           if neighbor[0] != start_vertex]
        else:
            if end_vertex in self.adj_list[start_vertex]:
                self.adj_list[start_vertex].remove(end_vertex)
            if not self.is_directed and start_vertex in self.adj_list[end_vertex]:
                self.adj_list[end_vertex].remove(start_vertex)
        
        print(f"Ребро {start_vertex}-{end_vertex} успешно удалено!\n")
        return True
    
    def print_adjlist(self): # вывести список смежности в консоль 
        print("Список смежности графа {self.name}: ")
        for k, v in self.adj_list:
            print(f"{k}: ")
            for vs in v:
                print(f'{vs}, ')
            print("\n")

# Чтение всех графов из файла
graphs = Graph.file_constuctor("graphs.txt")

# Печать всех графов
for graph in graphs:
    graph.print_adjlist()

# Добавление ребра в первый граф
if graphs:
    graphs[0].add_edge(("A", "D", 2.5))