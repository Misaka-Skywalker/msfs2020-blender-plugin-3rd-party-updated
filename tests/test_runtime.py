import unittest

import addon_utils
import bpy


class RuntimeTests(unittest.TestCase):
    def test_extension_switch_stays_synchronized_without_recursion(self):
        scene = bpy.context.scene
        scene.msfs_exporter_settings.enable_msfs_extension = False
        self.assertFalse(scene.msfs_multi_exporter_settings.enable_msfs_extension)
        scene.msfs_multi_exporter_settings.enable_msfs_extension = True
        self.assertTrue(scene.msfs_exporter_settings.enable_msfs_extension)

    def test_inactive_scene_switch_does_not_change_active_scene(self):
        active = bpy.context.scene
        active.msfs_exporter_settings.enable_msfs_extension = True
        inactive = bpy.data.scenes.new("Inactive extension settings")
        self.addCleanup(bpy.data.scenes.remove, inactive)
        inactive.msfs_exporter_settings.enable_msfs_extension = False
        self.assertFalse(inactive.msfs_multi_exporter_settings.enable_msfs_extension)
        self.assertTrue(active.msfs_exporter_settings.enable_msfs_extension)
        self.assertTrue(active.msfs_multi_exporter_settings.enable_msfs_extension)
        inactive.msfs_multi_exporter_settings.enable_msfs_extension = True
        self.assertTrue(inactive.msfs_exporter_settings.enable_msfs_extension)
        inactive.msfs_multi_exporter_settings.enable_msfs_extension = False
        self.assertFalse(inactive.msfs_exporter_settings.enable_msfs_extension)
        self.assertTrue(active.msfs_exporter_settings.enable_msfs_extension)
        self.assertTrue(active.msfs_multi_exporter_settings.enable_msfs_extension)

    def test_collision_gizmos_can_be_created(self):
        for kind in ("sphere", "box", "cylinder"):
            bpy.ops.object.select_all(action="DESELECT")
            result = bpy.ops.msfs_collision_gizmo.add_gizmo(msfs_gizmo_type=kind)
            self.assertEqual(result, {"FINISHED"})
            self.assertEqual(bpy.context.object.msfs_gizmo_type, kind)

    def test_z_addon_can_be_disabled_and_enabled_again(self):
        addon_utils.disable("io_scene_gltf2_msfs_2020", default_set=True)
        self.assertFalse(hasattr(bpy.types.Scene, "msfs_exporter_settings"))
        addon_utils.enable("io_scene_gltf2_msfs_2020", default_set=True)
        self.assertTrue(hasattr(bpy.types.Scene, "msfs_exporter_settings"))
        self.assertTrue(hasattr(bpy.context.scene, "msfs_multi_exporter_settings"))
