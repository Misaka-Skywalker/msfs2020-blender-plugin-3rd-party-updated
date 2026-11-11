import hashlib
import contextlib
import io
import runpy
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = "io_scene_gltf2_msfs_2020"


class PackageTest(unittest.TestCase):
    def test_build_archive(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as directory:
            archive = Path(directory) / "addon.zip"
            stdout = io.StringIO()
            script = ROOT / "scripts" / "build_addon.py"
            with patch.object(sys, "argv", [str(script), str(archive)]), contextlib.redirect_stdout(stdout):
                runpy.run_path(str(script), run_name="__main__")
            self.assertIn(hashlib.sha256(archive.read_bytes()).hexdigest(), stdout.getvalue())
            with zipfile.ZipFile(archive) as z:
                names = z.namelist()
                expected = sorted(
                    f"{PACKAGE}/{p.relative_to(ROOT / 'addons' / PACKAGE).as_posix()}"
                    for p in (ROOT / "addons" / PACKAGE).rglob("*.py")
                    if "__pycache__" not in p.parts
                ) + [f"{PACKAGE}/{name}" for name in ("LICENSE.md", "NOTICE", "UPSTREAM.md", "CHANGELOG.md")]
                self.assertEqual(names, sorted(expected))
                self.assertEqual(z.read(f"{PACKAGE}/LICENSE.md"), (ROOT / "LICENSE.md").read_bytes())
                self.assertEqual(z.read(f"{PACKAGE}/NOTICE"), (ROOT / "NOTICE").read_bytes())
                self.assertEqual(z.read(f"{PACKAGE}/UPSTREAM.md"), (ROOT / "UPSTREAM.md").read_bytes())
                self.assertEqual(z.read(f"{PACKAGE}/CHANGELOG.md"), (ROOT / "CHANGELOG.md").read_bytes())
                for name in names:
                    self.assertNotIn("__pycache__", name)
                    if name.endswith(".py"):
                        compile(z.read(name), name, "exec")


if __name__ == "__main__":
    unittest.main()
