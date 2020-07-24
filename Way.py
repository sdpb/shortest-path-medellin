class Node:
    def __init__(self, point):
        self.point = point
        self.associated_ways = []

    def __str__(self):
        id = 'X: {} Y: {}'.format(round(self.point.x, 4), round(self.point.y, 4))
        for _ in self.associated_ways:
            id += ' - {}'.format(_.OBJECTID)
        return id


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
