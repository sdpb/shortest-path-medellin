class way:
    def __init__(self, row, intersections):
        self.OBJECTID = row['OBJECTID']
        self.NOMBRE = row['NOMBRE']
        self.INTERSECTIONS = intersections

    def __str__(self):
        txt = str(self.OBJECTID) + ' ' + self.NOMBRE
        for _ in self.INTERSECTIONS:
            txt += ' ' + str(_)

        return self.NOMBRE
