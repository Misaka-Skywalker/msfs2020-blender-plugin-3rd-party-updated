import json
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

import bpy

from io_scene_gltf2_msfs_2020.io.msfs_multi_export import MSFS2020_OT_MultiExportGLTF2

OUTPUT = Path(__file__).resolve().parents[1] / "test-output"


class ExportTests(unittest.TestCase):
    def setUp(self):
        if bpy.context.object and bpy.context.object.mode != "OBJECT":
            bpy.ops.object.mode_set(mode="OBJECT")
        for obj in list(bpy.data.objects):
            bpy.data.objects.remove(obj, do_unlink=True)
        bpy.context.scene.msfs_exporter_settings.enable_msfs_extension = True
        bpy.context.scene.msfs_exporter_settings.use_unique_id = True
        bpy.ops.mesh.primitive_cube_add()
        self.obj = bpy.context.object
        self.obj.name = "TestModel"
        material = bpy.data.materials.new("TestMaterial")
        material.msfs_material_type = "msfs_standard"
        self.obj.data.materials.append(material)
        self.path = OUTPUT / (self._testMethodName + ".gltf")

    def export(self, **kwargs):
        result = bpy.ops.export_scene.gltf(filepath=str(self.path), export_format="GLTF_SEPARATE", **kwargs)
        self.assertEqual(result, {"FINISHED"})
        return json.loads(self.path.read_text(encoding="utf-8"))

    def test_standard_export_preserves_asobo_data(self):
        self.obj.msfs_override_unique_id = True
        self.obj.msfs_unique_id = "custom-id"
        data = self.export()
        self.assertEqual(data["asset"]["extensions"]["ASOBO_normal_map_convention"], {"tangent_space_convention": "DirectX"})
        node = next(n for n in data["nodes"] if n["name"] == "TestModel")
        self.assertEqual(node["extensions"]["ASOBO_unique_id"]["id"], "custom-id")
        self.assertGreater(len(data["meshes"][0]["primitives"]), 0)

    def test_disabling_extension_exports_plain_gltf(self):
        bpy.context.scene.msfs_exporter_settings.enable_msfs_extension = False
        data = self.export()
        self.assertFalse(any(n.startswith("ASOBO_") for n in data.get("extensionsUsed", [])))

    def test_batch_export_uses_current_operator_options(self):
        MSFS2020_OT_MultiExportGLTF2.export(str(self.path))
        data = json.loads(self.path.read_text(encoding="utf-8"))
        self.assertIn("ASOBO_normal_map_convention", data["asset"]["extensions"])
        self.assertTrue(self.path.with_suffix(".bin").is_file())

    def test_plain_batch_webp_settings_preserve_compressed_texture(self):
        settings = bpy.context.scene.msfs_multi_exporter_settings
        settings.enable_msfs_extension = False
        settings.export_image_add_webp = True
        settings.export_image_webp_fallback = True
        self.addCleanup(setattr, settings, "export_image_add_webp", False)
        self.addCleanup(setattr, settings, "export_image_webp_fallback", False)
        material = self.obj.data.materials[0]
        material.msfs_material_type = "NONE"
        material.use_nodes = True
        image = bpy.data.images.new("BatchWebP", 4, 4)
        image.generated_color = (0.25, 0.5, 0.75, 1)
        image.filepath_raw = str(OUTPUT / "batch-webp-source.png")
        image.file_format = "PNG"
        image.save()
        image.source = "FILE"
        texture = material.node_tree.nodes.new("ShaderNodeTexImage")
        texture.image = image
        shader = next(node for node in material.node_tree.nodes if node.type == "BSDF_PRINCIPLED")
        material.node_tree.links.new(texture.outputs["Color"], shader.inputs["Base Color"])
        MSFS2020_OT_MultiExportGLTF2.export(str(self.path))
        data = json.loads(self.path.read_text(encoding="utf-8"))
        self.assertIn("EXT_texture_webp", data["extensionsUsed"])
        self.assertTrue(any(i.get("uri", "").endswith(".webp") for i in data["images"]))
        self.assertTrue(any(i.get("uri", "").endswith(".png") for i in data["images"]))

    def test_batch_draco_compression_remains_available(self):
        settings = bpy.context.scene.msfs_multi_exporter_settings
        settings.export_draco_mesh_compression_enable = True
        self.addCleanup(setattr, settings, "export_draco_mesh_compression_enable", False)
        MSFS2020_OT_MultiExportGLTF2.export(str(self.path))
        data = json.loads(self.path.read_text(encoding="utf-8"))
        self.assertIn("KHR_draco_mesh_compression", data["meshes"][0]["primitives"][0]["extensions"])

    def test_lod_batch_writes_models_and_xml(self):
        scene = bpy.context.scene
        scene.msfs_multi_exporter_current_tab = "OBJECTS"
        scene.multi_exporter_grouped_by_collections = False
        scene.msfs_multi_exporter_lod_groups.clear()
        group = scene.msfs_multi_exporter_lod_groups.add()
        group.group_name = "TestLOD"
        group.folder_path = str(OUTPUT)
        group.generate_xml = True
        for index, size in enumerate((80, 0)):
            lod = group.lods.add()
            lod.objectLOD = self.obj
            lod.enabled = True
            lod.file_name = "TestLOD_LOD0" + str(index)
            lod.lod_value = size
        self.assertEqual(bpy.ops.export_scene.multi_export_gltf(), {"FINISHED"})
        lods = ET.parse(OUTPUT / "TestLOD.xml").getroot().findall("LODS/LOD")
        self.assertEqual([lod.attrib["ModelFile"] for lod in lods], ["TestLOD_LOD00.gltf", "TestLOD_LOD01.gltf"])
        for lod in lods:
            data = json.loads((OUTPUT / lod.attrib["ModelFile"]).read_text())
            self.assertIn("meshes", data)

    def test_collision_extensions_export_and_import(self):
        for kind in ("sphere", "box", "cylinder"):
            bpy.ops.object.select_all(action="DESELECT")
            self.obj.select_set(True)
            bpy.context.view_layer.objects.active = self.obj
            bpy.ops.msfs_collision_gizmo.add_gizmo(msfs_gizmo_type=kind)
        data = self.export()
        collisions = data["meshes"][0]["extensions"]["ASOBO_gizmo_object"]["gizmo_objects"]
        self.assertEqual({c["type"] for c in collisions}, {"sphere", "box", "cylinder"})
        bpy.ops.object.select_all(action="SELECT")
        bpy.ops.object.delete(use_global=False)
        self.assertEqual(bpy.ops.import_scene.gltf(filepath=str(self.path)), {"FINISHED"})
        self.assertEqual({o.msfs_gizmo_type for o in bpy.context.scene.objects if o.type == "EMPTY"}, {"sphere", "box", "cylinder"})

    def test_light_exports_asobo_parameters(self):
        bpy.ops.object.light_add(type="SPOT")
        light = bpy.context.object
        light.name = "TestSpot"
        light.data.energy = 123
        light.msfs_light_flash_frequency = 2.5
        data = self.export(export_lights=True)
        node = next(n for n in data["nodes"] if n["name"] == "TestSpot")
        ext = node["extensions"]["ASOBO_macro_light"]
        self.assertAlmostEqual(ext["intensity"], 123)
        self.assertAlmostEqual(ext["flash_frequency"], 2.5)

    def test_object_animation_is_exported(self):
        self.obj.location.x = 0
        self.obj.keyframe_insert(data_path="location", frame=1)
        self.obj.location.x = 2
        self.obj.keyframe_insert(data_path="location", frame=10)
        data = self.export(export_animations=True, export_animation_mode="ACTIONS")
        self.assertTrue(data["animations"])
        self.assertTrue(any(c["target"]["path"] == "translation" for a in data["animations"] for c in a["channels"]))

    def test_skin_and_joint_unique_ids_export(self):
        mesh = self.obj
        bpy.ops.object.armature_add()
        rig = bpy.context.object
        rig.name = "TestRig"
        mesh.parent = rig
        modifier = mesh.modifiers.new("Armature", "ARMATURE")
        modifier.object = rig
        mesh.vertex_groups.new(name="Bone").add(list(range(len(mesh.data.vertices))), 1.0, "REPLACE")
        data = self.export(export_skins=True)
        self.assertTrue(data["skins"])
        joint = data["nodes"][data["skins"][0]["joints"][0]]
        self.assertEqual(joint["extensions"]["ASOBO_unique_id"]["id"], "Bone")
