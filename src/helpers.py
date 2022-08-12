from collections import namedtuple

import numpy as np

Coordinate = namedtuple('Coordinate', ('x', 'y'))


def distance_points(coord1, coord2=Coordinate(0, 0)):
    return np.sqrt((coord1.x - coord2.x) ** 2 + (coord1.y - coord2.y) ** 2)


def error(calculated, expected):
    return (calculated - expected) / expected


def create_coords(points, seed=None):
    rng = np.random.default_rng(seed)
    return (Coordinate(rng.uniform(), rng.uniform()) for _ in
            range(int(points)))
