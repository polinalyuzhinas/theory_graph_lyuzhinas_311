from itertools import combinations
from collections import deque
from heapq import heappush, heappop
from copy import deepcopy

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


    #================================================================================
    # преобразовать список смежности в список рёбер
    #================================================================================
    def transform_adj_list(self):
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


    #================================================================================
    # записать граф в файл
    #================================================================================
    def write_to_file(self, file_path): 
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


    #================================================================================
    # добавить вершину
    #================================================================================
    def add_vertex(self, new_vertex): 
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


    #================================================================================
    # добавить ребро (дугу)
    #================================================================================
    def add_edge(self, new_edge): 
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


    #================================================================================
    # удалить ребро (дугу)
    #================================================================================
    def del_edge(self, unnecessary_edge):
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


    #================================================================================
    # удалить вершину
    #================================================================================
    def del_vertex(self, unnecessary_vertex):  
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


    #================================================================================
    # существует ли ребро между данным вершинами
    #================================================================================
    def exist_edge(self, begin_vertex, end_vertex):
        if begin_vertex not in self.adj_list:
            return False
        
        # end_vertex: если это кортеж (для взвешенного графа), извлекаем имя вершины
        if isinstance(end_vertex, tuple):
            end_vertex_name = end_vertex[0]  # извлекаем вершину из (vertex, weight)
        else:
            end_vertex_name = end_vertex
        
        if end_vertex_name not in self.adj_list:
            return False
        
        if self.is_weighted:
            for neighbor in self.adj_list[begin_vertex]:
                if neighbor[0] == end_vertex_name:  # сравниваем имена вершин
                    return True
            return False
        else:
            return end_vertex_name in self.adj_list[begin_vertex] # для невзвешенного графа - прямая проверка

    #================================================================================
    # вывести список смежности в консоль
    #================================================================================
    def print_adj_list(self):
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


    #================================================================================
    # полустепень исхода вершины vertex
    #================================================================================
    def outdegree(self, vertex):
        if vertex not in self.adj_list: # если вершины нет в графе (проверка на всякий случай, чтобы программа не падала)
            return 0
        if self.is_weighted: # если граф взвешенный, каждое ребро представлено кортежем (сосед, вес)
            return len(self.adj_list[vertex]) # считаем количество соседей, куда можно попасть из данной вершины
        else:
            return len(self.adj_list[vertex])


    #================================================================================
    # вернуть множество всех вершин графа
    #================================================================================
    def V(self):
        v = set()
        for k in self.adj_list.keys():
            v.add(k)
        return v
    

    #================================================================================
    # построить дополнение для данного графа
    #================================================================================
    def construct_complement(self):
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


    #================================================================================
    # обход в глубину
    #================================================================================
    def dfs(self, start, visited=None):
        if visited is None:
            visited = set()
        visited.add(start) # посещение вершины
        for neighbor in self.adj_list.get(start, []):
            neighbor_vertex = neighbor if not self.is_weighted else neighbor[0]
            if neighbor_vertex not in visited:
                self.dfs(neighbor_vertex, visited)
        return visited


    #================================================================================
    # обход в глубину (вариант со стеком, нужен для алгоритма Косарайю)
    #================================================================================
    def dfs_ordered(self, start, stack=None, visited=None):
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
    

    #================================================================================
    # транспонировать граф
    #================================================================================
    def transpose(self):
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


    #================================================================================
    # обход в ширину с нахождением кратчайшего пути по количеству дуг
    #================================================================================
    def bfs_shortest_path(self, begin, end):
        if begin == end:
            return [begin]
        
        queue = deque([begin]) # deque - double-ended queue, нужна для bfs
        visited = {begin} # считаем, что начальную вершину уже посетили
        parent = {begin: None}  # словарь для восстановления пути
        
        while queue:
            current = queue.popleft() # извлечение головы (крайнего левого элемента)
            if current == end:
                break
            neighbors = self.adj_list.get(current, [])
            for neighbor in neighbors:
                neighbor_vertex = neighbor if not self.is_weighted else neighbor[0]
                
                if neighbor_vertex not in visited:
                    visited.add(neighbor_vertex)
                    parent[neighbor_vertex] = current
                    queue.append(neighbor_vertex) # добавляем в хвост (на крайнее справа место)
        
        if end not in parent: # проверка, а была ли в процессе обхода достигнута конечная вершина
            return []  # если нет, то пути не существует, возвращаем пустоту
        
        path = [] # восстанавливаем путь от end к begin
        current = end # начинаем с конечной вершины
        while current is not None:
            path.append(current)
            current = parent[current]
        
        path.reverse() # путь записывался в обратном порядке, нужно его развернуть
        return path


    #================================================================================
    # алгоритм Краскала (оптимизированный вариант)
    #================================================================================
    def find_root(self, parent, i): # поиск корня вершины i
        if parent[i] != i:
            parent[i] = self.find_root(parent, parent[i])  # переходим на один узел назад и так до корня
        return parent[i]
    
    def union_cc(self, parent, rank, x, y): # объединение двух компонент связности (первоначально все компоненты состоят из одной вершины)
        xroot = self.find_root(parent, x)
        yroot = self.find_root(parent, y)
        
        # rank - верхняя граница высоты дерева с корнем в x
        if rank[xroot] < rank[yroot]: # берём на рассмотрение наименьший из двух рангов
            parent[xroot] = yroot
        elif rank[xroot] > rank[yroot]:
            parent[yroot] = xroot
        else:
            parent[yroot] = xroot # если деревья одинаковых рангов, то увеличиваем его на 1
            rank[xroot] += 1
    
    def kruskal_main(self): # основной алгоритм
        result = []  # здесь храняться ребра MST
        
        # преобразуем вершины в числовые индексы для удобства
        vertices = list(self.adj_list.keys()) # тут важен порядок, метод V не используем
        vertex_to_index = {v: i for i, v in enumerate(vertices)}
        index_to_vertex = {i: v for i, v in enumerate(vertices)}

        edges = [] # собираем список с элементами формата (индекс начальной вершины, индекс конечной вершины, вес)
        for start_vertex, neighbors in self.adj_list.items():
            for neighbor in neighbors:
                end_vertex, weight = neighbor
                edges.append((vertex_to_index[start_vertex], vertex_to_index[end_vertex], weight))

        unique_edges = [] # надо убрать дубликаты (например, (u, v) и (v, u))
        for edge in edges:
            u, v, w = edge
            if (v, u, w) not in unique_edges:
                unique_edges.append(edge)

        # шаг 1: сортируем все ребра по весу в порядке возрастания
        unique_edges.sort(key=lambda x: x[2]) 
    
        parent = list(range(len(vertices)))
        rank = [0] * len(vertices) # у каждой вершины свой ранг, первоначально 0
        
        i = 0  # индекс для отсортированных ребер
        e = 0  # счетчик ребер для результата
        
        # количество ребер в MST будет V-1
        while e < len(vertices) - 1 and i < len(unique_edges):
            # шаг 2: выбираем наименьшее ребро
            u, v, w = unique_edges[i]
            i += 1
            
            x = self.find_root(parent, u)
            y = self.find_root(parent, v)
            
            if x != y: # предотвращаем появления циклов (то есть рёбра добавляем только между разными КС)
                e += 1
                result.append([u, v, w])
                self.union_cc(parent, rank, x, y)
        
        # преобразование рёбер в привычный формат
        mst_edges = [] # сюда кладутся преобразованные элементы result
        for u, v, w in result:
            mst_edges.append((index_to_vertex[u], index_to_vertex[v], w))
        
        mst_graph = Graph(f"MST_{self.name}", True, True) # теперь у нас есть MST данного графа, можно потом с ним работать
        for vertex in vertices:
            mst_graph.add_vertex(vertex)
        
        for u, v, w in mst_edges:
            mst_graph.add_edge((u, v, w))

        mst_graph.is_directed = False # нужно было поменять тип, чтобы обратные рёбра не включались
        return mst_graph


    #================================================================================
    # алгоритм Дейкстры
    #================================================================================
    def dijkstra(self, start, end): # основной алгоритм
        vertices = list(self.adj_list.keys())
        vertex_to_index = {v: i for i, v in enumerate(vertices)} # поиск индекса вершины с списке смежности

        if start not in vertex_to_index or end not in vertex_to_index:
            return [], float('inf')
        
        dist = [float('inf')] * len(vertices) # по умолчанию расстояние от данной вершины до всех остальных бесконечность
        prev = [-1] * len(vertices) # список предшественников (для восстановления пути)
        dist[vertex_to_index[start]] = 0 # расстояние от начальной вершины до неё же самой 0
        
        pq = [(0, start)] # очередь с парами формата (расстояние, вершина)
        
        while pq:
            current_dist, u = heappop(pq) # извлекаем элемент с хвоста
            if u == end: # если достигли конечной вершины, можно выйти
                break
            u_idx = vertex_to_index[u]  # получаем индекс один раз
            if current_dist > dist[u_idx]: # если расстояние в очереди больше текущего известного, пропускаем
                continue
            for neighbor, weight in self.adj_list[u]: # проверка соседей
                neighbor_idx = vertex_to_index[neighbor]  # получаем индекс соседа
                new_dist = dist[u_idx] + weight
                if new_dist < dist[neighbor_idx]: # если нашли пути короче, записываем пару в голову
                    dist[neighbor_idx] = new_dist
                    prev[neighbor_idx] = u
                    heappush(pq, (new_dist, neighbor))
        
        # восстановление пути
        end_idx = vertex_to_index[end]
        if prev[end_idx] == -1 and start != end:
            return []  # путь не существует
        path = []
        current = end
        while current != -1:
            path.append(current)
            current_idx = vertex_to_index[current]
            current = prev[current_idx]
        path.reverse()
        
        return path, dist[end_idx]


    #================================================================================
    # алгоритм Йена (использует алгоритм Дейкстры выше)
    #================================================================================
    def yen(self, start, end, k): # основной алгоритм
        
        first_path, first_length = self.dijkstra(start, end) # первый путь
        if not first_path:
            return []
        
        paths = [(first_length, first_path)] # все пути, формат (длина, список вершин пути)
        candidates = [] # потенциальные k-кратчайшие пути
        
        for _ in range(1, k): # поиск остальных k-1 путей
            if not paths:
                break
                
            prev_path = paths[-1][1] # берём последний найденный путь для генерации новых кандидатов

            for i in range(len(prev_path) - 1):
                spur = prev_path[i] # вершина отклонения
                root = prev_path[:i + 1] # префикс пути до spur
                
                temp_graph = deepcopy(self) # cохранение оригинального графа ...
                for _, path in paths: # ... поскольку его надо немного модифицировать
                    if len(path) > i and path[:i + 1] == root:
                        u, v = path[i], path[i + 1] # удаляем ребро, которое используется в уже найденных путях с таким же root-префиксом (чтобы избежать повторения путей)
                        weight = None
                        for neighbor, w in temp_graph.adj_list.get(u, []):
                            if neighbor == v:
                                weight = w
                                break
                        if weight is not None:
                            temp_graph.del_edge((u, v, weight)) 
        
                removed_nodes = [node for node in root if node != spur] # вершины для удаления (кроме spur)
                for node in removed_nodes: # удаляем все вершины из root-префикса кроме spur (это предотвращает возврат к уже пройденным вершинам)
                    if node in temp_graph.adj_list:
                        neighbors_to_remove = [] # удалить все рёбра, связанные с этой вершиной
                        for neighbor, weight in temp_graph.adj_list.get(node, []):
                            neighbors_to_remove.append((node, neighbor, weight))
                        for edge in neighbors_to_remove:
                            temp_graph.del_edge(edge)
                        del temp_graph.adj_list[node]
                    # очистка ссылок на удалённые вершины из всех списков смежности
                    for u in list(temp_graph.adj_list.keys()):
                        temp_graph.adj_list[u] = [
                            (neighbor, weight) for neighbor, weight in temp_graph.adj_list[u]
                            if neighbor not in removed_nodes # удаляем ссылки на удалённые вершины
                        ]
                
                dijkstra_result = temp_graph.dijkstra(spur, end) # поиск spur path (кратчайший путь от вершины отклонения до конечной вершины в модифицированном графе (без использованных рёбер и вершин))
                if not dijkstra_result or not dijkstra_result[0]: # если путь не найден
                    continue
                spur_path, _ = dijkstra_result # найденный spur path

                if spur_path: # если spur path найден, формируем полный путь-кандидат
                    total_path = root[:-1] + spur_path # объединяем root-префикс (без spur) и spur path
                    total_length = 0 # проверяем длину по исходному графу
                    valid = True
                    for j in range(len(total_path) - 1):
                        u, v = total_path[j], total_path[j + 1]
                        found = False
                        for n, w in self.adj_list.get(u, []): # поиск веса ребра в оригинальном графе
                            if n == v:
                                total_length += w
                                found = True
                                break
                        if not found:
                            valid = False # ребро не существует в оригинальном графе
                            break
                    
                    # добавляем кандидата если:
                    # 1. Путь корректен (все рёбра существуют)
                    # 2. Путь уникален (не содержится в paths или candidates)
                    if valid and not any(p == total_path for _, p in paths) and not any(p == total_path for _, p in candidates):
                        heappush(candidates, (total_length, total_path))
            
            # если кандидатов нет, завершаем поиск (больше путей не существует)
            if not candidates:
                break
            
            # извлекаем кандидата с наименьшей длиной и добавляем в результат
            length, path = heappop(candidates)
            paths.append((length, path))
        
        return paths[:k]
    

    #================================================================================
    # алгоритм Беллмана-Форда для поиска отрицательных циклов
    #================================================================================

    def bellman_ford_all_negative_cycles(self, start=None): # основной алгоритм
        if start is None:
            # поиск всех циклов в графе
            return self.find_all_cycles_in_graph()
        else:
            # поиск циклов из конкретной вершины
            return self.find_cycles_from_vertex(start)

    def find_all_cycles_in_graph(self): # поиск отрицательных циклов в графе
        all_cycles = set()
        vertices = list(self.adj_list.keys())
        
        # запуск из каждой вершины, собираем все уникальные циклы
        for start_vertex in vertices:
            _, _, _, cycles = self.find_cycles_from_vertex(start_vertex)
            for cycle in cycles:
                if self.is_negative_cycle(cycle):
                    cycle_tuple = tuple(cycle)
                    all_cycles.add(cycle_tuple)
        
        cycles_list = [list(cycle) for cycle in all_cycles]
        return len(cycles_list) > 0, {}, {}, cycles_list

    def find_cycles_from_vertex(self, start): # обнаружение всех отрицательных циклов из конкретной вершины
        vertices = list(self.adj_list.keys())
        
        # создание фиктивной вершины (позволяет найти только достижимые из конкретной вершины циклы)
        temp_vertex = "NIL"
        temp_adj_list = self.adj_list.copy()  # копируем исходный список смежности
        
        # фиктивная вершина соединена со всеми другими вершинами нулевыми рёбрами
        temp_adj_list[temp_vertex] = []
        for vertex in vertices:
            temp_adj_list[temp_vertex].append((vertex, 0))
            
        # преобразование вершин в индексе с графе с фиктивной вершиной
        extended_vertices = vertices + [temp_vertex]
        extended_vertex_to_index = {v: i for i, v in enumerate(extended_vertices)}
        extended_index_to_vertex = {i: v for i, v in enumerate(extended_vertices)}
        
        extended_n = len(extended_vertices)
        temp_idx = extended_vertex_to_index[temp_vertex]  # индекс фиктивной вершины
        
        # инициализация массивов для расширенного графа
        dist = [float('inf')] * extended_n
        parent = [-1] * extended_n
        dist[temp_idx] = 0

        # все рёбра расширенного графа
        edges = []
        for u, neighbors in temp_adj_list.items():
            u_idx = extended_vertex_to_index[u]
            for v, w in neighbors:
                v_idx = extended_vertex_to_index[v]
                edges.append((u_idx, v_idx, w))

        # фаза релаксации для расширенного графа
        for _ in range(extended_n - 1):
            updated = False
            for u_idx, v_idx, w in edges:
                if dist[u_idx] != float('inf') and dist[u_idx] + w < dist[v_idx]:
                    dist[v_idx] = dist[u_idx] + w
                    parent[v_idx] = u_idx
                    updated = True
            if not updated:
                break

        # поиск всех отрицательных циклов в расширенном графе
        negative_cycles = []  # список найденных циклов
        visited_cycles = set()  # множество для отслеживания уникальности
        
        for u_idx, v_idx, w in edges:  # проверяем все рёбра на наличие циклов
            if dist[u_idx] != float('inf') and dist[u_idx] + w < dist[v_idx]:
                # находим вершину, принадлежащую циклу
                x = v_idx  # начинаем с вершины v
                for _ in range(extended_n):
                    x = parent[x]
                    
                # восстанавливаем цикл, исключая фиктивную вершину
                cycle = self.reconstruct_cycle(parent, x, extended_index_to_vertex, temp_vertex)
                if cycle:
                    normalized_cycle = self.normalize_cycle(cycle)
                    cycle_tuple = tuple(normalized_cycle) 
                    
                    # добавляем цикл, если он уникален
                    if cycle_tuple not in visited_cycles:
                        negative_cycles.append(normalized_cycle)
                        visited_cycles.add(cycle_tuple)

        has_negative_cycles = len(negative_cycles) > 0
        dist_dict = {extended_index_to_vertex[i]: dist[i] for i in range(extended_n)}
        parent_dict = {extended_index_to_vertex[i]: extended_index_to_vertex[parent[i]] if parent[i] != -1 else None for i in range(extended_n)}
        return has_negative_cycles, dist_dict, parent_dict, negative_cycles
    
    def is_negative_cycle(self, cycle): # является ли цикл отрицательным
        if len(cycle) < 3:
            return False
        
        total_weight = 0
        for i in range(len(cycle) - 1):
            u, v = cycle[i], cycle[i + 1]
            weight_found = False
            for neighbor, w in self.adj_list.get(u, []):
                if neighbor == v:
                    total_weight += w
                    weight_found = True
                    break
            if not weight_found:
                return False
        
        return total_weight < 0

    def reconstruct_cycle(self, parent, start_idx, index_to_vertex, exclude_vertex=None): # восстанавливает цикл из родительских ссылок
        cycle = []  # список для хранения вершин цикла
        y = start_idx  # начинаем с заданной вершины
        visited = set()  # множество для отслеживания посещенных вершин
        
        while True:
            if y in visited:  # если вершина уже посещена - найден цикл
                break  # выходим из цикла
            visited.add(y)  # отмечаем вершину как посещенную
            
            vertex_name = index_to_vertex[y]  # получаем имя вершины
            if exclude_vertex is None or vertex_name != exclude_vertex:
                cycle.append(vertex_name)  # добавляем вершину в цикл, если она не исключена
                
            y = parent[y]  # переходим к предшественнику
            if y == -1:  # если предшественника нет
                return None  # цикл не найден
                
        # находим начало цикла в списке
        start_vertex_name = index_to_vertex[y]  # имя начальной вершины цикла
        
        # проверяем, не исключена ли начальная вершина
        if exclude_vertex is not None and start_vertex_name == exclude_vertex:
            return None  # цикл начинается с исключенной вершины
            
        # ищем позицию начальной вершины в найденном цикле
        cycle_start_idx = None
        for i, vertex in enumerate(cycle):  # перебираем вершины цикла
            if vertex == start_vertex_name:  # нашли начальную вершину
                cycle_start_idx = i  # запоминаем позицию
                break
            
        if cycle_start_idx is None:  # если начальная вершина не найдена в цикле
            return None  # цикла не образуется
        
        full_cycle = cycle[cycle_start_idx:] + [start_vertex_name]  # формируем полный цикл
        
        return full_cycle  # возвращаем цикл

    def normalize_cycle(self, cycle): # устранение дубликатов
        if len(cycle) <= 2:  # если цикл слишком короткий
            return cycle  # возвращаем как есть
        
        # убираем дублирующую конечную вершину если есть
        if cycle[0] == cycle[-1]:
            working_cycle = cycle[:-1]  # работаем без дублированной вершины
        else:
            working_cycle = cycle  # оставляем как есть
            
        min_rotation = working_cycle  # изначально минимальное представление - исходный цикл
        n = len(working_cycle)  # длина цикла без дублированной вершины
        
        for i in range(1, n):  # перебираем все возможные циклические сдвиги
            rotated = working_cycle[i:] + working_cycle[:i]  # циклический сдвиг
            if rotated < min_rotation:  # если нашли лексикографически меньшее представление
                min_rotation = rotated  # обновляем минимальное представление
            
        reversed_cycle = working_cycle[::-1]  # разворачиваем цикл
        for i in range(n):  # перебираем циклические сдвиги обратного направления
            rotated = reversed_cycle[i:] + reversed_cycle[:i]  # сдвиг обратного цикла
            if rotated < min_rotation:  # если нашли меньшее представление
                min_rotation = rotated  # обновляем
        
        # возвращаем цикл с дублированной начальной вершиной в конце
        return min_rotation + [min_rotation[0]]

    #================================================================================
    # алгоритм Диница для нахождения максимального потока
    #================================================================================
    def dinic(self, source, sink):
        residual_graph = {} # остаточная сеть (в виде словаря)
        for u in self.adj_list: 
            if u not in residual_graph: # инициализируем словарь смежности для вершины u в остаточной сети
                residual_graph[u] = {} 
            for v, capacity in self.adj_list[u]:
                residual_graph[u][v] = capacity # устанавливаем прямую пропускную способность равной исходной
                if v not in residual_graph:
                    residual_graph[v] = {} # добавление вершины v с словарь сети с пустыми словарём смежности
                # всегда инициализируем обратное ребро с пропускной способностью 0
                residual_graph[v][u] = 0
        
        max_flow = 0 # значение максимального потока
        
        def bfs_dinic(): # обход в ширину для построения слоистой сети
            level = {node: -1 for node in residual_graph} # уровень -1 - непосещённая вершина
            level[source] = 0 # уровень истока = 0
            
            queue = deque([source])
            while queue:
                u = queue.popleft()
                for v, capacity in residual_graph[u].items():
                    if level[v] == -1 and capacity > 0: # если вершина v не посещена и остаточная пропускная способность больше 0
                        level[v] = level[u] + 1 # устанавливаем уровень вершины v на 1 больше уровня u
                        queue.append(v) # добавляем вершину v в очередь
            
            return level # возвращаем словарь уровней
        
        def dfs_dinic(u, flow, level): # обход в глубину для нахождения блокирующего потока"""
            if u == sink: # если сток найден, то возвращаем поток
                return flow
            
            for v, capacity in residual_graph[u].items():
                # условия для добавления в блокирующий поток:
                # 1. уровень вершины v должен быть на 1 больше уровня u
                # 2. остаточная пропускная способность должна быть положительной
                if level[v] == level[u] + 1 and capacity > 0:
                    current_flow = min(flow, capacity) # возможный поток - минимум из текущего потока и остаточной способности
                    pushed_flow = dfs_dinic(v, current_flow, level) # поиск потока от вершины v до стока
                    
                    if pushed_flow > 0: # ненулевой поток найден
                        residual_graph[u][v] -= pushed_flow # уменьшаем пропускную способность прямого ребра на найденный поток
                        if v not in residual_graph: # гарантируем что обратное ребро существует
                            residual_graph[v] = {}
                        # обновляем обратное ребро
                        residual_graph[v][u] = residual_graph[v].get(u, 0) + pushed_flow
                        return pushed_flow
            
            return 0
        
        # основной цикл алгоритма Диница
        while True:
            level = bfs_dinic() # строим слоистую сеть
            if level[sink] == -1: # если сток недостижим, выходим из цикла
                break
                
            while True: # внутренний цикл для нахождения блокирующих потоков
                flow = dfs_dinic(source, float('inf'), level) # ищем блокирующий поток
                if flow == 0: # поток равен 0, выходим из внутреннего цикла
                    break
                max_flow += flow # увеличиваем общий максимальный поток на найденный блокирующий поток
        
        # восстановление потока на каждом ребре
        flow_on_edges = {} # словарь для хранения потока по рёбрам
        for u in self.adj_list: 
            flow_on_edges[u] = {} # словарь потока для вершины u
            for v, capacity in self.adj_list[u]:
                # поток по ребру = исходная пропускная способность - остаточная пропускная способность
                # используем get() для безопасного доступа к residual_graph
                flow_on_edges[u][v] = capacity - residual_graph[u].get(v, 0)
        
        return max_flow, flow_on_edges # возврат максимального потока + разложения его по рёбрам
    
    #================================================================================
    # вывод основной информации о графе (без списка смежности)
    #================================================================================
    def __str__(self):
        return f"<Класс Graph> Граф {self.name}, {'ориентированный' if self.is_directed else 'неориентированный'}, {'взвешенный'if self.is_weighted else 'невзвешенный'}"
