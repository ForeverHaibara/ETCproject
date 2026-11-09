"""Evaluate the generated ETC catalogue in homogeneous barycentric coordinates."""

import argparse
import ast
from functools import cache
import operator
from pathlib import Path

import sympy as sp


DATA = Path(__file__).resolve().parent / "data"
SIDES = sp.symbols("a b c", positive=True)
FUNCTIONS = {
    name: getattr(sp, name)
    for name in ("sqrt", "sin", "cos", "tan", "cot", "sec", "csc", "sinh", "asinh", "atan")
}
FUNCTIONS.update(ln=sp.log, abs=sp.Abs)
OPERATORS = {
    ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
    ast.Div: operator.truediv, ast.Pow: operator.pow,
}


class PointError(ValueError):
    """Missing recipe, unavailable direction, or undefined construction."""


def read_rows(path, separator=None):
    rows = {}
    with path.open(encoding="utf-8") as file:
        for line in file:
            fields = line.partition("#")[0].split(maxsplit=1)
            if len(fields) == 2:
                number, rest = fields
                rows[int(number)] = tuple(rest.split(separator))
    return rows


class Catalogue:
    """Load each needed chunk once. Native repairs are already in the chunks."""

    def __init__(self, data_dir):
        self.data_dir = Path(data_dir)
        self.chunks = {}
        self.native_weights = None
        self.native_directions = None
        self.gemini_vertices = None

    def recipe(self, number):
        chunk = number // 1000
        if chunk not in self.chunks:
            path = self.data_dir / "chunks" / f"{chunk}.txt"
            self.chunks[chunk] = read_rows(path) if path.is_file() else {}
        if number in self.chunks[chunk]:
            return self.chunks[chunk][number]
        if 1 <= number <= 3053:
            if self.native_weights is None:
                self.native_weights = read_rows(self.data_dir / "native-weights.txt")
                # A bare status ID records a sampled failure, not an ideal direction.
                self.native_directions = read_rows(self.data_dir / "native-status.txt")
            if number in self.native_directions:
                return ("I", *self.native_directions[number])
            if number in self.native_weights:
                # W is internal: ordinary native weights may also give ideal points.
                return ("W", self.native_weights[number][1])
        raise PointError("No generated recipe")

    def gemini_vertex(self, number):
        if self.gemini_vertices is None:
            self.gemini_vertices = read_rows(self.data_dir / "gemini-triangles.txt", "|")
        return self.gemini_vertices[number]


@cache
def parse_formula(text):
    source = text.replace("^", "**")
    return source, ast.parse(source, mode="eval").body


def scalar(text, values, digits):
    """Evaluate the small arithmetic grammar of generated formulas."""
    source, tree = parse_formula(text)

    def visit(node):
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return sp.Rational(source[node.col_offset:node.end_col_offset])
        if isinstance(node, ast.Name) and node.id in values:
            return values[node.id]
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
            value = visit(node.operand)
            return -value if isinstance(node.op, ast.USub) else value
        if isinstance(node, ast.BinOp) and type(node.op) in OPERATORS:
            left, right = visit(node.left), visit(node.right)
            result = OPERATORS[type(node.op)](left, right)
            if digits is not None and isinstance(node.op, (ast.Div, ast.Pow)):
                return real_number(result, digits)
            return result
        if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                and node.func.id in FUNCTIONS and len(node.args) == 1 and not node.keywords):
            result = FUNCTIONS[node.func.id](visit(node.args[0]))
            return result if digits is None else real_number(result, digits)
        raise PointError(f"Unsupported expression in {text!r}")

    return visit(tree)


def require_real(value):
    if value.is_finite is not True or value.is_real is not True:
        raise PointError("Nonreal or undefined coordinates")


def real_number(value, digits):
    # Keep rational constants exact, including exponents such as 2/3.
    # Evaluate algebraic constants like sqrt(3) before they enter the geometry.
    if not (value.is_Rational or value.is_Float):
        value = value.evalf(digits)
    require_real(value)
    return value


def vector(*entries):
    return sp.ImmutableMatrix(entries)


def rotate(items, turn):
    return items[turn:] + items[:turn]


def cross2(u, v):
    return u[0] * v[1] - u[1] * v[0]


