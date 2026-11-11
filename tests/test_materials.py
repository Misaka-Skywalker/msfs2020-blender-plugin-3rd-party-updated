import contextlib
import io
import json
from pathlib import Path
import struct
import tempfile
import unittest
from unittest.mock import patch

import bpy


class MaterialTests(unittest.TestCase):
    def setUp(self):
        self.errors = io.StringIO()
        self.enterContext(contextlib.redirect_stderr(self.errors))

    def tearDown(self):
        self.assertNotIn("Traceback", self.errors.getvalue(), self.errors.getvalue())

    def new_material(self, kind):
        material = bpy.data.materials.new("Test " + kind)
        self.addCleanup(bpy.data.materials.remove, material)
        material.msfs_material_type = kind
        return material

    def new_image(self, name):
        image = bpy.data.images.new(name, 4, 4)
        self.addCleanup(bpy.data.images.remove, image)
        image.generated_color = (0.3, 0.4, 0.5, 0.8)
        return image

    def test_material_kinds_and_alpha_modes(self):
        settings = bpy.types.Material.bl_rna.properties["msfs_material_type"]
        for item in settings.enum_items:
            with self.subTest(kind=item.identifier):
                material = self.new_material(item.identifier)
                nodes = material.node_tree.nodes
                output = next(node for node in nodes if node.type == "OUTPUT_MATERIAL")
                self.assertTrue(output.inputs["Surface"].is_linked)
                for mode, render_method in (
                    ("OPAQUE", "DITHERED"),
                    ("MASK", "DITHERED"),
                    ("BLEND", "BLENDED"),
                    ("DITHER", "DITHERED"),
                ):
                    material.msfs_alpha_mode = mode
                    self.assertEqual(material.surface_render_method, render_method)

    def test_anisotropic_and_hair_use_red_and_blue_texture_channels(self):
        for kind in ("msfs_anisotropic", "msfs_hair"):
            with self.subTest(kind=kind):
                material = self.new_material(kind)
                material.msfs_extra_slot1_texture = self.new_image("Anisotropy")
                shader = material.node_tree.nodes["Principled BSDF"]
                self.assertTrue(shader.inputs["Anisotropic"].is_linked)
                self.assertTrue(shader.inputs["Anisotropic Rotation"].is_linked)
                self.assertEqual(shader.inputs["Anisotropic"].links[0].from_socket.name, "Red")
                self.assertEqual(shader.inputs["Anisotropic Rotation"].links[0].from_socket.name, "Blue")

    def test_clearcoat_dirt_uses_weight_and_roughness_inputs(self):
        material = self.new_material("msfs_clearcoat")
        material.msfs_dirt_texture = self.new_image("Coat Dirt")
        shader = material.node_tree.nodes["Principled BSDF"]
        self.assertTrue(shader.inputs["Coat Weight"].is_linked)
        self.assertTrue(shader.inputs["Coat Roughness"].is_linked)
        self.assertEqual(shader.inputs["Coat Weight"].links[0].from_socket.name, "Red")
        self.assertEqual(shader.inputs["Coat Roughness"].links[0].from_socket.name, "Green")

    def test_external_textures_roundtrip(self):
        self.check_textured_material_roundtrip("GLTF_SEPARATE", "material.gltf")

    def test_embedded_textures_roundtrip(self):
        self.check_textured_material_roundtrip("GLB", "material.glb")

    def check_textured_material_roundtrip(self, export_format, filename):
        test_output = Path(__file__).resolve().parents[1] / "test-output"
        directory = self.enterContext(tempfile.TemporaryDirectory(dir=test_output))
        self.enterContext(patch.object(tempfile, "tempdir", directory))
        filepath = Path(directory) / filename
        material = self.new_material("msfs_standard")
        material.msfs_base_color_factor = (0.25, 0.5, 0.75, 0.8)
        material.msfs_detail_uv_scale = 2.5
        material.msfs_detail_normal_scale = 0.6
        material.msfs_alpha_mode = "MASK"
        material.msfs_alpha_cutoff = 0.35
        color_image = self.new_image("Base Color")
        if export_format == "GLTF_SEPARATE":
            color_image.filepath_raw = str(filepath.parent / "source-color.png")
            color_image.file_format = "PNG"
            color_image.save()
            color_image.source = "FILE"
        material.msfs_base_color_texture = color_image
        material.msfs_detail_normal_texture = self.new_image("Detail Normal")
        nodes_before = set(material.node_tree.nodes.keys())

        bpy.ops.mesh.primitive_plane_add()
        plane = bpy.context.object
        plane.data.materials.append(material)
        self.addCleanup(bpy.data.meshes.remove, plane.data)
        self.addCleanup(bpy.data.objects.remove, plane, do_unlink=True)
        result = bpy.ops.export_scene.gltf(
            filepath=str(filepath), export_format=export_format, use_selection=True,
        )
        self.assertEqual(result, {"FINISHED"})
        self.assertEqual(set(material.node_tree.nodes.keys()), nodes_before)
        if export_format == "GLB":
            glb = filepath.read_bytes()
            length, chunk_type = struct.unpack_from("<I4s", glb, offset=12)
            self.assertEqual(chunk_type, b"JSON")
            data = json.loads(glb[20:20 + length])
        else:
            data = json.loads(filepath.read_text(encoding="utf-8"))
        exported = data["materials"][0]
        detail = exported["extensions"]["ASOBO_material_detail_map"]
        self.assertEqual(detail["UVScale"], 2.5)
        self.assertAlmostEqual(detail["detailNormalTexture"]["scale"], 0.6)
        image_index = data["textures"][detail["detailNormalTexture"]["index"]]["source"]
        image = data["images"][image_index]
        if export_format == "GLB":
            self.assertIn("bufferView", image)
        else:
            self.assertTrue((filepath.parent / image["uri"]).is_file())
        self.assertEqual(exported["alphaMode"], "MASK")
        with self.subTest("exported alpha cutoff"):
            self.assertAlmostEqual(exported.get("alphaCutoff", 0.5), 0.35)

        existing_objects = set(bpy.data.objects)
        existing_meshes = set(bpy.data.meshes)
        existing_materials = set(bpy.data.materials)
        existing_images = set(bpy.data.images)
        result = bpy.ops.import_scene.gltf(filepath=str(filepath))
        for collection, previous in (
            (bpy.data.images, existing_images),
            (bpy.data.materials, existing_materials),
            (bpy.data.meshes, existing_meshes),
            (bpy.data.objects, existing_objects),
        ):
            for item in set(collection) - previous:
                self.addCleanup(collection.remove, item, do_unlink=True)
        self.assertEqual(result, {"FINISHED"})
        imported, = set(bpy.data.materials) - existing_materials
        self.assertEqual(imported.msfs_material_type, "msfs_standard")
        self.assertEqual(imported.msfs_alpha_mode, "MASK")
        with self.subTest("imported alpha cutoff"):
            self.assertAlmostEqual(imported.msfs_alpha_cutoff, 0.35)
        self.assertIsNotNone(imported.msfs_base_color_texture)
        self.assertIsNotNone(imported.msfs_detail_normal_texture)
        self.assertAlmostEqual(imported.msfs_detail_normal_scale, 0.6)
