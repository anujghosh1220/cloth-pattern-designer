# 🔄 Draping Threads - Update Guide

## How Updates Work for Your Clients

Your clients will receive updates **automatically** and **seamlessly** - no technical knowledge required!

---

## 🎯 What Happens When You Release an Update

### Step 1: You Make Changes
- Update your app code
- Test the changes
- Increment version number in `package.json`

### Step 2: Build & Release
```bash
npm run build-win
```
- Upload the new installer to GitHub Releases
- Clients get notified automatically

### Step 3: Client Experience
- **App starts** → Checks for updates
- **Update found** → Shows notification dialog
- **Client clicks "Download"** → Downloads in background
- **Download complete** → Shows "Restart Now" button
- **App restarts** → Updates automatically
- **Client continues** with new version

---

## 📱 Client Update Flow

### Notification Dialog
```
┌─────────────────────────────────┐
│     Update Available           │
│                                 │
│ A new version of Draping       │
│ Threads is available.          │
│                                 │
│ Version 1.1.0 is ready to      │
│ download.                      │
│                                 │
│ [Download Now]  [Later]        │
└─────────────────────────────────┘
```

### Download Complete Dialog
```
┌─────────────────────────────────┐
│        Update Ready            │
│                                 │
│ Update downloaded successfully! │
│                                 │
│ The app will restart to        │
│ install the update.            │
│                                 │
│ [Restart Now]  [Later]         │
└─────────────────────────────────┘
```

---

## 🚀 How to Release Updates

### 1. Update Version Number
Edit `package.json`:
```json
{
  "version": "1.1.0"
}
```

### 2. Build New Version
```bash
npm run build-win
```

### 3. Create GitHub Release
1. Go to your GitHub repository
2. Click "Releases" → "Create a new release"
3. Tag version: `v1.1.0`
4. Upload the new `.exe` file from `dist/`
5. Publish release

### 4. Automatic Distribution
- All clients will be notified within 24 hours
- Updates download in background
- No action required from you

---

## 📋 Update Settings Configuration

### Update Frequency
- **Check on startup**: Every time app launches
- **Background check**: Every 4 hours while running
- **Manual check**: Via Help menu

### Update Behavior
- **Silent download**: Updates download in background
- **User choice**: Client decides when to install
- **Auto-restart**: App restarts to apply updates
- **Rollback**: Previous version kept as backup

---

## 🛠️ Advanced Options

### Force Updates (Critical Security)
```javascript
// In main.js - for emergency updates
autoUpdater.on('update-available', (info) => {
  if (info.isCritical) {
    dialog.showMessageBox({
      type: 'warning',
      title: 'Critical Update Required',
      message: 'This update is required for security reasons.',
      buttons: ['Update Now']
    }).then(() => {
      autoUpdater.downloadUpdate();
    });
  }
});
```

### Staged Rollouts
- Release to 10% of users first
- Monitor for issues
- Gradually increase to 100%

### Custom Update Server
```json
"publish": {
  "provider": "generic",
  "url": "https://your-server.com/updates/"
}
```

---

## 🔍 Troubleshooting Updates

### Client Issues
- **No update notification**: Check internet connection
- **Download fails**: Try again later or restart app
- **Install fails**: Restart computer, try again

### Developer Issues
- **Build fails**: Check version number format
- **Upload fails**: Verify GitHub permissions
- **Update not found**: Check release tag format

---

## 📊 Update Analytics

You can track:
- Number of clients updated
- Update success rate
- Time to adoption
- Failed update reasons

---

## ✅ Best Practices

1. **Test thoroughly** before releasing
2. **Use semantic versioning** (1.0.0 → 1.0.1 → 1.1.0)
3. **Release notes** for each update
4. **Backup before major updates**
5. **Monitor feedback** after releases

---

## 🎉 Benefits for Your Clients

✅ **No technical knowledge needed**  
✅ **Updates happen automatically**  
✅ **Always latest features**  
✅ **Security patches applied**  
✅ **No manual downloading**  
✅ **Seamless experience**  

Your clients will always have the latest version without any technical effort!
