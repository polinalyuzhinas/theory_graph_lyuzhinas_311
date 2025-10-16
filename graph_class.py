from itertools import combinations

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
                line_lower = line.lower().split()
                if "ориентированный" in line_lower:
                    current_graph.is_directed = True
                elif "неориентированный" in line_lower:
                    current_graph.is_directed = False
                else:
                    current_graph.is_directed = False # значение по умолчанию
                if "взвешенный" in line_lower:
                    current_graph.is_weighted = True
                elif "невзвешенный" in line_lower:
                    current_graph.is_weighted = False
                else:
                    current_graph.is_weighted = False # значение по умолчанию

            elif ":" in line:
                if current_graph is None:
                    continue
                
                parts = line.split(":")
                vertex = parts[0].strip()
                current_graph.add_vertex(vertex)
                edges = parts[1].strip()
                
                if edges:
                    for edge in [e.strip() for e in edges.split(", ")]:
                        if current_graph.is_weighted:
                            if "(" in edge and ")" in edge: # обработка взвешенных рёбер (формат: вершина(вес))
                                end_vertex = edge[:edge.find("(")]
                                current_graph.add_vertex(end_vertex) # надо, надо добавить конечную вершину в граф
                                weight_str = edge[(edge.find("(") + 1):edge.find(")")]
                                try:
                                    weight = float(weight_str)
                                    current_graph.add_edge((vertex, end_vertex, weight))
                                except ValueError:
                                    print(f"<Класс Graph> Ошибка: некорректный вес {weight_str}\n")
                            else:
                                print(f"<Класс Graph> Ошибка: некорректный формат взвешенного графа\n")
                        else:
                            current_graph.add_vertex(edge) # надо, надо добавить конечную вершину в граф
                            current_graph.add_edge((vertex, edge)) # для невзвешенных графов - просто добавляем ребро
        if current_graph is not None:
            graphs.append(current_graph) 
        return graphs

    # методы
    def transform_adj_list(self): # преобразовать список смежности в список рёбер
        if not self.adj_list:
            print("<Класс Graph> Список смежности графа пуст, соответственно преобразовывать нечего\n")
            return False
        print(f"<Класс Graph> Превращение списка смежности графа {self.name} в список рёбер\n")
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
                        if self.is_weighted:
                            edge_list.append(" ".join(edge[:2]) + f" ({edge[-1]})")
                        else:
                            edge_list.append(" ".join(edge[:2]))
                else:
                    edge_comparator = (lambda e1, e2: e1[:2] == e2[:2]) if not self.is_weighted else (lambda e1, e2: e1 == e2)
                    edge_exists = any(edge_comparator(e, edge) for e in edge_list) # проверяем, что ребра нет в графе
                    if self.is_weighted:
                        edge_list.append(" ".join(edge[:2]) + f" ({edge[-1]})")
                    else:
                        edge_list.append(" ".join(edge[:2]))
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
            print("<Класс Graph> Некорректный формат данных\n")
            return False
        elif new_vertex in self.adj_list:
            print(f"<Класс Graph> Вершина {new_vertex} уже есть в графе\n")
            return False
        else:
            self.adj_list[new_vertex] = [] # по умолчанию у вершины нет соседей
            print(f"<Класс Graph> Вершина {new_vertex} успешно добавлена!\n")
            return True

    def add_edge(self, new_edge): # добавить ребро (дугу)
        if not self.is_weighted:
            if len(new_edge) == 2: # у ребра должен быть формат (start, end)
                start_vertex, end_vertex = new_edge
                weight = 0.0  # вес по умолчанию для невзвешенных графов
            else:
                print("<Класс Graph> Ребро задано некорректно: для невзвешенного графа ожидается 2 параметра\n")
                return False
        elif self.is_weighted:
            if len(new_edge) == 3: # если с весом, то (start, end, weight)
                start_vertex, end_vertex, weight = new_edge
            else:
                print("<Класс Graph> Ребро задано некорректно: для взвешенного графа ожидается 3 параметра\n")
                return False
        
        if not isinstance(start_vertex, str) or not isinstance(end_vertex, str):
            print("<Класс Graph> Некорректный формат вершин")
            return False
            
        if self.is_weighted and not isinstance(weight, (int, float)):
            print("<Класс Graph> Некорректный формат веса. Ожидается число.\n")
            return False
        
        if start_vertex not in self.adj_list:
            print(f"<Класс Graph> Вершина {start_vertex} не существует в графе. Добавьте её сначала.\n")
            return False
        if end_vertex not in self.adj_list:
            print(f"<Класс Graph> Вершина {end_vertex} не существует в графе. Добавьте её сначала.\n")
            return False
        
        if self.is_weighted:
            existing_edges = [neighbor for neighbor in self.adj_list[start_vertex] 
                        if neighbor[0] == end_vertex]
            if existing_edges:
                print(f"<Класс Graph> Ребро {start_vertex}-{end_vertex} уже существует с весом {existing_edges[0][1]}\n")
                return False
            self.adj_list[start_vertex].append((end_vertex, weight))
            if not self.is_directed:
                existing_reverse = [neighbor for neighbor in self.adj_list[end_vertex] # для неориентированного графа добавляем обратное ребро
                                if neighbor[0] == start_vertex]
                if not existing_reverse:
                    self.adj_list[end_vertex].append((start_vertex, weight))
        else:
            if end_vertex in self.adj_list[start_vertex]:
                print(f"<Класс Graph> Ребро {start_vertex}-{end_vertex} уже существует\n")
                return False
            self.adj_list[start_vertex].append(end_vertex)
            if not self.is_directed:
                if start_vertex not in self.adj_list[end_vertex]: # для неориентированного графа добавляем обратное ребро
                    self.adj_list[end_vertex].append(start_vertex)
        
        print(f"<Класс Graph> Ребро {start_vertex}-{end_vertex} успешно добавлено!")
        if self.is_weighted:
            print(f"<Класс Graph> Вес: {weight}")
        print()
        return True

    def del_edge(self, unnecessary_edge): # удалить ребро (дугу)
        if (not self.is_weighted and len(unnecessary_edge) != 2) or (self.is_weighted and len(unnecessary_edge) != 3):
            print("<Класс Graph> Ребро задано некорректно\n")
            return False
        
        if self.is_weighted:
            start_vertex, end_vertex, weight = unnecessary_edge
        else:
            start_vertex, end_vertex = unnecessary_edge
        
        if not isinstance(start_vertex, str) or not isinstance(end_vertex, str):
            print("<Класс Graph> Некорректный формат вершин\n")
            return False
        
        if start_vertex not in self.adj_list:
            print(f"<Класс Graph> Вершина {start_vertex} не найдена в графе\n")
            return False
        if end_vertex not in self.adj_list:
            print(f"<Класс Graph> Вершина {end_vertex} не найдена в графе\n")
            return False
        
        if self.is_weighted:
            edge_exists = any(neighbor[0] == end_vertex for neighbor in self.adj_list[start_vertex])
            if not edge_exists:
                print(f"<Класс Graph> Ребро {start_vertex}-{end_vertex} не найдено в графе\n")
                return False
        else:
            if end_vertex not in self.adj_list[start_vertex]:
                print(f"<Класс Graph> Ребро {start_vertex}-{end_vertex} не найдено в графе\n")
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
        
        print(f"<Класс Graph> Ребро {start_vertex}-{end_vertex} успешно удалено!\n")
        return True

    def del_vertex(self, unnecessary_vertex):  # удалить вершину
        if not isinstance(unnecessary_vertex, str):
            print("<Класс Graph> Некорректный формат данных\n")
            return False
        
        if unnecessary_vertex not in self.adj_list:
            print(f"<Класс Graph> Вершины {unnecessary_vertex} нет в графе\n")
            return False
        
        for vertex in self.adj_list: # убрать упоминания удаляемой вершины из рёбер
            if self.is_weighted:
                self.adj_list[vertex] = [neighbor for neighbor in self.adj_list[vertex] 
                                       if neighbor[0] != unnecessary_vertex] # пересобрать заново списки соседей
            else:
                self.adj_list[vertex] = [neighbor for neighbor in self.adj_list[vertex] 
                                       if neighbor != unnecessary_vertex]
        
        del self.adj_list[unnecessary_vertex]
        print(f"<Класс Graph> Вершина {unnecessary_vertex} успешно удалена!\n")
        return True

    def exist_edge(self, begin_vertex, end_vertex): # существует ли ребро между данным вершинами
        if begin_vertex not in self.adj_list or end_vertex not in self.adj_list:
            print("<Класс Graph> Одной из данных вершин нет в графе, добавьте их сначала\n")
            return False
    
        if self.is_weighted:
            for neighbor in self.adj_list[begin_vertex]: # для взвешенного графа: проверяем наличие кортежа (end_vertex, weight)
                if neighbor[0] == end_vertex:  # сравниваем только имя вершины, игнорируя вес
                    return True
            return False
        else:
            return end_vertex in self.adj_list[begin_vertex] # для невзвешенного графа: прямая проверка
        
    def print_adj_list(self): # вывести список смежности в консоль
        if not self.adj_list:
            print("<Класс Graph> Cписок смежности пуст\n")
        else:
            print(f"<Класс Graph> Список смежности графа {self.name}:")
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

    def outdegree(self, vertex): # полустепень исхода вершины vertex
        if vertex not in self.adj_list: # если вершины нет в графе (проверка на всякий случай, чтобы программа не падала)
            return 0
        if self.is_weighted: # если граф взвешенный, каждое ребро представлено кортежем (сосед, вес)
            return len(self.adj_list[vertex]) # считаем количество соседей, куда можно попасть из данной вершины
        else:
            return len(self.adj_list[vertex])

    def V(self): # вернуть множество всех вершин графа
        v = set()
        for k in self.adj_list.keys():
            v.add(k)
        return v

    def construct_complement(self): # построить дополнение для данного графа
        edge_list = self.transform_adj_list()
        if not edge_list:
            print("<Класс Graph> У данного графа нет рёбер, поэтому построение дополнения невозможно!\n")
            return False
        else:
            complement = Graph(f"{self.name}\'", self.is_directed, self.is_weighted)
            for vertex in self.adj_list:
                complement.add_vertex(vertex)
            all_variations = combinations("".join(complement.V()), 2) # список всех возможных рёбер из вершин данного графа
            for e in all_variations:
                if e not in edge_list:
                    complement.add_edge((e[0], e[1]))
        return complement

    def dfs(self, start, visited=None): # обход в глубину
        if visited is None:
            visited = set()
        visited.add(start) # посещение вершины
        for neighbor in self.adj_list.get(start, []):
            neighbor_vertex = neighbor if not self.is_weighted else neighbor[0]
            if neighbor_vertex not in visited:
                self.dfs(neighbor_vertex, visited)
        return visited

    def dfs_ordered(self, start, stack=None, visited=None): # обход в глубину (вариант со стеком, нужен для алгоритма Косарайю)
        if stack is None:
            stack = []
        if visited is None:
            visited = set()
        visited.add(start) # посещение вершины
        for neighbor in self.adj_list.get(start, []):
            neighbor_vertex = neighbor if not self.is_weighted else neighbor[0]
            if neighbor_vertex not in visited:
                self.dfs_ordered(neighbor_vertex, stack, visited)
        stack.append(start)  # добавление вершины в стек когда все её соседи обработаны
        return stack, visited
    
    def transpose(self): # транспонировать граф (только для орграфа)
        edge_list = self.transform_adj_list()
        if not edge_list:
            print("<Класс Graph> У данного графа нет рёбер, поэтому построение транспонированного графа невозможно!\n")
            return False
        else:
            transposed = Graph(f"{self.name}T", self.is_directed, self.is_weighted)
            for vertex in self.adj_list:
                transposed.add_vertex(vertex)
            for e in edge_list:
                e_list = e.split(" ")
                if self.is_weighted:
                    transposed.add_edge((e_list[1], e_list[0], float((e_list[2]).strip("()"))))
                else: 
                    transposed.add_edge((e_list[1], e_list[0]))
        return transposed

    def __str__(self): # вывод основной информации о графе (без списка смежности)
        return f"<Класс Graph> Граф {self.name}, {'ориентированный' if self.is_directed else 'неориентированный'}, {'взвешенный'if self.is_weighted else 'невзвешенный'}"
