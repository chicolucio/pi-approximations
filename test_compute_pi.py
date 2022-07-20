import math
from contextlib import nullcontext as does_not_raise

import pytest

from compute_pi import pi_leibniz, pi_euler, PiMonteCarlo


def test_leibniz_n1():
    assert pi_leibniz(1) == 8 / 3


def test_leibniz_n2():
    assert pi_leibniz(2) == 8 * (1 / 3 + 1 / 35)


def test_leibniz_n3():
    assert pi_leibniz(3) == 8 * (1 / 3 + 1 / 35 + 1 / 99)


def test_euler_n1():
    assert pi_euler(1) == math.sqrt(6)


def test_euler_n2():
    assert pi_euler(2) == math.sqrt(6 * (1 + 1 / 4))


def test_euler_n3():
    assert pi_euler(3) == math.sqrt(6 * (1 + 1 / 4 + 1 / 9))


class TestMonteCarlo:
    SEED = 42

    @pytest.mark.parametrize(
        'points, calculated, tolerance',
        (
                (10, 2.4, 0.01),
                (100, 3.04, 0.001),
                (1_000, 3.084, 0.001),
                (10_000, 3.16, 0.001),
                (100_000, 3.15008, 1E-6),
        )
    )
    def test_calculate(self, points, calculated, tolerance):
        instance = PiMonteCarlo(points, self.SEED)
        assert instance.calculate == pytest.approx(calculated, abs=tolerance)

    @pytest.mark.parametrize(
        'points, calculated, tolerance',
        (
                (10, -0.236, 0.0001),
                (100, -0.03233, 0.0001),
                (1_000, -0.01833, 0.0001),
                (10_000, 0.005859, 0.00001),
                (100_000, 0.0027016, 1E-6),
        )
    )
    def test_error(self, points, calculated, tolerance):
        instance = PiMonteCarlo(points, self.SEED)
        assert instance.error() == pytest.approx(calculated, abs=tolerance)

    @pytest.mark.parametrize(
        'seed, expectation',
        (
                (42, does_not_raise()),
                (0, does_not_raise()),
                (-1, does_not_raise()),
                (None, does_not_raise()),
                (1.0, pytest.raises(TypeError,
                                    match='Seed must be None or integer')),
                ('a', pytest.raises(TypeError,
                                    match='Seed must be None or integer')),
        )
    )
    def test_seed_setter(self, seed, expectation):
        with expectation:
            instance = PiMonteCarlo(10, seed)
            assert instance.seed == seed

    @pytest.mark.parametrize(
        'points, expectation',
        (
                (42, does_not_raise()),
                (0, pytest.raises(ValueError,
                                  match='Points must be a positive integer')),
                (-1, pytest.raises(ValueError,
                                   match='Points must be a positive integer')),
                (None, pytest.raises(TypeError,
                                     match='Points must be integer')),
                (1.0, pytest.raises(TypeError,
                                    match='Points must be integer')),
                ('a', pytest.raises(TypeError,
                                    match='Points must be integer')),
        )
    )
    def test_points_setter(self, points, expectation):
        with expectation:
            instance = PiMonteCarlo(points, self.SEED)
            assert instance.points == points
