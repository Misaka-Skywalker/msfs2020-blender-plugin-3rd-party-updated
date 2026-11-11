"""GPU integration smoke test. Run in a hidden Blender window, not --background."""
import json
from pathlib import Path
import sys
import traceback
from types import SimpleNamespace

import bpy
import gpu
from mathutils import Matrix, Vector

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "addons"))


def run():
    result = {"blender": bpy.app.version_string, "passed": False}
    try:
        from io_scene_gltf2_msfs_2020.blender.gizmo import MSFS2020CollisionGizmo
        # Exercise the production shader and batch with an actual GPU context.
        target = gpu.types.GPUOffScreen(32, 32)
        with target.bind():
            gpu.matrix.load_matrix(Matrix.Identity(4))
            gpu.matrix.load_projection_matrix(Matrix.Identity(4))
            framebuffer = gpu.state.active_framebuffer_get()
            framebuffer.clear(color=(0, 0, 0, 1))
            MSFS2020CollisionGizmo.draw_line_3d(
                None, (1, 0, 0, 1), 2, SimpleNamespace(width=32, height=32),
                [(-0.5, 0, 0), (0.5, 0, 0)],
            )
            pixels = framebuffer.read_color(0, 0, 32, 32, 4, 0, "FLOAT")
            pixels.dimensions = 32 * 32 * 4
            assert any(pixels[i] > 0.5 for i in range(0, len(pixels), 4)), "No line drawn"
        target.free()

        empty = bpy.data.objects.new("GPU state test", None)
        bpy.context.scene.collection.objects.link(empty)
        before = (gpu.state.blend_get(), gpu.state.depth_test_get())
        def fail_draw(*args):
            raise RuntimeError("injected drawing failure")
        dummy = SimpleNamespace(
            empty=empty, custom_shape_edges=[(Vector((0, 0, 0)), Vector((1, 0, 0)))],
            get_matrix=lambda: Matrix.Identity(4),
            apply_vert_transforms=lambda vertex, matrix: vertex,
            draw_line_3d=fail_draw,
        )
        try:
            MSFS2020CollisionGizmo.draw(dummy, bpy.context)
        except RuntimeError as error:
            assert str(error) == "injected drawing failure"
        else:
            raise AssertionError("Draw callback was not reached")
        assert (gpu.state.blend_get(), gpu.state.depth_test_get()) == before
        result["passed"] = True
    except Exception:
        result["error"] = traceback.format_exc()
    (ROOT / "test-output" / "gpu-smoke.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    bpy.ops.wm.quit_blender()


bpy.app.timers.register(run, first_interval=1.0)
