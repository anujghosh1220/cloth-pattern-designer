const { app, BrowserWindow, Menu, shell, dialog } = require('electron');
const path = require('path');
const { spawn, exec } = require('child_process');
const fs = require('fs');

let mainWindow;
let flaskProcess;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      enableRemoteModule: false,
      webSecurity: true
    },
    icon: path.join(__dirname, 'assets', 'icon.png'),
    show: false,
    titleBarStyle: 'default'
  });

  // Show window when ready to prevent visual flash
  mainWindow.once('ready-to-show', () => {
    mainWindow.show();
  });

  // Try to start with bundled Python first, then system Python
  startFlaskApp();
}

function startFlaskApp() {
  return new Promise((resolve, reject) => {
    console.log('Starting Flask server...');
    
    // Check for bundled Python in resources
    const bundledPythonPath = path.join(process.resourcesPath, 'python', 'python.exe');
    const appPath = path.join(__dirname, 'app.py');
    
    // Check if app.py exists
    if (!fs.existsSync(appPath)) {
      showError('Application File Missing', 
        'Required application file "app.py" not found.\n\n' +
        'Please reinstall the application.'
      );
      return;
    }
    
    let pythonCmd = '';
    let useBundled = false;
    
    // Try bundled Python first
    if (fs.existsSync(bundledPythonPath)) {
      pythonCmd = bundledPythonPath;
      useBundled = true;
      console.log('Using bundled Python:', pythonCmd);
    } else {
      // Fall back to system Python
      pythonCmd = 'python';
      console.log('Using system Python');
    }
    
    // Start Flask server
    flaskProcess = spawn(pythonCmd, ['app.py'], {
      cwd: __dirname,
      stdio: ['pipe', 'pipe', 'pipe'],
      env: {
        ...process.env,
        PYTHONPATH: useBundled ? path.join(process.resourcesPath, 'python', 'lib') : process.env.PYTHONPATH
      }
    });

    let serverStarted = false;
    let startupTimeout = setTimeout(() => {
      if (!serverStarted) {
        flaskProcess.kill();
        if (useBundled) {
          showError('Server Start Failed', 
            'Failed to start the application.\n\n' +
            'This is unusual as the app includes everything needed.\n\n' +
            'Please try restarting the application or contact support.'
          );
        } else {
          showError('Python Required', 
            'This application requires Python to run.\n\n' +
            'Please install Python from:\n' +
            'https://www.python.org/downloads/\n\n' +
            'Make sure to check "Add Python to PATH" during installation.\n\n' +
            'Or download the complete version with bundled Python.'
          );
        }
      }
    }, 30000);

    flaskProcess.stdout.on('data', (data) => {
      const output = data.toString();
      console.log('Flask stdout:', output);
      
      // Check if Flask server has started
      if (output.includes('Running on') || output.includes('DEBUG MODE')) {
        if (!serverStarted) {
          serverStarted = true;
          clearTimeout(startupTimeout);
          
          // Wait a moment for the server to be fully ready
          setTimeout(() => {
            mainWindow.loadURL('http://localhost:5000');
            resolve();
          }, 1000);
        }
      }
    });

    flaskProcess.stderr.on('data', (data) => {
      const output = data.toString();
      console.error('Flask stderr:', output);
      
      // Check for missing Flask
      if (output.includes('ModuleNotFoundError: No module named \'flask\'')) {
        clearTimeout(startupTimeout);
        flaskProcess.kill();
        showError('Flask Missing', 
          'Flask web framework is required but not installed.\n\n' +
          'This should not happen with the bundled version.\n\n' +
          'Please reinstall the application.'
        );
        return;
      }
      
      // Check if server started despite stderr output (common in development)
      if (output.includes('Running on') && !serverStarted) {
        serverStarted = true;
        clearTimeout(startupTimeout);
        setTimeout(() => {
          mainWindow.loadURL('http://localhost:5000');
          resolve();
        }, 1000);
      }
    });

    flaskProcess.on('error', (error) => {
      clearTimeout(startupTimeout);
      console.error('Failed to start Flask server:', error);
      
      if (useBundled) {
        showError('Application Error', 
          'Failed to start the application.\n\n' +
          'This is unusual as everything is bundled.\n\n' +
          'Please contact support for assistance.'
        );
      } else {
        showError('Python Not Found', 
          'Python is required to run this application.\n\n' +
          'Please install Python from:\n' +
          'https://www.python.org/downloads/\n\n' +
          'Make sure to check "Add Python to PATH" during installation.'
        );
      }
    });

    flaskProcess.on('close', (code) => {
      clearTimeout(startupTimeout);
      if (!serverStarted) {
        console.log(`Flask process exited with code ${code}`);
        if (useBundled) {
          showError('Application Failed', 
            'The application failed to start.\n\n' +
            'Please try:\n' +
            '1. Restarting the application\n' +
            '2. Restarting your computer\n' +
            '3. Reinstalling if the problem continues'
          );
        } else {
          showError('Server Exit', 
            'The application server exited unexpectedly.\n\n' +
            `Exit code: ${code}\n\n` +
            'Please ensure Python is properly installed.'
          );
        }
      }
    });
  });
}

