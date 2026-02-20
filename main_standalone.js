const { app, BrowserWindow, Menu, shell, dialog } = require('electron');
const path = require('path');
const { spawn, exec } = require('child_process');
const fs = require('fs');

let mainWindow;
let flaskProcess;

function checkPythonAndFlask() {
  return new Promise((resolve, reject) => {
    console.log('Checking for Python and Flask...');
    
    // Try different Python commands
    const pythonCommands = ['python', 'python3', 'py'];
    let pythonFound = false;
    let pythonCmd = '';
    
    const checkPython = (cmd) => {
      return new Promise((res) => {
        exec(`${cmd} --version`, (error, stdout, stderr) => {
          if (!error) {
            console.log(`Found Python: ${stdout || stderr}`);
            pythonFound = true;
            pythonCmd = cmd;
            res(true);
          } else {
            res(false);
          }
        });
      });
    };
    
    const checkFlask = (cmd) => {
      return new Promise((res) => {
        exec(`${cmd} -c "import flask; print(flask.__version__)"`, (error, stdout, stderr) => {
          if (!error) {
            console.log(`Found Flask: ${stdout}`);
            res(true);
          } else {
            res(false);
          }
        });
      });
    };
    
    // Check each Python command
    const checkAllPython = async () => {
      for (const cmd of pythonCommands) {
        const found = await checkPython(cmd);
        if (pythonFound) {
          const flaskFound = await checkFlask(cmd);
          if (flaskFound) {
            resolve({ pythonCmd, hasFlask: true });
            return;
          } else {
            resolve({ pythonCmd, hasFlask: false });
            return;
          }
        }
      }
      resolve({ pythonCmd: '', hasFlask: false });
    };
    
    checkAllPython();
  });
}

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

  // Check Python and Flask first
  checkPythonAndFlask().then(({ pythonCmd, hasFlask }) => {
    if (!pythonCmd) {
      showError('Python Not Found', 
        'Python is required to run this application.\n\n' +
        'Please install Python from:\n' +
        'https://www.python.org/downloads/\n\n' +
        'Make sure to check "Add Python to PATH" during installation.'
      );
      return;
    }
    
    if (!hasFlask) {
      showError('Flask Not Found', 
        'Flask is required to run this application.\n\n' +
        'Please install Flask by running:\n' +
        `${pythonCmd} -m pip install flask\n\n` +
        'Or contact support for assistance.'
      );
      return;
    }
    
    // Start Flask app
    startFlaskApp(pythonCmd);
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

function startFlaskApp(pythonCmd) {
  return new Promise((resolve, reject) => {
    console.log('Starting Flask server with:', pythonCmd);
    
    // Check if app.py exists
    const appPath = path.join(__dirname, 'app.py');
    if (!fs.existsSync(appPath)) {
      showError('Application File Missing', 
        'Required application file "app.py" not found.\n\n' +
        'Please reinstall the application.'
      );
      return;
    }
    
    // Start Flask server
    flaskProcess = spawn(pythonCmd, ['app.py'], {
      cwd: __dirname,
      stdio: ['pipe', 'pipe', 'pipe']
    });

    let serverStarted = false;
    let startupTimeout = setTimeout(() => {
      if (!serverStarted) {
        flaskProcess.kill();
        showError('Server Start Failed', 
          'Failed to start the application server.\n\n' +
          'Please check:\n' +
          '1. Python is properly installed\n' +
          '2. Flask is installed\n' +
          '3. No other app is using port 5000\n\n' +
          'Contact support if the issue persists.'
        );
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
      showError('Server Error', 
        'Failed to start the application server.\n\n' +
        `Error: ${error.message}\n\n` +
        'Please ensure Python and Flask are properly installed.'
      );
    });

    flaskProcess.on('close', (code) => {
      clearTimeout(startupTimeout);
      if (!serverStarted) {
        console.log(`Flask process exited with code ${code}`);
        showError('Server Exit', 
          'The application server exited unexpectedly.\n\n' +
          `Exit code: ${code}\n\n` +
          'Please try restarting the application.'
        );
      }
    });
  });
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
          label: 'Installation Help',
          click: () => {
            dialog.showMessageBox(mainWindow, {
              type: 'info',
              title: 'Installation Requirements',
              message: 'Application Requirements',
              detail: 'This application requires:\n\n' +
                      '1. Python 3.7 or higher\n' +
                      '2. Flask web framework\n\n' +
                      'To install Python:\n' +
                      'Visit https://www.python.org/downloads/\n\n' +
                      'To install Flask:\n' +
                      'Run: python -m pip install flask\n\n' +
                      'Make sure to check "Add Python to PATH" during Python installation.',
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
