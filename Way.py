class Node:
    def __init__(self, point, way):
        self.associated_ways = [way]
        self.point = point
        self.name = way.NOMBRE
        self.id = str(way.OBJECTID)
        for _ in self.associated_ways[1:]:
            self.id += ' ' + str(_.OBJECTID)

    def __str__(self):
        # return str(self.point)
        return str(self.id)  # + ' ' + str(self.name)
        # return str(self.point) + ' ' + str(self.id) + ' ' + str(self.name)


class Way:
    def __init__(self, row, intersections):
        self.OBJECTID = row['OBJECTID']
        self.NOMBRE = row['NOMBRE']
        self.INTERSECTIONS = intersections

    def __str__(self):
        txt = str(self.OBJECTID) + ' ' + self.NOMBRE
        for _ in self.INTERSECTIONS:
            txt += ' ' + str(_)

        return self.NOMBRE