function showError(title, message) {
  if (mainWindow) {
    dialog.showMessageBox(mainWindow, {
      type: 'error',
      title: title,
      message: message,
      buttons: ['OK']
    }).then(() => {
      app.quit();
    });
  } else {
    console.error(title + ': ' + message);
    app.quit();
  }
}

function createMenu() {
  const template = [
    {
      label: 'File',
      submenu: [
        {
          label: 'Quit',
          accelerator: process.platform === 'darwin' ? 'Cmd+Q' : 'Ctrl+Q',
          click: () => {
            app.quit();
          }
        }
      ]
    },
    {
      label: 'Edit',
      submenu: [
        { role: 'undo' },
        { role: 'redo' },
        { type: 'separator' },
        { role: 'cut' },
        { role: 'copy' },
        { role: 'paste' }
      ]
    },
    {
      label: 'View',
      submenu: [
        { role: 'reload' },
        { role: 'forceReload' },
        { role: 'toggleDevTools' },
        { type: 'separator' },
        { role: 'resetZoom' },
        { role: 'zoomIn' },
        { role: 'zoomOut' },
        { type: 'separator' },
        { role: 'togglefullscreen' }
      ]
    },
    {
      label: 'Window',
      submenu: [
        { role: 'minimize' },
        { role: 'close' }
      ]
    },
    {
      label: 'Help',
      submenu: [
        {
          label: 'Getting Started',
          click: () => {
            dialog.showMessageBox(mainWindow, {
              type: 'info',
              title: 'Getting Started',
              message: 'Welcome to Draping Threads!',
              detail: 'Login Information:\n\n' +
                      'Username: admin\n' +
                      'Password: admin2214\n\n' +
                      'You can change these after logging in.\n\n' +
                      'This application helps you:\n' +
                      '• Create clothing patterns\n' +
                      '• Manage customer measurements\n' +
                      '• Generate professional designs',
              buttons: ['OK']
            });
          }
        },
        {
          label: 'About',
          click: () => {
            shell.openExternal('https://github.com/anujghosh1220/cloth-pattern-designer');
          }
        }
      ]
    }
  ];

  const menu = Menu.buildFromTemplate(template);
  Menu.setApplicationMenu(menu);
}

// App event handlers
app.whenReady().then(() => {
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  // Kill Flask process when all windows are closed
  if (flaskProcess) {
    flaskProcess.kill();
  }
  
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('before-quit', () => {
  // Ensure Flask process is killed when app is quitting
  if (flaskProcess) {
    flaskProcess.kill();
  }
});

// Security: prevent new window creation
app.on('web-contents-created', (event, contents) => {
  contents.on('new-window', (event, navigationUrl) => {
    event.preventDefault();
    shell.openExternal(navigationUrl);
  });
});
