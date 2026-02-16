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
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy

# (list) Supported orientations - 横屏
# Valid options are: landscape, portrait, portrait-reverse or landscape-reverse
orientation = landscape

#
# Android specific
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (int) Target Android API, should be as high as possible.
# Android 11 = API 30
android.api = 30

# (int) Minimum API your APK / AAB will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (list) Permissions - 相机权限
android.permissions = CAMERA,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (bool) If True, then automatically accept SDK license
android.accept_sdk_license = True

# (str) screenOrientation to set for the main activity - 横屏
android.manifest.orientation = landscape

# (list) The Android archs to build for
android.archs = arm64-v8a, armeabi-v7a

# (bool) enables Android auto backup feature (Android API >=23)
android.allow_backup = True

# (str) The format used to package the app for debug mode (apk or aar).
android.debug_artifact = apk

# (str) The format used to package the app for release mode (aab or apk or aar).
android.release_artifact = apk

#
# Python for android (p4a) specific
#
p4a.bootstrap = sdl2

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
