import ast
from pathlib import Path

FORBIDDEN_MODULES = {"webscraper.fetch", "webscraper.collect", "webscraper.sites"}
DASHBOARD_DIR = Path(__file__).resolve().parent.parent / "dashboard"


def _imported_modules(py_file: Path) -> set[str]:
    tree = ast.parse(py_file.read_text(encoding="utf-8"), filename=str(py_file))
    modules = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            modules.add(node.module)
    return modules


def test_dashboard_does_not_import_scraping_modules_ac5():
    offending = []
    for py_file in DASHBOARD_DIR.glob("*.py"):
        hit = _imported_modules(py_file) & FORBIDDEN_MODULES
        if hit:
            offending.append(f"{py_file.name}: {sorted(hit)}")

    assert offending == []
