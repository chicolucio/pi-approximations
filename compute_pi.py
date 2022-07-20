import math
from functools import cached_property

import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go

from helpers import create_coords, distance_points, error


def pi_leibniz(number_of_terms):
    result = 0
    for k in range(number_of_terms):
        result += 1 / ((4 * k + 1) * (4 * k + 3))
    return 8 * result


def pi_euler(number_of_terms):
    result = 0
    for k in range(1, number_of_terms + 1):
        result += 1 / k ** 2
    return math.sqrt(6 * result)


class PiMonteCarlo:

    def __init__(self, points, seed=None):
        self.points = points
        self.seed = seed

    @property
    def seed(self):
        return self._seed

    @seed.setter
    def seed(self, value):
        if not isinstance(value, (type(None), int)):
            raise TypeError('Seed must be None or integer')
        else:
            self._clear_cache()
            self._seed = value

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, value):
        if not isinstance(value, int):
            raise TypeError('Points must be integer')
        if value > 0:
            self._clear_cache()
            self._points = value
        else:
            raise ValueError('Points must be a positive integer')

    def _gen_coords(self):
        return create_coords(self.points, self.seed)

    def _mask(self):
        return np.where(
            np.array([distance_points(c) for c in self.coords]) <= 1, 1,
            0)

    def _count(self):
        return np.sum(self._mask())

    @cached_property
    def coords(self):
        return tuple(self._gen_coords())

    @cached_property
    def calculate(self):
        area_estimate = self._count() / self.points
        return area_estimate * 4

    def error(self, expected=math.pi):
        return error(self.calculate, expected)

    def _clear_cache(self):
        if 'coords' in self.__dict__:
            del self.__dict__['coords']
        if 'calculate' in self.__dict__:
            del self.__dict__['calculate']

    def _colors(self, dot_colors=('red', 'blue')):
        return np.where(self._mask() == 1, *dot_colors)

    def _matplotlib(self, colors):
        fig, ax = plt.subplots(figsize=(8, 8), facecolor=(1, 1, 1))
        ax.scatter(*zip(*self.coords), color=colors)
        ax.set_title(fr"Points = {self.points:,.0f}   "
                     fr"$\pi \approx$ {self.calculate:.4f}   "
                     fr"Error = {self.error():.2%}")
        plt.show()

    def _plotly(self, colors):
        x, y = zip(*self.coords)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y,
                                 mode='markers',
                                 marker=dict(color=colors)))
        fig.add_shape(type='circle', x0=-1, x1=1, y0=-1, y1=1,
                      line_color=colors[0])
        fig.update_xaxes(range=[0, 1], constrain='domain')
        fig.update_yaxes(range=[0, 1], constrain='domain')
        fig.update_layout(xaxis=dict(scaleanchor="y", scaleratio=1))
        fig.show()
        # TODO title

    def plot(self, dot_colors=('red', 'blue'), backend='matplotlib'):
        colors = self._colors(dot_colors)
        if backend == 'matplotlib':
            self._matplotlib(colors)
        elif backend == 'plotly':
            self._plotly(colors)
        else:
            raise ValueError('Backend must be matplotlib or plotly')
