const { app, BrowserWindow, Menu, shell } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

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

  // Load the Flask app
  const startFlaskApp = () => {
    return new Promise((resolve, reject) => {
      console.log('Starting Flask server...');
      
      // Start Flask server
      flaskProcess = spawn('python', ['app.py'], {
        cwd: __dirname,
        stdio: ['pipe', 'pipe', 'pipe']
      });

      let serverStarted = false;
      let startupTimeout = setTimeout(() => {
        if (!serverStarted) {
          flaskProcess.kill();
          reject(new Error('Flask server failed to start within 30 seconds'));
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
        reject(error);
      });

      flaskProcess.on('close', (code) => {
        clearTimeout(startupTimeout);
        if (!serverStarted) {
          console.log(`Flask process exited with code ${code}`);
          reject(new Error(`Flask process exited with code ${code}`));
        }
      });
    });
  };

  startFlaskApp().catch(error => {
    console.error('Failed to start application:', error);
    // Show error page
    mainWindow.loadURL('data:text/html,<html><body><h1>Failed to start application</h1><p>Please ensure Python and Flask are installed.</p></body></html>');
  });

  // Handle external links
  mainWindow.webContents.setWindowOpenHandler(({ url }) => {
    shell.openExternal(url);
    return { action: 'deny' };
  });

  // Create menu
  createMenu();
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
