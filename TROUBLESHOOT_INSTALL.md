# 🔧 Installer Not Working - Troubleshooting Guide

## ❌ **Problem: Double-clicking installer does nothing**

---

## 🎯 **Quick Solutions (Try These First)**

### **Solution 1: Run as Administrator**
1. **Right-click** "Draping Threads Setup 1.0.0.exe"
2. **Select "Run as administrator"**
3. **Click "Yes"** on security prompt
4. **Follow installation steps**

### **Solution 2: Try the Unpacked Version**
1. **Go to folder:** `dist\win-unpacked\`
2. **Double-click:** "Draping Threads.exe"
3. **This runs the app directly without installing**

### **Solution 3: Copy to Desktop**
1. **Copy** "Draping Threads Setup 1.0.0.exe" to Desktop
2. **Double-click** from Desktop
3. **Sometimes path issues prevent running from dist folder**

---

## 🔍 **Why This Happens**

### **Common Causes:**
- **Antivirus blocking** the installer
- **Windows security** preventing execution
- **Missing permissions** on the folder
- **Corrupted download** or build
- **Path too long** for Windows

### **Windows Security Issues:**
- **"Windows protected your PC"** - Click "More info" → "Run anyway"
- **"SmartScreen prevented"** - Click "More info" → "Run anyway"
- **No error message** - Usually security software blocking silently

---

## 🛠️ **Advanced Solutions**

### **Solution 4: Check Antivirus**
1. **Open your antivirus software**
2. **Check quarantine/blocked files**
3. **Add exception** for "Draping Threads Setup 1.0.0.exe"
4. **Try running again**

### **Solution 5: Check Windows Defender**
1. **Open Windows Security**
2. **Go to "Virus & threat protection"**
3. **Click "Protection history"**
4. **Look for blocked threats**
5. **Allow the file if blocked**

### **Solution 6: Use Command Prompt**
1. **Press Win+R**, type `cmd`, press Enter
2. **Navigate to folder:**
   ```cmd
   cd "C:\Users\Anuj Ghosh\CascadeProjects\cloth-pattern-designer\dist"
   ```
3. **Run installer:**
   ```cmd
   "Draping Threads Setup 1.0.0.exe"
   ```

### **Solution 7: Test with Diagnostic**
1. **Run:** `INSTALL_DIAGNOSTIC.bat` (in main folder)
2. **Follow on-screen instructions**
3. **Shows detailed system information**

---

## 📦 **Alternative Installation Methods**

### **Method 1: Direct App Run (No Installation)**
```
Go to: dist\win-unpacked\
Double-click: DrapingThreads.exe
```
**Pros:** No installation required  
**Cons:** No desktop shortcut, no uninstaller

### **Method 2: Manual Installation**
1. **Copy entire `win-unpacked` folder** to `C:\Program Files\Draping Threads\`
2. **Create desktop shortcut** to `DrapingThreads.exe`
3. **Run from shortcut**

### **Method 3: Rebuild Installer**
```bash
npm run build-win
```
Creates fresh installer file

---

## 🎯 **What to Expect When It Works**

### **Successful Installation:**
1. **Installer window opens** with welcome screen
2. **Click Next** through installation steps
3. **Choose installation location** (default is fine)
4. **Wait for installation** to complete
5. **Desktop shortcut** appears automatically
6. **Launch from shortcut** or Start menu

### **Direct App Run:**
1. **App window opens** after 10-30 seconds
2. **Shows login screen** (admin/admin2214)
3. **Ready to use** immediately

---

## 📞 **Still Not Working?**

### **Information to Collect:**
- **Windows version** (Windows 10, 11, etc.)
- **Antivirus software** name
- **Exact error message** (if any)
- **What happens** when you double-click

### **Next Steps:**
1. **Try all solutions above**
2. **Run diagnostic tool**
3. **Contact support with details**
4. **Consider alternative installation method**

---

## ✅ **Prevention Tips**

### **For Future Installers:**
- **Always run as administrator**
- **Add antivirus exceptions**
- **Check Windows security settings**
- **Use shorter file paths**

### **For This App:**
- **Keep installer in safe location**
- **Don't move files after installation**
- **Create backup of installer**

---

**Most users fix this by running as administrator or trying the unpacked version!** 🎉
