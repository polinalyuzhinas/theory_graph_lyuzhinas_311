# !-- поменять формат вводимых рёбер (разбить на составляющие: ввести сначала начало, потом конец, потом вес если надо) 
class Graph:
    
    # конструкторы
    def __init__(self, name="G", is_directed=False, is_weighted=False, adj_list=None): # конструктор по умолчанию
        self.name = name # строка - имя графа (по умолчанию G)
        self.is_directed = is_directed # ориентирован ли граф (булево значение), по умолчанию гриф неориентирован
        self.is_weighted = is_weighted # взвешен ли граф (булево значение), по умлчанию граф невзвешен
        self.adj_list = adj_list if adj_list is not None else {} # список смежности (структура данных - словарь)


    def copy_constructor(self, original): # констуктор копии
        self.name = original.name
        self.is_directed = original.is_directed
        self.is_weighted = original.is_weighted
        self.adj_list = original.adj_list

    def file_constructor(self, file_path): # конструктор из файла (возвращает список объектов класса Graph)
        graphs = []
        current_graph = None
        
        with open(file_path, "r", encoding="utf-8") as f: # кодировка считываемого файла utf-8
            text = f.readlines()
        
        for i in range(0, len(text)):
            line = text[i].strip()
            if line == "":
                continue
            if line.startswith("Граф "):
                if current_graph is not None:
                    graphs.append(current_graph)
                current_graph = Graph(line[5:].strip())
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
                if len(parts) >= 2: # строка должна быть вида A: [B, C] или A:
                    vertex = parts[0].strip() # одна из вершин
                    current_graph.add_vertex(vertex)
                    edges = parts[1].strip() # вершины, с которыми связана вершина из переменной vertex
                    if edges:
                        for edge in [e.strip() for e in edges.split(",")]: # переводим строку в список
                            if current_graph.is_weighted:
                                if "(" in edge and ")" in edge:
                                    end_vertex = edge.split("(")[0].strip()
                                    weight_str = edge.split("(")[1].split(")")[0]
                                    try:
                                        weight = float(weight_str) # попытка перевести вес в число
                                        current_graph.add_edge((vertex, end_vertex, weight))
                                    except ValueError:
                                        print(f"Ошибка: некорректный вес {weight_str} для ребра {vertex}-{end_vertex}")
                                        break
                                else:
                                    current_graph.add_edge((vertex, edge, 0.0)) # по умолчанию вес ребра - 0
                            else:
                                current_graph.add_edge((vertex, edge))
        if current_graph is not None:
            graphs.append(current_graph) 
        return graphs

    # методы
    def transform_adj_list(self): # преобразовать список смежности в список рёбер
        if not self.adj_list:
            print("Список смежнсти графа пуст, соответсвенно преобразовывать нечего\n")
            return False
        print(f"Превращение списка смежности графа {self.name} в список рёбер\n")
        edge_list = []
    
        for vertex, neighbors in self.adj_list.items():
            for neighbor in neighbors:
                if self.is_weighted:
                    end_vertex, weight = neighbor # neighbor = (end_vertex, weight)
                    edge = (vertex, end_vertex, weight)
                    reverse_edge = (end_vertex, vertex, weight)
                else:
                    end_vertex = neighbor # neighbor = end_vertex
                    edge = (vertex, end_vertex)
                    reverse_edge = (end_vertex, vertex)
                
                if not self.is_directed:
                    edge_comparator = (lambda e1, e2: e1[:2] == e2[:2]) if not self.is_weighted else (lambda e1, e2: e1 == e2) # в взвешенных графах выбрасываем из сравнения веса, в обратном случае - сравниваем напрямую
                    edge_exists = any(edge_comparator(e, edge) for e in edge_list) # проверяем, что ребра нет в графе
                    reverse_exists = any(edge_comparator(e, reverse_edge) for e in edge_list) # проверяем, что обратного ребра нет в графе
                    
                    if not edge_exists and not reverse_exists:
                        edge_list.append("".join(edge[:2]))
                else:
                    edge_comparator = (lambda e1, e2: e1[:2] == e2[:2]) if not self.is_weighted else (lambda e1, e2: e1 == e2)
                    edge_exists = any(edge_comparator(e, edge) for e in edge_list) # проверяем, что ребра нет в графе
                    if not edge_exists:
                        edge_list.append("".join(edge[:2]))
        return edge_list


    def write_to_file(self, file_path): # записать граф в файл
        with open(file_path, "w", encoding="utf-8") as f: # создать файл с кодировкой utf-8
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
                f.write(", ".join(neighbor_strs)) # соседей перечислить через запятую
                f.write("\n")
            f.write("\n")  # пустая строка между графами (просто для красоты)


    def add_vertex(self, new_vertex): # добавить вершину
        if not isinstance(new_vertex, str): # если вершина не переводится в строку
            print("Некорректный формат данных\n")
            return False
        elif new_vertex in self.adj_list:
            print(f"Вершина {new_vertex} уже есть в графе\n")
            return False
        else:
            self.adj_list[new_vertex] = [] # по умолчанию у вершины нет соседей
            print(f"Вершина {new_vertex} успешно добавлена!\n")
            return True

    def add_edge(self, new_edge): # добавить ребро (дугу)
        if not self.is_weighted:
            if len(new_edge) == 2: # у ребра должен быть формат (start, end)
                start_vertex, end_vertex = new_edge
                weight = 0.0  # вес по умолчанию для невзвешенных графов
            else:
                print("Ребро задано некорректно: для невзвешенного графа ожидается 2 параметра\n")
                return False
        elif self.is_weighted:
            if len(new_edge) == 3: # если с весом, то (start, end, weight)
                start_vertex, end_vertex, weight = new_edge
            else:
                print("Ребро задано некорректно: для взвешенного графа ожидается 3 параметра\n")
                return False
        
        if not isinstance(start_vertex, str) or not isinstance(end_vertex, str):
            print("Некорректный формат вершин")
            return False
            
        if self.is_weighted and not isinstance(weight, (int, float)):
            print("Некорректный формат веса. Ожидается число.\n")
            return False
        
        if start_vertex not in self.adj_list:
            print(f"Вершина {start_vertex} не существует в графе. Добавьте её сначала.\n")
            return False
        if end_vertex not in self.adj_list:
            print(f"Вершина {end_vertex} не существует в графе. Добавьте её сначала.\n")
            return False
        
        if self.is_weighted:
            existing_edges = [neighbor for neighbor in self.adj_list[start_vertex] 
                        if neighbor[0] == end_vertex]
            if existing_edges:
                print(f"Ребро {start_vertex}-{end_vertex} уже существует с весом {existing_edges[0][1]}\n")
                return False
            self.adj_list[start_vertex].append((end_vertex, weight))
            if not self.is_directed:
                existing_reverse = [neighbor for neighbor in self.adj_list[end_vertex] # для неориентированного графа добавляем обратное ребро
                                if neighbor[0] == start_vertex]
                if not existing_reverse:
                    self.adj_list[end_vertex].append((start_vertex, weight))
        else:
            if end_vertex in self.adj_list[start_vertex]:
                print(f"Ребро {start_vertex}-{end_vertex} уже существует\n")
                return False
            self.adj_list[start_vertex].append(end_vertex)
            if not self.is_directed:
                if start_vertex not in self.adj_list[end_vertex]: # для неориентированного графа добавляем обратное ребро
                    self.adj_list[end_vertex].append(start_vertex)
        
        print(f"Ребро {start_vertex}-{end_vertex} успешно добавлено!")
        if self.is_weighted:
            print(f"Вес: {weight}")
        print()
        return True

    def del_edge(self, unnecessary_edge): # удалить ребро (дугу)
        if (not self.is_weighted and len(unnecessary_edge) != 2) or (self.is_weighted and len(unnecessary_edge) != 3):
            print("Ребро задано некорректно\n")
            return False
        
        if self.is_weighted:
            start_vertex, end_vertex, weight = unnecessary_edge
        else:
            start_vertex, end_vertex = unnecessary_edge
        
        if not isinstance(start_vertex, str) or not isinstance(end_vertex, str):
            print("Некорректный формат вершин\n")
            return False
        
        if start_vertex not in self.adj_list:
            print(f"Вершина {start_vertex} не найдена в графе\n")
            return False
        if end_vertex not in self.adj_list:
            print(f"Вершина {end_vertex} не найдена в графе\n")
            return False
        
        # Проверка существования ребра
        if self.is_weighted:
            edge_exists = any(neighbor[0] == end_vertex for neighbor in self.adj_list[start_vertex])
            if not edge_exists:
                print(f"Ребро {start_vertex}-{end_vertex} не найдено в графе\n")
                return False
        else:
            if end_vertex not in self.adj_list[start_vertex]:
                print(f"Ребро {start_vertex}-{end_vertex} не найдено в графе\n")
                return False
        
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

    def del_vertex(self, unnecessary_vertex):  # удалить вершину
        if not isinstance(unnecessary_vertex, str):
            print("Некорректный формат данных\n")
            return False
        
        if unnecessary_vertex not in self.adj_list:
            print(f"Вершины {unnecessary_vertex} нет в графе\n")
            return False
        
        for vertex in self.adj_list: # убрать упоминания удаляемой вершины из рёбер
            if self.is_weighted:
                self.adj_list[vertex] = [neighbor for neighbor in self.adj_list[vertex] 
                                       if neighbor[0] != unnecessary_vertex] # пересобрать заново списки соседей
            else:
                self.adj_list[vertex] = [neighbor for neighbor in self.adj_list[vertex] 
                                       if neighbor != unnecessary_vertex]
        
        del self.adj_list[unnecessary_vertex]
        print(f"Вершина {unnecessary_vertex} успешно удалена!\n")
        return True

    def print_adj_list(self): # вывести список смежности в консоль
        if not self.adj_list:
            print("Cписок смежности пуст\n")
        else:
            print(f"Список смежности графа {self.name}:")
            for vertex, neighbors in self.adj_list.items():
                print(f"{vertex}: ", end="")
                if not neighbors:
                    print("O/")
                    continue
                neighbor_strs = []
                for neighbor in neighbors:
                    if self.is_weighted:
                        end_vertex, weight = neighbor
                        neighbor_strs.append(f"{end_vertex}({weight})")
                    else:
                        neighbor_strs.append(str(neighbor))
                
                print(", ".join(neighbor_strs))
        print("\n")

    def __str__(self): # вывод основной информации о графе (без списка смежности)
        return f"Граф {self.name}, {"ориентированный" if self.is_directed else "неориентированный"}, {"взвешенный" if self.is_weighted else "невзвешенный"}"
