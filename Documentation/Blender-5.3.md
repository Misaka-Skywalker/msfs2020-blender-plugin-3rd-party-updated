# Blender 5.3 compatibility guide

[中文说明](Blender-5.3-zh-CN.md) · [Repository home](../README.md)

This is an unofficial third-party update based on the [official Asobo Studio MSFS 2020 add-on](https://github.com/AsoboStudio/Microsoft-Flight-Simulator-2020-glTF-Blender-IO), not affiliated with or endorsed by Asobo or Microsoft. First public version 3.3.4 builds on upstream version 3.3.2. Report fork bugs to [this repository](https://github.com/Misaka-Skywalker/msfs2020-blender-plugin-3rd-party-updated/issues) rather than Asobo. Back up your `.blend` files and associated textures and assets before opening or migrating them.

## Installation

Download `io_scene_gltf2_msfs_2020-blender-5.3.zip` from the fork's [release assets](https://github.com/Misaka-Skywalker/msfs2020-blender-plugin-3rd-party-updated/releases), not the automatically generated GitHub source ZIP. In Blender, use **Edit > Preferences > Get Extensions > Install from Disk**, select the ZIP, and enable **Microsoft Flight Simulator 2020: glTF Extension**. Blender's built-in glTF 2.0 importer/exporter must remain enabled. Use **File > Import/Export > glTF 2.0** and the MSFS material and multi-export panels. See the retained [upstream documentation](Documentation.md) for original usage guidance; it does not describe this patch.

## Changes and validation

The patch adapts `bgl`/GPU drawing, Draco library paths, WebP export arguments, node and image imports, recursive extension toggles, clearcoat weight sockets, MASK alpha cutoff preservation and embedded GLB image URIs. MSFS 2020 extension names, material properties and LOD file formats remain unchanged.

The lightweight Simplified Chinese translation follows Blender's language and interface translation settings in Preferences. Untranslated strings remain in English; there is no separate add-on language switch.

On Windows, Blender **5.3.0 build 02f0899d78e3**, version 3.3.4 passed 22 automated tests from source and from the ZIP installed into an isolated configuration, including language switching and translation cleanup. They cover registration and re-enabling, collision gizmos, creation of all 17 material options including Disabled and four transparency modes, standard-material texture glTF/GLB round trips, extension toggles in current and non-current scenes, animation, skinning and bone IDs, light export, LOD XML, multi-export, Draco, WebP and ZIP structure. A separate actual GPU drawing and state restoration smoke test passed; the complete interactive viewport was not exhaustively tested. Texture round trips may produce Khronos sampler warnings about multiple image nodes sharing a texture; output textures and key reimported parameters were checked.

These tests use generated scenes. Your projects and the MSFS 2020 SDK and game have not been validated. Older Blender version branches remain but were not retested. Future Blender compatibility updates are anticipated; see [compatibility notes](../COMPATIBILITY.md).

## Known inherited issues

- MASK cutoff is preserved on export, but Blender 5.3's viewport does not preview the corresponding hard cutoff.
- Anisotropic, hair and clearcoat textures round-trip, but creating the material type on reimport resets MASK to OPAQUE. Check and restore the transparency mode manually.
- Spotlight export parameters are correct, but reimport has an angle-unit issue: for example, 30° can become 180°. Correct the angle manually.

These issues were traced to upstream logic and remain outside this compatibility patch's scope.

## Build and test

From the repository root, using Python and Blender on `PATH`:

```sh
python -m unittest discover -s tests -p test_package.py -v
blender --background --factory-startup --python-exit-code 1 --python tests/run_blender_tests.py
python scripts/build_addon.py
```

The build creates `dist/io_scene_gltf2_msfs_2020-blender-5.3.zip` and prints its SHA-256. The package includes the Apache 2.0 license, NOTICE and upstream provenance. On Windows, use the bundled Python and Blender executable paths if they are not on `PATH`, for example `& 'C:/Program Files/Blender Foundation/Blender 5.3/5.3/python/bin/python.exe' scripts/build_addon.py`.

For the GPU smoke test, run Blender with a graphical context, without `--background`. Ensure `test-output/` exists first, then check `test-output/gpu-smoke.json` for `"passed": true`:

```sh
mkdir -p test-output
blender --factory-startup --python tests/run_gpu_smoke.py
```

To test the built ZIP in isolation, set all three Blender profile directories under `test-output/` before running the install test. For example, in a POSIX shell:

```sh
mkdir -p test-output/isolated/{scripts,config,extensions}
export BLENDER_USER_SCRIPTS="$PWD/test-output/isolated/scripts"
export BLENDER_USER_CONFIG="$PWD/test-output/isolated/config"
export BLENDER_USER_EXTENSIONS="$PWD/test-output/isolated/extensions"
blender --background --factory-startup --python-exit-code 1 --python tests/run_install_smoke.py
```

In PowerShell, create the same three directories and set `$env:BLENDER_USER_SCRIPTS`, `$env:BLENDER_USER_CONFIG`, and `$env:BLENDER_USER_EXTENSIONS` to their absolute paths before running the same Blender command. The installation script refuses to install outside `test-output/`. Tests do not save Blender preferences; generated files are in `test-output/`. A restricted environment may report an extension-cache write warning when the source test exits.
