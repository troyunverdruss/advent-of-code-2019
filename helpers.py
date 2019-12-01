from typing import List
from pathlib import Path


def path(caller_file, path):
    return Path(caller_file).parent.joinpath(path)


def read_numeric_entries(input_file) -> List[int]:
    numbers = []
    with open(input_file, 'r', encoding='utf8') as f:
        for line in f:
            numbers.append(int(line.strip()))

    return numbers


def read_raw_entries(input_file, strip=True) -> List[str]:
    lines = []
    with open(input_file, 'r', encoding='utf8') as f:
        for line in f:
            if strip:
                lines.append(line.strip())
            else:
                lines.append(line)

    return lines


class Point:
    def __init__(self, x=None, y=None, id=''):
        self.id = id
        self.x = int(x)
        self.y = int(y)

    def __add__(self, other):
        # Changing this will probably break some of the older puzzles, but
        # I think it's better this way ...
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        if type(other) != Point:
            return False
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return repr('{}({},{})'.format(self.id, self.x, self.y))

    def __hash__(self):
        return hash('{}({},{})'.format(self.id, self.x, self.y))

    def __str__(self):
        return '{}({},{})'.format(self.id, self.x, self.y)


class Point3d:
    def __init__(self, x=None, y=None, z=None, id=''):
        self.id = id
        self.x = int(x)
        self.y = int(y)
        self.z = int(z)

    def __add__(self, other):
        # Changing this will probably break some of the older puzzles, but
        # I think it's better this way ...
        return Point3d(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Point3d(self.x - other.x, self.y - other.y, self.z - other.z)

    def __eq__(self, other):
        if type(other) != Point3d:
            return False
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __repr__(self):
        return repr('{}({},{},{})'.format(self.id, self.x, self.y, self.z))

    def __hash__(self):
        return hash('{}({},{},{})'.format(self.id, self.x, self.y, self.z))

    def __str__(self):
        return '{}({},{},{})'.format(self.id, self.x, self.y, self.z)


class Point4d:
    def __init__(self, x=None, y=None, z=None, t=None, id=''):
        self.id = id
        self.x = int(x)
        self.y = int(y)
        self.z = int(z)
        self.t = int(t)

    def __add__(self, other):
        return Point4d(self.x + other.x, self.y + other.y, self.z + other.z, self.t + other.t)

    def __sub__(self, other):
        return Point4d(self.x - other.x, self.y - other.y, self.z - other.z, self.t - other.t)

    def __eq__(self, other):
        if type(other) != Point3d:
            return False
        return self.x == other.x and self.y == other.y and self.z == other.z and self.t == other.t

    def __repr__(self):
        return repr('{}({},{},{},{})'.format(self.id, self.x, self.y, self.z, self.t))

    def __hash__(self):
        return hash('{}({},{},{},{})'.format(self.id, self.x, self.y, self.z, self.t))

    def __str__(self):
        return '{}({},{},{},{})'.format(self.id, self.x, self.y, self.z, self.t)


def get_min_max(points: List[Point]):
    min_x = min(points, key=lambda s: s.x).x
    max_x = max(points, key=lambda s: s.x).x
    min_y = min(points, key=lambda s: s.y).y
    max_y = max(points, key=lambda s: s.y).y
    return min_x, max_x, min_y, max_y


def get_min_max_3d(points: List[Point3d]):
    min_x = min(points, key=lambda s: s.x).x
    max_x = max(points, key=lambda s: s.x).x
    min_y = min(points, key=lambda s: s.y).y
    max_y = max(points, key=lambda s: s.y).y
    min_z = min(points, key=lambda s: s.z).z
    max_z = max(points, key=lambda s: s.z).z
    return min_x, max_x, min_y, max_y, min_z, max_z


def manhattan_distance(a: Point, b: Point) -> int:
    return abs(a.x - b.x) + abs(a.y - b.y)


def manhattan_distance_3d(a: Point3d, b: Point3d) -> int:
    return abs(a.x - b.x) + abs(a.y - b.y) + abs(a.z - b.z)


def manhattan_distance_4d(a: Point4d, b: Point4d) -> int:
    return abs(a.x - b.x) + abs(a.y - b.y) + abs(a.z - b.z) + abs(a.t - b.t)
