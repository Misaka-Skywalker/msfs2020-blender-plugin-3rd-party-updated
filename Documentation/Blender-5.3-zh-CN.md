# Blender 5.3 兼容版说明

[English](Blender-5.3.md) · [兼容性与后续升级](../COMPATIBILITY.md)

这是基于官方源码制作的非官方兼容补丁，基于 Asobo Studio 的 Microsoft Flight Simulator 2020 glTF 插件，不代表官方发布。打开或转换原有工程前，请先备份 `.blend` 文件及其相关纹理和资源。

## 安装

1. 在 Blender 的“编辑 > 偏好设置 > 获取扩展”菜单中选择“从磁盘安装”，选择提供的 `io_scene_gltf2_msfs_2020-blender-5.3.zip`。
2. 在插件列表中启用 Microsoft Flight Simulator 2020: glTF Extension，并确保 Blender 内置的 glTF 2.0 导入/导出插件可用并启用。
3. 通过“文件 > 导入/导出 > glTF 2.0”使用 MSFS 扩展；材质和多重导出设置位于相应的属性面板。

## 简体中文界面

内置轻量中文语言包，覆盖 40 个常用 MSFS 界面标签。将 Blender 的界面语言设为简体中文并启用界面翻译后自动生效，切回英文或关闭界面翻译即恢复英文。未覆盖的文本保留原文，MSFS/glTF 字段名和技术标识不变，无单独语言开关。

## 兼容范围

本补丁针对 Blender 5.3 调整 `bgl`/GPU 绘制、Draco 库路径、WebP 导出参数以及节点和图像导入接口。已在 Blender 5.3 中进行实际测试，但尚未通过 MSFS SDK 或游戏验证。代码保留旧版 Blender 的兼容分支，旧版 Blender 尚未实测。

首次公开发布的补丁版本为 **3.3.4**，基于原始 **3.3.2**。MSFS2020 扩展名称、材质属性和 LOD 文件格式保持不变。具体修复还包括扩展开关递归导致的崩溃、清漆权重插槽适配、MASK 透明裁切阈值保留，以及 GLB 嵌入图片的 URI 处理。

验证环境：Windows，Blender **5.3.0**，构建 **02f0899d78e3**。源码运行与最终 ZIP 在隔离配置目录中安装后，均为 **22 项测试通过**。测试覆盖加载与重新启用、碰撞体、全部 17 个材质选项（含 Disabled）的创建及四种透明模式属性、标准材质贴图 glTF/GLB 往返导入、当前和非当前场景的 MSFS 扩展开关、动画、蒙皮与骨骼 ID、灯光导出、LOD XML、多重导出、Draco、WebP 和 ZIP 结构，以及语言切换和翻译清理。另有实际 GPU 绘制与状态恢复测试通过，完整交互视口未逐项验收。

这些是自动生成场景的回归测试；尚未用你的实际工程及 MSFS2020 SDK/游戏做验收。贴图往返测试会出现 Khronos 关于多图像节点共用纹理的采样器提示，来自现有材质节点结构；测试核验了输出贴图和重新导入后的关键参数。

## 已知原版问题（本次未扩改核心逻辑）

- MASK 的导出阈值已正确保留，但 Blender 5.3 视口仍不执行与该阈值一致的硬裁切预览。
- 各向异性、头发、清漆材质的贴图可以往返，但重导入时创建材质类型会将 MASK 透明模式重置为 OPAQUE，需手动核对并恢复。
- 聚光灯导出参数正常，但重导入存在角度单位问题，例如 30° 可能变为 180°，需手动校正。

上述问题经独立审查确认源于原版逻辑。此次按兼容性修改范围保留，并不代表插件所有原有功能已全面修复。

## 测试和打包

在项目根目录的 PowerShell 中执行：

```powershell
& 'C:/Program Files/Blender Foundation/Blender 5.3/5.3/python/bin/python.exe' -m unittest discover -s tests -p test_package.py -v
& 'C:/Program Files/Blender Foundation/Blender 5.3/blender.exe' --background --factory-startup --python-exit-code 1 --python tests/run_blender_tests.py
& 'C:/Program Files/Blender Foundation/Blender 5.3/5.3/python/bin/python.exe' scripts/build_addon.py
```

安装包写入 `dist/io_scene_gltf2_msfs_2020-blender-5.3.zip`，命令同时输出 SHA-256 校验值。源码按 Apache License 2.0 分发，安装包包含许可证。

GPU 测试需要有图形上下文的 Blender 进程，不能加 `--background`：

```powershell
$p = Start-Process -FilePath 'C:/Program Files/Blender Foundation/Blender 5.3/blender.exe' -ArgumentList '--factory-startup','--python','tests/run_gpu_smoke.py' -WindowStyle Hidden -PassThru
$p.WaitForExit()
Get-Content test-output/gpu-smoke.json
```

测试不会保存 Blender 用户偏好，产物位于 `test-output/`。`tests/run_install_smoke.py` 可进一步验证安装包；运行时须将 `BLENDER_USER_SCRIPTS`、`BLENDER_USER_CONFIG`、`BLENDER_USER_EXTENSIONS` 指向 `test-output/` 下的隔离目录，脚本拒绝安装到用户原有配置目录。受限环境下直接运行源码测试，退出时可能出现无法写入用户扩展缓存的提示。
