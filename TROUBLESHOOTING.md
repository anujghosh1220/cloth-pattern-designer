# 🔧 Draping Threads - Troubleshooting Guide

## ❌ "Failed to start application" Error

This error means the app can't find or start Python/Flask. Here's how to fix it:

---

## 🎯 **Quick Solutions**

### Solution 1: Install Python (Most Common)
1. **Download Python:** https://www.python.org/downloads/
2. **Download:** Python 3.9 or newer
3. **IMPORTANT:** Check "Add Python to PATH" during installation
4. **Restart computer** after installation
5. **Try the app again**

### Solution 2: Install Flask
1. **Open Command Prompt:** Press Win+R, type `cmd`, press Enter
2. **Run:** `python -m pip install flask`
3. **Wait** for installation to complete
4. **Try the app again**

### Solution 3: Check Python Installation
1. **Open Command Prompt**
2. **Type:** `python --version`
3. **Should show:** Python 3.x.x
4. **If error:** Python not installed properly

---

## 🔍 **Detailed Troubleshooting**

### Check What's Missing

**Open Command Prompt and run:**
```cmd
python --version
```
- **If error:** Python not installed
- **If shows version:** Python is installed

```cmd
python -c "import flask; print('Flask is installed')"
```
- **If error:** Flask not installed  
- **If no error:** Flask is installed

### Common Issues & Fixes

#### Issue: "Python is not recognized"
**Cause:** Python not in PATH
**Fix:**
1. Reinstall Python
2. Check "Add Python to PATH" 
3. Or add Python manually to Windows PATH

#### Issue: "ModuleNotFoundError: No module named 'flask'"
**Cause:** Flask not installed
**Fix:**
```cmd
python -m pip install flask
```

#### Issue: Port 5000 already in use
**Cause:** Another app using port 5000
**Fix:**
1. Close other apps
2. Restart computer
3. Try again

---

## 🛠️ **Advanced Solutions**

### Solution 4: Use Virtual Environment
1. **Open Command Prompt**
2. **Navigate to app folder:**
   ```cmd
   cd "C:\Program Files\Draping Threads"
   ```
3. **Create virtual environment:**
   ```cmd
   python -m venv venv
   ```
4. **Activate:**
   ```cmd
   venv\Scripts\activate
   ```
5. **Install Flask:**
   ```cmd
   pip install flask
   ```

### Solution 5: Manual Python Path
1. **Find Python installation:** Usually `C:\Python39\` or `C:\Users\[Username]\AppData\Local\Programs\Python\Python39\`
2. **Add to PATH:**
   - Press Win+R, type `sysdm.cpl`
   - Go to "Advanced" → "Environment Variables"
   - Add Python path to "Path" variable

---

## 📞 **Get Help**

### Built-in Help
1. **Open the app**
2. **Click Help menu**
3. **Select "Installation Help"**

### Contact Support
If none of these solutions work:
1. **Screenshot the error message**
2. **Note your Windows version**
3. **Contact support with details**

---

## ✅ **Prevention Tips**

1. **Always check "Add Python to PATH"** during Python installation
2. **Install Python as Administrator** (right-click → Run as admin)
3. **Use Python 3.9 or newer** (recommended)
4. **Keep Flask updated** with `pip install --upgrade flask`

---

## 🎉 **Success Indicators**

You'll know it's working when:
- ✅ App window opens without error
- ✅ Shows login screen (admin/admin2214)
- ✅ No "Failed to start application" message
- ✅ Flask server starts in background

---

**Still having issues? The app now provides detailed error messages to help identify the exact problem!**
