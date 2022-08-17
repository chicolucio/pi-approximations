import math
from functools import cached_property

import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
from matplotlib.patches import Arc

from src.helpers import create_coords, distance_points, error


def pi_leibniz(number_of_terms):
    """
    Pi approximation using Leibniz formula

    Parameters
    ----------
    number_of_terms : int
        Terms of the infinite series

    Returns
    -------
    float
        Pi approximation
    """

    result = 0
    for k in range(number_of_terms):
        result += 1 / ((4 * k + 1) * (4 * k + 3))
    return 8 * result


def pi_euler(number_of_terms):
    """
    Pi approximation using Euler formula

    Parameters
    ----------
    number_of_terms : int
        Terms of the infinite series

    Returns
    -------
    float
        Pi approximation
    """

    result = 0
    for k in range(1, number_of_terms + 1):
        result += 1 / k ** 2
    return math.sqrt(6 * result)


class PiMonteCarlo:
    """
    Pi approximation by Monte Carlo method
    """

    def __init__(self, points, seed=None):
        """
        Class initialization

        Parameters
        ----------
        points : int
            number of points
        seed : number, optional
            seed used by the NumPy PRNG. Default None
        """

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
        """
        Generates points coordinates

        Returns
        -------
        generator
            Coordinates generator
        """
        return create_coords(self.points, self.seed)

    def _mask(self):
        """
        Array of 0's (points outside quadrant) and 1's (points inside quadrant)

        Returns
        -------
        numpy array
        """
        return np.where(
            np.array([distance_points(c) for c in self.coords]) <= 1, 1,
            0)

    def count_inside_quadrant(self):
        """
        Count points inside quadrant

        Returns
        -------
        int
        """
        return np.sum(self._mask())

    @cached_property
    def coords(self):
        """
        Points coordinates. This is a cached property which means that the values are
        calculated only on the first time. Posterior calls are faster since the value
        of the first calculation is cached.

        Returns
        -------
        tuple
        """
        return tuple(self._gen_coords())

    @cached_property
    def calculate(self):
        """
        Pi estimation. This is a cached property which means that the value is
        calculated only on the first time. Posterior calls are faster since the value
        of the first calculation is cached.

        Returns
        -------
        float
        """
        area_estimate = self.count_inside_quadrant() / self.points
        return area_estimate * 4

    def error(self, expected=math.pi):
        """
        Estimation erro

        Parameters
        ----------
        expected : float, optional
            Pi value of reference. Default: math.pi

        Returns
        -------
        float
        """
        return error(self.calculate, expected)

    def _clear_cache(self):
        """
        Clears the cached values. This internal method is called every time that a new
        seed and/or points are set because new coordinates, estimation and errors need
        to be calculated.
        """

        if 'coords' in self.__dict__:
            del self.__dict__['coords']
        if 'calculate' in self.__dict__:
            del self.__dict__['calculate']

    def _colors(self, dot_colors=('red', 'blue')):
        """
        Relates colors to points (inside, outside) the quadrant.

        Parameters
        ----------
        dot_colors : tuple of strings
            Colors for (inside, outside) the quadrant points. Default: ('red', 'blue')

        Returns
        -------
        numpy array
        """
        return np.where(self._mask() == 1, *dot_colors)

    def _matplotlib(self, colors, ax, arc):
        """
        Plot made with Matplotlib

        Parameters
        ----------
        colors : tuple of strings
            Colors for (inside, outside) the quadrant points.
        ax : matplotlib axis
            Axis on which the graph will be plotted
        arc : bool
            If the quadrant will be plotted

        Returns
        -------
        matplotlib axis
        """
        ax.scatter(*zip(*self.coords), color=colors)
        ax.set_title(fr"Points = {self.points:,.0f}   "
                     fr"$\pi \approx$ {self.calculate:.4f}   "
                     fr"Error = {self.error():.2%}")
        if arc:
            arc = Arc(xy=(0, 0), theta1=0, theta2=90, height=2, width=2,
                      color='red', linewidth=3)
            ax.add_patch(arc)
            ax.set_ylim(-0.02, 1.02)
            ax.set_xlim(-0.02, 1.02)
        return ax

    def _plotly(self, colors, arc):
        """
        Plot made with Plotly

        Parameters
        ----------
        colors : tuple of strings
            Colors for (inside, outside) the quadrant points.
        arc : bool
            If the quadrant will be plotted

        Returns
        -------
        Plotly figure
        """
        x, y = zip(*self.coords)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y,
                                 mode='markers',
                                 marker=dict(color=colors)))
        if arc:
            fig.add_shape(type='circle', x0=-1, x1=1, y0=-1, y1=1,
                          line_color=colors[0])
        fig.update_xaxes(range=[0, 1], constrain='domain')
        fig.update_yaxes(range=[0, 1], constrain='domain')
        fig.update_layout(xaxis=dict(scaleanchor="y", scaleratio=1),
                          autosize=True,
                          margin=dict(l=20, r=20, t=20, b=20),
                          modebar=dict(orientation='v'))
        # TODO title
        return fig

    def plot(self, dot_colors=('red', 'blue'), backend='matplotlib', ax=None, arc=False):
        """
        Public plot API

        Parameters
        ----------
        dot_colors : tuple of strings, optional
            Colors for (inside, outside) the quadrant points. Default: ('red', 'blue')
        backend : str, optional
            Plot engine: matplotlib or plotly. Default: matplotlib
        ax : matplotlib axis, optional
            Axis on which the graph will be plotted. If None, one will be created. Works
            only if backend is matplotlib. Default: None
        arc : bool
            If the quadrant will be plotted

        Returns
        -------
        Matplotlib axis or Plotly figure
        """

        colors = self._colors(dot_colors)
        if backend == 'matplotlib':
            if ax is None:
                fig, ax = plt.subplots(figsize=(8, 8), facecolor=(1, 1, 1))
            return self._matplotlib(colors, ax, arc)
        elif backend == 'plotly':
            return self._plotly(colors, arc)
        else:
            raise ValueError('Backend must be matplotlib or plotly')
