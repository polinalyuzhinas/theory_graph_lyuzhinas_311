from graph_class import Graph

all_graphs = []

def menu_for_choice_graph(allgr, directed=None, weighted=None): # функция выбора названия графа
        print("Выберите имя графа (можно выйти из программы доcрочно, напечатав 0, если все графы пустые): \n")
        print(", ".join([g.name for g in allgr]))
        print(input_string, end="")
        selected = input()
        print()
        if selected == "0":
            print("Хорошо, выходим из программы...")
            exit()
        for graph in allgr:
            if graph.name == selected:
                if directed is None and weighted is None:
                    return graph # если нам не требуется какой-то конкретный тип графа, то просто возвращаем выбранный
                elif graph.is_directed == directed or graph.is_weighted == weighted: # задан критерий на какой-то один вид
                    return graph
                elif (not directed is None and not weighted is None) and (graph.is_directed == directed and graph.is_weighted == weighted): # если критерии сразу на два вида
                    return graph
                else:
                    if directed is None: 
                        str_dir = ""
                    elif directed:
                        str_dir = "ориентированные"
                    else:
                        str_dir = "неориентированные"
                    
                    if weighted is None: 
                        str_weig = ""
                    elif weighted:
                        str_weig = "взвешенные"
                    else:
                        str_weig = "невзвешенные"
                    print(f"Мы принимаем только {str_dir} {str_weig} графы. Тот, что вы выбрали, к таковым не относится\n")
                    return False  
        print("Этого графа ещё не создавали\n")
        return False

def add_graphs_options(all_gr, dict): # функция добавления опций, связанных с графами (просто чтобы сократить код)
    added = False
    if all(o not in dict.keys() for o in range(4, 13)):
        dict[4] = "4 - вывести список смежности графа"
        dict[5] = "5 - добавить в граф вершину"
        dict[6] = "6 - удалить вершину из графа"
        dict[7] = "7 - добавить в граф ребро"
        dict[8] = "8 - удалить из графа ребро"
        dict[9] = "9 - вывести список рёбер графа"
        dict[10] = "10 - записать граф в текстовый (формат .txt) файл"
        dict[11] = "11 - скопировать существующий граф"
        dict[12] = "12 - вывести те вершины, полустепень исхода которых больше, чем у заданной вершины"
        added = True
    if all(n not in dict.keys() for n in (13, 14, 15, 16)) and any(g.is_directed for g in all_gr):
        dict[13] = "13 - вывести те вершины орграфа, которые являются одновременно заходящими и выходящими для заданной вершины"
        dict[14] = "14 - построить дополнение для данного орграфа"
        dict[15] = "15 - найти компоненты сильной связности орграфа"
        dict[16] = "16 - вывести один из кратчайших (по числу дуг) путей из вершины u в вершину v"
        added = True
    if 17 not in dict.keys() and any(g.is_weighted and not g.is_directed for g in all_gr):
        dict[17] = "17 - найти минимальное остовное дерево алгоритмом Краскала"
        added = True
    if all(n not in dict.keys() for n in (18, 19)) and any(g.is_weighted for g in all_gr):
        dict[18] = "18 - найти кратчайший путь (по весу) из вершины u в вершину v"
        dict[19] = "19 - найти k кратчайших путей (по весу) из вершины u в вершину v"
        added = True
    return added

