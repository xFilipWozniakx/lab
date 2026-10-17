[app]

title = Photo Sync
package.name = photosync
package.domain = org.example

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,json,crt
source.exclude_dirs = kivy-build-deps

version = 0.1.0

# Kivy is the UI toolkit; pyjnius is used for Android's folder picker and SAF streams.
requirements = python3,kivy,pyjnius

orientation = portrait
fullscreen = 0

# SAF folder selection does not require broad storage permissions.
android.permissions = INTERNET

android.api = 35
android.minapi = 24
android.ndk = 27c
android.archs = arm64-v8a
android.accept_sdk_license = True

p4a.branch = develop

# Use the Android activity result API to let the user select photo folders.
android.enable_androidx = True

[buildozer]
log_level = 2
warn_on_root = 1
