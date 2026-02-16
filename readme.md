Camera Grid App - 安卓横屏相机格子应用
应用功能
8行x50列数据网格
可视区域显示4行，默认显示第3-6行
上下滑动每次移动一整行（离散滑动）
格子宽度=高度×2，支持左右连续滑动
相机预览功能
拍照计数功能
打包方法
方法一：本地打包（推荐 Ubuntu 22.04）
1. 安装依赖
bash

sudo apt update
sudo apt install -y git zip unzip openjdk-17-jdk python3.11 python3.11-venv python3-pip build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev curl wget llvm libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev

# 设置 Python 3.11 为默认
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1
2. 安装 Buildozer
bash

pip3 install --user buildozer cython
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
3. 打包 APK
bash

cd camera-grid-app
buildozer android debug
打包完成后，APK 文件位于 bin/ 目录下。

方法二：使用 Docker
bash

# 拉取 buildozer 镜像
docker pull kivy/buildozer

# 在项目目录下运行
docker run --rm -v "$PWD":/home/user/hostcwd kivy/buildozer android debug
方法三：使用 GitHub Actions（最简单）
将此项目上传到 GitHub 仓库
创建 .github/workflows/build.yml 文件：
yaml

name: Build Android APK

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Build with Buildozer
      uses: ArtemSBulgakov/buildozer-action@v1
      id: buildozer
      with:
        workdir: .
        buildozer_version: stable
    
    - name: Upload APK
      uses: actions/upload-artifact@v4
      with:
        name: camera-grid-app
        path: ${{ steps.buildozer.outputs.filename }}
推送代码后，GitHub Actions 会自动构建 APK
在 Actions 页面下载构建好的 APK
系统要求
Android 5.0 (API 21) 或更高版本
推荐Android 11 (API 30)
需要相机权限
文件结构
text

camera-grid-app/
├── main.py          # 主程序
├── buildozer.spec   # Buildozer 配置文件
└── README.md        # 说明文档
注意事项
首次打包会下载 Android SDK、NDK 等工具，需要较长时间（约30-60分钟）
确保有足够的磁盘空间（至少10GB）
如遇到签名问题，可以使用 debug 版本进行测试