from graph_class import Graph

all_graphs = []

if __name__ == "__main__":
    input_string = ">>> "
    def menu_for_choice_graph(allgr, needtype=None): # функция выбора названия графа
        if not allgr:
            print("Пока не было создано ни одного графа. Нужно создать хотя бы один.\n")
            return False
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
                if needtype is None:
                    return graph # если нам не требуется какой-то конкретный тип графа, то просто возвращаем выбранный
                elif graph.isDirected == needtype:
                    return graph
                else:
                    print(f"Мы ищем только графы вида {needtype}. Тот, что вы выбрали, к таковым не относится\n")
                    return False  
        print("Этого графа ещё не создавали\n")
        return False
    print("Добро пожаловать в программу для работы с различными графами!" +
          "\n Добавили кое-что новенькое: если вы введёте вершину из графа, \n выведем те вершины, полустепень исхода которых больше, чем у данной! \n")
    print(choice:="\nВыберите действие: " +
          "\n 1 - создать граф по умолчанию" +
          "\n 2 - создать граф с пользовательскими атрибутами" + 
          "\n 3 - считать графы с текстового (.txt формата и только) файла" +
          "\n 4 - вывести список смежности графа" +
          "\n 5 - добавить в граф вершину" +
          "\n 6 - удалить вершину из графа" +
          "\n 7 - добавить в граф ребро" +
          "\n 8 - удалить из графа ребро" +
          "\n 9 - вывести список рёбер графа" +
          "\n 10 - записать граф в текстовый (формат .txt) файл" +
          "\n 11 - скопировать существующий граф" +
          "\n 12 - вывести те вершины, полустепень исхода которых больше, чем у заданной вершины"
          "\n 0 - выйти отсюда\n")
    print(input_string, end="")
    try:
        n = int(input())
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
                    print(f"Успешно загружено {len(graphs_from_file)} граф(ов)\n")
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
                selected.transform_adj_list()
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
                    print(f"А вот вершины, полустепень исхода которых больше: {', '.join(temp)}\n")
        elif n == 0:
            exit()
        elif n == -1:
            print("Некорректный ввод, выход из программы...")
            exit()
        else:
            print("Некорректный ввод\n")
        print("Введите номер опции. Чтобы вывести список опций, введите число 100\n")
        print(input_string, end="")
        try:
            n = int(input())
            if n == 100:
                print(choice)
                print(input_string, end="")
        except ValueError:
            n = -1
    print()
    