# Changelog

## 3.3.4 — 2026-11-12 — first public third-party update

Includes the Blender 5.3 compatibility work and adds lightweight Simplified Chinese translations that follow Blender's interface language and translation settings. Untranslated strings remain English; there is no separate language switch. Older Blender compatibility branches are retained for future updates, but have not been retested. See [compatibility notes](COMPATIBILITY.md). Validated on Blender 5.3.0: 22 automated tests passed from source and the installed ZIP, including language switching and translation cleanup. The license, NOTICE and upstream provenance are included in the package.

## 3.3.3 — local compatibility milestone

Based on Asobo Studio's 3.3.2 source. Adapted GPU drawing, Draco paths, WebP export parameters, node and image imports, extension toggle recursion, clearcoat weight sockets, MASK cutoff export and embedded GLB image URI handling. MSFS extension names, material properties and LOD formats are retained.

Validated on Windows with Blender 5.3.0 build 02f0899d78e3: 20 automated tests passed from source and an isolated installed ZIP; a separate GPU drawing and state restoration smoke test passed. The MSFS SDK and game were not tested, and older Blender versions were not retested. See the [compatibility guide](Documentation/Blender-5.3.md) for test coverage and inherited issues.

## 3.3.2 — upstream baseline

Original Asobo Studio version used as the baseline for this fork. See [upstream](https://github.com/AsoboStudio/Microsoft-Flight-Simulator-2020-glTF-Blender-IO).
