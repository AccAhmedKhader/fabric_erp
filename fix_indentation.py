from pathlib import Path
import re

PROJECT_ROOT = Path("GeneratedProject/fabric_erp")

PYTHON_KEYWORDS = {
    "class",
    "def",
    "if",
    "elif",
    "else",
    "try",
    "except",
    "finally",
    "for",
    "while",
    "with",
    "match",
    "case",
}


def should_decrease_indent(line: str) -> bool:
    stripped = line.strip()

    return (
        stripped.startswith("elif ")
        or stripped.startswith("else:")
        or stripped.startswith("except")
        or stripped.startswith("finally:")
        or stripped.startswith("case ")
    )


def should_increase_indent(line: str) -> bool:
    stripped = line.strip()

    if stripped.endswith(":"):
        return True

    return False


def fix_file(path: Path):

    lines = path.read_text(
        encoding="utf-8"
    ).splitlines()

    result = []

    indent = 0

    for line in lines:

        stripped = line.strip()

        if stripped == "":
            result.append("")
            continue

        if should_decrease_indent(stripped):
            indent = max(indent - 1, 0)

        result.append(
            ("    " * indent) + stripped
        )

        if should_increase_indent(stripped):
            indent += 1

    code = "\n".join(result)

    try:
        compile(code, str(path), "exec")
    except Exception as ex:
        print(f"[FAILED] {path}")
        print(ex)
        return

    path.write_text(
        code,
        encoding="utf-8"
    )

    print(f"[OK] {path}")


def main():

    files = list(PROJECT_ROOT.rglob("*.py"))

    print(f"Found {len(files)} python files")

    for file in files:
        fix_file(file)


if __name__ == "__main__":
    main()