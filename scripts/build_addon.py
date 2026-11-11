"""Build the legacy Blender add-on installation ZIP without importing bpy."""

import ast
import hashlib
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NAME = "io_scene_gltf2_msfs_2020"
SOURCE = ROOT / "addons" / NAME
DEFAULT = ROOT / "dist" / f"{NAME}-blender-5.3.zip"


def addon_version():
    tree = ast.parse((SOURCE / "__init__.py").read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == "bl_info" for target in node.targets
        ):
            return ast.literal_eval(node.value)["version"]
    raise ValueError("bl_info not found")


def main():
    output = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT
    output.parent.mkdir(parents=True, exist_ok=True)
    entries = [(f"{NAME}/{p.relative_to(SOURCE).as_posix()}", p)
               for p in SOURCE.rglob("*.py") if "__pycache__" not in p.parts]
    for filename in ("LICENSE.md", "NOTICE", "UPSTREAM.md", "CHANGELOG.md"):
        entries.append((f"{NAME}/{filename}", ROOT / filename))
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, path in sorted(entries):
            archive.write(path, name)
    print(f"Version: {'.'.join(map(str, addon_version()))}")
    print(f"ZIP: {output}")
    print(f"SHA256: {hashlib.sha256(output.read_bytes()).hexdigest()}")


if __name__ == "__main__":
    main()
