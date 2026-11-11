# Copyright 2026 The MSFS2020 Blender Plugin - 3rd Party Updated contributors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import bpy


DEFAULT_CONTEXT = bpy.app.translations.contexts.default
OPERATOR_CONTEXT = bpy.app.translations.contexts.operator_default

SIMPLIFIED_CHINESE = {
    # MSFS panels, extensions and collision controls.
    (DEFAULT_CONTEXT, "Microsoft Flight Simulator 2020 Extensions"): "Microsoft Flight Simulator 2020 扩展",
    (DEFAULT_CONTEXT, "Enable MSFS2020 glTF import extensions"): "启用 MSFS 2020 glTF 导入扩展",
    (DEFAULT_CONTEXT, "Enable MSFS2020 glTF export extensions"): "启用 MSFS 2020 glTF 导出扩展",
    (DEFAULT_CONTEXT, "MSFS2020 Properties"): "MSFS 2020 属性",
    (DEFAULT_CONTEXT, "MSFS2020 Material Params"): "MSFS 2020 材质参数",
    (DEFAULT_CONTEXT, "MSFS2020 Light Parameters"): "MSFS 2020 灯光参数",
    (DEFAULT_CONTEXT, "MSFS2020 Collision Parameters"): "MSFS 2020 碰撞参数",
    (DEFAULT_CONTEXT, "Microsoft Flight Simulator 2020 Collision"): "Microsoft Flight Simulator 2020 碰撞体",
    (DEFAULT_CONTEXT, "Sphere Collision Gizmo"): "球形碰撞体",
    (DEFAULT_CONTEXT, "Box Collision Gizmo"): "盒形碰撞体",
    (DEFAULT_CONTEXT, "Cylinder Collision Gizmo"): "圆柱形碰撞体",
    (DEFAULT_CONTEXT, "Road Collider"): "道路碰撞体",
    (OPERATOR_CONTEXT, "Add MSFS2020 Collision Gizmo"): "添加 MSFS 2020 碰撞体",

    # Export and LOD settings.
    (DEFAULT_CONTEXT, "Multi-Export glTF 2.0"): "批量导出 glTF 2.0",
    (OPERATOR_CONTEXT, "Multi-Export glTF 2.0"): "批量导出 glTF 2.0",
    (DEFAULT_CONTEXT, "Use ASOBO Unique ID"): "使用 ASOBO 唯一 ID",
    (DEFAULT_CONTEXT, "Use ASOBO Unique ID Extension"): "使用 ASOBO 唯一 ID 扩展",
    (DEFAULT_CONTEXT, "Use ASOBO Unique ID extension for nodes"): "为节点使用 ASOBO 唯一 ID 扩展",
    (DEFAULT_CONTEXT, "Enable ASOBO Unique ID extension"): "启用 ASOBO 唯一 ID 扩展",
    (DEFAULT_CONTEXT, "Override Unique ID"): "覆盖唯一 ID",
    (DEFAULT_CONTEXT, "No LODs found in scene"): "场景中未找到 LOD",
    (DEFAULT_CONTEXT, "LOD Value"): "LOD 阈值",
    (DEFAULT_CONTEXT, "Generate XML"): "生成 XML",
    (DEFAULT_CONTEXT, "Overwrite GUID"): "覆盖 GUID",
    (OPERATOR_CONTEXT, "Reload LOD groups"): "重新加载 LOD 组",
    (OPERATOR_CONTEXT, "Reload LODs"): "重新加载 LOD",

    # MSFS material types and parameters.
    (OPERATOR_CONTEXT, "Migrate Material Data"): "迁移材质数据",
    (DEFAULT_CONTEXT, "Geo Decal Frosted"): "磨砂几何贴花",
    (DEFAULT_CONTEXT, "Fake Terrain"): "模拟地形",
    (DEFAULT_CONTEXT, "Fresnel Fade"): "菲涅耳渐隐",
    (DEFAULT_CONTEXT, "Environment Occluder"): "环境遮挡体",
    (DEFAULT_CONTEXT, "Collision Material"): "碰撞材质",
    (DEFAULT_CONTEXT, "Road Collision Material"): "道路碰撞材质",
    (DEFAULT_CONTEXT, "Draw Order Offset"): "绘制顺序偏移",
    (DEFAULT_CONTEXT, "Detail UV Scale"): "细节 UV 缩放",
    (DEFAULT_CONTEXT, "Detail UV Offset U"): "细节 UV 偏移 U",
    (DEFAULT_CONTEXT, "Detail UV Offset V"): "细节 UV 偏移 V",
    (DEFAULT_CONTEXT, "Detail Normal Scale"): "细节法线强度",
    (DEFAULT_CONTEXT, "Rain Drop Scale"): "雨滴缩放",
    (DEFAULT_CONTEXT, "Glass Reflection Mask Factor"): "玻璃反射遮罩系数",
    (DEFAULT_CONTEXT, "Glass Deformation Factor"): "玻璃变形系数",
}


def register():
    bpy.app.translations.register(__name__, {
        "zh_HANS": SIMPLIFIED_CHINESE,
        "zh_CN": SIMPLIFIED_CHINESE,
    })


def unregister():
    bpy.app.translations.unregister(__name__)
