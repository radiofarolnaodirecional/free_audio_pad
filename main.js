const { app, BrowserWindow, ipcMain, dialog } = require('electron')

var mainWindow

app.on('ready', () => {
    mainWindow = new BrowserWindow({
        webPreferences:{
            nodeIntegration: true,
            contextIsolation: false,
            devTools: false
        },
        width: 955,
        height: 600,
        resizable:true,
        minWidth:700,
        minHeight:440,
        transparent:false,
        frame:false,
    });

    //mainWindow.loadURL(`File://${__dirname}/ui/templates/index.html`)
    mainWindow.loadURL('http://localhost:5000')

    // Listener para abrir o file browser
    ipcMain.handle('open-file-dialog', async () => {
        const result = await dialog.showOpenDialog(mainWindow, {
            properties: ['openFile'],
            filters: [
                { name: 'file', extensions: ['wav', 'mp3', 'png', 'jpeg'] }
            ]
        })
        return result.filePaths[0] || null
    })

    // Listen for the maximize event
    mainWindow.on('maximize', () => {
        console.log('Window maximized')
        mainWindow.webContents.send('window-maximized')
    })
    mainWindow.on('unmaximize', () => {
        console.log('Window unmaximized')
        mainWindow.webContents.send('window-unmaximized')
    })

    ipcMain.on('close', (e, csrf) => {
        mainWindow.close()
    })

    app.on('window-all-closed', () => {
        if (process.platform !== 'darwin') {
            app.quit()
        }

    })

})
