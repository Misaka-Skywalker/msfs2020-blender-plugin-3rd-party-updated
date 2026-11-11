# Blender compatibility and future updates

This fork updates Asobo Studio's official MSFS 2020 add-on for newer Blender
versions while retaining version-specific paths for the older versions supported
by the imported source. It does not replace the core MSFS extension schemas.

## Compatibility status

| Blender | Status for this fork |
| --- | --- |
| 5.3.0 | Runtime tested on Windows, build `02f0899d78e3`; current release target |
| 4.5 LTS | Existing compatibility paths retained; not runtime retested |
| 4.2 LTS | Existing compatibility paths retained; not runtime retested |
| 3.6 LTS | Existing compatibility paths retained; not runtime retested |
| 3.3 LTS | Existing compatibility paths retained; not runtime retested |
| Future versions | Not yet supported or tested; follow the process below |

Blender 5.3.0 is the latest stable target verified for this release as of
2026-11-12. This is a dated compatibility statement, not a promise about future
Blender releases. MSFS SDK compilation and in-game results remain unverified.

Keeping older code paths is a compatibility goal, not evidence that every older
runtime works. Do not remove a version branch solely because the newest version
uses a different API. The regression suite currently targets Blender 5.3; earlier
versions may require a version-appropriate test harness and fixture assertions.

## Where compatibility lives

- `blender/gizmo.py`: GPU state and shader-name version handling.
- `blender/material/`: material node and Principled socket compatibility.
- `blender/translations.py`: partial Chinese dictionaries for current and legacy
  Blender locale identifiers; translation registration follows add-on lifecycle.
- `io/msfs_material.py`: bundled glTF image-loader and material integration.
- `io/msfs_multi_export.py`: version-specific export options and RNA detection
  for renamed WebP/compressed-image properties.
- `io/msfs_multi_export_settings.py`: Draco availability detection with fallback.

## Adding a future Blender version

1. Reproduce the failure with the unmodified add-on in the target Blender build.
   Record its version, build hash and bundled glTF exporter version.
2. Compare the actual Blender/glTF APIs. Prefer capability detection when an API
   may vary independently; use explicit version branches when appropriate.
3. Preserve the current paths for older supported versions. If support must be
   dropped, document that separately instead of silently raising the requirement.
4. Add a regression that fails before the fix, including actual exported JSON or
   reimported data. An operator reporting `FINISHED` alone is insufficient.
5. Run source, installed-ZIP and GPU tests where applicable. Verify current and
   older runtimes that are available; state any untested versions plainly.
6. Update `bl_info["version"]`, this table, the English/Chinese guides and changelog.
   If the target changes, update the package filename and corresponding docs/tests.
7. Build using `scripts/build_addon.py`, inspect license/attribution contents,
   publish a versioned Release with the ZIP and SHA-256, and retain prior releases.

The manual packaging workflow checks the archive; it does **not** certify Blender
runtime or simulator compatibility. No automatic support claim is made for an
unreleased or newly released Blender build.
