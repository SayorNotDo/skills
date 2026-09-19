import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "scan_project.py"
SPEC = importlib.util.spec_from_file_location("scan_project", SCRIPT)
scan_project = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(scan_project)


class ScanProjectTests(unittest.TestCase):
    def test_detects_typescript_vue_and_package_scripts(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "src").mkdir()
            (root / "src" / "App.vue").write_text("<template />", encoding="utf-8")
            (root / "tsconfig.json").write_text("{}", encoding="utf-8")
            (root / "vite.config.ts").write_text("export default {}", encoding="utf-8")
            (root / "package.json").write_text(json.dumps({
                "devDependencies": {"typescript": "*", "vue": "*", "vite": "*", "vitest": "*"},
                "scripts": {"lint": "eslint .", "typecheck": "vue-tsc --noEmit", "test": "vitest run"},
            }), encoding="utf-8")
            profile = scan_project.scan(root)
            self.assertEqual(profile["project"]["languages"], ["typescript"])
            self.assertEqual(profile["project"]["frameworks"], ["vite", "vue"])
            self.assertEqual(profile["quality"]["test_runner"]["command"], "npm run test")

    def test_detects_python_tools(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "pyproject.toml").write_text(
                "[tool.ruff]\nline-length = 100\n[tool.pytest.ini_options]\ntestpaths = ['tests']\n[tool.mypy]\nstrict = true\n",
                encoding="utf-8",
            )
            profile = scan_project.scan(root)
            self.assertEqual(profile["project"]["languages"], ["python"])
            self.assertEqual(profile["quality"]["linter"]["name"], "ruff")
            self.assertEqual(profile["quality"]["typecheck"]["name"], "mypy")
            self.assertEqual(profile["quality"]["test_runner"]["name"], "pytest")

    def test_detects_rust_defaults(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "Cargo.toml").write_text("[package]\nname='demo'\nversion='0.1.0'\n", encoding="utf-8")
            profile = scan_project.scan(root)
            self.assertEqual(profile["project"]["languages"], ["rust"])
            self.assertEqual(profile["quality"]["formatter"]["name"], "rustfmt")
            self.assertEqual(profile["quality"]["test_runner"]["command"], "cargo test")

    def test_existing_output_is_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / ".engineering" / "project-profile.yaml"
            output.parent.mkdir()
            output.write_text("keep: true\n", encoding="utf-8")
            result = scan_project.main([str(root), "--output", str(output)])
            self.assertEqual(result, 2)
            self.assertEqual(output.read_text(encoding="utf-8"), "keep: true\n")


if __name__ == "__main__":
    unittest.main()
