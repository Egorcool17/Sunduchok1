[app]
title = Сундучок
package.name = sunduchok
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy==2.2.0,cython==0.29.33
orientation = portrait
fullscreen = 1

android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True
android.api = 33
android.ndk = 25b
android.ndk_api = 21

[buildozer]
log_level = 2
warn_on_root = 1
