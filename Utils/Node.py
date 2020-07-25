class Node:
    def __init__(self, point):
        self.point = point
        self.id = 'X: {} Y: {}'.format(round(point.x, 4), round(point.y, 4))
        self.associated_ways = []

    def __str__(self):
        ID = list(map(lambda x: str(x.OBJECTID), self.associated_ways))
        return str(ID)
