"""Regression checks for the generated-data evaluator."""

import math
import unittest

import sympy as sp

from etc_point import DATA, SIDES, PointError, barycentric, cartesian, read_rows


class PointEvaluationTest(unittest.TestCase):
    def test_converted_native_weights_keep_area_and_fractional_exponent(self):
        a, b, c = SIDES
        area4 = sp.sqrt((a + b + c)*(-a + b + c)*(a - b + c)*(a + b - c))
        expected = sp.sqrt(3)*a**2*(a**2 - b**2 - c**2) - a**2*area4
        self.assertEqual(sp.simplify(barycentric(15)[0] - expected), 0)
        expected = -(a + b - c)*(a - b + c)*(a*(-a + b + c))**sp.Rational(2, 3)
        self.assertEqual(sp.simplify(barycentric(506)[0] - expected), 0)

    def test_all_reviewed_native_overrides_match_signed_reference_distances(self):
        # Signed distance from BC in the source review's 6–9–13 triangle.
        expected = {
            369: 3.226427108490245, 459: 1.8571771799622385, 1071: 7.896654233888623,
            1285: .10296691685647652, 1908: 1.2802359760886326, 1913: .7225047024565878,
            1939: .7993252177184844, 2923: -5.853795909608209, 2924: 7.2931191813607,
            2925: 19.011461735073297, 2926: 53.48469040713851, 2927: -23.522547806981656,
            2928: -7.067034997766579, 3020: 2.8569360841651337,
        }
        self.assertEqual(set(read_rows(DATA / "native-patches.txt")), set(expected))
        self.assertFalse(set(expected) & read_rows(DATA / "native-weights.txt").keys())
        height = math.sqrt(13**2 - ((6**2 + 13**2 - 9**2) / 12)**2)
        for number, distance in expected.items():
            with self.subTest(number=number):
                weight = barycentric(number, sides=(6, 9, 13))[0]
                self.assertAlmostEqual(float(weight)*height, distance, places=9)

    def test_symbolic_and_numeric_paths_agree(self):
        sides = (6, 9, 13)
        substitutions = dict(zip(SIDES, sides))
        for number in (4201, 10493, 25969, 38910):
            with self.subTest(number=number):
                weights = [w.evalf(35, subs=substitutions) for w in barycentric(number)]
                actual = barycentric(number, sides=sides)
                for value, weight in zip(actual, weights):
                    self.assertAlmostEqual(float(value), float(weight / sum(weights)), places=12)

    def test_cartesian_coordinates_in_the_supplied_frame(self):
        self.assertEqual(tuple(map(float, cartesian(3, ((0, 0), (3, 0), (0, 4))))),
                         (1.5, 2.0))
        abc = ((2, 3), (2, -3), (6, 2))
        for center_id, inputs in ((11618, (6, 14, 15)), (11619, (5, 6, 22))):
            center = cartesian(center_id, abc)
            distances = [math.dist(center, cartesian(n, abc)) for n in inputs]
            self.assertAlmostEqual(max(distances), min(distances), places=12)

    def test_ideal_and_unavailable_coordinates(self):
        self.assertEqual(sum(barycentric(30)), 0)
        self.assertAlmostEqual(float(sum(barycentric(30, sides=(6, 9, 13)))), 0)
        with self.assertRaisesRegex(PointError, "finite point"):
            cartesian(30, ((0, 0), (6, 0), (1, 4)))
        with self.assertRaisesRegex(PointError, "no usable direction"):
            barycentric(64802)
        with self.assertRaisesRegex(PointError, "No generated recipe"):
            barycentric(368)
        with self.assertRaisesRegex(ValueError, "nondegenerate"):
            barycentric(1, sides=(2, 3, 5))
        with self.assertRaisesRegex(PointError, "Coincident"):
            barycentric(30, sides=(1, 1, 1))
