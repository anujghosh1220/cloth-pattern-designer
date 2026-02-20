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

  // Start Flask with comprehensive Python detection
  startFlaskApp();
}

async function findPython() {
  const pythonCommands = ['python', 'python3', 'py'];
  const pythonPaths = [
    'C:\\Python39\\python.exe',
    'C:\\Python310\\python.exe',
    'C:\\Python311\\python.exe',
    'C:\\Python312\\python.exe',
    'C:\\Program Files\\Python39\\python.exe',
    'C:\\Program Files\\Python310\\python.exe',
    'C:\\Program Files\\Python311\\python.exe',
    'C:\\Program Files\\Python312\\python.exe',
    'C:\\Users\\' + process.env.USERNAME + '\\AppData\\Local\\Programs\\Python\\Python39\\python.exe',
    'C:\\Users\\' + process.env.USERNAME + '\\AppData\\Local\\Programs\\Python\\Python310\\python.exe',
    'C:\\Users\\' + process.env.USERNAME + '\\AppData\\Local\\Programs\\Python\\Python311\\python.exe',
    'C:\\Users\\' + process.env.USERNAME + '\\AppData\\Local\\Programs\\Python\\Python312\\python.exe'
  ];

  // Try bundled Python first
  const bundledPython = path.join(__dirname, 'python', 'python.exe');
  if (fs.existsSync(bundledPython)) {
    console.log('Found bundled Python:', bundledPython);
    return bundledPython;
  }

  // Try system Python paths
  for (const pythonPath of pythonPaths) {
    if (fs.existsSync(pythonPath)) {
      console.log('Found system Python:', pythonPath);
      return pythonPath;
    }
  }

  // Try Python commands
  for (const cmd of pythonCommands) {
    try {
      await new Promise((resolve, reject) => {
        exec(`"${cmd}" --version`, (error, stdout, stderr) => {
          if (!error) {
            console.log(`Found Python command: ${cmd}`);
            resolve(cmd);
          } else {
            reject(error);
          }
        });
      });
      return cmd;
    } catch (e) {
      // Continue to next command
    }
  }

  return null;
}

async function installFlask(pythonCmd) {
  return new Promise((resolve, reject) => {
    console.log('Installing Flask...');
    const pipProcess = spawn(pythonCmd, ['-m', 'pip', 'install', 'flask'], {
      stdio: ['pipe', 'pipe', 'pipe']
    });

    let output = '';
    pipProcess.stdout.on('data', (data) => {
      output += data.toString();
    });

    pipProcess.stderr.on('data', (data) => {
      output += data.toString();
    });

    pipProcess.on('close', (code) => {
      if (code === 0) {
        console.log('Flask installed successfully');
        resolve(true);
      } else {
        console.log('Flask installation failed:', output);
        resolve(false);
      }
    });

    pipProcess.on('error', (error) => {
      console.log('Flask installation error:', error);
      resolve(false);
    });
  });
}

async function checkFlask(pythonCmd) {
  return new Promise((resolve) => {
    exec(`"${pythonCmd}" -c "import flask; print('OK')"`, (error, stdout, stderr) => {
      resolve(!error);
    });
  });
}

async function startFlaskApp() {
  try {
    // Show loading message
    if (mainWindow) {
      mainWindow.loadURL('data:text/html,<html><body style="font-family: Arial; text-align: center; margin-top: 100px;"><h2>🧵 Draping Threads</h2><p>Starting application...</p><p>Please wait, this may take 30-60 seconds...</p></body></html>');
    }

    // Find Python
    const pythonCmd = await findPython();
    if (!pythonCmd) {
      showPythonNotInstalledError();
      return;
    }

    // Check Flask
    const hasFlask = await checkFlask(pythonCmd);
    if (!hasFlask) {
      // Try to install Flask automatically
      const installed = await installFlask(pythonCmd);
      if (!installed) {
        showFlaskNotInstalledError();
        return;
      }
    }

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
          'Please try:\n' +
          '1. Restarting the application\n' +
          '2. Closing other applications\n' +
          '3. Restarting your computer\n\n' +
          'If the problem continues, contact support.'
        );
      }
    }, 60000); // 60 seconds timeout

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
          }, 1000);
        }
      }
    });

    flaskProcess.stderr.on('data', (data) => {
      const output = data.toString();
      console.error('Flask stderr:', output);
      
      // Check for port already in use
      if (output.includes('Address already in use') || output.includes('Port 5000 is already in use')) {
        clearTimeout(startupTimeout);
        flaskProcess.kill();
        showError('Port Already in Use', 
          'Port 5000 is already being used by another application.\n\n' +
          'Please:\n' +
          '1. Close other applications\n' +
          '2. Restart your computer\n' +
          '3. Try again'
        );
        return;
      }
      
      // Check if server started despite stderr output
      if (output.includes('Running on') && !serverStarted) {
        serverStarted = true;
        clearTimeout(startupTimeout);
        setTimeout(() => {
          mainWindow.loadURL('http://localhost:5000');
        }, 1000);
      }
    });

    flaskProcess.on('error', (error) => {
      clearTimeout(startupTimeout);
      console.error('Failed to start Flask server:', error);
      showError('Server Error', 
        'Failed to start the application server.\n\n' +
        `Error: ${error.message}\n\n` +
        'Please try restarting the application.'
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

  } catch (error) {
    console.error('Error in startFlaskApp:', error);
    showError('Application Error', 
      'An unexpected error occurred.\n\n' +
      'Please restart the application.\n\n' +
      'If the problem continues, contact support.'
    );
  }
}

function showPythonNotInstalledError() {
  if (mainWindow) {
    dialog.showMessageBox(mainWindow, {
      type: 'error',
      title: 'Python Required',
      message: 'Python is required to run this application.',
      detail: 'This application needs Python to work, but it was not found on your computer.\n\n' +
              'For non-technical users:\n' +
              '1. Click the link below to download Python\n' +
              '2. Run the installer\n' +
              '3. Check "Add Python to PATH" during installation\n' +
              '4. Restart this application\n\n' +
              'Download Python: https://www.python.org/downloads/\n\n' +
              'Or contact support for assistance.',
      buttons: ['Download Python', 'Close']
    }).then((result) => {
      if (result.response === 0) {
        shell.openExternal('https://www.python.org/downloads/');
      }
      app.quit();
    });
  }
}

function showFlaskNotInstalledError() {
  if (mainWindow) {
    dialog.showMessageBox(mainWindow, {
      type: 'error',
      title: 'Flask Required',
      message: 'Flask web framework is required but not installed.',
      detail: 'The application tried to install Flask automatically but failed.\n\n' +
              'Please:\n' +
              '1. Open Command Prompt\n' +
              '2. Type: python -m pip install flask\n' +
              '3. Press Enter\n' +
              '4. Restart this application\n\n' +
              'Or contact support for assistance.',
      buttons: ['OK']
    }).then(() => {
      app.quit();
    });
  }
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