def input_number(value):
    if isinstance(value, sp.Expr) and value.is_number and value.is_real and value.is_finite:
        return value
    try:
        return sp.Rational(str(value))
    except (TypeError, ValueError) as error:
        raise ValueError(f"Expected a finite real number, got {value!r}") from error


def read_vertices(vertices):
    points = tuple(vector(*map(input_number, xy)) for xy in vertices)
    if len(points) != 3 or any(len(p) != 2 for p in points):
        raise ValueError("Expected three pairs of vertex coordinates")
    return points


class Triangle:
    """Formula variables and a Cartesian chart with A=(0,0), B=(c,0)."""

    def __init__(self, sides, vertices, precision):
        if sides is not None and vertices is not None:
            raise ValueError("Supply sides or vertices")
        if precision < 16:
            raise ValueError("Use at least 16 digits of working precision")
        self.numeric = sides is not None or vertices is not None
        self.digits = precision if self.numeric else None
        self.original_vertices = None
        area2 = None
        if vertices is not None:
            points = self.original_vertices = read_vertices(vertices)
            a, b, c = (sp.sqrt((q - p).dot(q - p)) for p, q in
                       ((points[1], points[2]), (points[2], points[0]), (points[0], points[1])))
            area2 = abs(cross2(points[1] - points[0], points[2] - points[0]))
            if area2 == 0:
                raise ValueError("The vertices must form a nondegenerate triangle")
        elif sides is not None:
            a, b, c = map(input_number, sides)
            if min(a, b, c) <= 0 or 2 * max(a, b, c) >= a + b + c:
                raise ValueError("The side lengths must form a nondegenerate triangle")
        else:
            a, b, c = SIDES

        s = (a + b + c) / 2
        sa, sb, sc = s - a, s - b, s - c
        S = 2 * sp.sqrt(s * sa * sb * sc) if area2 is None else area2
        SA, SB, SC = ((v*v + w*w - u*u) / 2 for u, v, w in
                      ((a, b, c), (b, c, a), (c, a, b)))
        SW = (a*a + b*b + c*c) / 2
        R = a * b * c / (2 * S)
        E = 4 * R**2
        values = dict(a=a, b=b, c=c, A=sp.atan2(S, SA), B=sp.atan2(S, SB), C=sp.atan2(S, SC),
                      s=s, sa=sa, sb=sb, sc=sc, S=S, SA=SA, SB=SB, SC=SC, SW=SW,
                      r=S / (2*s), R=R, E=E, F=SW-E, pi=sp.pi)
        self.values = {name: value.evalf(precision) for name, value in values.items()} if self.numeric else values
        self.base, self.offset, self.height = (self.working(t) for t in (c, SA / c, S / c))
        self.tolerance = sp.Rational(10) ** (8 - precision)

    def working(self, value):
        return value.evalf(self.digits) if self.numeric else value

    def zero(self, value, scale=1):
        if self.numeric:
            return value == 0 or abs(value) <= self.tolerance * scale
        return value == 0

    def ideal(self, point):
        return self.zero(sum(point), sum(abs(t) for t in point) if self.numeric else 1)

    def affine(self, point):
        if self.ideal(point):
            raise PointError("This construction needs a finite point")
        return point / sum(point)

    def linear_xy(self, weights):
        """Apply the Cartesian chart to affine weights or a zero-sum direction."""
        _, y, z = weights
        return vector(self.base*y + self.offset*z, self.height*z)

    def xy(self, point):
        return self.linear_xy(self.affine(point))

    def barycentric(self, xy):
        x, y = xy
        gamma = y / self.height
        beta = (x - gamma*self.offset) / self.base
        return vector(1 - beta - gamma, beta, gamma)


