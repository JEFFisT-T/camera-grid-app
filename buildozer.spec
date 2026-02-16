[app]

# (str) Title of your application
title = Camera Grid

# (str) Package name
package.name = cameragrid

# (str) Package domain (needed for android/ios packaging)
package.domain = org.cameragrid

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,json

# (str) Application versioning (method 1)
version = 1.0.0

# (list) Application requirements
requirements = python3,kivy,pyjnius

# (list) Supported orientations - 横屏
orientation = landscape

#
# Android specific
#

fullscreen = 0

android.api = 30
android.minapi = 21
android.ndk = 25b

android.permissions = CAMERA,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

android.accept_sdk_license = True
android.manifest.orientation = landscape

android.archs = arm64-v8a, armeabi-v7a

android.allow_backup = True
android.debug_artifact = apk
android.release_artifact = apk

#
# Python for android (p4a) specific - 关键修复
#
p4a.bootstrap = sdl2
p4a.branch = develop

[buildozer]

log_level = 2
warn_on_root = 1
