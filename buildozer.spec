[app]

# (str) Title of your application
title = Food Clicker

# (str) Package name
package.name = foodclicker

# (str) Package domain (needed for android packaging)
package.domain = org.pythonexpert

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include
source.include_exts = py,kv,png,jpg,jpeg,mp3,ttа,txt,wav

# (list) List of directory to exclude
source.exclude_dirs = .venv,.idea,__pycache__,bin,build,.buildozer

# (list) List of exclusions using pattern matching
source.exclude_exts = pyc,pyo,xcf

# (str) Application versioning
version = 1.0

# (list) Application requirements
requirements = python3==3.11.10,kivy,charset-normalizer==2.1.1

# (str) Custom source code for launcher icon
icon.filename = %(source.dir)s/assets/image/icon.png

# (str) Supported orientation
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# (int) Target Android API
android.api = 33

# (int) Minimum API required to run the app
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (list) The Android archs to build for
android.archs = arm64-v8a

# (bool) Accept SDK license automatically
android.accept_sdk_license = True

# (str) python-for-android git clone branch to use
#p4a.branch = develop

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1
