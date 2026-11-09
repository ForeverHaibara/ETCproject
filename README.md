# ETC Triangle Centers / ETC 三角形中心

[中文](#zh) · [English](#en) · [复现命令 / Commands](#commands) · 勘误表 / Errata [中文](docs/etc-source-errata.md) · [English](docs/etc-source-errata.en.md)

<a id="zh"></a>

[https://foreverhaibara.github.io/#/geogebra](https://foreverhaibara.github.io/#/geogebra)

## 中文

本仓库把《Encyclopedia of Triangle Centers》（ETC）Part 1–37 的几何关系和坐标转换为 GeoGebra 可用的构造配方。导入器读取网页、应用已审阅的修正、筛选候选并检查依赖，再按编号分块。当前提交的 **70,213 条记录**包含 14 条 GeoGebra 原生覆盖配方，也包含理想点状态。

### 从哪里读起

- [生成数据](data/chunks/)保存构造和理想点记录。例如 `4201 J 2 3 8 38` 表示 `X(4201)` 是直线 `X(2)X(3)` 与 `X(8)X(38)` 的交点。[分块语法](docs/chunks-syntax.en.md)解释了分块的格式。
- [人工配方](data/seeds.txt)记录审阅后采用的构造、明确排除和定义域。另有[原生覆盖](data/native-patches.txt)、[原生状态](data/native-status.txt)和[共享 Gemini 模板](data/gemini-triangles.txt)。
- [勘误表](docs/etc-source-errata.md)按类型区分源错误、待核实冲突和本地实现问题。

### 如何复现

1. 从仓库根目录安装依赖并运行 `verify`。新克隆即可检查已提交配方的依赖与类型，预期输出 `Valid: 70213 recipes`。
2. 完整复现需要原 ETC 快照 `.cache/triangle-centers/sources/ETCPart1.html` 至 `ETCPart37.html`，以及 GeoGebra 原生坐标采样 `.cache/triangle-centers/native/native-atlas.json`。两者均在 Git 忽略的目录下，需单独取得。`fetch` 下载当前网页，内容可能与原快照不同。原生采样可通过配套 GeoGebra 站点的 `/scripts/geogebra/browser/verification.html?page=center-anchors` 导出，历史采样使用 5.4.920.0。
3. 有上述输入后，运行 `check` 离线重算并与提交的分块逐文件比较。需要写回分块时运行 `build`。可选的完整 Python 测试还需要 `.cache/triangle-centers/gemini-triangle.html`。

<a id="en"></a>

## English

This repository converts geometry and coordinates from Parts 1–37 of the *Encyclopedia of Triangle Centers* (ETC) into GeoGebra construction recipes. The importer reads the source pages, applies reviewed corrections, and screens candidates and their dependencies before grouping the results by ID. The checked-in catalogue has **70,213 records**, including 14 GeoGebra native overrides and records for ideal points.

### Where to start

- [Generated data](data/chunks/) contains constructions and ideal-point records. For example, `4201 J 2 3 8 38` defines `X(4201)` as the intersection of `X(2)X(3)` and `X(8)X(38)`. See [chunk syntax](docs/chunks-syntax.en.md) for details.
- [Reviewed seeds](data/seeds.txt) record constructions, explicit exclusions, and domain decisions. See also the [native overrides](data/native-patches.txt), [native status](data/native-status.txt), and [shared Gemini templates](data/gemini-triangles.txt).
- The [errata](docs/etc-source-errata.en.md) separates source errors, unresolved conflicts, and local implementation issues.

### Reproduce the catalogue

1. Install the dependencies and run `verify` from the repository root. A fresh clone has the data needed to check dependencies and types. Expect `Valid: 70213 recipes`.
2. A full reproduction requires the original ETC snapshots `.cache/triangle-centers/sources/ETCPart1.html` through `ETCPart37.html` and the GeoGebra coordinate samples in `.cache/triangle-centers/native/native-atlas.json`. Obtain both separately, since Git ignores the cache. `fetch` downloads the current pages, which may differ from the original snapshots. Export the coordinate samples from `/scripts/geogebra/browser/verification.html?page=center-anchors` on the companion GeoGebra site. The historical samples used version 5.4.920.0.
3. With those inputs, run `check` to regenerate offline and compare each chunk against the checked-in data. Use `build` to write the chunks. The optional full Python test suite also requires `.cache/triangle-centers/gemini-triangle.html`.

<a id="commands"></a>

## 复现命令 / Commands

**1. 安装与校验 / Install and verify**

```sh
python -m pip install -r requirements.txt
python tools/triangle_center_import.py verify
```

**2. 可选，获取当前网页到本地缓存 / Optional, fetch current pages into the local cache**

```sh
python tools/triangle_center_import.py fetch
```

**3. 以已有输入复算并比较 / Recompute and compare using local inputs**

```sh
python tools/triangle_center_import.py check
```

**可选，写回分块或运行测试 / Optional, write chunks or run tests**

```sh
python tools/triangle_center_import.py build
python -m unittest discover -s tools -p 'test_*.py'
```
