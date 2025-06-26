[app]

# (str) Title of your application
title = TerlineT

# (str) Package name
package.name = terlinet

# (str) Package domain (needed for android/ios packaging)
package.domain = com.terlinet.app

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,txt,gguf

# (str) Application versioning (method 1)
version = 1.0.0

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy,llama-cpp-python,numpy,typing-extensions,diskcache,jinja2,markupsafe

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,RECORD_AUDIO,WAKE_LOCK

# (list) The Android archs to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a

# (bool) enables Android auto backup feature (Android API >=23)
android.allow_backup = True

# (bool) indicates whether the build should use ANDROIDX compatibility library
android.enable_androidx = False

# (str) The format used to package the app for debug mode (apk or aab)
android.debug_artifact = apk

# (str) The format used to package the app for release mode (apk or aab)
android.release_artifact = apk

# (str) Path to build output (i.e. .apk, .aab, .ipa) storage
bin_dir = ./APK

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1