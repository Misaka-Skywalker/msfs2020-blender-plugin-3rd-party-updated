"""Run with blender --background --factory-startup --python-exit-code 1 --python this_file.

Optional arguments after --: a test glob (default test_*.py), then an addon directory.
No Blender preferences are saved. Generated fixtures stay in test-output/.
"""
import pathlib
import sys
import tempfile
import unittest

import addon_utils
import bpy

ROOT = pathlib.Path(__file__).resolve().parents[1]
args = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
pattern = args[0] if args else "test_*.py"
addon_dir = pathlib.Path(args[1]) if len(args) > 1 else ROOT / "addons"
sys.path.insert(0, str(addon_dir))
sys.path.insert(0, str(ROOT / "tests"))
(ROOT / "test-output").mkdir(exist_ok=True)
tempfile.tempdir = str(ROOT / "test-output")

def raise_error(error):
    raise error

addon_utils.enable("io_scene_gltf2", default_set=True, handle_error=raise_error)
addon_utils.enable("io_scene_gltf2_msfs_2020", default_set=True, handle_error=raise_error)
print("TEST_BLENDER_VERSION", bpy.app.version_string, bpy.app.build_hash)
print("TEST_ADDON_DIRECTORY", addon_dir)
suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"), pattern=pattern)
result = unittest.TextTestRunner(verbosity=2).run(suite)
if not result.wasSuccessful():
    raise RuntimeError("Blender compatibility tests failed")
