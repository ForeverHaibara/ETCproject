"""Convert the supplied GeoGebra AlgoKimberlingWeights.java snapshot once."""

import argparse
import ast
import hashlib
from pathlib import Path
import re

from triangle_center_coordinates import validate_formula


DATA = Path(__file__).resolve().parents[1] / "data"
CASE = re.compile(r"\bcase\s+(\d+)\s*:\s*(.*?)(?=\b(?:case\s+\d+|default)\s*:)", re.S)
NAMES = {
    **{f"{side}{n}": f"({side}**{n})" for side in "abc" for n in range(2, 11)},
    "Q": "((b**2-c**2)**2)",
    "R": "(b**2+c**2)",
    "S": "(2*S)",
    "T": "(-2*SA)",
    "U": "(2*SC)",
    "V": "(2*SB)",
    "angleA": "A",
    "angleB": "B",
    "angleC": "C",
    "Math.PI": "pi",
    "Math.sin": "sin",
    "Math.cos": "cos",
    "u": "sqrt",
}


class Powers(ast.NodeTransformer):
    def visit_Call(self, node):
        self.generic_visit(node)
        if isinstance(node.func, ast.Name) and node.func.id == "p":
            base, exponent = node.args
            return ast.BinOp(base, ast.Pow(), exponent)
        return node


def convert(source: Path, output: Path):
    raw = source.read_bytes()
    java = raw.decode("utf-8")
    license_header = java.partition("*/")[0].removeprefix("/*")
    if "EUPL 1.2" not in license_header:
        raise ValueError("Expected the GeoGebra copyright and license header")

    # Reviewed overrides already have recipes, including the Java fall-through
    # group 2923–2928, so no translation of that Java control flow is needed.
    overrides = {
        int(line.split()[0])
        for line in (DATA / "native-patches.txt").read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }
    java = re.sub(r"/\*.*?\*/|//[^\n]*", "", java, flags=re.S)
    cases = {}
    for number, body in CASE.findall(java):
        n = int(number)
        if n in cases:
            raise ValueError(f"Duplicate Java case X({n})")
        cases[n] = body.strip()
    if cases.keys() != set(range(1, 3054)) - {368, 369, 370, 1144}:
        raise ValueError("Unexpected coverage in the Java snapshot")

    rows = []
    for number in sorted(cases.keys() - overrides):
        statement = re.fullmatch(r"return\s+([^;]+);", cases[number])
        if statement is None:
            raise ValueError(f"X({number}) is not a single Java return expression")
        expression = re.sub(r"\s+", "", statement[1])
        expression = re.sub(r"\b(\d+)[dD]\b", r"\1.0", expression)
        expression = re.sub(r"\b(?:Math\.)?[A-Za-z]\w*\b",
                            lambda token: NAMES.get(token[0], token[0]), expression)
        tree = Powers().visit(ast.parse(expression, mode="eval"))
        formula = ast.unparse(tree).replace(" ", "").replace("**", "^")
        validate_formula(formula)
        rows.append(f"{number} B {formula}")

    license_rows = ["# " + line.strip().removeprefix("*").strip()
                    for line in license_header.splitlines() if line.strip() not in {"", "*"}]
    header = [
        "# Generated from GeoGebra AlgoKimberlingWeights.java by tools/convert_native_weights.py.",
        f"# Source SHA256: {hashlib.sha256(raw).hexdigest()}",
        "# Cyclic barycentric first weights. S is twice the area in this table.",
        "# Reviewed overrides live in data/chunks. Missing cases: 368, 370, 1144.",
    ]
    output.write_text("\n".join([*header, *license_rows, "", *rows]) + "\n",
                      encoding="utf-8", newline="\n")
    return len(rows)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--output", type=Path, default=DATA / "native-weights.txt")
    args = parser.parse_args()
    print(f"Converted {convert(args.source, args.output)} native weights")
