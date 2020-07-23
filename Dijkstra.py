from matplotlib.pyplot import subplots, show
from networkx import draw, draw_shell, dijkstra_path, dijkstra_path_length
from geopandas import GeoDataFrame, read_file
from shapely.geometry import Point, MultiPoint
from shapely.ops import unary_union
from itertools import combinations, permutations
from Way import Way, Node
import networkx as nx

data_frame = []
geoms = []
node_list = []
raw_data = GeoDataFrame
fp = r"Data/Corredores_para_Transporte_de_Pasajeros.shp"


def read_with_GeoPandas(path):
    global geoms, raw_data, data_frame
    raw_data = read_file(path)
    geoms = [feature for feature in raw_data.geometry]
    data_frame = [Way(row, []) for index, row in raw_data.iterrows()]


def get_intersections(ways):
    """
    Calculates the intersection points of all roads
    :param ways: List of shapely geometries representing road segments
    """
    global data_frame
    intersection_list = []
    local_intersections = []
    ways_length = len(ways)
    index_i = 0
    for way, i in zip(permutations(ways, 2), range(ways_length * (ways_length - 1))):
        if way[0].intersects(way[1]):
            intersection = way[0].intersection(way[1])
            intersection_type(intersection, intersection_list, local_intersections)
        boundary = [pt for pt in way[0].boundary]
        intersection_list.extend(boundary)
        if i % (ways_length - 1) == (ways_length - 2):
            local_intersections.extend(boundary)
            aux = []
            [aux.append(x) for x in local_intersections if x not in aux]
            data_frame[index_i].INTERSECTIONS = aux
            index_i += 1
            local_intersections = []

    # The unary_union removes duplicate points
    union = unary_union(intersection_list)

    # Ensure the result is a MultiPoint, since calling functions expect an iterable
    if 'Point' == union.type:
        union = MultiPoint([union])

    return union


def intersection_type(intersection, intersection_list, local_intersections):
    if 'Point' == intersection.type:
        add_intersections([intersection], intersection_list, local_intersections)
    elif 'MultiPoint' == intersection.type:
        aux = multi_intersection_process(intersection)
        add_intersections(aux, intersection_list, local_intersections)
    elif 'MultiLineString' == intersection.type:
        aux = multi_intersection_process(intersection)
        add_intersections(aux, intersection_list, intersection)


def add_intersections(intersection, intersection_list, local_intersections):
    intersection_list.extend(intersection)
    local_intersections.extend(intersection)


def multi_intersection_process(intersects):
    process_data = [_ for _ in intersects]
    if intersects.type == 'MultiPoint':
        return process_data
    elif intersects.type == 'MultiLineString':
        first_coords = process_data[0].coords[0]
        last_coords = process_data[len(process_data) - 1].coords[1]
        first_point = Point(first_coords[0], first_coords[1])
        second_point = Point(last_coords[0], last_coords[1])
        return [first_point, second_point]


# Needs improve
def make_nodes(data_f, time, nodelist):
    aux_points = []
    G = nx.Graph()
    index = len(data_f) - 1
    flag = True
    flag2 = True
    print('Loading...')
    for way in data_f:
        print(index, 'Left')
        for way_point in way.INTERSECTIONS:
            node_u = Node(way_point, way)
            for another_way in data_f[-index:]:
                if way_point in aux_points:
                    flag2 = False
                    break
                elif way_point in another_way.INTERSECTIONS:
                    node_u.associated_ways.append(another_way)
                    flag = False
            if not flag and way_point not in aux_points:
                flag = True
                aux_points.append(way_point)
                nodelist.append(node_u)
            elif flag2:
                nodelist.append(node_u)
            flag2 = True
        index -= 1
    weight(nodelist, time, G)
    return G


def weight(nodes, time, G):
    for i, j in combinations(nodes, 2):
        for _ in i.associated_ways:
            if _ in j.associated_ways:
                G.add_edge(i, j, weight=weather(time, i, j))


def weather(time, i, j):
    if time == 'soleado':
        return i.point.distance(j.point)
    elif time == 'lluvioso':
        return (i.point.distance(j.point) * 3) // 2


def graphics(graph, intersects):
    fig, ax = subplots()
    raw_data.plot(ax=ax, color='blue')
    pts = GeoDataFrame([[intersects]], columns=['geometry'])  # GeoDataFrame
    pts.plot(ax=ax, marker='o', color='red', markersize=15)

    fig2, ax2 = subplots()
    draw(graph, with_labels=True, ax=ax2)
    show()


def exe(data):
    read_with_GeoPandas(fp)
    intersects = get_intersections(geoms)
    graph = make_nodes(data_frame[:data], 'lluvioso', node_list)

    print('\n************* Node List *******************\n')

    for _ in node_list:
        print(str(_))

    print('\n************* Shortest Path *******************\n')
    for _ in dijkstra_path(graph, node_list[11], node_list[12]):
        print(_)

    # print(dijkstra_path_length(graph, node_list[11], node_list[12]))
    graphics(graph, intersects)
