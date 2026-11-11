"""Install and test the built ZIP using an isolated BLENDER_USER_SCRIPTS directory."""
from pathlib import Path
import runpy
import sys

import addon_utils
import bpy

ROOT = Path(__file__).resolve().parents[1]
scripts = Path(bpy.utils.user_resource("SCRIPTS")).resolve()
assert scripts.is_relative_to(ROOT / "test-output"), "Refusing to install into the user's Blender profile"
archive = ROOT / "dist" / "io_scene_gltf2_msfs_2020-blender-5.3.zip"
assert bpy.ops.preferences.addon_install(filepath=str(archive), overwrite=True) == {"FINISHED"}
module = addon_utils.enable("io_scene_gltf2_msfs_2020", default_set=True)
assert module is not None
assert Path(module.__file__).resolve().is_relative_to(scripts)
source_metadata = runpy.run_path(str(ROOT / "scripts" / "build_addon.py"))
assert module.bl_info["version"] == source_metadata["addon_version"]()
print("INSTALLED_ZIP_MODULE", module.__file__)
sys.argv = [__file__, "--", "test_*.py", str(scripts / "addons")]
runpy.run_path(str(ROOT / "tests" / "run_blender_tests.py"), run_name="__main__")
