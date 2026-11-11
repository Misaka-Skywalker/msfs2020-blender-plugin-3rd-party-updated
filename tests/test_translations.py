import unittest

import addon_utils
import bpy


ADDON_NAME = "io_scene_gltf2_msfs_2020"


class TranslationTests(unittest.TestCase):
    def setUp(self):
        self.view = bpy.context.preferences.view
        self.addCleanup(setattr, self.view, "language", self.view.language)
        self.addCleanup(setattr, self.view, "use_translate_interface", self.view.use_translate_interface)
        self.view.use_translate_interface = True
        languages = self.view.bl_rna.properties["language"].enum_items
        self.view.language = "zh_HANS" if "zh_HANS" in languages else "zh_CN"

    def test_interface_follows_language_and_translation_preference(self):
        gettext = bpy.app.translations.pgettext_iface
        label = "MSFS2020 Material Params"
        operator = bpy.ops.export_scene.multi_export_gltf.get_rna_type()
        self.assertEqual(gettext(label), "MSFS 2020 材质参数")
        self.assertEqual(gettext(operator.name, operator.translation_context), "批量导出 glTF 2.0")

        self.view.use_translate_interface = False
        self.assertEqual(gettext(label), label)
        self.view.use_translate_interface = True
        self.view.language = "en_US"
        self.assertEqual(gettext(label), label)
        self.assertEqual(gettext(operator.name, operator.translation_context), operator.name)

    def test_addon_disable_unregisters_translation_catalog(self):
        gettext = bpy.app.translations.pgettext_iface
        label = "MSFS2020 Properties"
        self.assertEqual(gettext(label), "MSFS 2020 属性")
        addon_utils.disable(ADDON_NAME, default_set=True)
        try:
            self.assertEqual(gettext(label), label)
        finally:
            addon_utils.enable(ADDON_NAME, default_set=True)
        self.assertEqual(gettext(label), "MSFS 2020 属性")
