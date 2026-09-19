# (str) Title of your application
#title = Audio Max

# (str) Package name
package.name = audiomax

# (str) Package domain (needed for android/ios packaging)
package.domain = org.kandomx

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,ttf,mp3,ogg,wav

# (list) List of inclusions using pattern matching
#source.include_patterns = assets/*,images/*.png

# (list) Source files to exclude (let empty to not exclude anything)
#source.exclude_exts = spec

# (list) List of directory to exclude (let empty to not exclude anything)
#source.exclude_dirs = tests, bin

# (list) List of exclusions using pattern matching
#source.exclude_patterns = license,images/*/*.jpg

# (str) Application versioning (method 1)
version = 1.0.0

# (str) Application versioning (method 2)
# version.regex = __version__ = ['"](.*)['"]
# version.filename = %(source.dir)s/main.py

# (list) Application requirements
# Comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy>=2.1.0,pygame>=2.5.0,mutagen>=1.46.0,pydub>=0.25.1

# (str) Custom source folders for requirements
# Sets custom source for any requirements with recipes
# requirements.source = 

# (list) Garden requirements
#garden_requirements = 

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientation (one of landscape, portrait or all)
orientation = all

# (list) List of service to declare
#services = NAME:ENTRYPOINT

# (str) Android logcat filter
#android.logcat_filters = *:S python:D

# (bool) Copy library instead of making a libs.zip
#android.copy_libs = 1

# (str) Android NDK version (default is 19b)
#android.ndk = 19b

# (bool) Use --private data storage (True) or --dir public storage (False)
#android.private_storage = True

# (str) Android app permissions
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,WAKE_LOCK,VIBRATE

# (int) Android API to use
#android.api = 30

# (int) Minimum API required
#android.minapi = 21

# (int) Android SDK version to use
#android.sdk = 20

# (str) Android NDK directory (if empty, it will be automatically downloaded.)
#android.ndk_path = 

# (str) Android SDK directory (if empty, it will be automatically downloaded.)
#android.sdk_path = 

# (str) python-for-android branch to use
#p4a.branch = master

# (str) OUYA Console category. Should be one of GAME or APP
# If you leave this blank, OUYA support will not be enabled
#android.ouya.category = GAME

# (str) Filename of the Android application manifest
#android.manifest = 

# (str) Android additional libraries to copy into libs/armeabi
#android.add_libs_armeabi = libs/android/*.so

# (str) Android additional libraries to copy into libs/armeabi-v7a
#android.add_libs_armeabi_v7a = libs/android-v7/*.so

# (str) Android additional libraries to copy into libs/arm64-v8a
#android.add_libs_arm64_v8a = libs/android-v8/*.so

# (str) Android additional libraries to copy into libs/x86
#android.add_libs_x86 = libs/android-x86/*.so

# (str) Android additional libraries to copy into libs/x86_64
#android.add_libs_x86_64 = libs/android-x64/*.so

# (bool) Indicate whether the screen should stay on
# Don't forget to add the WAKE_LOCK permission if you set this to True
#android.wakelock = False

# (list) Android application meta-data to set (key=value format)
#android.meta_data = 

# (list) Android library project to add (will be added in the
# project.properties automatically.)
#android.library_references = 

# (str) Android logcat filters
#android.logcat_filters = *:S python:D

# (bool) Copy library instead of making a libs.zip
#android.copy_libs = 1

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.arch = arm64-v8a

# (int) Android API to use
android.api = 30

# (int) Minimum API required
android.minapi = 21

# (bool) Whether it should create an activity for each screen
#kivy.create_activity = True

# (str) Filename of the Android application manifest
#android.manifest = 

# (str) Full name of the application
fullname = Audio Max

# (str) Short name of the application
#shortname = audiomax

# (str) Author of the application
author = KANDOMX

# (str) Homepage of the application
#homepage = 

# (str) Application description
#description = A modern music player

# (str) Application icon (32x32 PNG)
#icon.filename = assets/icon.png

# (str) Application icon (64x64 PNG)
#icon.filename = assets/icon64.png

# (str) Application icon (128x128 PNG)
#icon.filename = assets/icon128.png

# (str) Application icon (256x256 PNG)
#icon.filename = assets/icon256.png

# (str) Application icon (512x512 PNG)
#icon.filename = assets/icon512.png

# (str) Application presplash (PNG or JPG)
#presplash.filename = assets/presplash.png

# (str) Application orientation
#orientation = portrait

# (str) Application permissions
#android.permissions = INTERNET

# (str) Application package name
#package.name = org.kandomx.audiomax

# (str) Application package domain
#package.domain = org.kandomx

# (str) Application source directory
#source.dir = .

# (str) Application version
#version = 1.0.0

# (str) Application requirements
#requirements = python3,kivy,pygame,mutagen,pydub

# (str) Additional requirements for p4a
#p4a.requirements = 

# (bool) Use Pyjnius
#p4a.use_pyjnius = True

# (bool) Use Pyjnius with SDK
#p4a.use_pyjnius_sdk = True

# (bool) Use Pyjnius with NDK
#p4a.use_pyjnius_ndk = True
