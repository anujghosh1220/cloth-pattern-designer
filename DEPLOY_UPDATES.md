# 🚀 Deploying Updates - Step-by-Step

## Quick Workflow (5 Minutes)

### 1. Make Your Changes
- Edit your code
- Test everything works
- Update version in `package.json`

### 2. Build New Version
```bash
npm run build-win
```

### 3. Release to GitHub
- Go to: https://github.com/anujghosh1220/cloth-pattern-designer/releases
- Click "Create a new release"
- Tag: `v1.1.0` (match your version)
- Title: `Version 1.1.0`
- Description: List your changes
- Upload: `Draping Threads Setup 1.1.0.exe`
- Click "Publish release"

### 4. Done! 🎉
- All clients will be notified automatically
- Updates download in background
- No further action needed

---

## 📋 Detailed Steps

### Step 1: Update Version Number
Edit `package.json`:
```json
{
  "name": "cloth-pattern-designer",
  "version": "1.1.0",  // Change this
  "description": "..."
}
```

**Version Format:**
- `1.0.1` - Bug fixes
- `1.1.0` - New features  
- `2.0.0` - Major changes

### Step 2: Build the App
```bash
# Build Windows version
npm run build-win

# Files created in dist/ folder:
# - Draping Threads Setup 1.1.0.exe (installer)
# - latest.yml (update metadata)
```

### Step 3: Create GitHub Release

1. **Navigate to Releases**
   - Go to your repository
   - Click "Releases" tab
   - Click "Create a new release"

2. **Fill Release Details**
   - **Tag**: `v1.1.0` (must start with 'v')
   - **Target**: `main` branch
   - **Release title**: `Version 1.1.0`
   - **Description**: 
     ```
     ## New Features
     - Added customer export feature
     - Improved pattern generation
     
     ## Bug Fixes  
     - Fixed measurement saving issue
     - Improved performance
     ```

3. **Upload Files**
   - Click "Attach binaries"
   - Select: `Draping Threads Setup 1.1.0.exe`
   - Wait for upload to complete

4. **Publish**
   - Click "Publish release"
   - GitHub will create the release

### Step 4: Client Update Process

**What Happens Automatically:**
1. Client apps check GitHub for updates
2. New version detected (1.1.0)
3. Show update notification to client
4. Client clicks "Download Now"
5. Update downloads in background
6. Client clicks "Restart Now"
7. App updates and restarts with new version

---

## ⚡ Pro Tips

### Testing Updates
1. **Test locally**: `npm run dev`
2. **Build test version**: Change version to `1.0.1-test`
3. **Create test release**: Use pre-release tag
4. **Verify update flow**: Install old version, check for update

### Release Notes Template
```markdown
## Version 1.1.0 - [Date]

### ✨ New Features
- Feature 1 description
- Feature 2 description

### 🐛 Bug Fixes  
- Fixed issue with measurements
- Fixed crash on startup

### 🔧 Improvements
- Faster loading times
- Better error messages

### ⚠️ Important
- Database migration required
- Backup recommended before update
```

### Version Management
```bash
# Current version: 1.0.0
# Bug fix: 1.0.1
# Feature: 1.1.0  
# Major: 2.0.0
```

---

## 🔧 Advanced Options

### Private Updates (GitHub Private Repo)
```json
"publish": {
  "provider": "github",
  "owner": "your-username", 
  "repo": "private-repo",
  "private": true
}
```

### Custom Server
```json
"publish": {
  "provider": "generic",
  "url": "https://your-server.com/updates/"
}
```

### Manual Update Check
Add to Help menu:
```javascript
// In main.js menu template
{
  label: 'Help',
  submenu: [
    {
      label: 'Check for Updates',
      click: () => autoUpdater.checkForUpdates()
    }
  ]
}
```

---

## 📊 Monitoring Updates

### Track Update Adoption
- Check GitHub release downloads
- Monitor client feedback
- Watch for error reports

### Rollback Plan
If something goes wrong:
1. **Quick fix**: Release patch version (1.1.1)
2. **Rollback**: Re-release previous version
3. **Communicate**: Notify clients of issues

---

## 🎯 Success Checklist

Before releasing:
- [ ] Version number updated
- [ ] App tested thoroughly  
- [ ] Release notes written
- [ ] Backup of current version
- [ ] GitHub repo ready

After releasing:
- [ ] Monitor download stats
- [ ] Watch for client feedback
- [ ] Test update on clean machine
- [ ] Document any issues

---

## 🆘 Common Issues

### Update Not Found
- Check version format (must be `v1.1.0`)
- Verify release is published (not draft)
- Check GitHub permissions

### Download Fails
- Check file size (too large?)
- Verify internet connection
- Try restarting app

### Install Fails
- Check Windows permissions
- Antivirus blocking?
- Disk space available

---

**That's it! Your clients will now receive updates automatically! 🎉**
