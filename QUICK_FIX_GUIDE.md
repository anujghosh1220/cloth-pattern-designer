# 🔧 Quick Fix Guide for Common Issues

## 🎯 **If You're Seeing an Error, Try These Solutions:**

---

### **Solution 1: Use the Simple Launcher**
1. **Double-click:** `START_APP_SIMPLE.bat` (in the main folder)
2. **This version** has better error handling and clearer messages
3. **Follow the on-screen instructions**

---

### **Solution 2: Try the Unpacked Version**
1. **Go to folder:** `dist\win-unpacked\`
2. **Double-click:** `DrapingThreads.exe`
3. **This runs directly** without any Python detection

---

### **Solution 3: Run as Administrator**
1. **Right-click** the launcher file
2. **Select "Run as administrator"**
3. **Click "Yes"** on security prompt

---

## 🔍 **Common Error Messages & Solutions**

### **"Python not found"**
**What it means:** Python isn't installed on your computer
**Solution:** 
- Install Python from https://www.python.org/downloads/
- Check "Add Python to PATH" during installation
- Try the launcher again

### **"Flask not found"**
**What it means:** Flask web framework isn't installed
**Solution:** 
- The simple launcher installs Flask automatically
- Or manually run: `python -m pip install flask`

### **"Port 5000 already in use"**
**What it means:** Another app is using port 5000
**Solution:** 
- Close other applications
- Restart your computer
- Try again

### **"app.py not found"**
**What it means:** Application file is missing
**Solution:** 
- Make sure all files are in the same folder
- Re-download the complete package
- Don't move individual files

---

## 🛠️ **Advanced Troubleshooting**

### **Check File Structure**
Make sure your folder looks like this:
```
📁 Draping Threads/
├── START_APP_SIMPLE.bat
├── app.py
├── static/
├── templates/
└── [other files]
```

### **Test Python Installation**
1. **Open Command Prompt** (Win+R, type `cmd`)
2. **Type:** `python --version`
3. **Should show:** Python 3.x.x
4. **If error:** Python not installed properly

### **Test Flask Installation**
1. **Open Command Prompt**
2. **Type:** `python -c "import flask; print('Flask OK')"`
3. **Should show:** Flask OK
4. **If error:** Flask not installed

---

## 📞 **Still Having Issues?**

### **Information to Collect:**
1. **Exact error message** (copy the text)
2. **Windows version** (Windows 10, 11, etc.)
3. **What you clicked** before the error
4. **All files in your folder**

### **Contact Support:**
- **Email:** [your-email@example.com]
- **Phone:** [your-phone-number]
- **Include:** Screenshot of error message

---

## 🎯 **Prevention Tips**

### **For Best Results:**
1. **Keep all files together** - Don't separate them
2. **Use the simple launcher** - `START_APP_SIMPLE.bat`
3. **Run as administrator** if permissions issues
4. **Install Python with PATH** if needed

### **Recommended Setup:**
- **Windows 10 or 11**
- **Python 3.9 or newer** (with PATH)
- **Flask installed** (auto-installed by launcher)
- **All files in same folder**

---

## ✅ **Success Indicators**

### **When It's Working:**
- ✅ Launcher shows "✅ Found Python"
- ✅ Launcher shows "✅ Flask is installed"
- ✅ Browser opens to http://localhost:5000
- ✅ Login screen appears
- ✅ Can login with admin/admin2214

### **Expected Startup Sequence:**
```
🔍 Checking for Python...
✅ Found Python: python
🔍 Checking for Flask...
📦 Installing Flask... (if needed)
✅ Flask installed successfully!
🚀 Starting Draping Threads application...
[Browser opens with login screen]
```

---

**Most issues are fixed by using START_APP_SIMPLE.bat!** 🎉
