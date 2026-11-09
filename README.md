# ETC TriangleCenter 数据维护

在此工作区解析 Encyclopedia of Triangle Centers，审阅几何定义，生成 GeoGebra 扩展点配方。

## 维护与构建

从本工作区根目录运行。已迁入 Part 1–37 源页和原生采样数据，可直接离线运行。

~~~sh
python -m pip install -r requirements.txt
python tools/triangle_center_import.py build
python tools/triangle_center_import.py verify
python -m unittest discover -s tools -p 'test_*.py'
~~~

- [tools/README.md](tools/README.md) 记录导入语法、参数、诊断和审阅方法。用 `python tools/triangle_center_import.py fetch --parts N` 更新指定 ETC 源页。
- `data/` 保存维护输入和生成的 `chunks/`。人工定义与排除在 `seeds.txt`，坐标锚点优先级在 `coordinate-priority.txt`。
- `.cache/triangle-centers/` 保存本地源页、原生 atlas 和分析资料。归档的实验和报告保留当时的路径与 Git 引用。部分历史对比脚本需要在主页的对应 Git 历史上运行。
- [ETC 源数据勘误表](docs/etc-source-errata.md) 按类型汇总网页错误、格式问题及本库处理。
- [覆盖与未决条目](docs/triangle-centers-uncovered.md)、[源定义复核](docs/triangle-centers-source-review.md) 和 [配方库演进](docs/catalogue-history.md) 记录分析历史。

GeoGebra 原生行为变化时，在主页开发服务器打开
`/scripts/geogebra/browser/verification.html?page=center-anchors`，
将下载的 atlas 保存到 `.cache/triangle-centers/native/native-atlas.json`。
需要更新原生方向时，运行 `python tools/triangle_center_import.py native`。

## 同步主页

构建完成后，把 `data/chunks/` 整个目录和 `data/` 下的
`native-patches.txt`、`native-status.txt`、`gemini-triangles.txt` 一起同步到主页
`src/features/geogebra/commands/custom/data/triangle-centers/`。
完整替换分块目录可以同时移除过期分块。