class Evaluator:
    """Evaluate the dependency graph using one triangle and one point cache."""

    def __init__(self, catalogue, triangle):
        self.catalogue = catalogue
        self.triangle = triangle
        self.points = {}
        self.active = set()

    def point(self, number):
        if number in self.points:
            return self.points[number]
        if number in self.active:
            raise PointError(f"Cyclic recipe at X({number})")
        self.active.add(number)
        try:
            op, *args = self.catalogue.recipe(number)
            point = self.evaluate(op, args)
            if self.triangle.numeric:
                for weight in point:
                    require_real(weight)
            if all(t.is_zero is True for t in point):
                raise PointError("All three homogeneous coordinates vanish")
            if op not in ("I", "W") and self.triangle.ideal(point):
                raise PointError("Finite construction has an ideal result")
        except PointError as error:
            raise PointError(f"X({number}): {error}") from error
        finally:
            self.active.remove(number)
        self.points[number] = point
        return point

    def cyclic(self, formula, inputs=()):
        values = self.triangle.values
        groups = ("abc", "ABC", ("sa", "sb", "sc"), ("SA", "SB", "SC"))
        groups += ("xyz", "uvw")[:len(inputs)]
        values = values | dict(zip("xyzuvw", (t for p in inputs for t in p)))
        return vector(*(scalar(formula, values | {
            name: values[rotated]
            for group in groups for name, rotated in zip(group, rotate(group, turn))
        }, self.triangle.digits) for turn in range(3)))

    def intersection(self, p, q, r, s):
        if ((self.triangle.ideal(p) and self.triangle.ideal(q))
                or (self.triangle.ideal(r) and self.triangle.ideal(s))):
            raise PointError("A defining line needs a finite endpoint")
        return self.cross(self.cross(p, q), self.cross(r, s))

    def cross(self, p, q):
        result = p.cross(q)
        if self.triangle.numeric:
            scale = max(map(abs, p)) * max(map(abs, q))
            if all(self.triangle.zero(t, scale) for t in result):
                raise PointError("Coincident points or lines")
        return result

    def project(self, p, q, r):
        triangle = self.triangle
        self.cross(q, r)
        if triangle.ideal(q):
            q, r = r, q
        anchor = triangle.xy(q)
        direction = triangle.linear_xy(r) if triangle.ideal(r) else triangle.xy(r) - anchor
        length2 = direction.dot(direction)
        if length2.is_zero is True:
            raise PointError("Coincident endpoints")
        return anchor + direction * ((p - anchor).dot(direction) / length2)

    def circle_center(self, p, q, r):
        u, v = q - p, r - p
        det = cross2(u, v)
        scale = max(map(abs, u)) * max(map(abs, v)) if self.triangle.numeric else 1
        if self.triangle.zero(det, scale):
            raise PointError("The three points do not determine a circle")
        return p + (u.dot(u)*vector(v[1], -v[0]) + v.dot(v)*vector(-u[1], u[0])) / (2*det)

    def invert(self, p, center, radius2):
        offset = p - center
        distance2 = offset.dot(offset)
        scale = max(map(abs, (*p, *center))) if self.triangle.numeric else 1
        if (self.triangle.zero(distance2, scale**2 * self.triangle.tolerance)
                or radius2.is_zero is True):
            raise PointError("Circle inversion has no finite result")
        return center + offset * (radius2 / distance2)

    def gemini(self, number, point):
        # If M has the three target vertices as columns, M*diag(adj(M)*1)
        # takes the vertex frame to those vertices and fixes the centroid.
        cyclic = tuple(self.cyclic(f) for f in self.catalogue.gemini_vertex(number))
        columns = [vector(*(cyclic[(i-turn) % 3][turn] for i in range(3))) for turn in range(3)]
        dual = [columns[(j+1) % 3].cross(columns[(j+2) % 3]) for j in range(3)]
        scales = [sum(row) for row in dual]
        triangle = self.triangle
        determinant = columns[0].dot(dual[0])
        determinant_scale = sum(abs(x*y) for x, y in zip(columns[0], dual[0])) if triangle.numeric else 1
        if (triangle.zero(determinant, determinant_scale)
                or any(triangle.zero(s, sum(map(abs, row)) if triangle.numeric else 1)
                       for s, row in zip(scales, dual))):
            raise PointError("Degenerate Gemini frame")
        return sum((w*s*col for w, s, col in zip(point, scales, columns)), vector(0, 0, 0))

    def combo(self, args):
        triangle = self.triangle
        pairs = [item.split(":", 1) for item in args]
        points = [triangle.affine(self.point(int(number))) for number, _ in pairs]
        values = triangle.values
        if len(points) == 2 and any("d" in formula for _, formula in pairs):
            delta = triangle.linear_xy(points[0] - points[1])
            values = values | {"d": sp.sqrt(delta.dot(delta))}
        weights = [scalar(formula, values, triangle.digits) for _, formula in pairs]
        total = sum(weights)
        if triangle.zero(total, sum(map(abs, weights)) if triangle.numeric else 1):
            raise PointError("The combination weights sum to zero")
        return sum((w*p for w, p in zip(weights, points)), vector(0, 0, 0)) / total

    def evaluate(self, op, args):
        triangle = self.triangle
        if op == "F":
            return self.combo(args)
        if op in ("B", "W"):
            *refs, formula = args
            inputs = tuple(self.point(int(n)) for n in refs)
            if formula.startswith("@g"):
                return self.gemini(int(formula[2:]), inputs[0])
            if formula not in ("x^2", "x^3"):
                inputs = tuple(triangle.affine(p) for p in inputs)
            return self.cyclic(formula, inputs)

        points = [self.point(int(n)) for n in args]
        if op == "I":
            if not points:
                raise PointError("Ideal point with no usable direction")
            self.cross(*points)
            p, q = map(triangle.affine, points)
            x, y, _ = q - p
            return vector(x, y, -x-y)
        if op == "J":
            return self.intersection(*points)
        if op in ("G", "T"):
            x, y, z = points[0]
            a, b, c = (triangle.values[name] for name in "abc")
            return vector(a*a*y*z, b*b*z*x, c*c*x*y) if op == "G" else vector(y*z, z*x, x*y)
        if op in ("C", "A"):
            p = triangle.affine(points[0])
            return vector(1, 1, 1) - p if op == "C" else vector(1, 1, 1) - 2*p
        if op == "M" or (op == "R" and len(points) == 2):
            p, q = map(triangle.affine, points)
            return p + q if op == "M" else 2*q - p
        if op in ("P", "R"):
            p, q, r = points
            xy = triangle.xy(p)
            foot = self.project(xy, q, r)
            return triangle.barycentric(foot if op == "P" else 2*foot - xy)
        if op == "O":
            return triangle.barycentric(self.circle_center(*map(triangle.xy, points)))
        if op == "V":
            xy = triangle.xy(points[0])
            if len(points) == 3:
                center, through = map(triangle.xy, points[1:])
                delta = through - center
                radius2 = delta.dot(delta)
            else:
                center = self.circle_center(vector(0, 0), vector(triangle.base, 0),
                                            vector(triangle.offset, triangle.height))
                radius2 = triangle.values["R"]**2
            return triangle.barycentric(self.invert(xy, center, radius2))
        raise PointError(f"Unknown operation {op!r}")