if __name__ == "__main__":
    update = "Добавлены новые опции! "
    input_string = ">>> "
    already_printed = False # если было обновление опций, то список опций выведется сразу по окончании операции, иначе нужно будет написать в консоль 100, этот флаг вспомогательный для этого функционала
    need_update = False # флаг, оповещающий о том, что надо поменять список опций
    print("Добро пожаловать в программу для работы с различными графами!")
    options = {0: "0 - выйти отсюда", 1: "1 - создать граф по умолчанию", 2: "2 - создать граф с пользовательскими атрибутами", 3: "3 - считать графы с текстового (.txt формата и только) файла"}
    print(choice:="Выберите действие: ")
    print("\n".join(options.values()))
    print(input_string, end="")
    try:
        n = int(input())
        if n not in options.keys():
            n = -1
    except ValueError:
        n = -1
    print()
    while n != 0:
        if n == 1:
            empty_graph = Graph()
            if any(empty_graph.name == graph.name for graph in all_graphs):
                print(f"Граф с именем {empty_graph.name} уже существует\n")
            else:
                print(f"Граф с именем {empty_graph.name} успешно создан!")
                all_graphs.append(empty_graph)
                print(empty_graph)
                empty_graph.print_adj_list()
                if add_graphs_options(all_graphs, options):
                    print(update + choice)
                    print("\n".join(value for _, value in sorted(options.items())))
                    already_printed = True
                    print(input_string, end="")
        elif n == 2:
            name = input("Введите имя графу ").strip()
            if name == "0": 
                print("0ём граф назвать нельзя, это служебное значение\n")
                continue
            if any(name == g.name for g in all_graphs):
                print(f"Граф с именем {name} уже существует\n")
                continue
            print()
            ans = input("Будет ли он ориентирован? (Да/Нет) ").strip()
            print()
            if ans.lower() == "да":
                is_directed = True
            elif ans.lower() == "нет":
                is_directed = False
            else:
                print("Неверный ввод\n")
                continue
            ans = input("Будет ли он взвешенным? (Да/Нет) ").strip()
            print()
            if ans.lower() == "да":
                is_weighted = True
            elif ans.lower() == "нет":
                is_weighted = False
            else:
                print("Неверный ввод\n")
                continue
            graph = Graph(name, is_directed, is_weighted)
            print(f"Граф с именем {graph.name} успешно создан!\n")
            all_graphs.append(graph)
            print(graph)
            graph.print_adj_list()
            if add_graphs_options(all_graphs, options):
                print(update + choice)
                print("\n".join(value for _, value in sorted(options.items())))
                already_printed = True
                print(input_string, end="")
        elif n == 3:
            file_path = input("Введите имя файла: ").strip()
            print()
            if not file_path.endswith(".txt"):
                print("Нужно обязательно указать расширение .txt\n")
            else:
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        pass  # проверка, что файл можно открыть
                except FileNotFoundError:
                    print(f"Файл {file_path} не найден\n")
                    continue
                except PermissionError:
                    print(f"Нет прав доступа к файлу {file_path}\n")
                except Exception as e:
                    print(f"Ошибка доступа к файлу {file_path}: {e}\n")
                    continue
                try:
                    temp_graph = Graph()
                    graphs_from_file = temp_graph.file_constructor(file_path)
                    for g in graphs_from_file:
                        if g.name == 0: 
                            print("0ём граф назвать нельзя, это служебное значение\n")
                        if any(g.name == gr.name for gr in all_graphs):
                            print(f"Граф с именем {g.name} уже существует\n")
                        else:
                            print(f"Граф с именем {g.name} успешно создан!\n")
                            all_graphs.append(g)
                            print(g)
                            g.print_adj_list()
                            if add_graphs_options(all_graphs, options): # проверяем для каждого созданного графа и накапливаем флаг
                                need_update = True

                    print(f"Успешно загружено {len(graphs_from_file)} граф(ов)\n")
                    if need_update: # если что-то в списке опций обновилось, выводим меню выбора
                        print(update + choice)
                        print("\n".join(value for _, value in sorted(options.items())))
                        already_printed = True
                        print(input_string, end="")
                except Exception as e:
                    print(f"Ошибка чтения файла: {e}\n")
        elif n == 4:
            selected = menu_for_choice_graph(all_graphs)
            if not selected: 
                continue 
            else:
                selected.print_adj_list()
        elif n == 5:
            selected = menu_for_choice_graph(all_graphs)
            if not selected: 
                continue 
            else:
                v = input("Введите название вершины, которую хотите добавить ").strip()
                selected.add_vertex(v)
                print()
        elif n == 6:
            selected = menu_for_choice_graph(all_graphs)
            if not selected: 
                continue
            else:
                v = input("Введите название вершины, которую хотите удалить ").strip()
                selected.del_vertex(v)
                print()
        elif n == 7:
            selected = menu_for_choice_graph(all_graphs)
            if not selected: 
                continue
            else:
                if not selected.adj_list:
                    print("Пока в графе вообще нет вершин, добавьте хоть одну сначала\n")
                    continue
                else:
                    start_vertex = input("Введите начальную вершину: ").strip()
                    end_vertex = input("Введите конечную вершину: ").strip()
                    
                    if start_vertex not in selected.adj_list:
                        print(f"Вершина {start_vertex} не существует в графе. Добавьте её сначала.\n")
                        continue
                    if end_vertex not in selected.adj_list:
                        print(f"Вершина {end_vertex} не существует в графе. Добавьте её сначала.\n")
                        continue
                        
                    if selected.is_weighted:
                        try:
                            weight = float(input("Введите вес ребра: ").strip())
                        except ValueError:
                            print("Некорректный формат веса. Используйте число.\n")
                            continue
                        selected.add_edge((start_vertex, end_vertex, weight))
                    else:
                        selected.add_edge((start_vertex, end_vertex))
                    print()
        elif n == 8:
            selected = menu_for_choice_graph(all_graphs)
            if not selected: 
                continue
            else:
                if not selected.adj_list:
                    print("Пока в графе вообще нет вершин, добавьте хоть одну сначала\n")
                    continue
                else:
                    start_vertex = input("Введите начальную вершину: ").strip()
                    end_vertex = input("Введите конечную вершину: ").strip()

                    if start_vertex not in selected.adj_list:
                        print(f"Вершина {start_vertex} не существует в графе.\n")
                        continue
                    if end_vertex not in selected.adj_list:
                        print(f"Вершина {end_vertex} не существует в графе.\n")
                        continue
                        
                    if selected.is_weighted:
                        try:
                            weight = float(input("Введите вес ребра: ").strip())
                        except ValueError:
                            print("Некорректный формат веса. Используйте число.\n")
                            continue
                        selected.del_edge((start_vertex, end_vertex, weight))
                    else:
                        selected.del_edge((start_vertex, end_vertex))
                    print()
        elif n == 9:
            selected = menu_for_choice_graph(all_graphs)
            if not selected: 
                continue
            else:
                print(", ".join(selected.transform_adj_list()))
        elif n == 10:
            selected = menu_for_choice_graph(all_graphs)
            if not selected: 
                continue
            else:
                file_path = input("Введите имя файла, куда записать граф: ").strip()
                print()
                if not file_path.endswith(".txt"):
                    print("Нужно обязательно указать расширение .txt\n")
                else:
                    selected.write_to_file(file_path)
        elif n == 11:
            selected = menu_for_choice_graph(all_graphs)
            if not selected: 
                continue
            else:
                copied_graph = Graph()
                copied_graph.copy_constructor(selected)
                print("Копирование произошло успешно!\n")
        elif n == 12:
            selected = menu_for_choice_graph(all_graphs)
            if not selected: 
                continue
            else:
                vertex = input("А теперь введите какую-нибудь вершину из этого графа: ")
                if vertex not in selected.adj_list:
                    print("Такой вершины в графе нет!\n")
                    continue
                else:
                    val = selected.outdegree(vertex)
                    print(f"Итак, полустепень исхода этой вершины = {val}\n")
                    temp = []
                    for v in selected.adj_list.keys():
                        if selected.outdegree(v) > val:
                            temp.append(v)
                    if not temp:
                        print("Искомые вершины не найдены\n")
                    else:
                        print(f"А вот вершины, полустепень исхода которых больше: {', '.join(temp)}\n")
        elif n == 13:
            print("Этот пункт выполняется только для ориентированных графов!\n")
            selected = menu_for_choice_graph(all_graphs, True)
            if not selected: 
                continue
            else:
                temp = []
                begin_vertex = input("Введите какую-нибудь вершину из этого графа: ")
                if begin_vertex not in selected.adj_list:
                    print("Такой вершины в графе нет!\n")
                    continue
                else:
                    for end_vertex in selected.adj_list[begin_vertex]:
                        if selected.exist_edge(begin_vertex, end_vertex) and selected.exist_edge(end_vertex, begin_vertex):
                            temp.append(end_vertex)
                    if not temp:
                        print("Искомые вершины не найдены\n")
                    else:
                        print(f"А вот вершины, которые являются одновременно заходящими и выходящими для заданной вершины: {', '.join(temp)}\n")
        elif n == 14:
            print("Этот пункт выполняется только для ориентированных графов!\n")
            selected = menu_for_choice_graph(all_graphs, True)
            if not selected: 
                continue
            else:
                comp = selected.construct_complement()
                if comp:
                    all_graphs.append(comp)
                print(f"Дополнение графа {selected.name} успешно построено!\n")
                print(comp)
                comp.print_adj_list()
                if add_graphs_options(all_graphs, options):
                    print(update + choice)
                    print("\n".join(value for _, value in sorted(options.items())))
                    already_printed = True
                    print(input_string, end="")
        elif n == 15: # тут использован алгоритм Косарайю/Косараджу или ещё как-то
            print("Этот пункт выполняется только для ориентированных графов!\n")
            selected = menu_for_choice_graph(all_graphs, True)
            if not selected: 
                continue
            else:
                if all(len(neighbors) == 0 for neighbors in selected.adj_list.values()):
                    print("Граф не имеет рёбер, искать тут нечего\n")
                    continue
                else:
                    # 1 шаг: dfs с определением порядков завершения для каждой вершины
                    visited = set()
                    stack = []
                    for vertex in selected.adj_list:
                        if vertex not in visited:
                            stack, component_visited = selected.dfs_ordered(vertex, stack, set())
                            visited.update(component_visited)
                    # 2 шаг: транспонирование графа
                    selectedt = selected.transpose()
                    if selectedt:
                        all_graphs.append(selectedt)
                        if add_graphs_options(all_graphs, options):
                            print(update + choice)
                            print("\n".join(value for _, value in sorted(options.items())))
                            already_printed = True
                            print(input_string, end="")
                    # 3 шаг: dfs по транспонированному графу
                    visited.clear() # очищаем visited, по новой всё будет посещаться 
                    scc_list = [] # список компонент сильной связности
                    for vertex in reversed(stack):
                        if vertex not in visited:
                            before_dfs = visited.copy()
                            component = selectedt.dfs(vertex, visited)
                            component = visited - before_dfs
                            scc_list.append(list(component))
                    if len(scc_list) == 0:
                        print("Компонент сильной связности не найдено\n")
                        continue
                    else:
                        print("Вот найденные компоненты сильной связности: \n")
                        for comp in scc_list:
                            print(", ".join(comp))
        elif n == 16:
            print("Этот пункт выполняется только для ориентированных графов!\n")
            selected = menu_for_choice_graph(all_graphs, True)
            if not selected: 
                continue
            else:
                begin_vertex = input("Введите какую-нибудь вершину из этого графа: ")
                if begin_vertex not in selected.adj_list:
                    print("Такой вершины в графе нет!\n")
                    continue
                else:
                    end_vertex = input("Введите ещё какую-нибудь вершину из этого графа: ")
                    if end_vertex not in selected.adj_list:
                        print("Такой вершины в графе нет!\n")
                        continue
                    else: 
                        path = selected.bfs_shortest_path(begin_vertex, end_vertex)
                        if path:
                            print(f"Кратчайший путь из {begin_vertex} в {end_vertex}: ")
                            print(" -> ".join(path))
                            print(f"Длина пути: {len(path) - 1} дуг\n")
                        else:
                            print(f"Пути из '{begin_vertex}' в '{end_vertex}' не существует!\n")
                            continue
        elif n == 17:
            print("Этот пункт выполняется только для неориентированных взвешенных графов!\n")
            selected = menu_for_choice_graph(all_graphs, False, True)
            if not selected: 
                continue
            else:
                vertices = list(selected.adj_list.keys())
                if not vertices:
                    print("Граф пустой, искать нечего\n")
                    continue
                    
                visited = selected.dfs(vertices[0])
                if len(visited) != len(vertices):
                    print("Граф не является связным! Алгоритм Краскала, увы, с такими не работает.\n")
                    continue

                mst = selected.kruskal_main() # получаем минимальное остовное дерево
                if mst:
                    print(f"Минимальное остовное дерево {mst.name} успешно создано!")
                    all_graphs.append(mst)
                    if add_graphs_options(all_graphs, options):
                        print(update + choice)
                        print("\n".join(value for _, value in sorted(options.items())))
                        already_printed = True
                        print(input_string, end="")
                    print(mst)
                    mst.print_adj_list()
        elif n == 18:
            print("Этот пункт выполняется только для взвешенных графов!\n")
            selected = menu_for_choice_graph(all_graphs, False, True)
            if not selected: 
                continue
            else:
                selected_alist = selected.adj_list
                if any(weight < 0 for neighbors in selected_alist.values() for _, weight in neighbors):
                    print("Алгоритм Дейкстры не работает с отрицательными весами\n")
                    continue
                else: 
                    begin_vertex = input("Введите какую-нибудь вершину из этого графа: ")
                    if begin_vertex not in selected_alist:
                        print("Такой вершины в графе нет!\n")
                        continue
                    else:
                        end_vertex = input("Введите ещё какую-нибудь вершину из этого графа: ")
                        if end_vertex not in selected_alist:
                            print("Такой вершины в графе нет!\n")
                            continue
                        else:
                            path, distance = selected.dijkstra(begin_vertex, end_vertex)
                            if not path:
                                print(f"Пути из вершины {begin_vertex} в вершину {end_vertex} не существует")
                            else:
                                print(f"Кратчайший путь из {begin_vertex} в {end_vertex}:")
                                print(" -> ".join(map(str, path)))
                                print(f"Длина пути: {distance}")

                                print("\nРёбра пути:")
                                for i in range(len(path) - 1):
                                    u, v = path[i], path[i + 1]
                                    weight = next(w for neighbor, w in selected.adj_list[u] if neighbor == v)
                                    print(f"  {u} -> {v} (вес: {weight})")
        elif n == 19:
            print("Этот пункт выполняется только для взвешенных графов!\n")
            selected = menu_for_choice_graph(all_graphs, False, True)
            if not selected: 
                continue
            else:
                selected_alist = selected.adj_list
                if any(weight < 0 for neighbors in selected_alist.values() for _, weight in neighbors):
                    print("Алгоритм Йена не работает с отрицательными весами\n")
                    continue
                else: 
                    begin_vertex = input("Введите какую-нибудь вершину из этого графа: ")
                    if begin_vertex not in selected_alist:
                        print("Такой вершины в графе нет!\n")
                        continue
                    else:
                        end_vertex = input("Введите ещё какую-нибудь вершину из этого графа: ")
                        if end_vertex not in selected_alist:
                            print("Такой вершины в графе нет!\n")
                            continue
                        else:
                            count = input("Введите какое-нибудь целое k: ")
                            try:
                                k = int(count)
                                if k <= 0:
                                    print("k должно быть положительным числом!\n")
                                    continue
                                
                                paths = selected.yen(begin_vertex, end_vertex, k)
                    
                                if not paths:
                                    print(f"Пути из вершины {begin_vertex} в вершину {end_vertex} не существует")
                                else:
                                    print(f"Найдено {len(paths)} кратчайших путей из {begin_vertex} в {end_vertex} (k = {k})\n")
                                    for path_num, (distance, path) in enumerate(paths, 1):
                                        print(f"Путь № #{path_num}:")
                                        print(f"Маршрут: {' -> '.join(map(str, path))}")
                                        print(f"Длина: {distance}")
                                        print(f"Рёбра пути:")
                                        total_weight = 0
                                        for i in range(len(path) - 1):
                                            u, v = path[i], path[i + 1]
                                            weight = next(w for neighbor, w in selected.adj_list[u] if neighbor == v)
                                            total_weight += weight
                                            print(f"{u} -> {v} (вес: {weight})")
                            except ValueError:
                                print("Введено не целое число\n")
                                continue
        elif n == 0:
            exit()
        elif n == -1:
            print("Некорректный ввод, выход из программы...")
            exit()
        elif n == 100:
            print(choice)
            print("\n".join(value for _, value in sorted(options.items())))
            print(input_string, end="")
            already_printed = True
        else:
            print("Некорректный ввод\n")
        if not already_printed:
            print("Введите номер опции. Чтобы вывести список опций, введите число 100\n")
            print(input_string, end="")
        already_printed = False
        try:
            n = int(input())
            if n not in options.keys() and n != 100:
                n = -1
        except ValueError:
            n = -1
    print()
    