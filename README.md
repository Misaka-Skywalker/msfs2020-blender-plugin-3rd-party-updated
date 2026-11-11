# MSFS2020 Blender Plugin — 3rd Party Updated

This is an **unofficial third-party update** of [Asobo Studio's official MSFS 2020 Blender add-on](https://github.com/AsoboStudio/Microsoft-Flight-Simulator-2020-glTF-Blender-IO). It is not affiliated with or endorsed by Asobo Studio or Microsoft. The first public version, **3.3.4**, builds on upstream version **3.3.2**, fixes compatibility with Blender 5.3.0 (the latest stable target verified as of 2026-11-12), and adds lightweight Simplified Chinese translations. Please report bugs in this fork to [this repository](https://github.com/Misaka-Skywalker/msfs2020-blender-plugin-3rd-party-updated/issues), not to Asobo.

The add-on extends Blender's glTF importer and exporter with MSFS 2020 materials, lights, collision gizmos, unique IDs and multi-export/LOD tools. Keep Blender's built-in glTF 2.0 add-on enabled. The add-on cannot import glTF files already processed by the simulator's Package Builder and is not compatible with legacy FSX/P3D exporters.

## Install

Back up your `.blend` projects and resources first. Download the **`io_scene_gltf2_msfs_2020-blender-5.3.zip` release asset** from [Releases](https://github.com/Misaka-Skywalker/msfs2020-blender-plugin-3rd-party-updated/releases), not GitHub's automatically generated source ZIP. In Blender, choose **Edit > Preferences > Get Extensions > Install from Disk**, select the asset, and enable **Microsoft Flight Simulator 2020: glTF Extension**. Keep the built-in glTF add-on enabled. Import and export through **File > Import/Export > glTF 2.0**.

Simplified Chinese follows Blender's language and interface translation settings in Preferences; untranslated strings remain in English. There is no separate add-on language switch. For installation, validation, known issues and build instructions see the [English compatibility guide](Documentation/Blender-5.3.md) or [中文说明](Documentation/Blender-5.3-zh-CN.md). See also [compatibility notes](COMPATIBILITY.md). The [upstream documentation](Documentation/Documentation.md) is retained as upstream material and may not describe this fork's changes.

## Validation and limitations

On Windows with Blender **5.3.0 build 02f0899d78e3**, version 3.3.4 passed 22 automated tests both from source and after installation of the ZIP in an isolated profile, including language switching and translation cleanup. A separate GPU drawing and state restoration smoke test also passed. These use generated scenes; MSFS SDK and game validation has not been performed. Older Blender compatibility branches remain in the code but have not been retested; the project leaves room for future Blender compatibility updates. See the guide for three known inherited issues and the limits of the tests.

## Attribution and license

This fork builds on the original work by Asobo Studio and its contributors. Asobo especially thanked Vitus of [Wing42](https://wing42.com/), [tml1024](https://github.com/tml1024), [ronh991](https://github.com/ronh991), and [pepperoni505](https://github.com/pepperoni505) of [FlyByWire](https://flybywiresim.com/). The Khronos glTF exporter remains the copyright of its respective authors. See [NOTICE](NOTICE), [UPSTREAM.md](UPSTREAM.md), and the [Apache License 2.0](LICENSE.md).