def barycentric(number: int, *, sides=None, vertices=None, precision: int = 40, data_dir=DATA):
    """Return three SymPy weights. Sides are opposite A, B, C, in that order.

    Omit the triangle for symbolic weights in a, b, c. Numeric finite
    weights sum to one. An ideal direction has weights summing to zero.
    """
    triangle = Triangle(sides, vertices, precision)
    point = Evaluator(Catalogue(data_dir), triangle).point(number)
    if not triangle.numeric:
        return tuple(point)
    if triangle.ideal(point):
        x, y, _ = point / max(map(abs, point))
        return x, y, -x-y
    return tuple(triangle.affine(point))


def cartesian(number: int, vertices, *, precision: int = 40, data_dir=DATA):
    """Return the finite center in the supplied vertex coordinate system."""
    triangle = Triangle(None, vertices, precision)
    point = Evaluator(Catalogue(data_dir), triangle).point(number)
    return tuple(sum((w*p for w, p in zip(triangle.affine(point), triangle.original_vertices)),
                     vector(0, 0)))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("number", type=int, help="ETC center ID")
    triangle = parser.add_mutually_exclusive_group()
    triangle.add_argument("--sides", nargs=3, metavar=("a", "b", "c"))
    triangle.add_argument("--vertices", nargs=6, metavar=("Ax", "Ay", "Bx", "By", "Cx", "Cy"))
    parser.add_argument("--cartesian", action="store_true", help="Return x y with --vertices")
    parser.add_argument("--precision", type=int, default=40, help="Numeric working digits")
    args = parser.parse_args()
    if args.cartesian and args.vertices is None:
        parser.error("--cartesian requires --vertices")
    vertices = tuple(zip(args.vertices[::2], args.vertices[1::2])) if args.vertices else None
    try:
        if args.cartesian:
            print(*cartesian(args.number, vertices, precision=args.precision))
        else:
            print(" : ".join(map(str, barycentric(args.number, sides=args.sides, vertices=vertices,
                                                  precision=args.precision))))
    except (ValueError, OSError) as error:
        parser.exit(1, f"{error}\n")


if __name__ == "__main__":
    main()
