# Draping Threads - Electron Desktop App

This is the desktop version of the Draping Threads cloth pattern designer web application, built with Electron.

## Installation

1. Install dependencies:
```bash
npm install
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Running the App

### Development Mode
```bash
npm run dev
```

### Production Mode
```bash
npm start
```

## Building for Distribution

### Windows
```bash
npm run build-win
```

### Linux
```bash
npm run build-linux
```

### macOS
```bash
npm run build-mac
```

### All Platforms
```bash
npm run build
```

## How It Works

The Electron app:
1. Launches a main process that creates a desktop window
2. Starts the Flask Python server in the background
3. Loads the web application in the Electron window
4. Provides native desktop features like menus and window management

## Features

- **Native Desktop Experience**: Window controls, menus, and shortcuts
- **Offline Capability**: Works without internet connection
- **Auto-start**: Flask server starts automatically when app launches
- **Cross-platform**: Works on Windows, macOS, and Linux
- **Installation**: Creates installable packages for easy distribution

## File Structure

```
cloth-pattern-designer/
├── main.js              # Electron main process
├── app.py               # Flask web application
├── package.json         # Node.js dependencies and Electron config
├── assets/              # App icons and resources
├── static/              # Static web assets
├── templates/           # HTML templates
└── dist/                # Built application (generated)
```

## Security

- Web security enabled in Electron
- External links open in system browser
- Node integration disabled for security
- Context isolation enabled

## Troubleshooting

### Python Not Found
Ensure Python is installed and available in system PATH.

### Flask Server Fails to Start
Check that all Python dependencies are installed:
```bash
pip install -r requirements.txt
```

### App Window Doesn't Load
Check the console output for Flask server startup messages.

## Development

To modify the app:
1. Edit the Flask app in `app.py` for web functionality
2. Edit `main.js` for Electron-specific features
3. Update `package.json` for build configuration
4. Test with `npm run dev` before building
