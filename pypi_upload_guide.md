# PyPI 上传指南

本文档详细说明如何将 bili-downloader 包上传到 PyPI。

## 📋 准备工作

### 1. 注册 PyPI 账号

首先需要在 PyPI 上注册账号：
- 访问: https://pypi.org/account/register/
- 完成注册并验证邮箱

### 2. 安装必要的工具

```bash
pip install --upgrade pip setuptools wheel twine
```

### 3. 配置 API Token (推荐)

在 PyPI 账号设置中生成 API Token:
1. 登录 PyPI
2. 进入 Account Settings → API tokens
3. 创建新的 token，选择整个账户范围
4. 复制 token

配置 token 到本地环境:
```bash
# 创建或编辑 ~/.pypirc
[pypi]
username = __token__
password = pypi-你的token字符串
```

## 🚀 打包和上传步骤

### 步骤 1: 检查项目结构

确保项目包含以下文件:
```
bili-downloader/
├── setup.py
├── pyproject.toml
├── MANIFEST.in
├── README.md
├── README_PYPI.md
├── requirements.txt
├── __init__.py
├── main.py
├── config/
│   └── config.json
├── modules/
│   ├── __init__.py
│   ├── login_manager.py
│   ├── video_info.py
│   ├── stream_downloader.py
│   └── ffmpeg_integration.py
└── utils/
    ├── __init__.py
    └── common_utils.py
```

### 步骤 2: 更新版本号

在发布新版本前，更新版本号：

**setup.py:**
```python
version="1.0.0"  # 更新版本号
```

**pyproject.toml:**
```toml
version = "1.0.0"  # 更新版本号
```

**__init__.py:**
```python
__version__ = "1.0.0"  # 更新版本号
```

### 步骤 3: 构建包

```bash
# 清理旧的构建文件
rm -rf build/ dist/ *.egg-info/

# 构建源码包和wheel包
python setup.py sdist bdist_wheel

# 或者使用现代构建方式
python -m build
```

### 步骤 4: 检查包内容

```bash
# 检查打包的文件
tar -tzf dist/bili-downloader-1.0.0.tar.gz

# 检查wheel包内容
unzip -l dist/bili_downloader-1.0.0-py3-none-any.whl
```

### 步骤 5: 测试上传到 TestPyPI

```bash
# 上传到 TestPyPI
python -m twine upload --repository testpypi dist/*

# 从 TestPyPI 安装测试
pip install --index-url https://test.pypi.org/simple/ bili-downloader
```

### 步骤 6: 正式上传到 PyPI

```bash
# 上传到正式 PyPI
python -m twine upload dist/*

# 或者使用配置的 token
python -m twine upload --repository pypi dist/*
```

## 🔧 常见问题解决

### 错误: 包名已存在

如果包名 `bili-downloader` 已被占用，需要修改包名：

**setup.py:**
```python
name="your-unique-package-name"
```

**pyproject.toml:**
```toml
name = "your-unique-package-name"
```

### 错误: 缺少依赖文件

确保 `MANIFEST.in` 包含所有必要文件:
```
include LICENSE
include README.md
include requirements.txt
include config/*.json
recursive-include config *.json
```

### 错误: 版本冲突

如果版本已存在，需要更新版本号:
```bash
# 更新为 1.0.0
sed -i 's/version="1.0.0"/version="1.0.0"/' setup.py
sed -i 's/version = "1.0.0"/version = "1.0.0"/' pyproject.toml
```

## 📊 版本管理规范

### 版本号格式: `主版本.次版本.修订版本`

- **主版本**: 不兼容的API修改
- **次版本**: 向后兼容的功能性新增
- **修订版本**: 向后兼容的问题修正

### 发布流程

1. 开发新功能 → 提交到 `develop` 分支
2. 测试通过 → 合并到 `main` 分支
3. 更新版本号 → 创建 git tag
4. 构建包 → 上传到 PyPI
5. 更新文档 → 发布 Release

## 🎯 最佳实践

### 1. 自动化发布

创建发布脚本 `scripts/release.sh`:
```bash
#!/bin/bash
set -e

# 更新版本号
VERSION=$1
sed -i "s/version=\".*\"/version=\"$VERSION\"/" setup.py
sed -i "s/version = \".*\"/version = \"$VERSION\"/" pyproject.toml
sed -i "s/__version__ = \".*\"/__version__ = \"$VERSION\"/" __init__.py

# 构建包
python -m build

# 上传到 PyPI
python -m twine upload dist/*

# 创建 git tag
git add .
git commit -m "Release version $VERSION"
git tag -a "v$VERSION" -m "Version $VERSION"
git push origin main --tags
```

### 2. CI/CD 集成

使用 GitHub Actions 自动化发布:

创建 `.github/workflows/publish.yml`:
```yaml
name: Publish Python Package

on:
  release:
    types: [created]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.x'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install setuptools wheel twine
    - name: Build package
      run: |
        python -m build
    - name: Publish package
      uses: pypa/gh-action-pypi-publish@release/v1
      with:
        password: ${{ secrets.PYPI_API_TOKEN }}
```

## 📝 发布检查清单

- [ ] 更新版本号
- [ ] 更新 CHANGELOG.md
- [ ] 测试本地安装
- [ ] 构建包并检查内容
- [ ] 测试上传到 TestPyPI
- [ ] 正式上传到 PyPI
- [ ] 创建 git tag
- [ ] 更新文档

## 🔗 有用链接

- [PyPI 文档](https://packaging.python.org/)
- [setuptools 文档](https://setuptools.pypa.io/)
- [twine 文档](https://twine.readthedocs.io/)
- [Python 打包指南](https://packaging.python.org/tutorials/packaging-projects/)

---

祝您发布顺利！🎉
