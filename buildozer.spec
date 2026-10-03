
[app]

# (str) Title of your application
title = Apex AI Studio

# (str) Package name
package.name = apexstudio

# (str) Package domain (needed for android/ios packaging)
package.domain = org.innovators

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (include main.py and any required extensions)
source.include_exts = py,png,jpg,kv,atlas

# (list) Application requirements
# Note: Set to python3,kivy,pyjnius for stability with Android APIs
requirements = python3,kivy,pyjnius

# (str) Application versioning
version = 0.1

# (list) Permissions required by the app
# Android permissions
# android.permissions = INTERNET

# (int) Target Android API, should be 33 for modern compatibility
android.api = 33

# (int) Minimum API your APK will support
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (bool) If True, then skip trying to update the SDK
android.skip_update = False

# (bool) If True, automatically accept SDK licenses
android.accept_sdk_license = True

# (str) The Android arch to build for
# Arm64-v8a is standard for modern devices
android.archs = arm64-v8a

# (bool) Enable AndroidX support
android.enable_androidx = True

# (list) List of Java classes to add to the compilation class path
# android.add_jars = foo.jar

# (list) Gradle dependencies to add
# android.gradle_dependencies =

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = false, 1 = true)
warn_on_root = 0

# (str) Path to build artifact storage, leave default
# build_dir = ./.buildozer

# (str) Path to build output (where .apk will be saved)
# bin_dir = ./bin
