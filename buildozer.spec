[app]

# (str) Title of your application
title = Food Clicker

# (str) Package name
package.name = foodclicker

# (str) Package domain (needed for android packaging)
package.domain = org.pythonexpert

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include (ttf строго латиницей)
source.include_exts = py,kv,png,jpg,jpeg,mp3,ttf,txt,wav

# (list) List of directory to exclude
source.exclude_dirs = .venv,.idea,__pycache__,bin,build,.buildozer

# (list) List of exclusions using pattern matching
source.exclude_exts = pyc,pyo,xcf

# (str) Application versioning
version = 1.0

# (list) Облегченные требования приложения (убран charset-normalizer)
requirements = python3==3.11.10,kivy

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

# Фиксируем стабильный релиз паковщика, чтобы использовать Python 3.11
p4a.branch = v2024.01.21

# Блокируем компиляцию неиспользуемых тяжелых кодеков и сетевых пакетов
p4a.recipe_options_blacklist = libwebp,libtiff,libjxl,libavif,dav1d,openssl,sqlite3

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1
