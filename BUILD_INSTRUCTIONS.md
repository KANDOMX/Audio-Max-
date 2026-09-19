# 📱 Building Audio Max APK - Online Services Guide

Since **Buildozer in Termux has limitations**, here are the **best online services** to build your APK without a PC.

---

## ✅ **Recommended Online Build Services**

### **1. Kivy Build Server (Official) - BEST OPTION**
🔗 **https://build.kivy.org/**

**Steps:**
1. Go to https://build.kivy.org/
2. Sign in with GitHub
3. Connect your repository: `KANDOMX/Audio-Max-`
4. Select branch: `main`
5. Choose **Android** platform
6. Click **Build**
7. Wait 10-30 minutes
8. Download APK from build artifacts

**Pros:**
- ✅ Free
- ✅ Official Kivy service
- ✅ No local setup needed
- ✅ Automatic dependency handling

**Cons:**
- ⏳ Build queue (may take time)

---

### **2. Python-for-Android Builder**
🔗 **https://github.com/kivy/python-for-android**

**Online Builder:** https://p4a.readthedocs.io/en/develop/buildoptions/

**Steps:**
1. Clone your repo to their builder
2. Configure build options
3. Download APK

---

### **3. GitHub Actions (Automated Building)**

I've created a **GitHub Actions workflow** for you!

#### **How to Use:**

1. **Create `.github/workflows/build_android.yml`** in your repo:

```yaml
name: Build Android APK

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        pip install buildozer
        sudo apt-get update
        sudo apt-get install -y git zip unzip openjdk-17-jdk python3-pip
    
    - name: Install Buildozer dependencies
      run: |
        sudo apt-get install -y ccache
        pip install kivy==2.1.0
    
    - name: Build APK
      run: |
        cd ${{ github.workspace }}
        buildozer -v android debug
    
    - name: Upload APK
      uses: actions/upload-artifact@v3
      with:
        name: audio-max-apk
        path: bin/*.apk
```

2. **Push to GitHub**
3. **Go to Actions tab** in your repo
4. **Run workflow** manually or wait for push
5. **Download APK** from artifacts

---

### **4. Replit + Buildozer (Cloud IDE)**
🔗 **https://replit.com/**

**Steps:**
1. Create new Replit project
2. Import your GitHub repo
3. Install Buildozer:
   ```bash
   pip install buildozer
   ```
4. Run build:
   ```bash
   buildozer -v android debug
   ```
5. Download APK from Replit

**Note:** Replit has storage limits, may need premium for full builds.

---

### **5. Google Colab (Free Cloud Notebook)**
🔗 **https://colab.research.google.com/**

**Steps:**
1. Create new notebook
2. Run these commands:

```python
# Install dependencies
!pip install buildozer
!apt-get update
!apt-get install -y git zip unzip openjdk-17-jdk python3-pip

# Clone your repo
!git clone https://github.com/KANDOMX/Audio-Max-.git
%cd Audio-Max-

# Build APK (takes 20-40 minutes)
!buildozer -v android debug

# Download APK
from google.colab import files
files.download('bin/AudioMax-1.0.0-debug.apk')
```

**Pros:**
- ✅ Free GPU/CPU
- ✅ 12+ hours runtime
- ✅ No local installation

**Cons:**
- ⏳ May timeout on large builds

---

## 📋 **Buildozer Configuration**

Your `buildozer.spec` is already configured with:
- ✅ Package name: `org.kandomx.audiomax`
- ✅ Version: `1.0.0`
- ✅ Requirements: Kivy, pygame, mutagen, pydub
- ✅ Permissions: Storage, Internet, Wake Lock
- ✅ API Level: 21+ (Android 5.0+)
- ✅ Architecture: arm64-v8a

---

## 🎯 **Quick Start - Use Kivy Build Server**

This is the **easiest method**:

1. ✅ **Your code is already in GitHub**
2. ✅ **buildozer.spec is configured**
3. ✅ **Just go to https://build.kivy.org/**
4. ✅ **Connect your repo and build!**

---

## 🔧 **Custom Buildozer.spec Settings**

If you need to customize, edit `buildozer.spec`:

```ini
# Change app name
fullname = Audio Max

# Change package name
package.name = audiomax
package.domain = org.kandomx

# Change version
version = 1.0.0

# Change orientation (portrait/landscape/all)
orientation = all

# Change permissions
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,WAKE_LOCK,VIBRATE

# Change minimum API level
android.minapi = 21
android.api = 30

# Change architecture
android.arch = arm64-v8a
```

---

## 📱 **Installing APK on Your Tablet**

1. **Download APK** from build service
2. **Transfer to tablet** (Google Drive, email, etc.)
3. **Enable Unknown Sources:**
   - Settings → Security → Unknown Sources → Enable
4. **Install APK** by tapping the file

---

## ⚠️ **Troubleshooting**

### **Build Fails?**
- Check `buildozer.spec` for typos
- Ensure all requirements are listed
- Try removing `pygame` (use Kivy's SoundLoader instead)

### **APK Crashes?**
- Check Android version compatibility (minapi = 21)
- Test on Android 7.0+ for best results
- Check permissions in Android manifest

### **Storage Access Denied?**
- Add `READ_EXTERNAL_STORAGE` and `WRITE_EXTERNAL_STORAGE` permissions
- Request permissions at runtime in your code

---

## 💡 **Best Service for You**

| Service | Difficulty | Speed | Cost | Success Rate |
|---------|-----------|-------|------|--------------|
| **Kivy Build Server** | ⭐ Easy | ⏳ Medium | Free | ⭐⭐⭐⭐⭐ |
| **GitHub Actions** | ⭐⭐ Medium | ⚡ Fast | Free | ⭐⭐⭐⭐ |
| **Google Colab** | ⭐⭐ Medium | ⏳ Slow | Free | ⭐⭐⭐ |
| **Replit** | ⭐⭐ Medium | ⚡ Fast | Free* | ⭐⭐ |

**Recommendation:** Start with **Kivy Build Server** → If queue is long, try **GitHub Actions**

---

## 🎉 **You're Ready!**

Your project has:
- ✅ Kivy mobile app code (`src/audio_max/kivy_app.py`)
- ✅ Buildozer config (`buildozer.spec`)
- ✅ Requirements for mobile (`requirements_kivy.txt`)
- ✅ Mobile entry point (`mobile_main.py`)

**Just go to https://build.kivy.org/ and build your APK!**

---

## 📞 **Need Help?**

If you encounter issues:
1. Check the build logs
2. Google the error message + "kivy"
3. Ask in Kivy Discord: https://discord.gg/kivy
4. Open an issue in your GitHub repo

---

**Happy Building! 🚀**
